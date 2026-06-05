# Annotated Bibliography: Minimum Wage Effects on Employment

**Date:** 2026-05-08 **Topic:** The employment effects of minimum wage increases in the United States **Papers reviewed:** 12

## Directly Related

### Card and Krueger (1994) — Minimum Wages and Employment: A Case Study of the Fast-Food Industry in New Jersey and Pennsylvania

- **Journal:** American Economic Review
- **Proximity:** 5
- **Main contribution:** Pioneered the use of natural experiments to study minimum wage effects, comparing fast-food employment in NJ (treatment) and PA (control) after NJ's 1992 minimum wage increase.
- **Identification strategy:** DiD
- **Key finding:** No significant negative employment effect; point estimate of +0.59 FTEs per restaurant (SE 1.20), contradicting the competitive labor market prediction.
- **Relevance:** Foundational paper for the modern minimum wage literature; our identification strategy builds directly on their cross-border comparison design.

### Dube, Lester, and Reich (2010) — Minimum Wage Effects Across State Borders

- **Journal:** Review of Economics and Statistics
- **Proximity:** 5
- **Main contribution:** Generalized the border-discontinuity approach to all contiguous US county pairs straddling state lines, addressing spatial heterogeneity bias in national-level studies.
- **Identification strategy:** DiD
- **Key finding:** Employment elasticity of -0.01 to 0.02 (not statistically distinguishable from zero) for restaurant workers, with earnings elasticity of 0.20-0.25.
- **Relevance:** Our empirical strategy follows their contiguous county-pair design; we extend it with staggered treatment timing methods.

### Cengiz, Dube, Lindner, and Zipperer (2019) — The Effect of Minimum Wages on Low-Wage Jobs

- **Journal:** Quarterly Journal of Economics
- **Proximity:** 5
- **Main contribution:** Introduced a bunching estimator that examines the entire wage distribution around the minimum wage, avoiding reliance on a single comparison group.
- **Identification strategy:** DiD
- **Key finding:** Missing jobs below the new minimum are offset by excess jobs above it; net employment effect near zero with an elasticity of -0.036 (SE 0.042).
- **Relevance:** Their distributional approach complements our design; we use their bunching estimates as a benchmark for our ATT estimates.

### Harasztosi and Lindner (2019) — Who Pays for the Minimum Wage?

- **Journal:** American Economic Review
- **Proximity:** 4
- **Main contribution:** Exploited a large (60%) minimum wage increase in Hungary to study firm-level adjustment margins, including employment, prices, profitability, and capital-labor substitution.
- **Identification strategy:** DiD
- **Key finding:** Employment fell by 10% at affected firms, but most adjustment came through reduced profits (-13%) and higher prices (+3%), not layoffs.
- **Relevance:** Informs our heterogeneity analysis by firm size and profit margin; different context but same causal question.

## Same Method, Different Context

### Dustmann, Lindner, Schoenberg, Umkehrer, and vom Berge (2022) — Reallocation Effects of the Minimum Wage

- **Journal:** Quarterly Journal of Economics
- **Proximity:** 4
- **Main contribution:** Studied Germany's 2015 national minimum wage introduction using administrative employer-employee data, showing reallocation from small to large firms.
- **Identification strategy:** DiD
- **Key finding:** Minimum wage reduced employment at small firms by 2.3% while increasing earnings by 4.8%; workers reallocated to higher-paying, more productive establishments.
- **Relevance:** Uses the same DiD framework in a different institutional context; their reallocation findings motivate our firm-size heterogeneity analysis.

### Jardim, Long, Plotnick, van Inwegen, Vigdor, and Wething (2022) — Minimum Wage Increases and Individual Employment Trajectories

- **Journal:** Journal of Labor Economics
- **Proximity:** 3
- **Main contribution:** Used administrative data from Washington State to track individual workers before and after Seattle's minimum wage increase, separating incumbent from new worker effects.
- **Identification strategy:** DiD
- **Key finding:** Hours worked by low-wage workers fell 6-7%, partially offsetting hourly wage gains; experienced workers saw net earnings increases while new entrants faced reduced opportunities.
- **Relevance:** Their individual-level tracking approach motivates our robustness check using worker-level (rather than county-level) outcomes.

## Same Context, Different Method

### Neumark, Salas, and Wascher (2014) — Revisiting the Minimum Wage-Employment Debate

- **Journal:** Journal of Labor Economics
- **Proximity:** 3
- **Main contribution:** Challenged the contiguous county-pair design by arguing that spatial controls absorb real variation, and that traditional panel methods with state and time fixed effects recover negative employment effects.
- **Identification strategy:** IV
- **Key finding:** Employment elasticities of -0.15 to -0.20 for teens and -0.10 to -0.15 for restaurant workers when using longer panels and state-level variation.
- **Relevance:** Primary counterpoint to our identification strategy; we address their critique by implementing the Callaway-Sant'Anna estimator that handles staggered timing transparently.

### Aaronson, French, Sorkin, and To (2018) — Industry Dynamics and the Minimum Wage

- **Journal:** Econometrica
- **Proximity:** 3
- **Main contribution:** Developed and estimated a structural model of restaurant industry dynamics with putty-clay technology, where minimum wage effects depend on the vintage of capital in place.
- **Identification strategy:** structural
- **Key finding:** Short-run employment elasticity of -0.04 but long-run elasticity of -0.18, as firms gradually exit and adjust technology; welfare effects depend on discount rates and adjustment costs.
- **Relevance:** Their structural estimates bracket the reduced-form effects we identify; we compare our ATT to their model-implied treatment effects.

## Theoretical Foundations

### Manning (2003) — Monopsony in Motion

- **Journal:** Princeton University Press
- **Proximity:** 2
- **Main contribution:** Provided the modern theoretical framework for labor market monopsony, showing that search frictions generate employer wage-setting power even in markets with many employers.
- **Identification strategy:** descriptive
- **Key finding:** When labor supply to individual firms is imperfectly elastic, moderate minimum wage increases can raise both wages and employment, rationalizing the Card-Krueger findings.
- **Relevance:** Core theoretical motivation for our paper; the monopsony model predicts the near-zero employment effects we find empirically.

### Burdett and Mortensen (1998) — Wage Differentials, Employer Size, and Unemployment

- **Journal:** International Economic Review
- **Proximity:** 2
- **Main contribution:** Developed an equilibrium search model generating a non-degenerate wage distribution even among homogeneous workers, where larger firms pay higher wages to reduce turnover.
- **Identification strategy:** descriptive
- **Key finding:** The model predicts that minimum wages compress the lower tail of the wage distribution and can reduce frictional unemployment by raising the opportunity cost of non-employment.
- **Relevance:** Provides the structural search-theoretic underpinning for the monopsony interpretation of our reduced-form results.

## Methods Papers

### Callaway and Sant'Anna (2021) — Difference-in-Differences with Multiple Time Periods

- **Journal:** Journal of Econometrics
- **Proximity:** 4
- **Main contribution:** Developed group-time average treatment effects ATT(g,t) for staggered DiD designs that are robust to treatment effect heterogeneity, unlike TWFE estimators.
- **Identification strategy:** DiD
- **Key finding:** TWFE can be severely biased with heterogeneous treatment effects; their estimator recovers interpretable causal parameters under parallel trends conditional on covariates.
- **Relevance:** Our primary estimation method; we implement their R package `did` for all main specifications and event study plots.

### Roth, Sant'Anna, Bilinski, and Poe (2023) — What's Trending in Difference-in-Differences?

- **Journal:** Journal of Econometrics
- **Proximity:** 3
- **Main contribution:** Comprehensive review of recent advances in DiD methodology, covering staggered adoption, pre-testing, sensitivity analysis, and alternative identification strategies.
- **Identification strategy:** descriptive
- **Key finding:** Recommend the Rambachan-Roth sensitivity analysis for assessing robustness of parallel trends assumptions; document widespread misuse of pre-trend tests as validation.
- **Relevance:** We follow their recommended best practices: Callaway-Sant'Anna for estimation, Rambachan-Roth for sensitivity, and honest confidence intervals for pre-trends.