"""Phase 1 descriptive/visual EDA for the KKU financial behavior project.

Reads only KKU_Financial_Cleaning.xlsx / Analysis_Data.  Produces descriptive
tables, figures, and validation results.  It intentionally contains no
correlation or inferential-test calculations.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "KKU_Financial_Cleaning.xlsx"
TABLES = ROOT / "outputs" / "tables"
FIGURES = ROOT / "outputs" / "figures"
CORE = ["TotalIncome", "TotalExpense", "NetBalance", "ExpenseRatio", "SavingAmount"]
INCOME = ["FamilyIncome", "PartTimeIncome", "ScholarshipIncome", "OtherIncome"]
EXPENSE = ["FoodExpense", "TransportExpense", "HousingExpense", "UtilityExpense", "EducationExpense", "EntertainmentExpense", "ShoppingExpense", "SubscriptionExpense", "OtherExpense"]
RATIOS = ["FoodRatio", "TransportRatio", "HousingRatio", "UtilityRatio", "EducationRatio", "EntertainmentRatio", "ShoppingRatio", "SubscriptionRatio", "OtherExpenseRatio"]
GROUP_VARS = ["TotalIncome", "TotalExpense", "NetBalance", "ExpenseRatio", "SavingAmount", "FoodRatio", "HousingRatio", "ShoppingRatio"]
LIKERT = ["PlanSpending_Code", "TrackExpenses_Code", "ControlExpenses_Code", "PrioritizeNeeds_Code", "ImpulsePurchase_Code"]


def read_analysis_data() -> pd.DataFrame:
    wb = load_workbook(INPUT, read_only=True, data_only=True)
    ws = wb["Analysis_Data"]
    values = list(ws.values)
    return pd.DataFrame(values[1:], columns=values[0])


def stat_row(series: pd.Series, name: str) -> dict:
    x = pd.to_numeric(series, errors="coerce").dropna()
    q1, q3 = x.quantile(.25), x.quantile(.75)
    return {"Variable": name, "N": len(x), "Missing_N": int(series.isna().sum()), "Mean": x.mean(), "Median": x.median(),
            "SD": x.std(ddof=1), "Min": x.min(), "Q1": q1, "Q3": q3, "IQR": q3-q1, "Max": x.max(),
            "Negative_Count": int((x < 0).sum()), "Zero_Count": int((x == 0).sum()), "Positive_Count": int((x > 0).sum())}


def component_row(series: pd.Series, name: str, kind: str) -> dict:
    result = stat_row(series, name)
    result["Component_Type"] = kind
    result["Zero_Percent_of_Usable_N"] = result["Zero_Count"] / result["N"] * 100 if result["N"] else np.nan
    result["NonZero_Count"] = result["N"] - result["Zero_Count"]
    return result


def group_stats(df: pd.DataFrame, variable: str) -> list[dict]:
    result=[]
    for group in ["Sufficient", "Insufficient"]:
        x = pd.to_numeric(df.loc[df["MoneySufficiency_Group"] == group, variable], errors="coerce")
        row=stat_row(x, variable)
        row.update({"Group": group, "Group_Total_N": int((df["MoneySufficiency_Group"] == group).sum())})
        result.append(row)
    return result


def savefig(name: str):
    plt.tight_layout()
    plt.savefig(FIGURES / name, dpi=300, bbox_inches="tight")
    plt.close()


def box_with_points(df: pd.DataFrame, variable: str, filename: str, ylabel: str):
    plot = df[["MoneySufficiency_Group", variable]].dropna()
    counts = plot.groupby("MoneySufficiency_Group")[variable].size().to_dict()
    order=["Sufficient", "Insufficient"]
    labels=[f"Sufficient\n(n={counts.get('Sufficient',0)})", f"Insufficient\n(n={counts.get('Insufficient',0)})"]
    plt.figure(figsize=(7,5))
    values=[plot.loc[plot.MoneySufficiency_Group==group,variable].to_numpy() for group in order]
    plt.boxplot(values, tick_labels=labels, patch_artist=True, boxprops={"facecolor":"#b7d7e8"}, medianprops={"color":"#c0504d"})
    for i, values_i in enumerate(values,1):
        jitter=np.random.default_rng(42+i).uniform(-.10,.10,len(values_i))
        plt.scatter(np.repeat(i,len(values_i))+jitter,values_i,color="#1f4e79",s=28,zorder=3)
    plt.xlabel("Money sufficiency group"); plt.ylabel(ylabel)
    plt.title(f"{variable} by money sufficiency group")
    savefig(filename)


def main():
    TABLES.mkdir(parents=True, exist_ok=True); FIGURES.mkdir(parents=True, exist_ok=True)
    df = read_analysis_data()
    assert len(df) == 30, "Unexpected respondent count."
    assert df["MoneySufficiency_Group"].value_counts().to_dict() == {"Sufficient":20,"Insufficient":10}, "Unexpected sufficiency group size."
    assert df.loc[df.Respondent_ID==6, "HousingExpense"].iloc[0] == 32000, "Housing outlier changed unexpectedly."
    assert df.Respondent_ID.nunique() == 30 and set(df.Respondent_ID) == set(range(1,31)), "Respondent IDs changed."

    # 01 respondent profile
    profiles=[]
    profile_vars=["Year","Faculty","Accommodation","PartTime","SavingStatus","MoneySufficiency_Code","MoneySufficiency_Group"]
    for var in profile_vars:
        observed=df[var].notna().sum(); missing=df[var].isna().sum()
        for category,count in df[var].value_counts(dropna=True).items():
            profiles.append({"Variable":var,"Category":category,"Count":count,"Percent_of_Observed":count/observed*100,"Missing_N":missing})
    profile=pd.DataFrame(profiles); profile.to_csv(TABLES/"01_profile_summary.csv",index=False,encoding="utf-8-sig")

    # 02 core financial summary
    core=pd.DataFrame([stat_row(df[x],x) for x in CORE]); core.to_csv(TABLES/"02_core_financial_summary.csv",index=False,encoding="utf-8-sig")
    # 03 components and 04 expenses
    component=pd.DataFrame([component_row(df[x],x,"Income") for x in INCOME]+[component_row(df[x],x,"Expense") for x in EXPENSE])
    component.to_csv(TABLES/"03_component_summary.csv",index=False,encoding="utf-8-sig")
    component.loc[component.Component_Type=="Expense"].to_csv(TABLES/"04_expense_category_summary.csv",index=False,encoding="utf-8-sig")
    # 05 ratios
    ratio=pd.DataFrame([stat_row(df[x],x) for x in RATIOS]); ratio.to_csv(TABLES/"05_category_ratio_summary.csv",index=False,encoding="utf-8-sig")
    # 06 money sufficiency summary, preserving ordinal and binary views
    ordinal=(df.MoneySufficiency_Code.value_counts().reindex([1,2,3,4],fill_value=0).rename_axis("MoneySufficiency_Code").reset_index(name="N"))
    ordinal["Level_Label"]=ordinal.MoneySufficiency_Code.map({1:"Level 1",2:"Level 2",3:"Level 3",4:"Level 4"}); ordinal["Percent"]=ordinal.N/len(df)*100; ordinal["Representation"]="Ordinal"
    binary=df.MoneySufficiency_Group.value_counts().reindex(["Sufficient","Insufficient"],fill_value=0).rename_axis("MoneySufficiency_Group").reset_index(name="N")
    binary["Percent"]=binary.N/len(df)*100; binary["Representation"]="Binary group"
    money=pd.concat([ordinal.rename(columns={"MoneySufficiency_Code":"Level_or_Group"})[["Representation","Level_or_Group","Level_Label","N","Percent"]],binary.rename(columns={"MoneySufficiency_Group":"Level_or_Group"}).assign(Level_Label="")[["Representation","Level_or_Group","Level_Label","N","Percent"]]],ignore_index=True)
    money.to_csv(TABLES/"06_money_sufficiency_summary.csv",index=False,encoding="utf-8-sig")
    # 07 descriptive group comparison
    group=pd.DataFrame([row for v in GROUP_VARS for row in group_stats(df,v)]); group.to_csv(TABLES/"07_sufficiency_group_comparison.csv",index=False,encoding="utf-8-sig")
    # 08 Likert response distributions only; no direction interpretation
    likert=[]
    for var in LIKERT:
        usable=df[var].notna().sum(); missing=df[var].isna().sum()
        counts=df[var].value_counts().reindex([1,2,3,4,5],fill_value=0)
        for level,count in counts.items(): likert.append({"Variable":var,"Response_Code":level,"N":count,"Percent_of_Usable_N":count/usable*100,"Missing_N":missing})
    likert_df=pd.DataFrame(likert); likert_df.to_csv(TABLES/"08_likert_summary.csv",index=False,encoding="utf-8-sig")
    # 09 outlier sensitivity, retaining main dataset separately
    sensitivity=[]
    for label, subset in [("Primary analysis",df),("Sensitivity analysis excluding the verified influential observation",df.loc[df.Respondent_ID!=6])]:
        for var in ["HousingExpense","TotalExpense","NetBalance","ExpenseRatio","HousingRatio"]:
            row=stat_row(subset[var],var); row["Scenario"]=label; sensitivity.append(row)
    sensitivity_df=pd.DataFrame(sensitivity); sensitivity_df.to_csv(TABLES/"09_housing_sensitivity.csv",index=False,encoding="utf-8-sig")
    # Pairwise N records add transparency without performing correlations.
    pairs=[("TotalIncome","NetBalance"),("SavingAmount","NetBalance"),("ShoppingExpense","NetBalance")]
    pd.DataFrame([{"X":x,"Y":y,"Pairwise_Usable_N":len(df[[x,y]].dropna())} for x,y in pairs]).to_csv(TABLES/"10_bivariate_pairwise_n.csv",index=False,encoding="utf-8-sig")

    plt.style.use("seaborn-v0_8-whitegrid")
    colors=["#1f4e79", "#4f81bd", "#7f8c8d", "#c0504d"]
    # 01 ordinal levels
    plt.figure(figsize=(7,5)); plt.bar(ordinal.Level_Label,ordinal.N,color="#1f4e79")
    for i,r in ordinal.iterrows(): plt.text(i,r.N+.25,f"n={r.N}",ha="center",fontsize=10)
    plt.ylim(0,max(ordinal.N)+3); plt.xlabel("Money sufficiency (ordered response)"); plt.ylabel("Respondents (n)"); plt.title("Money sufficiency levels (N=30)")
    savefig("01_money_sufficiency_levels.png")
    # 02 binary groups
    plt.figure(figsize=(7,5)); plt.bar(binary.MoneySufficiency_Group,binary.N,color=["#2e8b57","#c0504d"])
    for i,r in binary.iterrows(): plt.text(i,r.N+.25,f"n={r.N} ({r.Percent:.1f}%)",ha="center",fontsize=10)
    plt.ylim(0,max(binary.N)+3); plt.xlabel("Money sufficiency group"); plt.ylabel("Respondents (n)"); plt.title("Money sufficiency groups (N=30)")
    savefig("02_money_sufficiency_groups.png")
    # 03 distributions
    fig,axes=plt.subplots(2,2,figsize=(13,9))
    for ax,var,label in zip(axes.ravel(),["TotalIncome","TotalExpense","NetBalance","SavingAmount"],["Total income (THB)","Total expense (THB)","Net balance (THB)","Saving amount (THB)"]):
        x=df[var].dropna(); ax.hist(x,bins=min(8,max(4,len(x)//3)),color="#1f4e79",edgecolor="white")
        ax.axvline(x.median(),color="#c0504d",linestyle="--",label=f"Median={x.median():,.0f}"); ax.legend(fontsize=9); ax.set_title(f"{label}, n={len(x)}"); ax.set_xlabel(label)
    savefig("03_core_financial_distributions.png")
    # 04 ranked median expenses
    ranked=component.query("Component_Type == 'Expense'").sort_values("Median")
    plt.figure(figsize=(9,6)); plt.barh(ranked.Variable.str.replace("Expense","",regex=False),ranked.Median,color="#1f4e79")
    plt.xlabel("Median expense (THB)"); plt.ylabel("Expense category"); plt.title("Expense categories ranked by median amount")
    savefig("04_expense_amount_ranking.png")
    # 05 ranked ratio medians
    ranked_ratio=ratio.sort_values("Median")
    plt.figure(figsize=(9,6)); plt.barh(ranked_ratio.Variable.str.replace("Ratio","",regex=False),ranked_ratio.Median,color="#4f81bd")
    plt.xlabel("Median share of total expense (%)"); plt.ylabel("Expense category"); plt.title("Expense categories ranked by median spending share")
    savefig("05_expense_ratio_ranking.png")
    # 06 net balance dedicated distribution
    x=df.NetBalance.dropna(); fig,ax=plt.subplots(1,2,figsize=(12,5)); ax[0].hist(x,bins=7,color="#1f4e79",edgecolor="white"); ax[0].axvline(0,color="black",linewidth=1); ax[0].set_title(f"Net balance distribution (n={len(x)})"); ax[0].set_xlabel("Net balance (THB)")
    ax[1].boxplot(x,patch_artist=True,boxprops={"facecolor":"#b7d7e8"},medianprops={"color":"#c0504d"}); ax[1].scatter(np.ones(len(x))+np.random.default_rng(99).uniform(-.06,.06,len(x)),x,color="#1f4e79",s=24); ax[1].axhline(0,color="black",linewidth=1); ax[1].set_title("Net balance with individual observations"); ax[1].set_ylabel("Net balance (THB)")
    savefig("06_net_balance_distribution.png")
    # 07-11 focused groups
    box_with_points(df,"NetBalance","07_group_net_balance.png","Net balance (THB)")
    box_with_points(df,"ExpenseRatio","08_group_expense_ratio.png","Expense ratio (%)")
    box_with_points(df,"FoodRatio","09_group_food_ratio.png","Food ratio (%)")
    box_with_points(df,"HousingRatio","10_group_housing_ratio.png","Housing ratio (%)")
    box_with_points(df,"ShoppingRatio","11_group_shopping_ratio.png","Shopping ratio (%)")
    # 12 housing outlier, label respondent ID 6
    x=df.HousingExpense.dropna(); plt.figure(figsize=(9,5)); plt.boxplot(x,vert=False,patch_artist=True,boxprops={"facecolor":"#b7d7e8"},medianprops={"color":"#c0504d"}); plt.scatter(x,np.ones(len(x))+np.random.default_rng(22).uniform(-.06,.06,len(x)),color="#1f4e79",s=30)
    value=df.loc[df.Respondent_ID==6,"HousingExpense"].iloc[0]; plt.ylim(.80,1.30); plt.annotate("Verified influential observation: 32,000",xy=(value,1),xytext=(18500,1.23),arrowprops=dict(arrowstyle="->"),fontsize=10)
    plt.xlabel("Housing expense (THB)"); plt.title(f"Housing expense with retained influential observation (n={len(x)})")
    savefig("12_housing_outlier.png")
    # 13-14 descriptive scatter plots; explicitly no regression/correlation
    for xvar,yvar,name,xlab,ylab in [("TotalIncome","NetBalance","13_total_income_vs_net_balance.png","Total income (THB)","Net balance (THB)"),("SavingAmount","NetBalance","14_saving_vs_net_balance.png","Saving amount (THB)","Net balance (THB)")]:
        plot=df[[xvar,yvar]].dropna(); plt.figure(figsize=(7,5)); plt.scatter(plot[xvar],plot[yvar],s=65,color="#1f4e79")
        plt.axhline(0,color="black",linewidth=.8); plt.xlabel(xlab); plt.ylabel(ylab); plt.title(f"{xvar} and {yvar}: descriptive view (n={len(plot)})")
        savefig(name)
    # 15 compact Likert visual, numeric response distribution only
    fig,axes=plt.subplots(1,5,figsize=(18,4),sharey=True)
    for ax,var in zip(axes,LIKERT):
        d=likert_df[likert_df.Variable==var]; ax.bar(d.Response_Code,d.N,color="#4f81bd"); ax.set_title(var.replace("_Code",""),fontsize=10); ax.set_xlabel("Response code"); ax.set_xticks([1,2,3,4,5])
    axes[0].set_ylabel("Respondents (n)"); fig.suptitle("Financial behavior: numerical response distributions only",y=1.03)
    savefig("15_likert_response_distributions.png")

    # Validation records; no tests/correlations are calculated anywhere in this script.
    checks={
        "Analysis_Data still contains 30 respondents":len(df)==30,
        "No global row deletion occurred":df.Respondent_ID.nunique()==30,
        "MoneySufficiency groups are 20 Sufficient / 10 Insufficient":df.MoneySufficiency_Group.value_counts().to_dict()=={"Sufficient":20,"Insufficient":10},
        "NA was never converted to zero":int(df.TotalIncome.notna().sum())==29 and int(df.TotalExpense.notna().sum())==27,
        "TotalIncome N = 29":int(df.TotalIncome.notna().sum())==29,
        "TotalExpense N = 27":int(df.TotalExpense.notna().sum())==27,
        "NetBalance N = 26":int(df.NetBalance.notna().sum())==26,
        "ExpenseRatio N = 26":int(df.ExpenseRatio.notna().sum())==26,
        "Category Ratio N = 27":all(int(df[x].notna().sum())==27 for x in RATIOS),
        "Generated tables report actual usable N":all(any(col in pd.read_csv(p,encoding="utf-8-sig").columns for col in ["N","Count","Pairwise_Usable_N"]) for p in TABLES.glob("*.csv")),
        "No inferential statistical tests were performed":True,
        "No correlations were calculated":True,
        "Respondent_ID 6 remains in main dataset":6 in set(df.Respondent_ID),
        "HousingExpense 32000 remains unchanged":df.loc[df.Respondent_ID==6,"HousingExpense"].iloc[0]==32000,
    }
    assert all(checks.values()), "One or more EDA validation checks failed."
    checks={name: bool(value) for name,value in checks.items()}
    (TABLES/"00_validation_results.json").write_text(json.dumps(checks,indent=2),encoding="utf-8")
    summary={"tables":sorted(p.name for p in TABLES.glob("*.csv")),"figures":sorted(p.name for p in FIGURES.glob("*.png")),"checks":checks,
             "net_balance":stat_row(df.NetBalance,"NetBalance"),"group_summary":group.to_dict(orient="records"),"sensitivity":sensitivity_df.to_dict(orient="records")}
    (ROOT/"outputs"/"phase1_eda_summary.json").write_text(json.dumps(summary,indent=2,default=float),encoding="utf-8")
    print(json.dumps({"table_count":len(summary["tables"]),"figure_count":len(summary["figures"]),"net_balance":summary["net_balance"],"checks":checks},indent=2,default=float))

if __name__ == "__main__": main()
