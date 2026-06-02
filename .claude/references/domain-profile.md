# Domain Profile

<!--
HOW TO USE: Fill this in manually OR let /discover (interactive interview) generate it.
All agents read this file to calibrate their field-specific behavior.
-->

## Field

**Primary:** Ingeniería de Sistemas — Machine Learning aplicado a Supply Chain Management
**Adjacent subfields:** Operations Research, Inventory Optimization, Demand Forecasting, Prescriptive Analytics

---

## Target Journals (for bibliography reference)

<!-- Used to identify high-quality references, not for submission (this is a thesis). -->

| Tier | Journals |
|------|----------|
| Top | International Journal of Production Economics (IJPE), European Journal of Operational Research (EJOR) |
| Strong field | Computers & Industrial Engineering, Applied Soft Computing, Expert Systems with Applications |
| Specialty | Journal of Business Logistics, International Journal of Logistics Management |
| Conferences | IEEE ICMLA, LACCEI, CIMPS |

---

## Common Data Sources

| Dataset | Type | Access | Notes |
|---------|------|--------|-------|
| Historical purchase orders | Transactional | Company (private) | Core dataset — compras del área logística |
| ERP/WMS exports | System logs | Company (private) | Stock levels, lead times, supplier data |
| INEI Peru statistics | Administrative | Public | Sector logístico peruano — contexto macro |
| Kaggle supply chain datasets | Benchmark | Public | For methodology validation if needed |

---

## Methodology Framework

<!-- This project uses ML algorithm comparison, not causal inference. -->

| Approach | Application | Key Metric |
|----------|------------|------------|
| Train/Test temporal split | Avoid data leakage in time series | Out-of-sample performance |
| K-Fold Cross-validation | Hyperparameter tuning | Generalization error |
| Backtesting | Simulate real deployment | Cumulative cost savings |
| Baseline comparison | ARIMA, Holt-Winters, EOQ | Improvement over traditional methods |

---

## Field Conventions

- **Metrics:** RMSE, MAE, MAPE for prediction; total cost, service level, fill rate for prescriptive
- **Baselines obligatorios:** Al menos un método estadístico clásico (ARIMA/ETS) y un modelo simple (linear regression)
- **Algorithms to compare:** Random Forest, XGBoost, LightGBM, LSTM/GRU (if temporal), SVR
- **Prescriptive component:** Optimization layer on top of predictions (minimize cost subject to service level)
- **Validation:** Out-of-time validation (not random split) for time-series data
- **Reporting:** Tabla comparativa de todos los modelos con múltiples métricas + test estadístico de diferencias
- **Reproducibility:** Seeds fijos, requirements.txt, datos preprocesados documentados

---

## Notation Conventions

| Symbol | Meaning | Anti-pattern |
|--------|---------|-------------|
| $\hat{y}_t$ | Predicted demand at time $t$ | Don't use $\hat{d}$ without defining |
| $X \in \mathbb{R}^{n \times p}$ | Feature matrix ($n$ samples, $p$ features) | Don't use $D$ for both data and demand |
| $Q^*$ | Optimal order quantity | Don't confuse with $Q$ (generic quantity) |
| $L$ | Lead time | Don't use $l$ (looks like 1) |
| $SS$ | Safety stock | Spell out on first use |
| $\text{MAPE}$ | Mean Absolute Percentage Error | Always in text mode |

---

## Seminal References

| Paper | Why It Matters |
|-------|---------------|
| Silver, Pyke & Peterson (1998) | Inventory Management and Production Planning — textbook foundation |
| Syntetos et al. (2009) | Demand categorization for forecasting method selection |
| Carbonneau et al. (2008) | ML vs traditional methods for supply chain demand forecasting |
| Bohanec et al. (2017) | ML for inventory management — comprehensive review |
| Bertsimas & Kallus (2020) | Data-driven prescriptive analytics framework (from predict to prescribe) |
| Huber et al. (2019) | ML for demand forecasting in retail — benchmark study |
| Priore et al. (2019) | ML for inventory control: review and taxonomy |

---

## Field-Specific Reviewer Concerns

- "¿Por qué ML y no métodos estadísticos clásicos?" — must demonstrate improvement over baselines
- "¿Cómo manejas el data leakage temporal?" — critical for credibility
- "¿Qué tan generalizable es a otras empresas?" — external validity
- "¿Cuál es el beneficio económico concreto?" — cost-benefit analysis expected
- "¿Cómo implementarías esto en producción?" — feasibility discussion
- "¿Qué pasa con productos de baja rotación?" — intermittent demand challenge

---

## Quality Tolerance Thresholds

| Quantity | Tolerance | Rationale |
|----------|-----------|-----------|
| MAPE | Report to 2 decimals | Standard in forecasting literature |
| RMSE | Report to 2 decimals | Consistent precision |
| Cost savings | Report to nearest integer (soles) | Practical interpretation |
| p-values (stat tests) | 3 decimals or < 0.001 | Standard |
