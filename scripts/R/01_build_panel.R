# 01_build_panel.R
# Merges BERTopic notebook output with census + election data to produce
# regression-ready county panels.
#
# Inputs (from notebooks / HuggingFace — place in data/cleaned/ before running):
#   bertopic_panel_{MODEL_NAME}.csv  — lccn × year_month aggregated panel
#
# Inputs (from data/raw/):
#   ca_title_metadata.csv       — LCCN → lat/lon, partisan affiliation
#   elect_df.csv                — county-level election returns
#   Elections Dates.xlsx        — state × election date lookup
#   gis/ICPSR_08611/DS0001/     — 1860 county-level census + demographics
#
# Outputs (data/cleaned/):
#   cong_pnl.rds, cong_pnl_{1-4}.rds
#   pres_pnl.rds, pres_pnl_{1-4}.rds

library(here)
library(dplyr)
library(tidyr)
library(readr)
library(readxl)
library(haven)
library(purrr)
library(lubridate)
library(sf)
library(stringr)

RAW  <- here::here("data/raw")
PROC <- here::here("data/cleaned")

dir.create(PROC, recursive = TRUE, showWarnings = FALSE)

# ── 1. BERTopic panel ─────────────────────────────────────────────────────────

bert_files <- list.files(PROC, pattern = "^bertopic_panel_.*\\.csv$",
                         full.names = TRUE)

if (length(bert_files) == 0) {
  stop(
    "No bertopic_panel_*.csv found in data/cleaned/.\n",
    "Download from HuggingFace: hf://datasets/patrickjcrawford/civil-war-news/\n",
    "Place in data/cleaned/ and re-run."
  )
}

if (length(bert_files) > 1) {
  message("Multiple bertopic_panel files — using most recently modified.")
  bert_files <- bert_files[order(file.mtime(bert_files), decreasing = TRUE)][1]
}

message("Loading: ", basename(bert_files))
bert <- read_csv(bert_files, show_col_types = FALSE) %>%
  mutate(lccn = as.character(lccn),
         year = as.integer(year))

cos_vars <- c("cos_sim_politics", "cos_sim_slavery_direct",
              "cos_sim_slavery_ideology", "cos_sim_abolition",
              "cos_sim_race", "cos_sim_black_military")

missing <- setdiff(cos_vars, names(bert))
if (length(missing) > 0)
  stop("BERTopic panel missing columns: ", paste(missing, collapse = ", "))

# ── 2. Newspaper metadata ─────────────────────────────────────────────────────

meta <- read_csv(file.path(RAW, "ca_title_metadata.csv"),
                 show_col_types = FALSE) %>%
  select(lccn, lat, lon, state, any_of("partisan_lean")) %>%
  distinct(lccn, .keep_all = TRUE) %>%
  mutate(lccn = as.character(lccn))

# ── 3. Census demographics (ICPSR 08611) ─────────────────────────────────────

icpsr_path <- file.path(RAW, "gis/ICPSR_08611/DS0001/08611-0001-Data.dta")
if (!file.exists(icpsr_path))
  stop("ICPSR county data not found: ", icpsr_path)

census <- read_dta(icpsr_path) %>%
  rename_with(toupper) %>%
  rename_with(tolower)

# The precise variable names vary by ICPSR release; inspect with names(census).
# Common 1860 variables (update to match codebook if needed):
#   aga001 = total population
#   agb001 = total free colored population (free Black)
#   ags001 = urban population (places >= 2500)
#   agt002 = manufacturing wages / labor cost

census_clean <- census %>%
  mutate(across(everything(), as.numeric)) %>%
  mutate(
    FreeCol_share    = if ("agb001" %in% names(.) && "aga001" %in% names(.))
                         agb001 / aga001 else NA_real_,
    Urb2.5_pop_share = if ("ags001" %in% names(.) && "aga001" %in% names(.))
                         ags001 / aga001 else NA_real_,
    Manu_LabCost     = if ("agt002" %in% names(.)) agt002 else NA_real_
  ) %>%
  select(any_of(c("gisjoin", "state", "county", "lat", "lon")),
         FreeCol_share, Urb2.5_pop_share, Manu_LabCost)

# ── 4. Election returns ───────────────────────────────────────────────────────

elect <- read_csv(file.path(RAW, "elect_df.csv"), show_col_types = FALSE) %>%
  rename_with(tolower)

elect_dates <- read_excel(file.path(RAW, "Elections Dates.xlsx")) %>%
  rename_with(tolower)

# ── 5. Spatial join: LCCN → nearest county ───────────────────────────────────

county_pts <- census_clean %>%
  filter(!is.na(lat), !is.na(lon)) %>%
  st_as_sf(coords = c("lon", "lat"), crs = 4326)

lccn_pts <- meta %>%
  filter(!is.na(lat), !is.na(lon)) %>%
  st_as_sf(coords = c("lon", "lat"), crs = 4326)

message("Spatial join: LCCN → county ...")
nn <- st_nearest_feature(lccn_pts, county_pts)

lccn_county <- lccn_pts %>%
  st_drop_geometry() %>%
  bind_cols(
    county_pts[nn, ] %>%
      st_drop_geometry() %>%
      select(gisjoin, FreeCol_share, Urb2.5_pop_share, Manu_LabCost,
             lat, lon)
  )

# ── 6. Build full congressional panel ─────────────────────────────────────────

cong_elect <- elect %>%
  filter(tolower(election_type) == "congressional")

cong_pnl <- bert %>%
  left_join(lccn_county, by = "lccn") %>%
  left_join(cong_elect, by = c("gisjoin", "year")) %>%
  filter(!is.na(gisjoin), !is.na(pcDem))

# ── 7. Election-window aggregation ───────────────────────────────────────────

build_window <- function(pnl_full, elect_type, n_months) {
  dates <- elect_dates %>%
    filter(tolower(type) == tolower(elect_type)) %>%
    mutate(ym_elect = format(
      as.Date(paste0(year, "-", str_pad(month, 2, pad = "0"), "-01")), "%Y-%m"
    )) %>%
    select(state, year, ym_elect)

  pnl_full %>%
    left_join(dates, by = c("state", "year")) %>%
    filter(!is.na(ym_elect)) %>%
    mutate(
      d_art  = as.Date(paste0(year_month, "-01")),
      d_elec = as.Date(paste0(ym_elect, "-01")),
      months_before = as.integer(
        round(as.numeric(difftime(d_elec, d_art, units = "days")) / 30.44)
      )
    ) %>%
    filter(months_before >= 1, months_before <= n_months)
}

agg_window <- function(w) {
  grp_vars <- c("lccn", "gisjoin", "year", "state", "lat", "lon",
                "pcDem", "pcRep", "FreeCol_share", "Urb2.5_pop_share",
                "Manu_LabCost")
  # include any Ctrl_1858_* columns
  ctrl_cols <- names(w)[startsWith(names(w), "Ctrl_")]
  grp_vars  <- c(grp_vars, ctrl_cols)
  grp_vars  <- intersect(grp_vars, names(w))

  w %>%
    group_by(across(all_of(grp_vars))) %>%
    summarise(
      across(all_of(cos_vars), \(x) mean(x, na.rm = TRUE)),
      vader_compound = mean(vader_compound, na.rm = TRUE),
      n_months       = n(),
      .groups        = "drop"
    )
}

make_cong_window <- function(n) agg_window(build_window(cong_pnl, "congressional", n))
make_pres_window <- function(n) agg_window(build_window(pres_pnl, "presidential",  n))

message("Building congressional window panels ...")
cong_pnl_1 <- make_cong_window(1)
cong_pnl_2 <- make_cong_window(2)
cong_pnl_3 <- make_cong_window(3)
cong_pnl_4 <- make_cong_window(4)

# Presidential panel
pres_elect <- elect %>% filter(tolower(election_type) == "presidential")

pres_pnl <- bert %>%
  left_join(lccn_county, by = "lccn") %>%
  left_join(pres_elect, by = c("gisjoin", "year")) %>%
  filter(!is.na(gisjoin), !is.na(pcDem))

message("Building presidential window panels ...")
pres_pnl_1 <- make_pres_window(1)
pres_pnl_2 <- make_pres_window(2)
pres_pnl_3 <- make_pres_window(3)
pres_pnl_4 <- make_pres_window(4)

# ── 8. Save ───────────────────────────────────────────────────────────────────

message("Saving to ", PROC, " ...")

panels <- list(
  cong_pnl   = cong_pnl,
  cong_pnl_1 = cong_pnl_1, cong_pnl_2 = cong_pnl_2,
  cong_pnl_3 = cong_pnl_3, cong_pnl_4 = cong_pnl_4,
  pres_pnl   = pres_pnl,
  pres_pnl_1 = pres_pnl_1, pres_pnl_2 = pres_pnl_2,
  pres_pnl_3 = pres_pnl_3, pres_pnl_4 = pres_pnl_4
)

iwalk(panels, \(df, nm)
  saveRDS(df, file.path(PROC, paste0(nm, ".rds")), compress = FALSE)
)

message("Panel build complete.")
iwalk(panels, \(df, nm) message(sprintf("  %-14s %d rows", nm, nrow(df))))
