# Hiring Marketplace Analytics Dashboard

> ⚠️ **Synthetic data for portfolio purposes only.** All data was generated with a Python script. These are not real numbers or any real company's data.

A live analytics dashboard for a hyperlocal, vernacular job marketplace - built using Python, Streamlit, Plotly, and pandas. 

**Live Dashboard:** https://hiring-marketplace-analytics-28.streamlit.app/
**Data covers:** 1 June 2026 - 29 August 2026 (90 days, synthetic)

---


## Architecture

```
Python generator (generate_data.py)
        |
        v
Google Sheets (Live Data Source)     SQLite DB (marketplace.db)
        |                                   |
        v                                   v
Streamlit App (dashboard.py)         SQL Validation (queries.sql)
        |
        v
Interactive Live Dashboard
```

| Layer | Tool | Role |
|---|---|---|
| Data generation | Python (numpy, pandas) | Creates realistic marketplace data with planted patterns |
| Storage | Google Sheets / SQLite | Live source of truth for the dashboard and local validation |
| Dashboard | Streamlit, Plotly | KPIs, interactive charts, data tables, and dynamic filtering |
| Validation | SQL (SQLite) | Independent check of dashboard numbers |

---

## Business Questions & KPIs

| # | Question | Metric |
|---|---|---|
| Q1 | How healthy is the overall hiring funnel? | Views, applies, recruiter views, responses, interviews, hires |
| Q2 | Which cities and tiers convert worst from view to apply? | View to Apply % by city and tier |
| Q3 | Are employers responding fast enough? | Avg hours to first response, % within 24h |
| Q4 | Which job categories have slow or weak hiring outcomes? | Response rate and hire rate by category |
| Q5 | Do verified employers perform better? | Response rate, hire rate - verified vs unverified |
| Q6 | Which acquisition channels bring seekers who actually apply? | View to Apply % by channel |
| Q7 | Does the posting day matter? | Response rate, weekday vs weekend |
| Q8 | Is anything changing suddenly? | Weekly applies and View to Apply %, by city |

See `docs/kpi_definitions.md` for precise metric definitions.

---

## Data Description

Four synthetic tables, generated with a fixed seed (42) so results are reproducible.

| Table | Rows | Description |
|---|---|---|
| `seekers` | ~6,000 | Job seekers across 21 cities, 8 languages, 4 acquisition channels |
| `employers` | 400 | Employers, 60% verified |
| `jobs` | 2,000 | Jobs across 7 categories and all cities |
| `funnel` | ~29,000 | One row per seeker-job view, with all funnel stages as flags |

**Planted patterns** (designed into the data to create realistic stories):
- Tier-3 cities: 0.72x apply probability vs. Tier-2
- Verified employers: 0.90 recruiter view rate vs. 0.60 for unverified
- Delivery & Logistics: 0.75x response probability, ~60h median response time
- Weekend postings: 0.9x recruiter view rate, 1.3x response time
- WhatsApp Share: 1.30x apply probability; Paid Ads: 0.80x
- Nagpur: 0.35x apply probability for days 40-54 (11-25 Jul 2026)

**To regenerate the data:**
```bash
python scripts/generate_data.py
```

---

## Key Findings

1. **Tier-3 cities convert worse from view to apply** - ~15.2% vs ~22.0% for Tier-2
2. **Verified employers respond 2.5x more** - 57.4% response rate vs 22.2% for unverified
3. **Delivery & Logistics is the slowest category** - avg 70.5h vs 33.0h for Sales
4. **Weekend postings get lower response rate** - 36.6% vs 46.0% for weekday
5. **WhatsApp Share brings the best applicants; Paid Ads the worst** - 25.1% vs 15.7% apply rate
6. **Nagpur applications dropped sharply for two weeks in July** - dropped to ~6-9% apply rate

---

## SQL Validation & Reconciliation

The six headline funnel counts were reconciled against SQL queries run on the same CSV data loaded into SQLite.

**Run the validation:**
```bash
python sql/load_db.py      # loads CSVs into marketplace.db
sqlite3 marketplace.db     # then paste sql/queries.sql
```

**Reconciliation result** (dashboard vs. SQL - 0 difference on headline metrics):

| Metric | SQL Result | Dashboard | Difference |
|---|---|---|---|
| Views | 28,934 | 28,934 | 0 |
| Applications | 5,727 | 5,727 | 0 |
| Recruiter Views | 4,334 | 4,334 | 0 |
| Responses | 2,486 | 2,486 | 0 |
| Interviews | 1,179 | 1,179 | 0 |
| Hires | 362 | 362 | 0 |

---

## Limitations

- **Synthetic data** - all patterns were designed in, not discovered from real user behavior.
- **Google Sheets scale** - the funnel tab (~29K rows) is manageable, but for production >50K rows, a proper database (like BigQuery) is needed.
- **Cache Delay** - The dashboard fetches from Google Sheets with a 60-second cache (TTL). Edits in the Sheet take up to a minute to reflect.
- **No data quality checks** - a production pipeline would include deduplication, bot filtering, and timezone normalization.

---

## Repo Structure

```
hiring-marketplace-analytics/
  dashboard.py              # Streamlit dashboard code (fetches data from Google Sheets)
  requirements.txt          # Python dependencies
  scripts/
    generate_data.py        # generates CSVs locally
  sql/
    queries.sql             # reconciliation + analysis queries
    load_db.py              # loads CSVs into SQLite
  docs/
    requirements.md         # business requirements (MoSCoW)
    kpi_definitions.md      # KPI dictionary
    insights.md             # findings and recommendations
```
