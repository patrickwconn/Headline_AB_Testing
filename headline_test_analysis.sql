-- ============================================================
-- Project 3: Editorial A/B Test Analysis — Headline Style
-- Synthetic data simulating a headline A/B test on an editorial site
-- Variant A: descriptive headline (control)
-- Variant B: curiosity-driven headline (treatment)
-- ============================================================

-- ------------------------------------------------------------
-- STEP 1: Table Creation
-- ------------------------------------------------------------
DROP TABLE IF EXISTS headline_test;

CREATE TABLE headline_test (
    user_id BIGINT PRIMARY KEY,
    variant CHAR(1) NOT NULL,
    device_type VARCHAR(20),
    region VARCHAR(50),
    session_date DATE,
    clicked_through BOOLEAN,
    time_on_page_seconds NUMERIC,
    bounced BOOLEAN
);

-- Import (run from psql, adjust path to match your file location):
-- \copy headline_test FROM 'C:\path\to\headline_test_synthetic.csv' WITH (FORMAT CSV, HEADER);

-- ------------------------------------------------------------
-- STEP 2: Data Validation
-- ------------------------------------------------------------

-- Confirm row count
SELECT COUNT(*) FROM headline_test; -- expect 200000

-- Confirm randomization balance (should be close to 50/50)
SELECT variant, COUNT(*) AS total_users
FROM headline_test
GROUP BY variant;

-- Confirm no user appears more than once
SELECT COUNT(*) AS duplicate_users
FROM (
    SELECT user_id, COUNT(*) AS n
    FROM headline_test
    GROUP BY user_id
    HAVING COUNT(*) > 1
) dupes; -- expect 0

-- Confirm null-handling logic: non-clickers should have no time_on_page value
SELECT COUNT(*) FROM headline_test
WHERE clicked_through = TRUE AND time_on_page_seconds IS NULL; -- expect 0

SELECT COUNT(*) FROM headline_test
WHERE clicked_through = FALSE AND time_on_page_seconds IS NOT NULL; -- expect 0

-- ------------------------------------------------------------
-- STEP 3: Core Conversion Rate by Variant
-- ------------------------------------------------------------
SELECT variant,
       COUNT(*) AS total_users,
       SUM(CASE WHEN clicked_through THEN 1 ELSE 0 END) AS total_clicks,
       CAST(SUM(CASE WHEN clicked_through THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) AS click_through_rate
FROM headline_test
GROUP BY variant;

-- Result:
-- Variant A: 99,768 users, 8,154 clicks, 8.17% CTR
-- Variant B: 100,232 users, 11,273 clicks, 11.25% CTR

-- ------------------------------------------------------------
-- STEP 4: Segmentation by Device Type
-- ------------------------------------------------------------
SELECT variant, device_type,
       COUNT(*) AS total_users,
       CAST(SUM(CASE WHEN clicked_through THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) AS click_through_rate
FROM headline_test
GROUP BY variant, device_type
ORDER BY device_type, variant;

-- Result: Lift was consistent across all device types (~3 percentage points each)
-- Desktop: ~3.0pp lift | Mobile: ~3.2pp lift | Tablet: ~3.0pp lift

-- ------------------------------------------------------------
-- STEP 5: Segmentation by Region
-- ------------------------------------------------------------
SELECT variant, region,
       COUNT(*) AS total_users,
       CAST(SUM(CASE WHEN clicked_through THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) AS click_through_rate
FROM headline_test
GROUP BY variant, region
ORDER BY region, variant;

-- ------------------------------------------------------------
-- STEP 6: Secondary Metrics — Time on Page and Bounce Rate
-- ------------------------------------------------------------
SELECT variant,
       AVG(time_on_page_seconds) AS avg_time_on_page,
       CAST(SUM(CASE WHEN bounced THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) AS bounce_rate
FROM headline_test
GROUP BY variant;

-- ------------------------------------------------------------
-- NOTE: Statistical significance testing (chi-squared test) was
-- performed separately in Python (ab_test_significance.py), since
-- SQL alone cannot calculate p-values or confidence intervals.
-- Result: chi-squared = 538.37, p-value < 0.001 (highly significant)
-- ------------------------------------------------------------
