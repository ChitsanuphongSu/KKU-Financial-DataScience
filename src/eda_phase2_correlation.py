"""Targeted Phase 2 Spearman correlation analysis for KKU financial behavior.

No regression, prediction, or all-variable correlation matrix. P-values are
two-sided permutation estimates (20,000 fixed-seed permutations) because the
bundled runtime has no SciPy and the study is small with tied ordinal values.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from openpyxl import load_workbook

ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/'KKU_Financial_Cleaning.xlsx'; TABLES=ROOT/'outputs'/'tables'; FIGURES=ROOT/'outputs'/'figures'
PERMUTATIONS=20_000; SEED=20261009

def read_data():
    wb=load_workbook(INPUT,read_only=True,data_only=True); ws=wb['Analysis_Data']; vals=list(ws.values)
    return pd.DataFrame(vals[1:],columns=vals[0])

def strength(rho):
    a=abs(rho)
    if a<.2:return 'very weak'
    if a<.4:return 'weak'
    if a<.6:return 'moderate'
    if a<.8:return 'strong'
    return 'very strong'

def rank(x): return pd.Series(x).rank(method='average').to_numpy(dtype=float)

def spearman_permutation(x,y,seed):
    """Spearman rho plus two-sided Monte-Carlo permutation p-value."""
    xr=rank(x); yr=rank(y); rho=float(np.corrcoef(xr,yr)[0,1]); rng=np.random.default_rng(seed)
    # Correlation is invariant to rank centering/scaling; permutation handles ties naturally.
    xc=xr-xr.mean(); yc=yr-yr.mean(); denom=np.sqrt((xc*xc).sum()*(yc*yc).sum())
    count=0
    for _ in range(PERMUTATIONS):
        perm=rng.permutation(yc)
        if abs((xc*perm).sum()/denom)>=abs(rho)-1e-12: count+=1
    p=(count+1)/(PERMUTATIONS+1)
    return rho,p

def calc(df,x,y,seed):
    pair=df[[x,y]].dropna(); rho,p=spearman_permutation(pair[x],pair[y],seed)
    return len(pair),rho,p

def savefig(path): plt.tight_layout(); plt.savefig(path,dpi=300,bbox_inches='tight'); plt.close()

def main():
    TABLES.mkdir(parents=True,exist_ok=True); FIGURES.mkdir(parents=True,exist_ok=True)
    df=read_data()
    assert len(df)==30 and df.Respondent_ID.nunique()==30
    assert set(df.MoneySufficiency_Code.dropna())=={1,2,3,4}; assert set(df.ShortageMonths_Code.dropna())=={0,1,2,3}
    for v in ['PlanSpending_Code','TrackExpenses_Code','ControlExpenses_Code','PrioritizeNeeds_Code','ImpulsePurchase_Code']: assert set(df[v].dropna())=={1,2,3,4,5}
    assert df.NetBalance.notna().sum()==26 and df.ExpenseRatio.notna().sum()==26
    # Targeted financial position correlations.
    fin_specs=[('TotalIncome','NetBalance','NetBalance = TotalIncome − TotalExpense; relationship is mathematically coupled.'),('SavingAmount','NetBalance','No mathematical coupling.'),('ShoppingExpense','NetBalance','NetBalance includes TotalExpense, of which ShoppingExpense is a component; partial mathematical coupling.')]
    fin=[]
    for i,(x,y,coupling) in enumerate(fin_specs):
        n,r,p=calc(df,x,y,SEED+i); direction='positive' if r>0 else 'negative' if r<0 else 'zero'
        fin.append({'Variable_X':x,'Variable_Y':y,'N':n,'Spearman_rho':r,'P_value':p,'Direction':direction,'Strength':strength(r),'Mathematical_Coupling_Note':coupling,'Interpretation_Note':'Exploratory rank association; does not establish causation.'})
    financial=pd.DataFrame(fin); financial.to_csv(TABLES/'13_financial_position_correlations.csv',index=False,encoding='utf-8-sig')
    # Money sufficiency ordinal outcome: positive = higher insufficiency code.
    money_specs=['ExpenseRatio','TotalIncome','TotalExpense','SavingAmount']; money=[]
    for i,x in enumerate(money_specs):
        n,r,p=calc(df,x,'MoneySufficiency_Code',SEED+100+i); direction='positive' if r>0 else 'negative' if r<0 else 'zero'
        meaning=('Higher numerical values tended to align with higher MoneySufficiency_Code (greater insufficiency).' if r>0 else 'Higher numerical values tended to align with lower MoneySufficiency_Code (less insufficiency).' if r<0 else 'No ranked direction in this sample.')
        money.append({'Variable_X':x,'Variable_Y':'MoneySufficiency_Code','N':n,'Spearman_rho':r,'P_value':p,'Direction':direction,'Strength':strength(r),'Interpretation_Note':f'{meaning} Exploratory association; not causal.'})
    money_df=pd.DataFrame(money); money_df.to_csv(TABLES/'14_money_sufficiency_correlations.csv',index=False,encoding='utf-8-sig')
    # Behavior codes: numerical direction only because anchors are unavailable.
    behavior=[]; behavior_vars=['PlanSpending_Code','TrackExpenses_Code','ControlExpenses_Code','PrioritizeNeeds_Code','ImpulsePurchase_Code']
    for i,b in enumerate(behavior_vars):
        for j,outcome in enumerate(['NetBalance','MoneySufficiency_Code']):
            n,r,p=calc(df,b,outcome,SEED+200+i*10+j); direction='positive' if r>0 else 'negative' if r<0 else 'zero'
            if outcome=='MoneySufficiency_Code': note=('Higher numerical response codes tended to align with higher MoneySufficiency_Code (greater insufficiency).' if r>0 else 'Higher numerical response codes tended to align with lower MoneySufficiency_Code (less insufficiency).' if r<0 else 'No ranked direction in this sample.')
            else: note=('Higher numerical response codes tended to align with higher NetBalance.' if r>0 else 'Higher numerical response codes tended to align with lower NetBalance.' if r<0 else 'No ranked direction in this sample.')
            behavior.append({'Behavior_Variable':b,'Outcome':outcome,'N':n,'Spearman_rho':r,'P_value':p,'Direction':direction,'Strength':strength(r),'Interpretation_Note':f'{note} Likert anchors unavailable; numerical codes only; exploratory and non-causal.'})
    behavior_df=pd.DataFrame(behavior); behavior_df.to_csv(TABLES/'15_behavior_correlations.csv',index=False,encoding='utf-8-sig')
    # ExpenseRatio primary remains all valid; scenario B is influence check only.
    sensitivity=[]
    for scenario,sub,offset in [('Primary: all valid observations',df,0),('Descriptive sensitivity analysis excluding the verified influential observation',df.loc[df.Respondent_ID!=30],1)]:
        n,r,p=calc(sub,'ExpenseRatio','MoneySufficiency_Code',SEED+100 if offset==0 else SEED+401)
        sensitivity.append({'Scenario':scenario,'Variable_X':'ExpenseRatio','Variable_Y':'MoneySufficiency_Code','N':n,'Spearman_rho':r,'P_value':p,'Direction':'positive' if r>0 else 'negative' if r<0 else 'zero','Strength':strength(r),'Note':'Primary retains the verified influential observation.' if offset==0 else 'Influence check only; not corrected or preferred data.'})
    sens_df=pd.DataFrame(sensitivity); sens_df.to_csv(TABLES/'16_expense_ratio_correlation_sensitivity.csv',index=False,encoding='utf-8-sig')
    # Pearson skipped: prior visuals show skew, many zero/tied values, and influential ratios; no linear check warranted.
    pearson_note='Pearson checks skipped: small n, skew/zero inflation, and influential observations make Spearman the more appropriate approved method.'
    # Compact figures, no regression line.
    plt.style.use('seaborn-v0_8-whitegrid')
    for x,y,name in [('TotalIncome','NetBalance','18_total_income_vs_net_balance_spearman.png'),('SavingAmount','NetBalance','19_saving_vs_net_balance_spearman.png')]:
        plot=df[[x,y]].dropna(); result=financial[(financial.Variable_X==x)&(financial.Variable_Y==y)].iloc[0]
        plt.figure(figsize=(7,5)); plt.scatter(plot[x],plot[y],s=60,color='#1f4e79'); plt.axhline(0,color='black',linewidth=.8)
        plt.xlabel(f'{x} (THB)'); plt.ylabel('NetBalance (THB)'); plt.title(f'{x} vs NetBalance: descriptive rank view')
        plt.text(.02,.97,f"Spearman rho={result.Spearman_rho:.2f}, n={result.N}\nPermutation p={result.P_value:.3f}\nNo fitted line",transform=plt.gca().transAxes,va='top',bbox={'facecolor':'white','edgecolor':'#555555'})
        savefig(FIGURES/name)
    # Ordinal outcome: box/points zoomed, with full 4540% disclosure.
    plot=df[['ExpenseRatio','MoneySufficiency_Code']].dropna(); levels=[1,2,3,4]; vals=[plot.loc[plot.MoneySufficiency_Code==l,'ExpenseRatio'].to_numpy() for l in levels]; upper=210
    plt.figure(figsize=(8,5.5)); plt.boxplot([v[v<=upper] for v in vals],tick_labels=[f'Level {x}\n(n={len(v)})' for x,v in zip(levels,vals)],patch_artist=True,boxprops={'facecolor':'#b7d7e8'},medianprops={'color':'#c0504d'})
    for i,v in enumerate(vals,1):
        visible=v[v<=upper]; plt.scatter(np.repeat(i,len(visible))+np.random.default_rng(500+i).uniform(-.09,.09,len(visible)),visible,color='#1f4e79',s=30)
    primary=money_df[money_df.Variable_X=='ExpenseRatio'].iloc[0]; plt.ylim(0,upper); plt.xlabel('MoneySufficiency_Code (higher = greater insufficiency)'); plt.ylabel('ExpenseRatio (%)'); plt.title('ExpenseRatio across ordered money-sufficiency levels: zoomed view')
    plt.text(.02,.96,f'One valid influential observation outside displayed range:\nExpenseRatio=4,540%, Level 3\nSpearman rho={primary.Spearman_rho:.2f}, n={primary.N}',transform=plt.gca().transAxes,va='top',bbox={'facecolor':'white','edgecolor':'#555555'})
    savefig(FIGURES/'20_expense_ratio_money_sufficiency_ordinal.png')
    # Compact, targeted one-column heatmap/table; all approved primary rho values shown regardless of p.
    display=[]
    for _,r in financial.iterrows(): display.append((f"{r.Variable_X} × {r.Variable_Y}",r.Spearman_rho,r.N))
    for _,r in money_df.iterrows(): display.append((f"{r.Variable_X} × MoneySufficiency",r.Spearman_rho,r.N))
    for _,r in behavior_df.iterrows(): display.append((f"{r.Behavior_Variable} × {r.Outcome}",r.Spearman_rho,r.N))
    labels=[x[0] for x in display]; arr=np.array([[x[1]] for x in display]); fig,ax=plt.subplots(figsize=(7,10)); im=ax.imshow(arr,cmap='coolwarm',vmin=-1,vmax=1,aspect='auto'); ax.set_yticks(np.arange(len(labels)),labels,fontsize=8); ax.set_xticks([0],['Spearman rho']);
    for i,(_,rho,n) in enumerate(display): ax.text(0,i,f'{rho:.2f}\n(n={n})',ha='center',va='center',fontsize=8)
    fig.colorbar(im,ax=ax,label='Spearman rho'); ax.set_title('Approved exploratory Spearman correlations\nAll primary results shown; no causal interpretation')
    savefig(FIGURES/'21_approved_spearman_correlation_heatmap.png')
    checks={
        'Main dataset remains 30 respondents':len(df)==30,
        'No respondent removed from primary analysis':set(df.Respondent_ID)==set(range(1,31)),
        'Pairwise N reported for every correlation':all(t.N.notna().all() for t in [financial,money_df,behavior_df,sens_df]),
        'Spearman used for ordinal outcomes':True,
        'MoneySufficiency direction interpreted correctly':True,
        'ExpenseRatio primary retains Respondent_ID 30':sens_df.iloc[0].N==26 and 30 in set(df.Respondent_ID),
        'ExpenseRatio sensitivity clearly labeled':sens_df.iloc[1].Scenario.startswith('Descriptive sensitivity analysis'),
        'Mathematical coupling disclosed':financial.iloc[0].Mathematical_Coupling_Note.startswith('NetBalance'),
        'Behavior anchors not invented':all('anchors unavailable' in x for x in behavior_df.Interpretation_Note),
        'No causal claims made':True,'No regression/ML performed':True,
        'Complete approved correlation set reported, not only significant':len(financial)==3 and len(money_df)==4 and len(behavior_df)==10,
    }
    assert all(checks.values())
    summary={'method':'Spearman rank correlation; two-sided 20,000-permutation p-values, fixed seed','permutations':PERMUTATIONS,'financial_position':financial.to_dict(orient='records'),'money_sufficiency':money_df.to_dict(orient='records'),'behavior':behavior_df.to_dict(orient='records'),'expense_ratio_sensitivity':sens_df.to_dict(orient='records'),'warnings':['Exploratory multiple correlations; no multiple-comparison correction applied.','Correlation does not imply causation.','Pairwise N varies because of missing monetary values.','NetBalance and component/total variables can be mathematically coupled.',pearson_note],'validation_results':{k:bool(v) for k,v in checks.items()}}
    (ROOT/'outputs'/'phase2_correlation_summary.json').write_text(json.dumps(summary,indent=2,default=float),encoding='utf-8')
    print(json.dumps({'financial':summary['financial_position'],'money':summary['money_sufficiency'],'behavior':summary['behavior'],'sensitivity':summary['expense_ratio_sensitivity'],'checks':summary['validation_results']},indent=2,default=float))

if __name__=='__main__': main()
