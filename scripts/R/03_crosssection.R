# 03_crosssection.R
# H2 – H4: Vote share effects, partisan asymmetry, and sentiment moderation
#
# H2: Higher slavery-proximate discourse → higher Democratic vote share
# H3: Same specification on Republican vote share yields null / weaker result
# H4: Interaction CosSim × vader_compound < 0 for Democrats:
#     fear-invoking tone amplifies the Democratic advantage
#
# Model (for party P, topic k, window w):
#   pcP = β0 + β1·cos_sim_k + β2·vader_compound
#             + β3·(cos_sim_k × vader_compound) + β4·cos_sim_politics
#             [+ β5·Ctrl_1858_pcP + β6·FreeCol_share
#              + β7·Urb2.5_pop_share + β8·Manu_LabCost] + ε
#
#   Conley spatial HAC SEs (250 km cutoff)
#
# Topics: slavery_direct, slavery_ideology, abolition, race, black_military
# Windows: 1-month (cong_pnl_1), 3-month (cong_pnl_3)
# Outcomes: pcDem, pcRep
#
# Output:
#   data/cleaned/crosssec_models.rds
#   data/cleaned/crosssec_coefs.csv
#   data/cleaned/marginals_h2_slavery_dem_1mo.csv
#   paper/tables/03_crosssection/tbl_vote_dem_{topic}.tex
#   paper/tables/03_crosssection/tbl_vote_rep_{topic}.tex
#   paper/tables/03_crosssection/tbl_main_h2_h3.tex

library(here)
library(fixest)
library(modelsummary)
library(dplyr)
library(tidyr)
library(purrr)
library(stringr)
library(broom)

OUT <- here::here("data/cleaned")
TBL <- here::here("paper/tables/03_crosssection")

dir.create(TBL, recursive = TRUE, showWarnings = FALSE)

# ── Load panels ────────────────────────────────────────────────────────────────

pnl_1 <- readRDS(file.path(OUT, "cong_pnl_1.rds"))
pnl_3 <- readRDS(file.path(OUT, "cong_pnl_3.rds"))

conley <- \() vcov_conley(lat = "lat", lon = "lon", cutoff = 250)

topics <- c("slavery_direct", "slavery_ideology", "abolition",
            "race", "black_military")

# ── Core regression function ───────────────────────────────────────────────────

run_cross <- function(outcome, topic, data, controlled = FALSE) {
  cos_var   <- paste0("cos_sim_", topic)
  inter_var <- paste0(cos_var, ":vader_compound")
  ctrl_var  <- paste0("Ctrl_1858_pc", str_remove(outcome, "pc"))

  base_rhs <- sprintf("%s * vader_compound + cos_sim_politics", cos_var)
  ctrl_rhs <- sprintf("%s + %s + FreeCol_share + Urb2.5_pop_share + Manu_LabCost",
                      base_rhs, ctrl_var)

  fml <- as.formula(
    sprintf("%s ~ %s", outcome, if (controlled) ctrl_rhs else base_rhs)
  )

  tryCatch(
    feols(fml, data = data, vcov = conley()),
    error = function(e) { warning(e$message); NULL }
  )
}

# ── Fit all models ─────────────────────────────────────────────────────────────
# topics × outcomes × windows × specs = 5 × 2 × 2 × 2 = 40 models

message("Fitting cross-sectional models ...")

outcomes <- c("pcDem", "pcRep")
panels   <- list("1mo" = pnl_1, "3mo" = pnl_3)

crosssec_models <- list()

for (t in topics) {
  for (out in outcomes) {
    for (w in names(panels)) {
      party <- str_remove(out, "pc")
      key_base <- sprintf("%s_%s_%s_base", t, party, w)
      key_ctrl <- sprintf("%s_%s_%s_ctrl", t, party, w)
      crosssec_models[[key_base]] <- run_cross(out, t, panels[[w]], FALSE)
      crosssec_models[[key_ctrl]] <- run_cross(out, t, panels[[w]], TRUE)
    }
  }
}

crosssec_models <- Filter(Negate(is.null), crosssec_models)

# ── Tidy coefficient extract ───────────────────────────────────────────────────

crosssec_coefs <- imap_dfr(crosssec_models, function(m, nm) {
  tryCatch(
    broom::tidy(m, conf.int = TRUE) %>% mutate(model = nm),
    error = function(e) NULL
  )
})

# ── Marginal effects for H4 ───────────────────────────────────────────────────

marginal_sentiment <- function(model, cos_var,
                               sentiment_vals = c(-0.5, 0, 0.5)) {
  coefs     <- coef(model)
  main      <- coefs[cos_var]
  inter_key <- paste0(cos_var, ":vader_compound")
  inter     <- if (inter_key %in% names(coefs)) coefs[inter_key] else 0
  tibble(
    sentiment       = sentiment_vals,
    marginal_effect = main + inter * sentiment_vals
  )
}

m_h2 <- crosssec_models[["slavery_direct_Dem_1mo_ctrl"]]
if (!is.null(m_h2)) {
  marg <- marginal_sentiment(m_h2, "cos_sim_slavery_direct")
  write.csv(marg, file.path(OUT, "marginals_h2_slavery_dem_1mo.csv"),
            row.names = FALSE)
}

# ── Tables via modelsummary ────────────────────────────────────────────────────
#
# One table per topic × outcome: 4 columns (1mo base, 1mo ctrl, 3mo base, 3mo ctrl)

coef_map <- function(topic) {
  cos_var <- paste0("cos_sim_", topic)
  c(
    setNames(list("Cosine sim."), cos_var),
    list("vader_compound" = "VADER compound"),
    setNames(list("Cosine sim. × sentiment"),
             paste0(cos_var, ":vader_compound")),
    list("cos_sim_politics" = "Politics baseline"),
    list("Ctrl_1858_pcDem" = "1858 Dem. vote",
         "Ctrl_1858_pcRep" = "1858 Rep. vote",
         "FreeCol_share"   = "Free colored share",
         "Urb2.5_pop_share"= "Urban share",
         "Manu_LabCost"    = "Mfg. labor cost")
  )
}

make_table <- function(topic, outcome) {
  party <- str_remove(outcome, "pc")
  get_m <- function(w, ctrl)
    crosssec_models[[sprintf("%s_%s_%s_%s", topic, party, w,
                             if (ctrl) "ctrl" else "base")]]

  mods <- list(
    "(1)" = get_m("1mo", FALSE), "(2)" = get_m("1mo", TRUE),
    "(3)" = get_m("3mo", FALSE), "(4)" = get_m("3mo", TRUE)
  )
  mods <- Filter(Negate(is.null), mods)
  if (length(mods) == 0) return(invisible(NULL))

  topic_title <- str_replace_all(topic, "_", " ") %>% str_to_title()
  out_label   <- if (outcome == "pcDem") "Democratic" else "Republican"

  modelsummary(
    mods,
    output        = "latex_tabular",
    coef_map      = coef_map(topic),
    gof_map       = c("nobs", "r.squared"),
    stars         = c("*" = 0.10, "**" = 0.05, "***" = 0.01),
    notes         = "Conley spatial HAC SEs (250 km cutoff).",
    title         = sprintf(
      "Effect of %s Discourse on %s Vote Share", topic_title, out_label
    )
  ) %>%
  writeLines(
    file.path(TBL, sprintf("tbl_vote_%s_%s.tex", tolower(party), topic))
  )
}

message("Writing tables ...")
for (t in topics) {
  make_table(t, "pcDem")
  make_table(t, "pcRep")
}

# Combined H2–H3 table: slavery_direct, Democrat vs Republican, 1-month window
main_mods <- list(
  "(1) Dem base" = crosssec_models[["slavery_direct_Dem_1mo_base"]],
  "(2) Dem ctrl" = crosssec_models[["slavery_direct_Dem_1mo_ctrl"]],
  "(3) Rep base" = crosssec_models[["slavery_direct_Rep_1mo_base"]],
  "(4) Rep ctrl" = crosssec_models[["slavery_direct_Rep_1mo_ctrl"]]
)
main_mods <- Filter(Negate(is.null), main_mods)

if (length(main_mods) > 0) {
  modelsummary(
    main_mods,
    output   = "latex_tabular",
    coef_map = coef_map("slavery_direct"),
    gof_map  = c("nobs", "r.squared"),
    stars    = c("*" = 0.10, "**" = 0.05, "***" = 0.01),
    notes    = "Conley spatial HAC SEs (250 km). Topic: institutional slavery keywords (direct).",
    title    = "H2–H3: Slavery Discourse and Vote Share (1-month window)"
  ) %>%
  writeLines(file.path(TBL, "tbl_main_h2_h3.tex"))
}

# ── Save ───────────────────────────────────────────────────────────────────────

saveRDS(crosssec_models, file.path(OUT, "crosssec_models.rds"), compress = FALSE)
write.csv(crosssec_coefs, file.path(OUT, "crosssec_coefs.csv"), row.names = FALSE)

message("Cross-section complete. Objects saved to ", OUT)
