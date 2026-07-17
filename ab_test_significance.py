"""
Project 3: Editorial A/B Test — Statistical Significance Test
Runs a chi-squared test on click-through counts to determine whether
the observed difference between Variant A and Variant B is statistically
significant, or could plausibly be due to random chance.

Requires: pip install numpy scipy

Run: python ab_test_significance.py
"""

import numpy as np
from scipy.stats import chi2_contingency

# --- Input your actual SQL query results here ---
a_total, a_clicks = 99768, 8154     # Variant A: total users, total clicks
b_total, b_clicks = 100232, 11273   # Variant B: total users, total clicks
# --------------------------------------------------

# Build a 2x2 contingency table: rows = variant, columns = [clicked, not clicked]
contingency_table = np.array([
    [a_clicks, a_total - a_clicks],
    [b_clicks, b_total - b_clicks]
])

chi2, p_value, dof, expected = chi2_contingency(contingency_table)

a_ctr = a_clicks / a_total
b_ctr = b_clicks / b_total
absolute_lift_pp = (b_ctr - a_ctr) * 100
relative_lift_pct = (b_ctr - a_ctr) / a_ctr * 100

print(f"Variant A: {a_clicks:,} clicks / {a_total:,} users ({a_ctr:.4%} CTR)")
print(f"Variant B: {b_clicks:,} clicks / {b_total:,} users ({b_ctr:.4%} CTR)")
print(f"Chi-squared statistic: {chi2:.4f}")
print(f"Degrees of freedom: {dof}")
print(f"P-value: {p_value:.15f}")
print(f"Absolute lift: {absolute_lift_pp:.2f} percentage points")
print(f"Relative lift: {relative_lift_pct:.1f}%")

alpha = 0.05
if p_value < alpha:
    print(f"\nResult is statistically significant at alpha = {alpha}.")
    print("Reject the null hypothesis: Variant B's higher CTR is unlikely due to random chance.")
else:
    print(f"\nResult is NOT statistically significant at alpha = {alpha}.")
    print("Fail to reject the null hypothesis: cannot conclude Variant B outperforms Variant A.")
