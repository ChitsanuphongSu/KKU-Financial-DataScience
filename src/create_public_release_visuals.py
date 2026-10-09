"""Create aggregate-only visualizations for the public repository release.

This script reads only approved aggregate CSV tables already included in the
repository.  It never reads respondent-level data or reconstructs records.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
PUBLIC = ROOT / "outputs" / "figures" / "public"
BLUE = "#1f4e79"
RED = "#c0504d"
GREEN = "#2e8b57"


def read(name: str) -> pd.DataFrame:
    return pd.read_csv(TABLES / name, encoding="utf-8-sig")


def save(name: str) -> None:
    plt.tight_layout()
    plt.savefig(PUBLIC / name, dpi=200, bbox_inches="tight")
    plt.close()


def money(value: float) -> str:
    return f"THB {value:,.0f}"


def main() -> None:
    PUBLIC.mkdir(parents=True, exist_ok=True)

    profile = read("01_profile_summary.csv")
    groups = profile.loc[profile.Variable.eq("MoneySufficiency_Group")]
    plt.figure(figsize=(8, 5))
    bars = plt.bar(groups.Category, groups.Count, color=[GREEN, RED])
    plt.title("Money sufficiency groups (voluntary sample, N=30)")
    plt.ylabel("Respondents (n)")
    for bar, count, pct in zip(bars, groups.Count, groups.Percent_of_Observed):
        plt.text(bar.get_x() + bar.get_width() / 2, count + 0.35, f"n={count} ({pct:.1f}%)", ha="center")
    save("01_money_sufficiency_public.png")

    core = read("02_core_financial_summary.csv")
    financial = core.loc[core.Variable.isin(["TotalIncome", "TotalExpense", "SavingAmount"])]
    labels = ["Total income", "Total expense", "Saving amount"]
    plt.figure(figsize=(8, 5.5))
    bars = plt.bar(labels, financial.Median, color=BLUE)
    plt.title("Approved median financial summaries", pad=18)
    plt.ylabel("THB")
    plt.ylim(0, financial.Median.max() * 1.28)
    for bar, median, n in zip(bars, financial.Median, financial.N):
        plt.text(bar.get_x() + bar.get_width() / 2, median + financial.Median.max() * 0.035, f"{money(median)}\n(n={n})", ha="center")
    save("02_financial_summary_public.png")

    expense = read("04_expense_category_summary.csv")
    order = expense.sort_values("Median", ascending=True)
    labels = order.Variable.str.replace("Expense", "", regex=False).replace({"Other": "Other"})
    plt.figure(figsize=(8, 5.5))
    plt.barh(labels, order.Median, color=BLUE)
    plt.title("Median monthly expense by category")
    plt.xlabel("THB")
    save("03_expense_categories_public.png")

    net = core.loc[core.Variable.eq("NetBalance")].iloc[0]
    counts = [net.Positive_Count, net.Zero_Count, net.Negative_Count]
    plt.figure(figsize=(8, 5.5))
    bars = plt.bar(["Positive", "Zero", "Negative"], counts, color=[GREEN, "#777777", RED])
    plt.title("Net balance summary (complete cases)")
    plt.ylabel("Respondents (n)")
    for bar, count in zip(bars, counts):
        plt.text(bar.get_x() + bar.get_width() / 2, count + 0.3, f"n={count}", ha="center")
    plt.figtext(0.5, 0.01, f"Median NetBalance: {money(net.Median)}; complete cases n={net.N}", ha="center")
    save("04_net_balance_summary_public.png")

    group = read("07_sufficiency_group_comparison.csv")
    saving = group.loc[group.Variable.eq("SavingAmount")]
    plt.figure(figsize=(8, 5))
    bars = plt.bar(saving.Group, saving.Median, color=[GREEN, RED])
    plt.title("Median saving amount by money-sufficiency group", pad=18)
    plt.ylabel("THB")
    plt.ylim(0, saving.Median.max() * 1.22)
    for bar, median, group_n in zip(bars, saving.Median, saving.Group_Total_N):
        plt.text(bar.get_x() + bar.get_width() / 2, median + saving.Median.max() * 0.035, f"{money(median)}\n(group n={group_n})", ha="center")
    plt.figtext(0.5, 0.01, "Exploratory association only; correlation does not establish causation.", ha="center")
    save("05_saving_sufficiency_public.png")

    sensitivity = read("12_expense_ratio_sensitivity.csv")
    overall = sensitivity.loc[sensitivity.Scope.eq("Overall")]
    plt.figure(figsize=(8, 5))
    x = range(len(overall))
    plt.bar(x, overall.Median, color=[BLUE, "#6e9ec5"])
    plt.errorbar(x, overall.Median, yerr=[overall.Median - overall.Q1, overall.Q3 - overall.Median], fmt="none", ecolor="black", capsize=7)
    plt.xticks(x, ["Primary\n(n=26)", "Sensitivity\n(n=25)"])
    plt.title("Expense-ratio sensitivity: median and IQR")
    plt.ylabel("Expense ratio (%)")
    plt.figtext(0.5, 0.01, "Sensitivity is an influence check, not corrected or preferred data.", ha="center")
    save("06_expense_ratio_sensitivity_public.png")

    money_corr = read("14_money_sufficiency_correlations.csv")
    financial_corr = read("13_financial_position_correlations.csv")
    behavior = read("15_behavior_correlations.csv")
    selected = pd.concat([
        financial_corr.loc[financial_corr.Variable_X.eq("TotalIncome") & financial_corr.Variable_Y.eq("NetBalance")].assign(Label="TotalIncome × NetBalance†"),
        money_corr.loc[money_corr.Variable_X.eq("SavingAmount")].assign(Label="SavingAmount × MoneySufficiency"),
        behavior.loc[(behavior.Behavior_Variable.eq("PrioritizeNeeds_Code")) & (behavior.Outcome.eq("MoneySufficiency_Code"))].rename(columns={"Spearman_rho": "Spearman_rho"}).assign(Label="PrioritizeNeeds code × MoneySufficiency*"),
        behavior.loc[(behavior.Behavior_Variable.eq("ImpulsePurchase_Code")) & (behavior.Outcome.eq("NetBalance"))].assign(Label="ImpulsePurchase code × NetBalance*"),
    ], ignore_index=True)
    plt.figure(figsize=(11, 6))
    bars = plt.barh(selected.Label, selected.Spearman_rho, color=[BLUE if x < 0 else RED for x in selected.Spearman_rho])
    plt.axvline(0, color="black", linewidth=0.8)
    plt.xlim(-0.6, 0.6)
    plt.xlabel("Spearman rho")
    plt.title("Selected approved exploratory correlations")
    for bar, rho, n, p in zip(bars, selected.Spearman_rho, selected.N, selected.P_value):
        plt.text(rho / 2, bar.get_y() + bar.get_height() / 2, f"rho={rho:.3f}\nn={n}; p={p:.3f}", va="center", ha="center", color="white", fontsize=9, fontweight="bold")
    plt.figtext(0.5, 0.01, "† Mathematically coupled. * Numerical response codes only; original Likert anchors unavailable.", ha="center")
    save("07_correlation_summary_public.png")


if __name__ == "__main__":
    main()
