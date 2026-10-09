# Data Privacy Audit

## Classification

| Candidate | Classification | Reason |
|---|---|---|
| Raw survey CSV | PRIVATE | Exact timestamps, free text, detailed demographics, and respondent-level financial values. |
| Cleaning/analysis workbooks | PRIVATE | Respondent-level financial, demographic, saving, behavior-code, and sufficiency data. |
| Aggregate CSV tables | PUBLIC-SAFE | Summaries, group counts, and approved correlation results without respondent rows. |
| Expense-ratio investigation table | PRIVATE — EXCLUDED FROM PUBLIC REPOSITORY | It contains respondent-level financial and survey-derived values, so it must not be published. |
| Approved aggregate and de-identified figures | PUBLIC-SAFE | Aggregate/descriptive visuals without respondent identifiers or respondent-level record callouts. |
| Housing-outlier visual | PRIVATE — EXCLUDED FROM PUBLIC REPOSITORY | It contained a respondent-level identifier paired with an individual financial value. |
| Final presentation | PRIVATE / INSTRUCTOR-ONLY — EXCLUDED FROM PUBLIC REPOSITORY | It embeds a respondent-level visual disclosure. |

## Decision

Do not publish raw or processed respondent-level data. Public reproducibility is limited to approved aggregates and documentation. No names, email addresses, phone numbers, student IDs, credentials, or API secrets were copied.

## Release artifact classification

| Artifact category | Public-release status |
|---|---|
| README | PUBLIC-SAFE |
| Public walkthrough notebook | PUBLIC-SAFE |
| Source scripts | PUBLIC-SAFE; private-data pipeline inputs and private exports are excluded by `.gitignore` |
| Aggregate tables | PUBLIC-SAFE, excluding the private expense-ratio investigation table |
| Figures | PUBLIC-SAFE aggregate-only release layer under `outputs/figures/public/` |
| Documentation | PUBLIC-SAFE |
| Final presentation | PRIVATE / INSTRUCTOR-ONLY — excluded from public GitHub |

### Figure classification after rendered-content review

**PUBLIC-SAFE aggregate release figures:** `public/01_money_sufficiency_public.png`, `public/02_financial_summary_public.png`, `public/03_expense_categories_public.png`, `public/04_net_balance_summary_public.png`, `public/05_saving_sufficiency_public.png`, `public/06_expense_ratio_sensitivity_public.png`, and `public/07_correlation_summary_public.png`.

**PRIVATE / EXCLUDED figures:** `12_housing_outlier.png` (respondent identifier paired with an individual financial value).

**PRIVATE / EXCLUDED raw-observation figures:** `07_group_net_balance.png`, `08_group_expense_ratio.png`, `09_group_food_ratio.png`, `10_group_housing_ratio.png`, `11_group_shopping_ratio.png`, `18_total_income_vs_net_balance_spearman.png`, `19_saving_vs_net_balance_spearman.png`, `20_expense_ratio_money_sufficiency_ordinal.png`, `presentation/06b_net_balance_presentation.png`, and `presentation/08b_expense_ratio_presentation.png`. These were removed from the public working tree and protected by `.gitignore`.

### Aggregate-only public visual provenance

| Public claim | Approved aggregate source | Public release visual |
|---|---|---|
| Money-sufficiency group counts and percentages | `outputs/tables/01_profile_summary.csv` | `public/01_money_sufficiency_public.png` |
| Median income, expense, and saving amounts | `outputs/tables/02_core_financial_summary.csv` | `public/02_financial_summary_public.png` |
| Median expense categories | `outputs/tables/04_expense_category_summary.csv` | `public/03_expense_categories_public.png` |
| NetBalance positive/zero/negative counts and median | `outputs/tables/02_core_financial_summary.csv` | `public/04_net_balance_summary_public.png` |
| Group median saving amounts | `outputs/tables/07_sufficiency_group_comparison.csv` | `public/05_saving_sufficiency_public.png` |
| Expense-ratio median and IQR sensitivity | `outputs/tables/12_expense_ratio_sensitivity.csv` | `public/06_expense_ratio_sensitivity_public.png` |
| Selected approved Spearman statistics | `outputs/tables/13_financial_position_correlations.csv`, `14_money_sufficiency_correlations.csv`, and `15_behavior_correlations.csv` | `public/07_correlation_summary_public.png` |

No respondent-level data were read or recomputed while creating these visuals.
