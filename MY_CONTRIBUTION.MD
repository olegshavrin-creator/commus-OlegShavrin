# My Contribution to KOMUS Credit Risk

**Author:** Oleg Shavrin  
**Role:** Research & experimentation — hypothesis validation, model comparison, and the financial "traffic light" methodology.

---

## Summary

In this project I focused on research and experimentation rather than product engineering. My work covered three areas:

1. **Financial "Traffic Light" V2** — designed and validated an interpretable, rule-based alternative to pure ML default prediction.
2. **ML model comparison** — ran controlled experiments comparing GBDT and modern neural architectures on tabular credit data.
3. **Research artifacts** — produced notebooks, machine-readable summaries, figures, and presentation materials for reproducibility.

---

## 1. Financial "Traffic Light" V2

### Concept

The traffic light is an interpretable risk score (0–100) that combines four components into a single assessment with four levels: **GREEN, YELLOW, ORANGE, RED**.

| Component | Weight | What it measures |
| --- | --- | --- |
| Current financial state | 60% | Debt load, liquidity, ability to service obligations, profitability |
| Dynamics | 25% | Year-over-year change in key indicators |
| Events | 15% | Strong discrete signals (e.g. >50% revenue drop, profit → loss) |
| Negative equity | special | Critical signal (+10 points), handled separately from standard Debt/Equity |

### How it works

- **Current state** is measured across four blocks: debt load, liquidity, ability to service obligations, profitability. Each indicator is normalized via percentile-rank to 0–1 with risk direction applied. Available indicators are averaged within a block; four blocks have equal weight inside the current state.
- **Dynamics** compares the current year to the previous available year. Deterioration increases risk; improvement decreases it. Tracked indicators: revenue, pre-tax profit, operating cash flow, equity, cash, share of liabilities in assets, current liquidity.
- **Events** capture: >50% revenue drop, transition from profit to loss, worsening loss, recovery from loss, sharp revenue drop combined with worsening result, revenue growth combined with recovery from loss.
- **Negative equity** is treated as a separate critical signal, not as a standard Debt/Equity threshold.

### Empirical validation

Working sample: **33,493 observations**, 5,436 companies, 2011–2025.

**Score distribution:**

| Level | Share |
| --- | ---: |
| GREEN | 13.70% |
| YELLOW | 52.61% |
| ORANGE | 26.53% |
| RED | 7.16% |
| ORANGE + RED | 33.69% |

**Year-over-year direction:**

| Direction | Observations | Share |
| --- | ---: | ---: |
| Strong deterioration | 10,221 | 30.52% |
| Deterioration | 3,240 | 9.67% |
| Stable | 1,796 | 5.36% |
| Improvement | 3,232 | 9.65% |
| Strong improvement | 9,697 | 28.95% |
| First observation | 5,307 | 15.85% |

**Key findings:**

- Level transitions occur predominantly between adjacent levels, confirming gradual risk change.
- 3,554 transitions from ORANGE/RED back to GREEN/YELLOW (31.50% of ORANGE/RED observations) — the methodology captures both short-term and persistent risk.
- Maximum continuous ORANGE/RED streak: 15 years.
- Analysis of 51 GREEN → RED and 46 RED → GREEN transitions confirmed the 60/25/15 weights and percentile-rank normalization are empirically justified at this stage.

---

## 2. Demonstrated Cases

I built a demonstration set of five "INN — year" pairs from the calculated `df_v2_final` dataset, covering distinct scenarios:

| Scenario | INN — Year | What it shows |
| --- | --- | --- |
| Sharp deterioration | 1006027561 — 2022 | GREEN → RED, score 97.2 (+85.4) |
| Sharp recovery | 1655141117 — 2022 | RED → GREEN, score 8.4 (−84.0) |
| Negative equity | 278106345 — 2016 | Critical special signal, score 100.0 |
| Prolonged high risk | 814166855 — 2025 | Stable RED, score 90.8 (+0.5) |
| Stable low risk | 1650079031 — 2025 | Stable GREEN, score 4.7 (−3.8) |

Each case shows not just the final color, but its full context: Risk Score, year-over-year change, score history, component breakdown, key factors, and dynamics direction.

---

## 3. ML Experiments and Model Comparison

In parallel with the traffic light research, I designed and ran controlled ML experiments:

- **Prepared datasets** and built sampling pipelines with fixed TRAIN / TEST splits and reproducible protocols.
- **Compared model architectures:** GBDT (CatBoost, XGBoost, LightGBM) and modern neural approaches for tabular data (TabM, FT-Transformer, TabR, TabPFN, TabFM, RealMLP, xRFM).
- **Applied strict leakage-safe protocols** — final test is never used for model, feature, hyperparameter, or threshold selection.

### Selected results

| Model | Metric | Value |
| --- | --- | ---: |
| XGBoost (baseline) | OOF Gini | 0.803990 |
| TabR + GBDT (Fold 1) | Outer Gini | 0.794973 |
| TabR + GBDT (Fold 1) | ROC-AUC | 0.897487 |
| TabR + GBDT (Fold 1) | PR-AUC | 0.596971 |
| TabR + GBDT (Fold 2) | Best inner Gini | 0.810747 |

On Fold 1, TabR did not exceed the strong GBDT baseline by Gini (Δ = −0.009017). This is an honest negative result, consistent with the project's research principle of reporting what the data actually shows rather than chasing a higher Gini.

---

## 4. Research Artifacts

Produced for reproducibility and future defense:

- notebooks documenting each research stage;
- machine-readable summaries and diagnostics;
- figures for analysis and presentation;
- presentation-ready materials.

Stored in `reports/` and `credit-scoring/notebooks/`.

---

## Contact

- LinkedIn: [www.linkedin.com/in/olegshavrin](https://www.linkedin.com/in/olegshavrin)
- Email: olegshavrin@gmail.com
