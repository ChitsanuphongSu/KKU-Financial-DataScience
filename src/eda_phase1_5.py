"""Focused ExpenseRatio investigation and sensitivity review; no correlations/tests."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from openpyxl import load_workbook

ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/'KKU_Financial_Cleaning.xlsx'
TABLES=ROOT/'outputs'/'tables'
FIGURES=ROOT/'outputs'/'figures'
COMPONENTS=['FamilyIncome','PartTimeIncome','ScholarshipIncome','OtherIncome','FoodExpense','TransportExpense','HousingExpense','UtilityExpense','EducationExpense','EntertainmentExpense','ShoppingExpense','SubscriptionExpense','OtherExpense']

def read_data():
    wb=load_workbook(INPUT,read_only=True,data_only=True); ws=wb['Analysis_Data']; values=list(ws.values)
    return pd.DataFrame(values[1:],columns=values[0])

def stats(x):
    x=pd.to_numeric(x,errors='coerce').dropna(); q1=x.quantile(.25); q3=x.quantile(.75)
    return {'N':len(x),'Mean':x.mean(),'Median':x.median(),'SD':x.std(ddof=1),'Min':x.min(),'Q1':q1,'Q3':q3,'IQR':q3-q1,'Max':x.max()}

def savefig(path):
    plt.tight_layout(); plt.savefig(path,dpi=300,bbox_inches='tight'); plt.close()

def main():
    TABLES.mkdir(parents=True,exist_ok=True); FIGURES.mkdir(parents=True,exist_ok=True)
    df=read_data(); assert len(df)==30 and df.Respondent_ID.nunique()==30
    extreme=df.loc[df.ExpenseRatio.idxmax()].copy(); rid=int(extreme.Respondent_ID)
    manual=extreme.TotalExpense/extreme.TotalIncome*100
    assert np.isclose(manual,extreme.ExpenseRatio)
    assert rid==30 and extreme.ExpenseRatio==4540 and extreme.HousingExpense==3500
    # Investigation table includes values used to independently calculate the ratio.
    investigation=pd.DataFrame([{'Respondent_ID':rid,'MoneySufficiency_Code':extreme.MoneySufficiency_Code,'MoneySufficiency_Group':extreme.MoneySufficiency_Group,
        'TotalIncome':extreme.TotalIncome,'TotalExpense':extreme.TotalExpense,'NetBalance':extreme.NetBalance,'ExpenseRatio':extreme.ExpenseRatio,
        'Manual_Calculation':f"({extreme.TotalExpense:.0f} / {extreme.TotalIncome:.0f}) × 100",'Manual_ExpenseRatio':manual,
        **{x:extreme[x] for x in COMPONENTS},'Finding':'Very small but valid TotalIncome; retained as reported'}])
    investigation.to_csv(TABLES/'11_expense_ratio_investigation.csv',index=False,encoding='utf-8-sig')
    # Main data retains respondent; scenario B is sensitivity only.
    full=df[df.ExpenseRatio.notna()].copy(); sensitivity=df[(df.ExpenseRatio.notna()) & (df.Respondent_ID!=rid)].copy()
    rows=[]
    for scenario,subset in [('All valid observations',full),('Descriptive sensitivity analysis excluding the influential observation',sensitivity)]:
        row=stats(subset.ExpenseRatio); row.update({'Scenario':scenario,'Scope':'Overall','Group':'All valid observations'}); rows.append(row)
        for group in ['Sufficient','Insufficient']:
            part=subset[subset.MoneySufficiency_Group==group]; row=stats(part.ExpenseRatio); row.update({'Scenario':scenario,'Scope':'Money sufficiency group','Group':group}); rows.append(row)
    sensitivity_table=pd.DataFrame(rows)[['Scenario','Scope','Group','N','Mean','Median','SD','Min','Q1','Q3','IQR','Max']]
    sensitivity_table.to_csv(TABLES/'12_expense_ratio_sensitivity.csv',index=False,encoding='utf-8-sig')
    # New zoomed group view, with the full-range original untouched.
    plt.style.use('seaborn-v0_8-whitegrid')
    zoom_upper=float(sensitivity.ExpenseRatio.max())+15
    plot=full.copy(); order=['Sufficient','Insufficient']; values=[plot.loc[plot.MoneySufficiency_Group==g,'ExpenseRatio'].to_numpy() for g in order]
    labels=[f"Sufficient\n(n={len(values[0])})",f"Insufficient\n(n={len(values[1])})"]
    plt.figure(figsize=(8,5.5)); plt.boxplot(values,tick_labels=labels,patch_artist=True,boxprops={'facecolor':'#b7d7e8'},medianprops={'color':'#c0504d'})
    for i,a in enumerate(values,1):
        visible=a[a<=zoom_upper]; plt.scatter(np.repeat(i,len(visible))+np.random.default_rng(100+i).uniform(-.09,.09,len(visible)),visible,color='#1f4e79',s=32,zorder=3)
    plt.ylim(0,zoom_upper); plt.xlabel('Money sufficiency group'); plt.ylabel('Expense ratio (%)')
    plt.title('ExpenseRatio by money sufficiency group: zoomed descriptive view')
    plt.text(.02,.96,f'1 influential observation outside displayed range:\nExpenseRatio = {extreme.ExpenseRatio:,.0f}% (Insufficient)',transform=plt.gca().transAxes,va='top',fontsize=10,bbox={'facecolor':'white','edgecolor':'#555555','alpha':.95})
    savefig(FIGURES/'08b_group_expense_ratio_zoomed.png')
    # Refined net-balance figure: horizontal boxplot has no meaningless category tick.
    x=df.NetBalance.dropna(); plt.figure(figsize=(10,4.5)); plt.boxplot(x,vert=False,patch_artist=True,boxprops={'facecolor':'#b7d7e8'},medianprops={'color':'#c0504d'})
    plt.scatter(x,np.ones(len(x))+np.random.default_rng(56).uniform(-.07,.07,len(x)),color='#1f4e79',s=30,zorder=3); plt.axvline(0,color='black',linewidth=1)
    plt.yticks([]); plt.xlabel('Net balance (THB)'); plt.title(f'Net balance distribution with individual observations (n={len(x)})')
    savefig(FIGURES/'06b_net_balance_distribution_refined.png')
    checks={
        'Analysis_Data still contains 30 respondents':len(df)==30,
        'No respondent was removed from main dataset':df.Respondent_ID.nunique()==30 and rid in set(df.Respondent_ID),
        'Extreme ExpenseRatio formula independently verified':np.isclose(manual,extreme.ExpenseRatio),
        'Source components inspected':set(COMPONENTS).issubset(investigation.columns),
        'No extreme value changed':df.loc[df.Respondent_ID==rid,'ExpenseRatio'].iloc[0]==4540,
        'Original full-range ExpenseRatio visualization remains available':(FIGURES/'08_group_expense_ratio.png').exists(),
        'Zoomed visualization discloses out-of-range observation':(FIGURES/'08b_group_expense_ratio_zoomed.png').exists(),
        'No correlation was calculated':True,
        'No hypothesis test was performed':True,
        'HousingExpense = 32000 remains unchanged':df.loc[df.Respondent_ID==6,'HousingExpense'].iloc[0]==32000,
    }
    assert all(checks.values())
    summary={'extreme_case':investigation.iloc[0].to_dict(),'sensitivity':sensitivity_table.to_dict(orient='records'),'checks':{k:bool(v) for k,v in checks.items()},'zoom_upper':zoom_upper}
    (ROOT/'outputs'/'phase1_5_review_summary.json').write_text(json.dumps(summary,indent=2,default=float),encoding='utf-8')
    print(json.dumps({'extreme_case':{'Respondent_ID':rid,'ExpenseRatio':extreme.ExpenseRatio,'Manual_ExpenseRatio':manual},'sensitivity':summary['sensitivity'],'checks':summary['checks']},indent=2,default=float))

if __name__=='__main__': main()
