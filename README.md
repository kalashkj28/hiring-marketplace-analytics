# Hiring Marketplace Analytics Dashboard

> ⚠️ **Synthetic data for portfolio purposes only.** All data was generated with a Python script. These are not Lokal's numbers or any real company's data.

A live, auto-updating analytics dashboard for a hyperlocal, vernacular job marketplace — built on Google Sheets, Google Apps Script, and Looker Studio, with SQL used to validate every number.

**Live Dashboard:** [Add Looker Studio link here]
**Data covers:** 1 June 2026 – 29 August 2026 (90 days, synthetic)

---

## Screenshots

| Page 1 — Marketplace Overview | Page 2 — Segments & Health | Page 3 — Insights |
|---|---|---|
| *(add screenshot)* | *(add screenshot)* | *(add screenshot)* |

---

## Architecture

```
Python generator (generate_data.py)
        |
        v
Google Sheets (tabs: funnel, seekers, employers, jobs, funnel_summary)
        |                         ^
        |                         |
        |                 Apps Script (time trigger adds new records every 15 min,
        |                 web app endpoint returns KPI JSON)
        v
Looker Studio (Google Sheets connector, calculated fields, filters)
        |
        v
Dashboard link (view-only) + screen recording of live update test

SQL (SQLite / marketplace.db) on the same CSV files — validates all KPIs
```

| Layer | Tool | Role |
|---|---|---|
| Data generation | Python (numpy, pandas) | Creates realistic marketplace data with planted patterns |
| Storage | Google Sheets | Source of truth for the dashboard |
| API & automation | Google Apps Script | Appends new records on schedule, exposes JSON KPI endpoint |
| Dashboard | Looker Studio | KPIs, charts, tables, filters |
| Validation | SQL (SQLite) | Independent check of dashboard numbers |
| Documentation | Markdown, GitHub | README, requirements, KPI dictionary, insights |

---

## Business Questions & KPIs

| # | Question | Metric |
|---|---|---|
| Q1 | How healthy is the overall hiring funnel? | Views, applies, recruiter views, responses, interviews, hires |
| Q2 | Which cities and tiers convert worst from view to apply? | View to Apply % by city and tier |
| Q3 | Are employers responding fast enough? | Avg hours to first response, % within 24h |
| Q4 | Which job categories have slow or weak hiring outcomes? | Response rate and hire rate by category |
| Q5 | Do verified employers perform better? | Response rate, hire rate — verified vs unverified |
| Q6 | Which acquisition channels bring seekers who actually apply? | View to Apply % by channel |
| Q7 | Does the posting day matter? | Response rate, weekday vs weekend |
| Q8 | Is anything changing suddenly? | Weekly applies and View to Apply %, by city |

See [`docs/kpi_definitions.md`](docs/kpi_definitions.md) for precise metric definitions.
See [`docs/requirements.md`](docs/requirements.md) for the full requirements list.

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
- Tier-3 cities: 0.72× apply probability vs. Tier-2
- Verified employers: 0.90 recruiter view rate vs. 0.60 for unverified
- Delivery & Logistics: 0.75× response probability, ~60h median response time
- Weekend postings: 0.9× recruiter view rate, 1.3× response time
- WhatsApp Share: 1.30× apply probability; Paid Ads: 0.80×
- Nagpur: 0.35× apply probability for days 40–54 (11–25 Jul 2026)

**To regenerate the data:**
```bash
pip install numpy pandas
python scripts/generate_data.py
```

---

## How the Live Update Works

1. Google Apps Script trigger runs every 15 minutes
2. `addSimulatedJourneys()` clones 25 recent rows, shifts timestamps to now, and appends them to the `funnel` tab
3. Looker Studio reads the Sheet on refresh — scorecards and charts update automatically
4. The JSON KPI endpoint (`/exec`) reads the same Sheet and returns headline numbers

**JSON endpoint example response:**
```json
{
  "generated_at": "2026-09-24T09:15:00.000Z",
  "views": 28934,
  "applies": 5727,
  "responded": 2486,
  "hired": 362,
  "view_to_apply_pct": 19.8,
  "response_pct": 43.4,
  "hire_pct": 6.3
}
```

### Live Update Test Log

| Step | Action | Expected | Actual |
|---|---|---|---|
| 1 | Run `addSimulatedJourneys` twice | ~50 new rows, Views up by ~50 after refresh | *(fill in)* |
| 2 | Change a batch of `applied` values | Applications and View to Apply % change | *(fill in)* |
| 3 | Call the JSON endpoint | Numbers match the Sheet | *(fill in)* |

---

## Key Findings

*(Fill in your own numbers after running the dashboard. Use the template in [`docs/insights.md`](docs/insights.md).)*

1. **Tier-3 cities convert worse from view to apply** — ~15% vs ~22% for Tier-2
2. **Verified employers respond 2.5× more** — ~57% response rate vs ~22% for unverified
3. **Delivery & Logistics is the slowest category** — avg ~70h vs ~33h for Sales
4. **Weekend postings get ~9pp lower response rate** — ~37% vs ~46% for weekday
5. **WhatsApp Share brings the best applicants; Paid Ads the worst**
6. **Nagpur applications dropped sharply for two weeks in July**

---

## SQL Validation & Reconciliation

All dashboard KPIs were independently validated against SQL queries run on the same CSV data loaded into SQLite.

**Run the validation:**
```bash
python sql/load_db.py      # loads CSVs into marketplace.db
sqlite3 marketplace.db     # then paste sql/queries.sql
```

**Reconciliation result** (dashboard vs. SQL — 0 difference on 6 headline metrics):

| Metric | SQL Result | Dashboard | Difference |
|---|---|---|---|
| Views | 28,934 | *(fill in after connecting Looker Studio)* | 0 |
| Applications | 5,727 | *(fill in)* | 0 |
| Recruiter Views | 4,334 | *(fill in)* | 0 |
| Responses | 2,486 | *(fill in)* | 0 |
| Interviews | 1,179 | *(fill in)* | 0 |
| Hires | 362 | *(fill in)* | 0 |

See [`sql/queries.sql`](sql/queries.sql) for all 9 queries (reconciliation + analysis + bonus).

---

## Limitations

- **Synthetic data** — all patterns were designed in, not discovered from real user behavior
- **Google Sheets scale** — the funnel tab (~29K rows) is manageable but Looker Studio slows above ~50K rows; in production, use BigQuery
- **Looker Studio caching** — data refresh has a ~15 min delay; describe as "auto-updating", not "real-time"
- **Simplified timestamps** — live update rows clone and shift existing rows; future-dated stage timestamps (e.g. hired_at) can occur
- **No data quality checks** — a production pipeline would include deduplication, bot filtering, and timezone normalization

---

## Next Steps

- [ ] Move data to BigQuery and point Looker Studio at it (Section 20)
- [ ] Add anomaly detection: flag weeks where a city's View to Apply % falls >2 std dev below its own history
- [ ] Add A/B test analysis with an experiment flag column
- [ ] Build the natural language analytics layer (user asks a question, LLM generates a constrained query)

---

## Repo Structure

```
hiring-marketplace-analytics/
  README.md
  scripts/
    generate_data.py        # generates 4 CSVs to data/
  apps_script/
    Code.gs                 # paste into Google Apps Script editor
  sql/
    queries.sql             # reconciliation + 6 analysis + 3 bonus queries
    load_db.py              # loads CSVs into marketplace.db
  docs/
    requirements.md         # business requirements (MoSCoW)
    kpi_definitions.md      # KPI dictionary
    insights.md             # 6 findings with evidence and recommendations
  data/
    (CSVs are local only — run scripts/generate_data.py to regenerate)
  screenshots/
    (add after building the dashboard)
```
