# Project 3: Editorial A/B Test Analysis — Headline Style

## Overview
This project simulates and analyzes an A/B test comparing two editorial headline styles — a descriptive headline (Variant A, control) versus a curiosity-driven headline (Variant B, treatment) — to determine which drives stronger reader engagement. The scenario mirrors real decisions made in editorial content strategy, using a synthetic dataset (200,000 simulated users) to avoid exposing proprietary company data.

**Tools used:** Python (NumPy/pandas for data generation, SciPy for significance testing), PostgreSQL (data validation, conversion rate, segmentation), Tableau (visualization).

**Business question:** Does a curiosity-driven headline style produce a statistically significant improvement in click-through rate compared to a descriptive headline, and is the effect consistent across devices and regions?

---

## Methodology

### 1. Synthetic Data Generation
Built a 200,000-row synthetic dataset (`generate_headline_test_data.py`) simulating user-level A/B test data: 50/50 variant assignment, device type, region, session date, click-through outcome, time-on-page, and bounce status. A deliberate click-through rate difference was built in (8% base for Variant A, 11% for Variant B) along with a small device-based adjustment, to simulate a realistic effect size rather than an implausibly large one.

### 2. Data Loading and Validation (PostgreSQL)
Loaded the synthetic CSV into a `headline_test` table and ran four validation checks before any analysis:
- Row count matches expected total (200,000)
- Randomization is balanced between variants (99,768 vs. 100,232 — within natural random variance)
- No duplicate user_id values (confirms no user appears in both groups)
- Null-handling logic is correct (non-clickers have no time-on-page value, clickers always do)

### 3. Core Conversion Rate Analysis (SQL)
Calculated click-through rate per variant using conditional aggregation (`CASE WHEN` + `SUM`):

| Variant | Total Users | Total Clicks | Click-Through Rate |
|---|---|---|---|
| A (descriptive) | 99,768 | 8,154 | 8.17% |
| B (curiosity-driven) | 100,232 | 11,273 | 11.25% |

**Absolute lift:** 3.07 percentage points
**Relative lift:** 37.6%

### 4. Segmentation Analysis (SQL)
Broke down click-through rate by device type and region to check whether the effect was consistent or concentrated in a specific segment.

**Finding:** The lift held consistently across all device types (~3 percentage points each for mobile, desktop, and tablet), indicating a broad, reliable effect rather than a device-specific anomaly. This is a stronger, more actionable result than an uneven lift would be, since it removes ambiguity about where to roll out the change.

### 5. Statistical Significance Testing (Python)
SQL can calculate the observed difference but cannot determine whether that difference is statistically significant — this requires a proper hypothesis test. Ran a chi-squared test (`ab_test_significance.py`) on the click/no-click counts for each variant:

- **Chi-squared statistic:** 538.37
- **P-value:** effectively 0 (< 0.001)
- **Conclusion:** The result is highly statistically significant — Variant B's higher click-through rate is extremely unlikely to be due to random chance.

This division of labor (SQL for data prep and aggregation, Python for statistical testing) reflects a realistic, real-world analyst workflow rather than forcing everything into one tool.

---

## Business Recommendation
Variant B (curiosity-driven headline style) produced a statistically significant 37.6% relative lift in click-through rate compared to Variant A (descriptive headline style), based on a sample of 200,000 users (chi-squared = 538.37, p < 0.001). The lift was consistent across all device types, indicating a broad, reliable effect. Recommend rolling out Variant B across all platforms without needing device-specific exceptions.

---

## Files in This Repository
- `generate_headline_test_data.py` — synthetic data generation script
- `headline_test_analysis.sql` — table creation, validation, conversion rate, and segmentation queries
- `ab_test_significance.py` — chi-squared statistical significance test
- `headline_test_synthetic.csv` — the generated dataset (if included)

---

## Skills Demonstrated
- Synthetic data generation with controlled, realistic probability distributions
- SQL data validation methodology (row counts, randomization checks, duplicate detection, null-handling verification)
- Conditional aggregation (`CASE WHEN` + `SUM`) for conversion rate calculation
- Multi-dimensional segmentation analysis (device type, region)
- Statistical hypothesis testing (chi-squared test) and interpretation of p-values
- Realistic division of labor between SQL and Python in an analytics workflow

---

## Connection to Professional Experience
As a senior editor managing content strategy across 30+ sites, evaluating headline and layout performance is a routine part of the role. This project formalizes that decision-making process into a reproducible, statistically rigorous analytics workflow — directly bridging existing editorial expertise with SQL and Python analytics skills.
