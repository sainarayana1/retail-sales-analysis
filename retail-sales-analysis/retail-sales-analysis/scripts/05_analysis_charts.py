"""Pandas analysis + matplotlib charts -> outputs/charts/"""
import pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("data/superstore_clean.csv", parse_dates=["Order Date"])
out = "outputs/charts/"

m = df.groupby("Year-Month")[["Sales", "Profit"]].sum()
ax = m.plot(figsize=(11, 4.5), title="Monthly Sales & Profit")
ax.set_ylabel("Amount ($)"); plt.xticks(rotation=45); plt.tight_layout(); plt.savefig(out + "1_monthly_trend.png", dpi=150); plt.close()

s = df.groupby("Sub-Category")["Profit"].sum().sort_values()
s.plot.barh(figsize=(8, 6), color=["#d9534f" if v < 0 else "#2e7d32" for v in s], title="Total Profit by Sub-Category")
plt.xlabel("Profit ($)"); plt.tight_layout(); plt.savefig(out + "2_profit_by_subcategory.png", dpi=150); plt.close()

df["Discount Band"] = pd.cut(df["Discount"], [-.01, 0, .2, .4, 1], labels=["0%", "1-20%", "21-40%", ">40%"])
g = df.groupby("Discount Band", observed=True)[["Sales", "Profit"]].sum()
d = g["Profit"] / g["Sales"] * 100
ax = d.plot.bar(figsize=(7, 4.5), color="#1f77b4", title="Profit Margin % by Discount Band")
ax.set_ylabel("Profit margin (%)"); ax.axhline(0, color="black", lw=.8); plt.xticks(rotation=0)
plt.tight_layout(); plt.savefig(out + "3_discount_vs_margin.png", dpi=150); plt.close()

p = df.pivot_table(index="Region", columns="Category", values="Sales", aggfunc="sum")
p.plot.bar(figsize=(8, 5), title="Sales by Region and Category"); plt.xticks(rotation=0)
plt.ylabel("Sales ($)"); plt.tight_layout(); plt.savefig(out + "4_region_category.png", dpi=150); plt.close()

print("Total sales : ${:,.0f}".format(df.Sales.sum()))
print("Total profit: ${:,.0f}  (margin {:.1f}%)".format(df.Profit.sum(), df.Profit.sum() / df.Sales.sum() * 100))
print("\nMargin % by discount band:\n", d.round(2).to_string())
print("\nLoss-making sub-categories:", list(s[s < 0].index) or "none")
print("Charts saved to outputs/charts/")
