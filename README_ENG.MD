# Komus Credit Risk

KOMUS Credit Risk is a research prototype for reproducible ML experiments focused on predicting organizational default.

Current user flow: Data → Features → Model → Experiment → Result.

Frontend: Streamlit.

## How to Run

For the first run, clone the project, install dependencies, and install the KOMUS commands.

### First Run

```powershell
git clone https://github.com/komus-research/komus-credit-risk.git
cd komus-credit-risk
uv sync
.\scripts\install-komus-commands.ps1
```

After installation, close and reopen PowerShell, then run:

```powershell
comus
```

The application can now be launched with a single command from any directory.

### Manual Launch

Canonical manual launch:

```powershell
uv run python -m streamlit run app/streamlit_app.py
```

## Dataset

`Data_final.xlsb` is not stored in GitHub. If you have the file, after running `comus` you can select it using the file picker in the application.

Alternatively, place it in advance at:

`data/raw/Data_final.xlsb`

The full current experiment uses the validated `Data_final` version. Another file can be selected and checked, but automatic preparation of a completely new dataset for ML is still under development.

## What You Can Try

- select a data source;
- enable and disable feature groups and individual features;
- choose CatBoost, XGBoost, LightGBM, or `GBDT_mean`;
- configure the experiment config;
- review the plan before running;
- run a 3-fold OOF experiment;
- view and compare saved results;
- freely navigate between stages that have already been reached.

## Current Limitations

- arbitrary dataset onboarding is not yet implemented;
- a new dataset requires its own Dataset Contract, Feature Registry, and Evaluation Population;
- `Q_B1_norm` and `Q_B2_norm` are not predictors;
- the final test set is not used for model selection;
- the LLM Result Interpreter is not a credit predictor;
- user-facing LLM explanations are not yet connected as a ready-to-use feature in the current Streamlit flow.

## Current Status

- core model research Stages 1–20 are completed and fixed according to the current project docs;
- current development focuses on the reproducible experiment pipeline and user-facing prototype;
- next product direction: new dataset preparation / feature onboarding, model onboarding, and result interpretation.

## Main Goal

The goal is not simply to achieve a high Gini, but to build a reproducible research system that makes it possible to:

- fairly compare models using the same protocol;
- enable, disable, and group features;
- investigate new factors and modern CPU-based approaches;
- measure Gini, ROC-AUC, PR-AUC, Precision, Recall, F1, and error structure;
- account for CPU runtime, resources, and model size;
- explain global and local predictions;
- tune the threshold and business cost scenario for FN/FP;
- account for limits on the volume of manual review;
- preserve reproducible experiment artifacts;
- preserve a presentation-ready history of each research stage;
- gradually evolve into a backend and then a research frontend without duplicating ML logic.

## Documentation

The current project documentation is stored in `docs/`:

- [`PROJECT_CONTEXT.md`](docs/PROJECT_CONTEXT.md) — current project state, baseline, sources, and limitations;
- [`PRODUCT_SPEC.md`](docs/PRODUCT_SPEC.md) — what the research product should be able to do;
- [`BUSINESS_RULES.md`](docs/BUSINESS_RULES.md) — confirmed requirements and client constraints;
- [`ARCHITECTURE.md`](docs/ARCHITECTURE.md) — module boundaries and the system's development direction;
- [`ROADMAP.md`](docs/ROADMAP.md) — work stages and completion criteria;
- [`DECISIONS.md`](docs/DECISIONS.md) — log of significant product, research, and architectural decisions;
- [`RESEARCH_RECORD.md`](docs/RESEARCH_RECORD.md) — unified rules for storing evidence for each Stage and preparing materials for the future report/presentation.

## Research Evidence

The `reports/` directory is part of the research source of truth:

- `reports/summary/` — compact, verifiable summaries;
- `reports/generated/` — machine-readable results, diagnostics, and checkpoints required for reproducibility or the next Stage;
- `reports/figures/` — individual plots and visual tables for analysis, reporting, and presentation;
- `reports/presentation/` — the final curated set of materials directly for the defense.

These directories are allowed to be stored in Git and should not be entirely excluded through `.gitignore`.

## Working Principle

One research question → one controlled experiment → measurement → conclusion.

The working baseline is not rewritten without a reason. The final test set is not used for model, feature, hyperparameter, or threshold selection. Any important result must be reproducible from the data, configuration, seed/split, and saved metadata.

After a significant Stage, the following should remain: a notebook, a machine-readable summary, the required generated artifacts, key figure files, limitations, the decision, and the next research question. This makes it possible to assemble the final report and presentation from verified sources rather than reconstructing the history from memory or old chats.

## Data and Git

The raw dataset `Data_final.xlsb`, other large tabular files, secrets, local environments, caches/logs, and large model checkpoints remain outside regular Git.

This does not mean that research results are categorically excluded from Git: validated tables, diagnostics, reasonably sized OOF/checkpoints, and plots should be stored in the repository when they are needed for reproducibility or the future defense.

If genuinely sensitive data is introduced into the project later, a dedicated rule for it should first be explicitly added to `.gitignore` and the documentation.
