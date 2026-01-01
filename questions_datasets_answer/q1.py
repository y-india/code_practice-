# How does average and median Net PnL behave under Fear, Neutral, and Greed? 
# Are the differences statistically and practically meaningful?


# ---------------------------
# Step 0: Imports
# ---------------------------
import pandas as pd
import numpy as np
from scipy.stats import kruskal
import matplotlib.pyplot as plt
import seaborn as sns
print("imported !")






# ----------------
# Load trader-day dataset
# ---------------------------
trader_day = pd.read_csv("clean_trader_day.csv")






# ------------------------
# Compute mean, median, std PnL per sentiment
# ---------------------------
pnl_summary = trader_day.groupby('sentiment')['daily_net_pnl'].agg(
    mean_pnl='mean',
    median_pnl='median',
    std_pnl='std',
    count='count'
).reset_index()

print("\nNet PnL Summary per Sentiment:\n", pnl_summary)









# -------------
# Compute profitability rate per sentiment
# ---------------------------
profit_rate = trader_day.assign(
    profitable=trader_day['daily_net_pnl'] > 0
).groupby('sentiment')['profitable'].mean().reset_index()

print("\nProfitability Rate per Sentiment:\n", profit_rate)










# ---------------
# Kruskal-Wallis test for statistical significance
# -----------------------
fear = trader_day[trader_day['sentiment']=='Fear']['daily_net_pnl']
neutral = trader_day[trader_day['sentiment']=='Neutral']['daily_net_pnl']
greed = trader_day[trader_day['sentiment']=='Greed']['daily_net_pnl']

stat, p = kruskal(fear, neutral, greed)
print(f"\nKruskal-Wallis statistic: {stat:.4f}, p-value: {p:.4f}")










# ---------------------------
# Visualization
# -----------------
plt.figure(figsize=(8,5))
sns.barplot(data=pnl_summary, x='sentiment', y='mean_pnl', palette='coolwarm')

plt.title("Average Daily Net PnL per Sentiment")

plt.ylabel("Mean Net PnL")
plt.xlabel("Market Sentiment")

plt.show()






ANSWER1 = """We analyzed trader performance using the trader_day dataset, which contains one row per trader per day under a specific sentiment (Fear, Neutral, or Greed). Key metrics include daily Net PnL and profitability.

Net PnL Summary per Sentiment:

Sentiment | Mean PnL | Median PnL | Std PnL | Count
Fear | 5185 | 123 | 31224 | 790
Greed | 4144 | 265 | 29252 | 1174
Neutral | 3439 | 168 | 17448 | 376

The mean PnL is highest under Fear, influenced by a few extreme wins.

Median PnL shows typical traders earn more under Greed (265) than Fear (123).

High standard deviation shows large variability, especially during Fear and Greed.

Profitability Rate per Sentiment:

Sentiment | Profitability
Fear | 60.4%
Greed | 64.3%
Neutral | 62.2%

Traders were most profitable under Greed and least under Fear.

Neutral days are in between, showing moderate results.

Statistical Significance (Kruskal-Wallis Test):

Statistic | p-value
4.7644 | 0.0923

p-value > 0.05, so differences in Net PnL across sentiments are not statistically significant. Differences could be due to random variation.

Conclusion:

Traders behave differently depending on sentiment: Fear days have fewer profitable days, while Greed days have higher profitability.

Extreme wins during Fear inflate mean PnL, but median shows most traders perform better under Greed.

Statistical testing shows differences are not significant, highlighting large variability in trader performance.

"""
print(ANSWER1)