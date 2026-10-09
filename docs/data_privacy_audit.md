# การตรวจสอบความเป็นส่วนตัวของข้อมูล

## การจัดประเภท

| รายการ | สถานะ | เหตุผล |
|---|---|---|
| Raw survey CSV | PRIVATE | มีเวลา ข้อความอิสระ ประชากรศาสตร์ละเอียด และค่าการเงินระดับผู้ตอบ |
| workbooks สำหรับ cleaning/analysis | PRIVATE | มีข้อมูลการเงิน ประชากรศาสตร์ เงินออม รหัสพฤติกรรม และความเพียงพอระดับผู้ตอบ |
| ตาราง CSV แบบ aggregate | PUBLIC-SAFE | เป็นผลสรุป จำนวนกลุ่ม และผลสหสัมพันธ์ที่อนุมัติแล้วโดยไม่มีแถวระดับผู้ตอบ |
| ตารางตรวจสอบ ExpenseRatio | PRIVATE — EXCLUDED FROM PUBLIC REPOSITORY | มีค่าการเงินและค่าที่คำนวณระดับผู้ตอบ |
| ภาพ aggregate และ de-identified | PUBLIC-SAFE | เป็นภาพสรุป/พรรณนาโดยไม่มีตัวระบุหรือคำอธิบายระดับผู้ตอบ |
| ภาพ housing outlier | PRIVATE — EXCLUDED FROM PUBLIC REPOSITORY | มีตัวระบุระดับผู้ตอบจับคู่กับค่าการเงินรายบุคคล |
| งานนำเสนอฉบับสุดท้าย | PRIVATE / INSTRUCTOR-ONLY — EXCLUDED FROM PUBLIC REPOSITORY | ฝังภาพที่เปิดเผยระดับผู้ตอบ |

## ข้อสรุป

ไม่เผยแพร่ข้อมูลดิบหรือข้อมูลประมวลผลระดับผู้ตอบ การทำซ้ำแบบสาธารณะจำกัดที่ผลสรุปและเอกสารที่อนุมัติแล้ว ไม่มีการคัดลอกชื่อ อีเมล โทรศัพท์ รหัสนักศึกษา credentials หรือ API secrets

## การจัดประเภทสิ่งเผยแพร่

| ประเภท | สถานะสำหรับเผยแพร่สาธารณะ |
|---|---|
| README | PUBLIC-SAFE |
| Public walkthrough notebook | PUBLIC-SAFE |
| Source scripts | PUBLIC-SAFE; inputs/exports ของ pipeline ส่วนตัวถูกยกเว้นด้วย `.gitignore` |
| ตาราง aggregate | PUBLIC-SAFE ยกเว้นตารางตรวจสอบ ExpenseRatio ส่วนตัว |
| ภาพ | PUBLIC-SAFE เฉพาะชั้นภาพ aggregate-only ภายใต้ `outputs/figures/public/` |
| เอกสาร | PUBLIC-SAFE |
| งานนำเสนอฉบับสุดท้าย | PRIVATE / INSTRUCTOR-ONLY — ไม่เผยแพร่บน GitHub |

### การจัดประเภทภาพหลังตรวจสอบภาพที่ render แล้ว

**ภาพ aggregate ที่ปลอดภัย:** `public/01_money_sufficiency_public.png`, `public/02_financial_summary_public.png`, `public/03_expense_categories_public.png`, `public/04_net_balance_summary_public.png`, `public/05_saving_sufficiency_public.png`, `public/06_expense_ratio_sensitivity_public.png` และ `public/07_correlation_summary_public.png`

**ภาพ PRIVATE / EXCLUDED:** `12_housing_outlier.png` (ตัวระบุระดับผู้ตอบจับคู่กับค่าการเงินรายบุคคล)

**ภาพ raw-observation ที่เป็น PRIVATE / EXCLUDED:** `07_group_net_balance.png`, `08_group_expense_ratio.png`, `09_group_food_ratio.png`, `10_group_housing_ratio.png`, `11_group_shopping_ratio.png`, `18_total_income_vs_net_balance_spearman.png`, `19_saving_vs_net_balance_spearman.png`, `20_expense_ratio_money_sufficiency_ordinal.png`, `presentation/06b_net_balance_presentation.png` และ `presentation/08b_expense_ratio_presentation.png` ถูกลบออกจาก working tree สาธารณะและป้องกันด้วย `.gitignore`

### ที่มาของภาพสาธารณะแบบ aggregate-only

| ข้อความสรุปสาธารณะ | แหล่งผลสรุปที่อนุมัติ | ภาพสาธารณะ |
|---|---|---|
| Money-sufficiency group counts and percentages | `outputs/tables/01_profile_summary.csv` | `public/01_money_sufficiency_public.png` |
| Median income, expense, and saving amounts | `outputs/tables/02_core_financial_summary.csv` | `public/02_financial_summary_public.png` |
| Median expense categories | `outputs/tables/04_expense_category_summary.csv` | `public/03_expense_categories_public.png` |
| NetBalance positive/zero/negative counts and median | `outputs/tables/02_core_financial_summary.csv` | `public/04_net_balance_summary_public.png` |
| Group median saving amounts | `outputs/tables/07_sufficiency_group_comparison.csv` | `public/05_saving_sufficiency_public.png` |
| Expense-ratio median and IQR sensitivity | `outputs/tables/12_expense_ratio_sensitivity.csv` | `public/06_expense_ratio_sensitivity_public.png` |
| Selected approved Spearman statistics | `outputs/tables/13_financial_position_correlations.csv`, `14_money_sufficiency_correlations.csv`, and `15_behavior_correlations.csv` | `public/07_correlation_summary_public.png` |

ไม่มีการอ่านหรือคำนวณใหม่จากข้อมูลระดับผู้ตอบขณะสร้างภาพเหล่านี้
