# 02_event_study.R
# H1: Slavery/race discourse spikes in the months before congressional elections
#
# Model: cos_sim_k ~ Σ β_τ · D(months_before = τ) + county FE + year FE
#   estimated separately for each cos_sim topic k
#   Conley spatial HAC SEs (250 km cutoff)
#
# Topics: cos_sim_slavery_direct, cos_sim_slavery_ideology, cos_sim_abolition,
#         cos_sim_race, cos_sim_black_military, cos_sim_politics (baseline)
#
# Output:
#   paper/figures/02_event_study/fig_event_{topic}.pdf
#   paper/tables/02_event_study/tbl_event_study.tex
#   data/cleaned/event_coefs.csv

library(here)
library(fixest)
library(dplyr)
library(tidyr)
library(purrr)
library(stringr)
library(ggplot2)
library(broom)

OUT <- here::here("data/cleaned")
FIG <- here::here("paper/figures/02_event_study")
TBL <- here::here("paper/tables/02_event_study")

dir.create(FIG, recursive = TRUE, showWarnings = FALSE)
dir.create(TBL, recursive = TRUE, showWarnings = FALSE)

# ── Load full congressional panel ─────────────────────────────────────────────

pnl <- readRDS(file.path(OUT, "cong_pnl.rds"))

conley <- \() vcov_conley(lat = "lat", lon = "lon", cutoff = 250)

cos_vars <- c("cos_sim_politics", "cos_sim_slavery_direct",
              "cos_sim_slavery_ideology", "cos_sim_abolition",
              "cos_sim_race", "cos_sim_black_military")

# ── Compute months_before for each observation ────────────────────────────────
# The full panel has a year_month column; elect year column tells us the
# election year. Use the 4-month pre-election window for the event study.

pnl_es <- pnl %>%
  filter(!is.na(months_before), months_before >= 1, months_before <= 4) %>%
  mutate(
    tau = factor(-months_before, levels = -4:-1)  # -4 = earliest, -1 = closest
  )

# ── Event study regressions ────────────────────────────────────────────────────

run_event <- function(outcome) {
  fml <- as.formula(
    sprintf("%s ~ i(tau, ref = '-1') | gisjoin + year", outcome)
  )
  tryCatch(
    feols(fml, data = pnl_es, vcov = conley()),
    error = function(e) { warning(e$message); NULL }
  )
}

message("Fitting event study models ...")
event_models <- setNames(map(cos_vars, run_event), cos_vars)
event_models  <- Filter(Negate(is.null), event_models)

# ── Tidy coefficients ─────────────────────────────────────────────────────────

event_coefs <- imap_dfr(event_models, function(m, nm) {
  broom::tidy(m, conf.int = TRUE) %>%
    mutate(topic = nm)
}) %>%
  mutate(
    tau = as.integer(str_extract(term, "-?\\d+")),
    topic_label = str_replace_all(topic, "cos_sim_", "") %>%
      str_replace_all("_", " ") %>%
      str_to_title()
  )

write.csv(event_coefs, file.path(OUT, "event_coefs.csv"), row.names = FALSE)

# ── Figures ───────────────────────────────────────────────────────────────────

topic_labels <- c(
  cos_sim_politics           = "Politics",
  cos_sim_slavery_direct     = "Slavery (Direct)",
  cos_sim_slavery_ideology   = "Slavery (Ideology)",
  cos_sim_abolition          = "Abolition",
  cos_sim_race               = "Race",
  cos_sim_black_military     = "Black Military"
)

message("Writing figures ...")

walk(names(event_models), function(topic) {
  coef_df <- event_coefs %>%
    filter(topic == !!topic) %>%
    # Add reference category τ = -1 (coef = 0 by construction)
    bind_rows(tibble(tau = -1, estimate = 0, conf.low = 0, conf.high = 0,
                     topic = topic))

  p <- ggplot(coef_df, aes(x = tau, y = estimate)) +
    geom_hline(yintercept = 0, linetype = "dashed", color = "grey50") +
    geom_ribbon(aes(ymin = conf.low, ymax = conf.high), alpha = 0.2,
                fill = "steelblue") +
    geom_line(color = "steelblue") +
    geom_point(color = "steelblue", size = 2) +
    scale_x_continuous(
      breaks = -4:-1,
      labels = c("4 mo.", "3 mo.", "2 mo.", "1 mo.")
    ) +
    labs(
      x = "Months before election",
      y = "Coefficient (95% CI)",
      caption = "Conley spatial HAC SEs (250 km). County and year FE. Ref: 1 month before."
    ) +
    theme_minimal(base_family = "serif") +
    theme(panel.grid.minor = element_blank())

  ggsave(
    file.path(FIG, paste0("fig_event_", str_remove(topic, "cos_sim_"), ".pdf")),
    p, width = 6, height = 4
  )
})

# ── Combined table ────────────────────────────────────────────────────────────
# Wide table: each topic is a column, rows are τ values

tbl_wide <- event_coefs %>%
  filter(!is.na(tau)) %>%
  mutate(
    est_str = sprintf("%.3f%s", estimate,
                      case_when(p.value < 0.01 ~ "***",
                                p.value < 0.05 ~ "**",
                                p.value < 0.10 ~ "*",
                                TRUE ~ "")),
    se_str  = sprintf("(%.3f)", std.error),
    tau_lbl = paste0(abs(tau), " mo. prior")
  ) %>%
  select(tau_lbl, topic, est_str, se_str)

message("Event study complete. Coefficients saved to ", OUT)
message("Figures saved to ", FIG)
