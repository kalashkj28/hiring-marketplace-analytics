-- ============================================================
-- Hiring Marketplace Analytics — SQL Queries
-- Database: marketplace.db (SQLite)
-- Load with: python sql/load_db.py
-- Run with:  sqlite3 marketplace.db
--            or DB Browser for SQLite
-- ============================================================


-- ============================================================
-- 0. RECONCILIATION QUERY
-- Match these 6 numbers exactly against your Looker Studio
-- dashboard scorecards and the funnel_summary Sheet tab.
-- Record the result in README.md as proof of validation.
-- ============================================================
SELECT
    COUNT(*)              AS views,
    SUM(applied)          AS applies,
    SUM(recruiter_viewed) AS recruiter_views,
    SUM(responded)        AS responses,
    SUM(interviewed)      AS interviews,
    SUM(hired)            AS hires
FROM funnel;


-- ============================================================
-- Q1. Funnel conversion by city (worst view-to-apply first)
-- Answers: Which cities and tiers convert worst?
-- ============================================================
SELECT
    city,
    city_tier,
    COUNT(*)                                                          AS views,
    SUM(applied)                                                      AS applies,
    ROUND(100.0 * SUM(applied) / COUNT(*), 1)                        AS view_to_apply_pct,
    ROUND(100.0 * SUM(responded) / NULLIF(SUM(applied), 0), 1)       AS response_pct,
    ROUND(100.0 * SUM(hired) / NULLIF(SUM(applied), 0), 1)           AS hire_pct
FROM funnel
GROUP BY city, city_tier
ORDER BY view_to_apply_pct;


-- ============================================================
-- Q2. Week-over-week change in applications for Nagpur
-- Answers: Can we spot the Nagpur dip anomaly?
-- Uses: CTE + LAG window function
-- ============================================================
WITH weekly AS (
    SELECT
        view_week,
        SUM(applied) AS applies
    FROM funnel
    WHERE city = 'Nagpur'
    GROUP BY view_week
)
SELECT
    view_week,
    applies,
    LAG(applies) OVER (ORDER BY view_week)                                              AS prev_week,
    ROUND(
        100.0 * (applies - LAG(applies) OVER (ORDER BY view_week))
        / NULLIF(LAG(applies) OVER (ORDER BY view_week), 0),
    1)                                                                                  AS wow_change_pct
FROM weekly
ORDER BY view_week;


-- ============================================================
-- Q3. Best-responding employers in each category
-- Answers: Who are the top performers per job category?
-- Uses: ROW_NUMBER, PARTITION BY
-- ============================================================
WITH emp AS (
    SELECT
        category,
        employer_id,
        SUM(applied)                                                   AS applies,
        ROUND(100.0 * SUM(responded) / NULLIF(SUM(applied), 0), 1)    AS response_pct
    FROM funnel
    GROUP BY category, employer_id
    HAVING SUM(applied) >= 15
),
ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY category
               ORDER BY response_pct DESC, applies DESC
           ) AS rn
    FROM emp
)
SELECT category, employer_id, applies, response_pct
FROM ranked
WHERE rn <= 2
ORDER BY category, rn;


-- ============================================================
-- Q4. Cumulative hires by week (running total)
-- Answers: Is hiring trending up over time?
-- Uses: SUM window function (running total)
-- ============================================================
WITH weekly AS (
    SELECT
        view_week,
        SUM(hired) AS hires
    FROM funnel
    GROUP BY view_week
)
SELECT
    view_week,
    hires,
    SUM(hires) OVER (ORDER BY view_week) AS cumulative_hires
FROM weekly
ORDER BY view_week;


-- ============================================================
-- Q5. Response speed by job category
-- Answers: Which categories are slowest to respond?
-- ============================================================
SELECT
    category,
    COUNT(hours_to_first_response)                                              AS responded_apps,
    ROUND(AVG(hours_to_first_response), 1)                                      AS avg_hours,
    ROUND(
        100.0 * SUM(CASE WHEN hours_to_first_response <= 24 THEN 1 ELSE 0 END)
        / NULLIF(SUM(applied), 0),
    1)                                                                          AS responded_within_24h_pct
FROM funnel
GROUP BY category
ORDER BY avg_hours DESC;


-- ============================================================
-- Q6. Seeker cohorts by signup week
-- Answers: Do newer cohorts apply at the same rate?
-- ============================================================
SELECT
    signup_week,
    COUNT(DISTINCT seeker_id)                                           AS active_seekers,
    SUM(applied)                                                        AS applies,
    ROUND(1.0 * SUM(applied) / NULLIF(COUNT(DISTINCT seeker_id), 0), 2) AS applies_per_seeker
FROM funnel
GROUP BY signup_week
ORDER BY signup_week;


-- ============================================================
-- BONUS Q7. Verified vs unverified employer performance
-- Answers: Does employer verification matter?
-- ============================================================
SELECT
    employer_verified,
    COUNT(*)                                                            AS views,
    SUM(applied)                                                        AS applies,
    ROUND(100.0 * SUM(responded) / NULLIF(SUM(applied), 0), 1)         AS response_rate_pct,
    ROUND(100.0 * SUM(hired) / NULLIF(SUM(applied), 0), 1)             AS hire_rate_pct,
    ROUND(AVG(CASE WHEN hours_to_first_response IS NOT NULL
                   THEN hours_to_first_response END), 1)                AS avg_hrs_to_response
FROM funnel
GROUP BY employer_verified
ORDER BY employer_verified;


-- ============================================================
-- BONUS Q8. Acquisition channel quality
-- Answers: Which channel brings seekers who actually apply?
-- ============================================================
SELECT
    acquisition_channel,
    COUNT(*)                                                            AS views,
    SUM(applied)                                                        AS applies,
    ROUND(100.0 * SUM(applied) / COUNT(*), 1)                          AS view_to_apply_pct,
    ROUND(100.0 * SUM(hired) / NULLIF(SUM(applied), 0), 1)             AS hire_rate_pct
FROM funnel
GROUP BY acquisition_channel
ORDER BY view_to_apply_pct DESC;


-- ============================================================
-- BONUS Q9. Weekday vs weekend posting performance
-- Answers: Does the posting day affect recruiter response?
-- ============================================================
SELECT
    posted_day_type,
    COUNT(*)                                                            AS views,
    SUM(applied)                                                        AS applies,
    ROUND(100.0 * SUM(responded) / NULLIF(SUM(applied), 0), 1)         AS response_rate_pct,
    ROUND(AVG(CASE WHEN hours_to_first_response IS NOT NULL
                   THEN hours_to_first_response END), 1)                AS avg_hrs_to_response
FROM funnel
GROUP BY posted_day_type
ORDER BY posted_day_type;
