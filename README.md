# KKU Student Financial Behavior Analysis

## Overview

An exploratory Data Science project on student income, expenses, saving, financial sufficiency, and financial behavior among a voluntary KKU survey sample.

## Research Objective

Describe financial patterns in the surveyed group, examine expense composition, and report exploratory associations with financial position and money sufficiency.

## Dataset

The survey contains 30 voluntary, self-reported respondents. This is not a representative estimate for all KKU students. Raw and respondent-level processed data are excluded from this repository to protect privacy.

## Analytical Workflow

Survey data → data cleaning → derived indicators → EDA → descriptive group comparison → Spearman correlation → sensitivity analysis → insights → presentation

## Key Variables

`TotalIncome`, `TotalExpense`, `NetBalance`, `ExpenseRatio`, `SavingAmount`, `MoneySufficiency_Code`, and `MoneySufficiency_Group` are described in [docs/data_dictionary.md](docs/data_dictionary.md).

## Methodology

- Median and IQR describe skewed financial variables.
- Levels 1–2 form Sufficient and Levels 3–4 form Insufficient for descriptive comparison.
- Spearman correlations use pairwise complete observations; Phase 2 used two-sided permutation p-values with 20,000 fixed-seed permutations.
- The valid ExpenseRatio=4,540% case remains in primary analysis and has a disclosed sensitivity check.

## Key Findings

- Food and housing were the largest typical expense components among 27 complete expense records.
- NetBalance varied across 26 complete cases: 18 positive, 2 zero, and 6 negative.
- SavingAmount and MoneySufficiency_Code showed an exploratory negative association, rho=-0.370, n=30, permutation p=0.047, classified as Weak.

## Important Methodological Notes

Correlation does not establish causation. The sample is voluntary and small. `TotalIncome × NetBalance` is mathematically coupled because NetBalance equals TotalIncome minus TotalExpense. Original Likert anchors are unavailable, so behavior variables remain numerical response codes only.

## Repository Structure

```text
data/        privacy policy and raw-data exclusion notice
docs/        methodology, data dictionary, cleaning, privacy, repository audit
notebooks/   reader-friendly analytical walkthrough
src/         reusable analysis scripts
outputs/     approved aggregate tables and aggregate-only public figures
```

## Reproducibility

The public portion is reproducible from the included aggregate tables, aggregate-only public figures, documentation, and notebook. Full regeneration requires the private raw survey data and private respondent-level workbook, which are intentionally excluded.

## Public GitHub Release

This public package includes the README, aggregate-only walkthrough notebook, source scripts, aggregate tables, public figures under `outputs/figures/public/`, and documentation. It deliberately excludes respondent-level tables, raw-observation plots, and private source data.

## Documentation and Walkthrough

- [Public walkthrough notebook](notebooks/Final_Project_Analysis.ipynb)
- [Methodology](docs/methodology.md)
- [Data dictionary](docs/data_dictionary.md)
- [Cleaning documentation](docs/cleaning_log.md)
- [Data privacy audit](docs/data_privacy_audit.md)

## How to Run

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook notebooks/Final_Project_Analysis.ipynb
```

The copied `src/` pipeline expects private source workbooks at the repository root and is therefore not executed by default in this public-safe copy.

## Presentation

The final classroom presentation is excluded from the public repository because one appendix visualization contains a respondent-level identifier paired with an individual financial value. It remains appropriate for private instructor distribution under course submission controls.

## Privacy and Limitations

See [docs/data_privacy_audit.md](docs/data_privacy_audit.md) and [docs/methodology.md](docs/methodology.md).
