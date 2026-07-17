"""
Project 3: Editorial A/B Test — Synthetic Data Generator
Generates synthetic user-level data simulating a headline A/B test
(Variant A: descriptive headline, Variant B: curiosity-driven headline).

Run: python generate_headline_test_data.py
Output: headline_test_synthetic.csv
"""

import numpy as np
import pandas as pd

# Reproducibility - locking the seed means you get the same dataset every time
np.random.seed(42)

n_users = 200000  # adjust as needed

# Step 1: Assign users to Variant A (control) or B (treatment), 50/50 split
variant = np.random.choice(['A', 'B'], size=n_users, p=[0.5, 0.5])

# Step 2: Assign device type and region (for segmentation analysis later)
device_type = np.random.choice(['mobile', 'desktop', 'tablet'], size=n_users, p=[0.55, 0.35, 0.10])
region = np.random.choice(['Northeast', 'Midwest', 'South', 'West'], size=n_users, p=[0.22, 0.24, 0.32, 0.22])

# Step 3: Assign a random session date within May 2026
session_date = pd.to_datetime(np.random.choice(pd.date_range('2026-05-01', '2026-05-31'), size=n_users))

# Step 4: Build in a realistic click-through rate difference between variants
base_ctr = {'A': 0.08, 'B': 0.11}
device_lift = {'mobile': -0.01, 'desktop': 0.02, 'tablet': 0.0}

click_prob = np.array([
    base_ctr[v] + device_lift[d] for v, d in zip(variant, device_type)
])
click_prob = np.clip(click_prob, 0.01, 0.99)

# Step 5: Simulate whether each user actually clicked through
clicked_through = np.random.binomial(1, click_prob).astype(bool)

# Step 6: Simulate time-on-page (only for users who clicked through)
time_on_page = np.where(
    clicked_through,
    np.random.normal(90, 30, n_users).clip(5, 400).round(0),
    np.nan
)

# Step 7: Simulate bounce (only meaningful for users who clicked through)
bounced = np.where(
    clicked_through,
    np.random.binomial(1, 0.35, n_users).astype(bool),
    True
)

# Step 8: Assemble into a DataFrame
df = pd.DataFrame({
    'user_id': np.arange(1, n_users + 1),
    'variant': variant,
    'device_type': device_type,
    'region': region,
    'session_date': session_date.date,
    'clicked_through': clicked_through,
    'time_on_page_seconds': time_on_page,
    'bounced': bounced
})

# Step 9: Save to CSV
df.to_csv('headline_test_synthetic.csv', index=False)

print(df.groupby('variant')['clicked_through'].mean())
print(df.shape)
print(df.head())
