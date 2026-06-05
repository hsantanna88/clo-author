# 04_mechanisms.R
# H5 – H8: Mechanisms — partisan press, geographic diffusion, presidential
#           elections, and battle proximity
#
# H5: Effect is larger for Democratic-leaning newspapers
# H6: Effect spills across county lines (spatial lag)
# H7: Effect holds / strengthens in presidential election years
# H8: Proximity to recent battle → attenuates slavery discourse effect
#
# Inputs:
#   data/cleaned/cong_pnl_{1,3}.rds
#   data/cleaned/pres_pnl_{1,3}.rds
#   data/raw/other/acw_battle_data/  (for H8)
#
# Output:
#   paper/tables/04_mechanisms/tbl_h5_partisan.tex
#   paper/tables/04_mechanisms/tbl_h6_spatial.tex
#   paper/tables/04_mechanisms/tbl_h7_presidential.tex
#   paper/tables/04_mechanisms/tbl_h8_battle.tex
#   paper/figures/04_mechanisms/fig_h7_pres_vs_cong.pdf

library(here)
library(fixest)
library(modelsummary)
library(dplyr)
library(tidyr)
library(purrr)
library(stringr)
library(ggplot2)
library(sf)
library(broom)

OUT <- here::here("data/cleaned")
TBL <- here::here("paper/tables/04_mechanisms")
FIG <- here::here("paper/figures/04_mechanisms")
RAW <- here::here("data/raw")

dir.create(TBL, recursive = TRUE, showWarnings = FALSE)
dir.create(FIG, recursive = TRUE, showWarnings = FALSE)

# ── Load panels ────────────────────────────────────────────────────────────────

cong_1 <- readRDS(file.path(OUT, "cong_pnl_1.rds"))
cong_3 <- readRDS(file.path(OUT, "cong_pnl_3.rds"))
pres_1 <- readRDS(file.path(OUT, "pres_pnl_1.rds"))
pres_3 <- readRDS(file.path(OUT, "pres_pnl_3.rds"))

conley <- \() vcov_conley(lat = "lat", lon = "lon", cutoff = 250)

# Focus topic for mechanisms: slavery_direct (main H2 topic)
TOPIC <- "cos_sim_slavery_direct"

# Base formula (controlled)
base_fml <- function(outcome, extra_rhs = "") {
  rhs <- sprintf(
    "%s * vader_compound + cos_sim_politics + Ctrl_1858_pc%s + %s
     FreeCol_share + Urb2.5_pop_share + Manu_LabCost",
    TOPIC, str_remove(outcome, "pc"),
    if (nchar(extra_rhs) > 0) paste0(extra_rhs, " +") else ""
  )
  as.formula(sprintf("%s ~ %s", outcome, rhs))
}

# ── H5: Partisan press heterogeneity ──────────────────────────────────────────
# Split by newspaper partisan lean (Dem / Rep / neutral from ca_title_metadata)
# and compare slavery_direct coefficient across groups.

message("H5: Partisan press ...")

run_partisan <- function(lean, data) {
  d <- if (!is.null(lean)) filter(data, partisan_lean == lean) else data
  tryCatch(
    feols(base_fml("pcDem"), data = d, vcov = conley()),
    error = function(e) NULL
  )
}

h5_mods <- list(
  "Dem-leaning"  = run_partisan("D", cong_1),
  "Rep-leaning"  = run_partisan("R", cong_1),
  "Full sample"  = run_partisan(NULL, cong_1)
)
h5_mods <- Filter(Negate(is.null), h5_mods)

if (length(h5_mods) > 0) {
  modelsummary(
    h5_mods,
    output   = "latex_tabular",
    coef_map = list(
      "cos_sim_slavery_direct"              = "Cosine sim.",
      "vader_compound"                      = "VADER compound",
      "cos_sim_slavery_direct:vader_compound" = "Cosine × sentiment",
      "cos_sim_politics"                    = "Politics baseline"
    ),
    gof_map  = c("nobs", "r.squared"),
    stars    = c("*" = 0.10, "**" = 0.05, "***" = 0.01),
    notes    = "Conley spatial HAC SEs (250 km). 1-month window. Outcome: Dem. vote share.",
    title    = "H5: Partisan Press Heterogeneity"
  ) %>%
  writeLines(file.path(TBL, "tbl_h5_partisan.tex"))
}

# ── H6: Spatial spillovers ────────────────────────────────────────────────────
# Add a spatial lag of cos_sim_slavery_direct (mean of neighbouring counties
# within 250 km) to test geographic diffusion.

message("H6: Spatial spillovers ...")

build_spatial_lag <- function(data, var, cutoff_km = 250) {
  pts <- data %>%
    filter(!is.na(lat), !is.na(lon)) %>%
    st_as_sf(coords = c("lon", "lat"), crs = 4326)

  dmat  <- st_distance(pts)
  units(dmat) <- NULL
  W <- (dmat > 0 & dmat <= cutoff_km * 1000) * 1L
  row_sums <- rowSums(W)
  W_row  <- W / ifelse(row_sums == 0, 1, row_sums)

  vals <- data[[var]][!is.na(data$lat) & !is.na(data$lon)]
  lag_vals <- as.numeric(W_row %*% vals)

  data %>%
    filter(!is.na(lat), !is.na(lon)) %>%
    mutate(!!paste0(var, "_lag") := lag_vals)
}

cong_1_lag <- tryCatch(
  build_spatial_lag(cong_1, TOPIC),
  error = function(e) { warning("Spatial lag failed: ", e$message); NULL }
)

if (!is.null(cong_1_lag)) {
  fml_h6 <- as.formula(
    sprintf("pcDem ~ %s + %s_lag + %s * vader_compound + cos_sim_politics +
             Ctrl_1858_pcDem + FreeCol_share + Urb2.5_pop_share + Manu_LabCost",
            TOPIC, TOPIC, TOPIC)
  )
  h6_mod <- tryCatch(
    feols(fml_h6, data = cong_1_lag, vcov = conley()),
    error = function(e) NULL
  )
  if (!is.null(h6_mod)) {
    modelsummary(
      list("(1) With spatial lag" = h6_mod),
      output  = "latex_tabular",
      gof_map = c("nobs", "r.squared"),
      stars   = c("*" = 0.10, "**" = 0.05, "***" = 0.01),
      notes   = "Conley spatial HAC SEs (250 km). Spatial lag: mean cos_sim of counties within 250 km.",
      title   = "H6: Spatial Spillover in Slavery Discourse"
    ) %>%
    writeLines(file.path(TBL, "tbl_h6_spatial.tex"))
  }
}

# ── H7: Presidential elections ────────────────────────────────────────────────
# Compare slavery_direct coefficient: congressional vs. presidential elections

message("H7: Presidential elections ...")

cong_base <- tryCatch(
  feols(base_fml("pcDem"), data = cong_1, vcov = conley()),
  error = function(e) NULL
)
pres_base <- tryCatch(
  feols(base_fml("pcDem"), data = pres_1, vcov = conley()),
  error = function(e) NULL
)

h7_mods <- Filter(Negate(is.null), list(
  "Congressional (1 mo.)" = cong_base,
  "Presidential  (1 mo.)" = pres_base
))

if (length(h7_mods) > 0) {
  modelsummary(
    h7_mods,
    output   = "latex_tabular",
    coef_map = list(
      "cos_sim_slavery_direct"              = "Cosine sim.",
      "vader_compound"                      = "VADER compound",
      "cos_sim_slavery_direct:vader_compound" = "Cosine × sentiment",
      "cos_sim_politics"                    = "Politics baseline"
    ),
    gof_map  = c("nobs", "r.squared"),
    stars    = c("*" = 0.10, "**" = 0.05, "***" = 0.01),
    notes    = "Conley spatial HAC SEs (250 km). 1-month window.",
    title    = "H7: Congressional vs. Presidential Elections"
  ) %>%
  writeLines(file.path(TBL, "tbl_h7_presidential.tex"))
}

# Coefficient comparison figure
if (length(h7_mods) == 2) {
  coef_h7 <- imap_dfr(h7_mods, function(m, nm) {
    broom::tidy(m, conf.int = TRUE) %>%
      filter(term == TOPIC) %>%
      mutate(election_type = nm)
  })

  p_h7 <- ggplot(coef_h7, aes(x = election_type, y = estimate,
                               ymin = conf.low, ymax = conf.high)) +
    geom_hline(yintercept = 0, linetype = "dashed", color = "grey50") +
    geom_pointrange(color = "steelblue") +
    labs(x = NULL, y = "Coefficient on cos_sim_slavery_direct",
         caption = "Conley spatial HAC SEs (250 km). 1-month pre-election window.") +
    theme_minimal(base_family = "serif")

  ggsave(file.path(FIG, "fig_h7_pres_vs_cong.pdf"), p_h7, width = 5, height = 4)
}

# ── H8: Battle proximity ──────────────────────────────────────────────────────
# Counties within 100 km of a recent battle (previous 6 months) show attenuated
# slavery discourse effect.

message("H8: Battle proximity ...")

battle_file <- file.path(RAW, "other/acw_battle_data/cwsac_battles.csv")

if (file.exists(battle_file)) {
  battles <- read.csv(battle_file, stringsAsFactors = FALSE)

  # Build battle indicator per county-year:
  # 1 if any battle occurred within 100 km in the 6 months prior to election window
  # (simplified: use battle year and county lat/lon — refine if battle dates available)

  if (all(c("lat", "lon", "year") %in% tolower(names(battles)))) {
    names(battles) <- tolower(names(battles))
    battle_pts <- battles %>%
      filter(!is.na(lat), !is.na(lon)) %>%
      st_as_sf(coords = c("lon", "lat"), crs = 4326)

    county_pts <- cong_1 %>%
      filter(!is.na(lat), !is.na(lon)) %>%
      distinct(gisjoin, lat, lon) %>%
      st_as_sf(coords = c("lon", "lat"), crs = 4326)

    dmat <- st_distance(county_pts, battle_pts)
    units(dmat) <- NULL

    county_pts$near_battle <- apply(dmat, 1, function(row) any(row <= 100000))

    cong_1_battle <- cong_1 %>%
      left_join(
        county_pts %>% st_drop_geometry() %>%
          select(gisjoin, near_battle),
        by = "gisjoin"
      ) %>%
      mutate(near_battle = replace_na(near_battle, FALSE))

    fml_h8 <- as.formula(
      sprintf(
        "pcDem ~ %s * near_battle + %s * vader_compound + cos_sim_politics +
         Ctrl_1858_pcDem + FreeCol_share + Urb2.5_pop_share + Manu_LabCost",
        TOPIC, TOPIC
      )
    )
    h8_mod <- tryCatch(
      feols(fml_h8, data = cong_1_battle, vcov = conley()),
      error = function(e) NULL
    )
    if (!is.null(h8_mod)) {
      modelsummary(
        list("(1) Battle proximity" = h8_mod),
        output  = "latex_tabular",
        gof_map = c("nobs", "r.squared"),
        stars   = c("*" = 0.10, "**" = 0.05, "***" = 0.01),
        notes   = paste0("Conley spatial HAC SEs (250 km). near_battle = 1 if any CWSAC ",
                         "battle within 100 km. 1-month window."),
        title   = "H8: Battle Proximity and Slavery Discourse Effect"
      ) %>%
      writeLines(file.path(TBL, "tbl_h8_battle.tex"))
    }
  } else {
    message("Battle data missing lat/lon/year — skipping H8.")
  }
} else {
  message("Battle file not found, skipping H8: ", battle_file)
}

message("Mechanisms complete. Tables in ", TBL)
