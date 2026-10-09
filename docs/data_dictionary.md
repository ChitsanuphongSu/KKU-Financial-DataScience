# พจนานุกรมข้อมูล (Data Dictionary)

| ตัวแปร | ประเภท / หน่วย | ความหมายและค่าที่ใช้ได้ | สถานะ |
|---|---|---|---|
| FamilyIncome, PartTimeIncome, ScholarshipIncome, OtherIncome | Ratio, THB | องค์ประกอบรายรับรายเดือนแบบจำนวนจริง; NA คือไม่มี/ไม่ถูกต้อง ไม่ใช่ศูนย์ | ข้อมูลนำเข้าที่ทำความสะอาดแล้ว |
| FoodExpense ถึง OtherExpense | Ratio, THB | องค์ประกอบรายจ่ายรายเดือนแบบจำนวนจริง; NA คือไม่มี/ไม่ถูกต้อง ไม่ใช่ศูนย์ | ข้อมูลนำเข้าที่ทำความสะอาดแล้ว |
| SavingAmount | Ratio, THB | จำนวนเงินออมรายเดือนที่รายงาน | ข้อมูลนำเข้าที่ทำความสะอาดแล้ว |
| TotalIncome | Ratio, THB | ผลรวมองค์ประกอบรายรับ 4 ประเภท; เป็น NA หากองค์ประกอบที่จำเป็นเป็น NA | คำนวณขึ้น |
| TotalExpense | Ratio, THB | ผลรวมองค์ประกอบรายจ่าย 9 ประเภท; เป็น NA หากองค์ประกอบที่จำเป็นเป็น NA | คำนวณขึ้น |
| NetBalance | Ratio, THB | TotalIncome ลบ TotalExpense; เป็น NA หากตัวใดตัวหนึ่งเป็น NA | คำนวณขึ้น |
| ExpenseRatio | Ratio, percent | TotalExpense / TotalIncome × 100; เป็น NA เมื่อเศษ/ส่วนหาย หรือ TotalIncome=0 | คำนวณขึ้น |
| FoodRatio ถึง OtherExpenseRatio | Ratio, percent | CategoryExpense / TotalExpense × 100; เป็น NA เมื่อค่าหายหรือรายจ่ายรวมเป็นศูนย์/หาย | คำนวณขึ้น |
| MoneySufficiency_Code | Ordinal | 1=เพียงพอและมีเงินเหลือ; 2=เพียงพอพอดี; 3=ไม่เพียงพอบางเดือน; 4=ไม่เพียงพอเป็นประจำ | Outcome |
| MoneySufficiency_Group | Nominal | Sufficient สำหรับรหัส 1–2; Insufficient สำหรับรหัส 3–4 | กลุ่มเปรียบเทียบ |
| ShortageMonths_Code | Ordinal count | 0–3 เดือน | ผลลัพธ์ประกอบ |
| PlanSpending_Code ถึง ImpulsePurchase_Code | รหัสตัวเลขแบบอันดับ | ค่าที่พบ 1–5; ไม่มี anchors ดั้งเดิม | รหัสพฤติกรรม |

ศูนย์หมายถึงจำนวนเงินศูนย์จริง ค่าสูญหายจะไม่ถูกปฏิบัติเป็นศูนย์โดยปริยาย
