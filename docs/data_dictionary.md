# Data Dictionary

| Variable | Type / unit | Meaning and valid values | Status |
|---|---|---|---|
| FamilyIncome, PartTimeIncome, ScholarshipIncome, OtherIncome | Ratio, THB | Exact monthly income components; NA means unavailable/invalid, not zero | Cleaned input |
| FoodExpense through OtherExpense | Ratio, THB | Exact monthly expense components; NA means unavailable/invalid, not zero | Cleaned input |
| SavingAmount | Ratio, THB | Reported monthly saving amount | Cleaned input |
| TotalIncome | Ratio, THB | Sum of 4 income components; NA if any required component is NA | Derived |
| TotalExpense | Ratio, THB | Sum of 9 expense components; NA if any required component is NA | Derived |
| NetBalance | Ratio, THB | TotalIncome minus TotalExpense; NA if either is NA | Derived |
| ExpenseRatio | Ratio, percent | TotalExpense / TotalIncome × 100; NA for missing denominator/numerator or TotalIncome=0 | Derived |
| FoodRatio through OtherExpenseRatio | Ratio, percent | CategoryExpense / TotalExpense × 100; NA for missing value or zero/missing total expense | Derived |
| MoneySufficiency_Code | Ordinal | 1=เพียงพอและมีเงินเหลือ; 2=เพียงพอพอดี; 3=ไม่เพียงพอบางเดือน; 4=ไม่เพียงพอเป็นประจำ | Outcome |
| MoneySufficiency_Group | Nominal | Sufficient for codes 1–2; Insufficient for codes 3–4 | Comparison group |
| ShortageMonths_Code | Ordinal count | 0–3 months | Supporting outcome |
| PlanSpending_Code through ImpulsePurchase_Code | Ordinal numerical code | Observed values 1–5; original anchors unavailable | Behavior codes |

Zeros represent genuine zero amounts. Missing values are never silently treated as zero.
