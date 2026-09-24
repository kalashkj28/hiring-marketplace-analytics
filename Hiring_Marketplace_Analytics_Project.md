# Hiring Marketplace Analytics Dashboard

A live, auto-updating analytics dashboard for a hyperlocal, vernacular job marketplace, built on Google Sheets, Google Apps Script and Looker Studio, with SQL used to validate every number.

This document is the complete plan for the project: what to build, why, how, in what order, how to test it, how to write it up, and how to talk about it in an interview.

---

## 1. Project at a glance

| Item | Detail |
|---|---|
| Project name | Hiring Marketplace Analytics Dashboard |
| Purpose | Show an end to end analytics pipeline: data in Google Sheets, an Apps Script layer, a Looker Studio dashboard, and live updates when the data changes |
| Domain | Two sided job marketplace for Tier-2 and Tier-3 India (job seekers, employers, frontline roles, regional languages) |
| Data | Fully synthetic, generated with Python. No real company data |
| Dashboard tool | Looker Studio (free) |
| Data store and API layer | Google Sheets and Google Apps Script |
| Validation | SQL queries (CTEs, window functions) run on the same data, reconciled against dashboard numbers |
| Skills shown | SQL, Excel/Sheets, dashboarding, KPI design, funnel analysis, root cause analysis, requirement documentation, insight communication |
| Target role | Business Analyst at Lokal Jobs (Bangalore, onsite) and similar BA/DA roles |
| Estimated effort | 3 to 4 focused days (a minimum version can be done in 2) |

---

## 2. Why this project (mapped to the job description)

| Job description requirement | What this project demonstrates |
|---|---|
| Strong SQL and Excel proficiency | SQL validation queries with CTEs and window functions, plus Sheets formulas for the funnel summary |
| Experience with dashboards (Looker, Tableau, Power BI, Data Studio) | A published Looker Studio (formerly Google Data Studio) dashboard with KPIs, filters, tables and charts |
| Analyze large datasets to identify trends and insights | About 29,000 funnel records across 21 cities, 7 job categories and 3 months |
| Translate business questions into analytical problems | Section 5 lists the business questions, and each one is mapped to a metric and a chart |
| Build dashboards and reports to track key metrics | Three page report: overview, segments, insights |
| Support forecasting, performance tracking | Weekly trend, week over week change, cumulative hires |
| Document business requirements, definitions, process flows | Requirements list, KPI dictionary and process flow in Sections 5 and 15 |
| Present insights and recommendations clearly | Insights page with finding, evidence and recommendation for each issue |
| Process improvement | Recommendations aimed at recruiter response time, employer verification and Tier-3 conversion |

The same workflow applies to real data. The only difference is that the data source would be a warehouse instead of a generated Sheet.

---

## 3. Honesty note (important)

- The data is synthetic. Say so on the dashboard footer, in the README, on your resume and in interviews.
- The patterns in Section 7 are designed into the data. So the findings show your method (how you detect, quantify and explain a problem), not facts about any real company.
- Never present these numbers as Lokal's numbers or as results from a real internship or job.
- Add Looker Studio and Apps Script to your skills only after you have built this. Describe your level honestly, for example "built my first Looker Studio dashboard for this project".

---

## 4. Architecture

```
Python generator (synthetic data)
        |
        v
Google Sheets (tabs: funnel, seekers, employers, jobs, funnel_summary)
        |                         ^
        |                         |
        |                 Apps Script (time trigger adds new records,
        |                 web app endpoint returns KPI JSON)
        v
Looker Studio (Google Sheets connector, calculated fields, filters)
        |
        v
Dashboard link (view only) + screen recording of the live update test

SQL (SQLite or PostgreSQL) on the same CSV files, used to validate KPIs
```

| Layer | Tool | Role |
|---|---|---|
| Data generation | Python | Creates realistic marketplace data with planted patterns |
| Storage | Google Sheets | Source of truth for the dashboard |
| API and automation | Google Apps Script | Appends new records on a schedule, exposes a JSON KPI endpoint |
| Dashboard | Looker Studio | KPIs, charts, tables, filters |
| Validation | SQL | Independent check of dashboard numbers, and practice for interviews |
| Documentation | Markdown, GitHub | README, requirements, KPI dictionary, insights |

---

## 5. Business context, questions and requirements

### 5.1 Business context

A vernacular, hyperlocal job marketplace connects job seekers and employers in Tier-2 and Tier-3 cities across frontline roles such as sales, customer support, delivery, operations and telecalling. Growth depends on three things working well: seekers finding relevant jobs in their language, seekers actually applying, and employers responding quickly enough that the seeker stays engaged. The dashboard tracks that chain from view to hire.

### 5.2 Business questions the dashboard must answer

| # | Business question | Metric | Where it appears |
|---|---|---|---|
| Q1 | How healthy is the overall hiring funnel? | Views, applies, recruiter views, responses, interviews, hires, stage conversion | Page 1 funnel and scorecards |
| Q2 | Which cities and tiers convert worst from view to apply? | View to apply % by city and tier | Page 2 city table |
| Q3 | Are employers responding fast enough? | Response rate, average hours to first response, % responded within 24 hours | Page 1 scorecards, Page 2 category charts |
| Q4 | Which job categories have slow or weak hiring outcomes? | Response rate, hours to response and hire rate by category | Page 2 |
| Q5 | Do verified employers perform better? | Response rate and hire rate, verified vs unverified | Page 2 |
| Q6 | Which acquisition channels bring seekers who actually apply? | View to apply % by channel | Page 2 |
| Q7 | Does the posting day matter? | Response rate and response time, weekday vs weekend postings | Page 2 |
| Q8 | Is anything changing suddenly? | Weekly applies and view to apply %, by city | Page 1 trend, Page 2 city trend |

### 5.3 Stakeholders

| Stakeholder | What they care about |
|---|---|
| Product | Funnel drop off, language and city experience |
| Growth and marketing | Channel quality, seeker activation |
| Recruiter success and operations | Employer response time, verified employer quality, category level delays |
| Leadership | Hires, conversion, trends |

### 5.4 Requirements (lite business requirements document)

Priority uses MoSCoW: Must, Should, Could.

| ID | Requirement | Priority |
|---|---|---|
| R1 | Dashboard shows view, apply, recruiter view, response, interview and hire counts and stage conversion | Must |
| R2 | Users can filter by date range, city, city tier, language and job category | Must |
| R3 | Dashboard reads from Google Sheets and reflects data changes without rebuilding the report | Must |
| R4 | KPI definitions are documented and consistent across charts | Must |
| R5 | Response speed metrics: average hours to first response and % within 24 hours | Must |
| R6 | Segment comparison: city, category, verified vs unverified, channel, weekday vs weekend | Should |
| R7 | Insights page with findings and recommendations | Should |
| R8 | JSON endpoint returning headline KPIs | Should |
| R9 | Scheduled trigger that adds new records to simulate live data | Should |
| R10 | Anomaly view for a city trend | Could |
| R11 | Natural language query layer (see Section 20, stretch goals) | Could |

### 5.5 Process flow

```
Job seeker journey
  Signs up (city, language, channel)
    -> Views a job in own city
      -> Applies (or leaves)
        -> Recruiter views application (or never does)
          -> Recruiter responds (call, message)
            -> Interview
              -> Hire

Where the marketplace can leak
  view -> apply       : relevance, language, salary, trust
  apply -> recruiter view : employer attention, verification
  recruiter view -> response : speed, category, posting day
  response -> interview -> hire : job quality, fit, drop off
```

---

## 6. Data model

Four CSV files are generated. The dashboard connects to one flat table (`funnel`) so that Looker Studio needs no joins or blending. The other three tables are used for SQL practice and to show relational design.

### 6.1 seekers (about 6,000 rows)

| Column | Type | Description |
|---|---|---|
| seeker_id | text | Unique id, for example S00012 |
| city | text | City of the seeker |
| city_tier | text | Tier-2 or Tier-3 |
| language | text | Preferred language (Hindi, Marathi, Gujarati, Tamil, Telugu, Kannada, Odia, Bengali) |
| age | number | 18 to 50 |
| experience | text | Fresher, 1-3 years, 3+ years |
| acquisition_channel | text | Organic Search, WhatsApp Share, Paid Ads, Referral |
| signup_date | date | Signup date |

### 6.2 employers (400 rows)

| Column | Type | Description |
|---|---|---|
| employer_id | text | Unique id, for example E0042 |
| city | text | City of the employer |
| verified | text | Yes or No |
| company_size | text | 1-10, 11-50, 51-200, 200+ |

### 6.3 jobs (2,000 rows)

| Column | Type | Description |
|---|---|---|
| job_id | text | Unique id |
| employer_id | text | Links to employers |
| city | text | Same city as the employer |
| category | text | Sales, Customer Support, Delivery & Logistics, Operations, Telecalling, Retail, Back Office |
| monthly_salary | number | Monthly salary in rupees |
| salary_band | text | <12k, 12-18k, 18-25k, 25k+ |
| posted_date | date | Posting date |
| posted_day_type | text | Weekday or Weekend |

### 6.4 funnel (flat table, about 29,000 rows, 28 columns)

One row is one seeker viewing one job, and what happened next. Column letters are for the Sheets formulas in Section 9.

| Col | Column | Type | Description |
|---|---|---|---|
| A | journey_id | text | Unique id for the seeker and job view |
| B | seeker_id | text | Seeker |
| C | job_id | text | Job |
| D | employer_id | text | Employer |
| E | city | text | Seeker city (same as job city) |
| F | city_tier | text | Tier-2 or Tier-3 |
| G | language | text | Seeker language |
| H | category | text | Job category |
| I | salary_band | text | Salary band of the job |
| J | acquisition_channel | text | How the seeker joined |
| K | employer_verified | text | Yes or No |
| L | posted_day_type | text | Weekday or Weekend |
| M | signup_week | date | Monday of the seeker signup week |
| N | view_date | date | Date of the job view |
| O | view_week | date | Monday of the view week |
| P | viewed_at | datetime | Job viewed |
| Q | applied_at | datetime | Applied (blank if not applied) |
| R | recruiter_viewed_at | datetime | Recruiter opened the application |
| S | recruiter_responded_at | datetime | Recruiter responded |
| T | interviewed_at | datetime | Interview happened |
| U | hired_at | datetime | Hired |
| V | applied | 0 or 1 | Flag |
| W | recruiter_viewed | 0 or 1 | Flag |
| X | responded | 0 or 1 | Flag |
| Y | interviewed | 0 or 1 | Flag |
| Z | hired | 0 or 1 | Flag |
| AA | hours_to_first_response | number | Hours from apply to recruiter response (blank if none) |
| AB | furthest_stage | text | Viewed, Applied, Recruiter Viewed, Responded, Interviewed, Hired |

Why flags: with 0/1 columns, every rate in Looker Studio becomes `SUM(flag) / SUM(other flag)`, which is easy to read and easy to explain.

---

## 7. Synthetic data design (patterns planted on purpose)

Real analysts find patterns in messy data. Here the patterns are designed in, so the dashboard has real stories to surface. Volumes: 6,000 seekers, 400 employers, 2,000 jobs, about 29,000 funnel rows, 21 cities (14 Tier-2, 7 Tier-3), 90 days starting 1 June 2026.

| # | Pattern | How it is simulated | Where to see it | Question it answers |
|---|---|---|---|---|
| P1 | Tier-3 cities convert worse from view to apply | Apply probability multiplied by 0.72 for Tier-3 seekers | View to apply % by tier and city | Q2 |
| P2 | Verified employers respond far more | Recruiter view probability 0.90 vs 0.60, response probability scaled 1.0 vs 0.6 | Response rate, verified vs unverified | Q5 |
| P3 | Delivery & Logistics is slow to respond | Response probability x0.75, median response time 60 hours vs about 20 to 30 for others | Hours to first response by category | Q3, Q4 |
| P4 | Weekend postings get weaker responses | Recruiter view x0.9, response time x1.3 | Weekday vs weekend | Q7 |
| P5 | WhatsApp share brings the best applicants, paid ads the worst | Apply probability x1.30 for WhatsApp, x0.80 for paid ads | View to apply % by channel | Q6 |
| P6 | Nagpur has a two week drop | Apply probability x0.35 for Nagpur between day 40 and day 54 (about 11 to 25 July 2026) | Weekly applies for Nagpur | Q8 |
| P7 | Salary affects applies | Apply probability x0.85 for under 12k, x1.25 for 25k+ | Salary band vs view to apply % | Q2 |

Roughly what you should see with the provided script and seed (small differences are fine):

| Check | Approximate result |
|---|---|
| Funnel rows | About 28,900 |
| Total applications | About 5,700 |
| View to apply, Tier-2 vs Tier-3 | About 22% vs 15% |
| Response rate, verified vs unverified employers | About 57% vs 22% |
| Average hours to first response, Delivery & Logistics vs Sales | About 70 vs 33 |
| Response rate, weekday vs weekend postings | About 46% vs 37% |
| Nagpur weekly view to apply | Drops to roughly 6 to 9% in the two dip weeks, from about 17 to 30% |

---

## 8. Data generator script

Save as `generate_data.py`, install the requirements (`pip install numpy pandas`), and run `python generate_data.py`. It writes `seekers.csv`, `employers.csv`, `jobs.csv` and `funnel.csv` in the same folder. The seed is fixed, so everyone gets the same data. Change the seed or the constants if you want a different dataset.

```python
"""
Synthetic data generator for a hyperlocal job marketplace analytics project.
Creates four CSVs: seekers, employers, jobs, funnel (flat table used by the dashboard).
All data is simulated. Run: python generate_data.py
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)          # fixed seed so results are reproducible

N_SEEKERS, N_EMPLOYERS, N_JOBS, N_JOURNEYS = 6000, 400, 2000, 30000
START = pd.Timestamp("2026-06-01")
DAYS = 90
END = START + pd.Timedelta(days=DAYS)

# city: (tier, primary language)
CITIES = {
    "Indore": ("Tier-2", "Hindi"), "Jaipur": ("Tier-2", "Hindi"),
    "Lucknow": ("Tier-2", "Hindi"), "Patna": ("Tier-2", "Hindi"),
    "Raipur": ("Tier-2", "Hindi"), "Nagpur": ("Tier-2", "Marathi"),
    "Nashik": ("Tier-2", "Marathi"), "Surat": ("Tier-2", "Gujarati"),
    "Vadodara": ("Tier-2", "Gujarati"), "Coimbatore": ("Tier-2", "Tamil"),
    "Madurai": ("Tier-2", "Tamil"), "Vijayawada": ("Tier-2", "Telugu"),
    "Mysuru": ("Tier-2", "Kannada"), "Bhubaneswar": ("Tier-2", "Odia"),
    "Bilaspur": ("Tier-3", "Hindi"), "Jabalpur": ("Tier-3", "Hindi"),
    "Gorakhpur": ("Tier-3", "Hindi"), "Warangal": ("Tier-3", "Telugu"),
    "Tirunelveli": ("Tier-3", "Tamil"), "Belagavi": ("Tier-3", "Kannada"),
    "Siliguri": ("Tier-3", "Bengali"),
}
city_names = list(CITIES)

CATEGORIES = ["Sales", "Customer Support", "Delivery & Logistics", "Operations",
              "Telecalling", "Retail", "Back Office"]
CAT_W = [0.25, 0.20, 0.20, 0.12, 0.10, 0.08, 0.05]
CAT_SALARY = {"Sales": 16000, "Customer Support": 15000, "Delivery & Logistics": 14000,
              "Operations": 17000, "Telecalling": 12000, "Retail": 13000, "Back Office": 15000}
CHANNELS = ["Organic Search", "WhatsApp Share", "Paid Ads", "Referral"]
CHAN_W = [0.35, 0.25, 0.25, 0.15]

def band(s):
    return "<12k" if s < 12000 else "12-18k" if s < 18000 else "18-25k" if s < 25000 else "25k+"

# ---------- seekers ----------
seeker_city = rng.choice(city_names, N_SEEKERS)
seekers = pd.DataFrame({
    "seeker_id": [f"S{i:05d}" for i in range(N_SEEKERS)],
    "city": seeker_city,
    "city_tier": [CITIES[c][0] for c in seeker_city],
    "language": [CITIES[c][1] if rng.random() < 0.85 else "Hindi" for c in seeker_city],
    "age": np.clip(rng.normal(26, 6, N_SEEKERS), 18, 50).astype(int),
    "experience": rng.choice(["Fresher", "1-3 years", "3+ years"], N_SEEKERS, p=[0.45, 0.35, 0.20]),
    "acquisition_channel": rng.choice(CHANNELS, N_SEEKERS, p=CHAN_W),
    "signup_date": START + pd.to_timedelta(rng.integers(-60, DAYS, N_SEEKERS), unit="D"),
})

# ---------- employers ----------
emp_city = np.array([city_names[i % len(city_names)] for i in range(N_EMPLOYERS)])
employers = pd.DataFrame({
    "employer_id": [f"E{i:04d}" for i in range(N_EMPLOYERS)],
    "city": emp_city,
    "verified": rng.random(N_EMPLOYERS) < 0.60,
    "company_size": rng.choice(["1-10", "11-50", "51-200", "200+"], N_EMPLOYERS, p=[0.35, 0.35, 0.2, 0.1]),
})

# ---------- jobs ----------
job_emp = rng.integers(0, N_EMPLOYERS, N_JOBS)
job_cat = rng.choice(CATEGORIES, N_JOBS, p=CAT_W)
salary = np.array([CAT_SALARY[c] for c in job_cat]) * rng.normal(1.0, 0.25, N_JOBS)
salary = np.clip(salary, 8000, 40000).round(-3)
posted = START + pd.to_timedelta(rng.integers(0, DAYS - 7, N_JOBS), unit="D")
jobs = pd.DataFrame({
    "job_id": [f"J{i:05d}" for i in range(N_JOBS)],
    "employer_id": employers["employer_id"].values[job_emp],
    "city": emp_city[job_emp],
    "category": job_cat,
    "monthly_salary": salary.astype(int),
    "salary_band": [band(s) for s in salary],
    "posted_date": posted,
    "posted_day_type": np.where(posted.dayofweek >= 5, "Weekend", "Weekday"),
})
jobs_by_city = {c: jobs.index[jobs["city"] == c].to_numpy() for c in city_names}

# ---------- funnel journeys ----------
CAT_RESP = {"Delivery & Logistics": 0.75, "Telecalling": 1.10, "Sales": 1.0,
            "Customer Support": 1.0, "Operations": 1.0, "Retail": 0.95, "Back Office": 0.95}
CAT_RESP_HRS = {"Delivery & Logistics": 60, "Telecalling": 10, "Sales": 20,
                "Customer Support": 22, "Operations": 26, "Retail": 24, "Back Office": 30}
CHAN_APPLY = {"WhatsApp Share": 1.30, "Paid Ads": 0.80, "Organic Search": 1.0, "Referral": 1.10}
verified = employers.set_index("employer_id")["verified"].to_dict()

rows = []
for n in range(N_JOURNEYS):
    s = seekers.iloc[rng.integers(0, N_SEEKERS)]
    j = jobs.iloc[rng.choice(jobs_by_city[s["city"]])]
    view_ts = max(j["posted_date"], s["signup_date"]) + pd.Timedelta(
        days=float(rng.exponential(4)), hours=float(rng.uniform(6, 23)))
    if view_ts >= END:
        continue
    day_idx = (view_ts - START).days
    v = verified[j["employer_id"]]

    # apply probability (planted patterns: tier-3 lower, salary, channel, Nagpur dip)
    p_apply = 0.22 * CHAN_APPLY[s["acquisition_channel"]]
    if s["city_tier"] == "Tier-3": p_apply *= 0.72
    if j["salary_band"] == "<12k": p_apply *= 0.85
    if j["salary_band"] == "25k+": p_apply *= 1.25
    if s["city"] == "Nagpur" and 40 <= day_idx <= 54: p_apply *= 0.35
    applied = rng.random() < p_apply

    rv = resp = intv = hired = 0
    t_apply = t_rv = t_resp = t_int = t_hire = pd.NaT
    hrs = np.nan
    if applied:
        t_apply = view_ts + pd.Timedelta(minutes=float(rng.uniform(2, 60)))
        wk = 0.9 if j["posted_day_type"] == "Weekend" else 1.0
        p_rv = (0.90 if v else 0.60) * wk
        if rng.random() < p_rv:
            rv = 1
            t_rv = t_apply + pd.Timedelta(hours=float(rng.exponential(10 if v else 28)))
            p_resp = min(0.95, 0.70 * CAT_RESP[j["category"]] * (1.0 if v else 0.6) * wk)
            if rng.random() < p_resp:
                resp = 1
                med = CAT_RESP_HRS[j["category"]] * (0.7 if v else 1.0) * (1.3 if wk < 1 else 1.0)
                t_resp = t_rv + pd.Timedelta(hours=float(rng.lognormal(np.log(med), 0.6)))
                hrs = round((t_resp - t_apply).total_seconds() / 3600, 1)
                if rng.random() < (0.60 if j["category"] == "Sales" else 0.45):
                    intv = 1
                    t_int = t_resp + pd.Timedelta(days=float(rng.uniform(1, 5)))
                    if rng.random() < 0.32:
                        hired = 1
                        t_hire = t_int + pd.Timedelta(days=float(rng.uniform(1, 4)))
    stage = ("Hired" if hired else "Interviewed" if intv else "Responded" if resp
             else "Recruiter Viewed" if rv else "Applied" if applied else "Viewed")
    view_date = view_ts.normalize()
    rows.append({
        "journey_id": f"JR{n:06d}", "seeker_id": s["seeker_id"], "job_id": j["job_id"],
        "employer_id": j["employer_id"], "city": s["city"], "city_tier": s["city_tier"],
        "language": s["language"], "category": j["category"], "salary_band": j["salary_band"],
        "acquisition_channel": s["acquisition_channel"],
        "employer_verified": "Yes" if v else "No", "posted_day_type": j["posted_day_type"],
        "signup_week": (s["signup_date"] - pd.Timedelta(days=int(s["signup_date"].dayofweek))).date().isoformat(),
        "view_date": view_date.date().isoformat(),
        "view_week": (view_date - pd.Timedelta(days=int(view_date.dayofweek))).date().isoformat(),
        "viewed_at": view_ts, "applied_at": t_apply, "recruiter_viewed_at": t_rv,
        "recruiter_responded_at": t_resp, "interviewed_at": t_int, "hired_at": t_hire,
        "applied": int(applied), "recruiter_viewed": rv, "responded": resp,
        "interviewed": intv, "hired": hired, "hours_to_first_response": hrs,
        "furthest_stage": stage,
    })

funnel = pd.DataFrame(rows)
for c in ["viewed_at", "applied_at", "recruiter_viewed_at", "recruiter_responded_at", "interviewed_at", "hired_at"]:
    funnel[c] = funnel[c].dt.strftime("%Y-%m-%d %H:%M:%S")

seekers["signup_date"] = seekers["signup_date"].dt.strftime("%Y-%m-%d")
jobs["posted_date"] = jobs["posted_date"].dt.strftime("%Y-%m-%d")
employers["verified"] = employers["verified"].map({True: "Yes", False: "No"})

seekers.to_csv("seekers.csv", index=False)
employers.to_csv("employers.csv", index=False)
jobs.to_csv("jobs.csv", index=False)
funnel.to_csv("funnel.csv", index=False)
print("rows:", len(seekers), len(employers), len(jobs), len(funnel))
```

Tip: read the script once before running it. In an interview you should be able to explain how each pattern in Section 7 is created (the lines that multiply `p_apply`, `p_rv`, `p_resp` and the response time `med`).

---

## 9. Google Sheets setup

### 9.1 Create the spreadsheet

1. Create a new Google Sheet named `Hiring Marketplace Analytics`.
2. In File > Settings, set the time zone to India (Kolkata). Apps Script uses this time zone.
3. Import each CSV as its own tab: File > Import > Upload, choose "Insert new sheet(s)", and keep "Convert text to numbers, dates and formulas" ticked. Name the tabs exactly `funnel`, `seekers`, `employers`, `jobs`.
4. In `funnel`, freeze row 1 and check that:
   - the flag columns (V to Z) and `hours_to_first_response` (AA) are numbers
   - the timestamp columns (P to U) are recognised as date time values
   - `view_date` (N) and `view_week` (O) are recognised as dates

Size check: the `funnel` tab is about 29,000 rows by 28 columns, roughly 0.8 million cells. The Sheets limit is 10 million cells per spreadsheet, so there is plenty of room, but the file will feel a little heavy. Do not add more than a few thousand rows during live update tests.

### 9.2 Funnel summary tab (for the funnel chart)

Looker Studio has no built in funnel chart, so create a small helper tab named `funnel_summary` whose numbers are formulas on `funnel`. It updates automatically when `funnel` changes.

| A (Stage) | B (Count) | C (Order) |
|---|---|---|
| Viewed | `=COUNTA(funnel!A2:A)` | 1 |
| Applied | `=SUM(funnel!V2:V)` | 2 |
| Recruiter Viewed | `=SUM(funnel!W2:W)` | 3 |
| Responded | `=SUM(funnel!X2:X)` | 4 |
| Interviewed | `=SUM(funnel!Y2:Y)` | 5 |
| Hired | `=SUM(funnel!Z2:Z)` | 6 |

Put the headers `Stage`, `Count`, `Order` in row 1. In Looker Studio, use this tab as a second data source, and draw a horizontal bar chart with Stage as the dimension, Count as the metric, sorted by Order ascending.

Optional column D, "Conversion from previous stage": `=B3/B2` in D3, and so on down.

### 9.3 Housekeeping

- Keep `seekers`, `employers` and `jobs` as reference tabs. They are used for SQL practice and to show the relational design.
- Do not edit headers after connecting Looker Studio. Renamed headers break charts.

---

## 10. Apps Script layer (API and automation)

Purpose: prove that the pipeline is live. A time based trigger appends new simulated records to the Sheet, and a web app endpoint returns headline KPIs as JSON.

### 10.1 Open the editor

In the spreadsheet, go to Extensions > Apps Script. Delete the sample function and paste the code below into `Code.gs`.

```javascript
const SHEET_NAME = 'funnel';

// Reads the header row and returns a map of column name -> index
function headerIndex_(sh) {
  const header = sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0];
  const idx = {};
  header.forEach((h, i) => { idx[h] = i; });
  return { header: header, idx: idx };
}

// Monday of the week for a date, as yyyy-MM-dd
function weekStart_(d, tz) {
  const dayNum = Number(Utilities.formatDate(d, tz, 'u')); // 1 = Monday
  const monday = new Date(d.getTime() - (dayNum - 1) * 86400000);
  return Utilities.formatDate(monday, tz, 'yyyy-MM-dd');
}

// Appends N simulated journeys by cloning recent rows and shifting their timestamps to "now"
function addSimulatedJourneys() {
  const N = 25;
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sh = ss.getSheetByName(SHEET_NAME);
  const tz = ss.getSpreadsheetTimeZone();
  const info = headerIndex_(sh);
  const header = info.header, idx = info.idx;

  const lastRow = sh.getLastRow();
  const sampleStart = Math.max(2, lastRow - 2999);
  const sample = sh.getRange(sampleStart, 1, lastRow - sampleStart + 1, header.length).getValues();

  const now = new Date();
  const tsCols = ['viewed_at', 'applied_at', 'recruiter_viewed_at',
                  'recruiter_responded_at', 'interviewed_at', 'hired_at'];
  const out = [];
  for (let i = 0; i < N; i++) {
    const row = sample[Math.floor(Math.random() * sample.length)].slice();
    const oldView = row[idx['viewed_at']];
    if (!(oldView instanceof Date)) continue;   // skip rows whose timestamp was not parsed as a date
    const delta = now.getTime() - oldView.getTime();
    tsCols.forEach(function (c) {
      if (row[idx[c]] instanceof Date) row[idx[c]] = new Date(row[idx[c]].getTime() + delta);
    });
    row[idx['journey_id']] = 'JR' + now.getTime() + '_' + i;
    row[idx['view_date']] = Utilities.formatDate(now, tz, 'yyyy-MM-dd');
    row[idx['view_week']] = weekStart_(now, tz);
    out.push(row);
  }
  if (out.length) {
    sh.getRange(sh.getLastRow() + 1, 1, out.length, header.length).setValues(out);
  }
}

// Run once to start the schedule (adds records every 15 minutes)
function createTrigger() {
  ScriptApp.newTrigger('addSimulatedJourneys').timeBased().everyMinutes(15).create();
}

// Run once to stop the schedule (do this after your demo)
function deleteTriggers() {
  ScriptApp.getProjectTriggers().forEach(function (t) { ScriptApp.deleteTrigger(t); });
}

// Web app endpoint: returns headline KPIs as JSON
function doGet() {
  const sh = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
  const idx = headerIndex_(sh).idx;
  const n = sh.getLastRow() - 1;
  const sum = function (name) {
    return sh.getRange(2, idx[name] + 1, n, 1).getValues()
             .reduce(function (a, r) { return a + (Number(r[0]) || 0); }, 0);
  };
  const applies = sum('applied'), responded = sum('responded'), hired = sum('hired');
  const result = {
    generated_at: new Date().toISOString(),
    views: n,
    applies: applies,
    responded: responded,
    hired: hired,
    view_to_apply_pct: Number((100 * applies / n).toFixed(1)),
    response_pct: Number((100 * responded / applies).toFixed(1)),
    hire_pct: Number((100 * hired / applies).toFixed(1))
  };
  return ContentService.createTextOutput(JSON.stringify(result))
                       .setMimeType(ContentService.MimeType.JSON);
}
```

### 10.2 Test the script

1. Select `addSimulatedJourneys` in the function dropdown and click Run. Approve the permissions the first time.
2. Go back to the Sheet and check that about 25 new rows appear at the bottom with current timestamps.

If no rows appear, your timestamp columns were probably imported as text and not as dates. Re-import with "Convert text to numbers, dates and formulas" ticked, or select columns P to U and set Format > Number > Date time.

### 10.3 Start the schedule

Run `createTrigger` once. Every 15 minutes, 25 new rows are added. Run `deleteTriggers` when you finish recording your demo so the sheet does not keep growing.

Simplification to be aware of: because rows are cloned and shifted, later stage timestamps (for example `hired_at`) can land slightly in the future. That is fine for a simulation. If it bothers you, mention it in the README.

### 10.4 Deploy the JSON endpoint

1. Click Deploy > New deployment, choose type Web app.
2. Execute as: Me. Who has access: Only myself is safest while testing. "Anyone" is acceptable for synthetic data if you want a public demo link.
3. Copy the web app URL and test it:

```
curl -L "https://script.google.com/macros/s/YOUR_DEPLOYMENT_ID/exec"
```

Expected response shape:

```json
{"generated_at":"2026-09-24T09:15:00.000Z","views":28934,"applies":5727,"responded":2486,"hired":362,"view_to_apply_pct":19.8,"response_pct":43.4,"hire_pct":6.3}
```

If access is set to "Only myself", the curl call needs authentication. In that case, open the URL in your browser while signed in to show the JSON in a screenshot.

The endpoint is the "API" in the pipeline: Google Sheets to Apps Script API to KPI output. Looker Studio reads the Sheet directly, and the endpoint shows that the same data can serve other consumers.

---

## 11. Looker Studio build

### 11.1 Learn the basics first (2 to 3 hours)

Before building the real report, make a throwaway report with one scorecard, one bar chart and one filter, so you know where things are. Google's own Looker Studio help and tutorials, or any beginner YouTube walkthrough, are enough. Learn these five things:

1. Add a data source (Google Sheets connector)
2. Chart types: scorecard, time series, bar chart, table
3. Dimensions vs metrics
4. Calculated fields
5. Filter controls (drop down, date range)

### 11.2 Connect the data

1. Go to lookerstudio.google.com, choose Create > Report, and pick the Google Sheets connector.
2. Select your spreadsheet and the `funnel` tab. Keep "Use first row as headers" ticked.
3. Add the data source. Then, in Resource > Manage added data sources > Edit, check the field types:
   - `applied`, `recruiter_viewed`, `responded`, `interviewed`, `hired`, `hours_to_first_response`: Number
   - `view_date`, `view_week`, `signup_week`: Date
   - `viewed_at` and the other timestamp fields: Date & Time
   - Everything else: Text
4. Add `funnel_summary` as a second data source (Resource > Manage added data sources > Add a data source).

### 11.3 Calculated fields

Create these in the `funnel` data source (Add a field). Set the output type to Percent where a ratio is shown.

| Field name | Formula | Type |
|---|---|---|
| Views | `COUNT(journey_id)` | Number |
| Applications | `SUM(applied)` | Number |
| View to Apply % | `SUM(applied) / COUNT(journey_id)` | Percent |
| Recruiter View Rate | `SUM(recruiter_viewed) / SUM(applied)` | Percent |
| Response Rate | `SUM(responded) / SUM(applied)` | Percent |
| Interview Rate | `SUM(interviewed) / SUM(responded)` | Percent |
| Hire Rate | `SUM(hired) / SUM(applied)` | Percent |
| Avg Hours to First Response | `AVG(hours_to_first_response)` | Number |
| Responded Within 24h % | `SUM(CASE WHEN hours_to_first_response <= 24 THEN 1 ELSE 0 END) / SUM(applied)` | Percent |

If a formula errors on blank cells, check that the column type is Number and that blank hours are truly empty in the Sheet.

### 11.4 Report layout

Use one consistent color palette (for example one primary color, one highlight color for problems, grey for everything else). Give every chart a plain English title, for example "Where do seekers drop off?" instead of "Funnel chart". Add a footer on every page: "Synthetic data for portfolio purposes".

#### Page 1: Marketplace Overview

| Position | Component | Data source and setup |
|---|---|---|
| Top row | Six scorecards: Views, Applications, View to Apply %, Response Rate, Avg Hours to First Response, Hires | `funnel`, metrics from the calculated fields, with comparison to the previous period turned on |
| Left middle | Funnel: horizontal bar chart of stage counts | `funnel_summary`, Stage as dimension, Count as metric, sorted by Order |
| Right middle | Time series: Views and Applications by week | `funnel`, dimension `view_week`, metrics Views and Applications |
| Bottom | Time series: View to Apply % and Response Rate by week | `funnel`, dimension `view_week` |
| Top or left panel | Filter controls: date range, City Tier, City, Language, Category | Apply to the whole page, or to the whole report if you want them everywhere |

#### Page 2: Segments and Marketplace Health

| Component | Setup | Question |
|---|---|---|
| Table with heatmap: one row per city with Views, Applications, View to Apply %, Response Rate, Hire Rate | Dimension `city`, sort by View to Apply % ascending, apply heatmap style to the rate columns | Q2 |
| Bar chart: View to Apply % by City Tier | Dimension `city_tier` | Q2 |
| Bar chart: Response Rate by Category | Dimension `category` | Q4 |
| Bar chart: Avg Hours to First Response by Category | Dimension `category`, sort descending | Q3, Q4 |
| Bar chart: Response Rate by Employer Verified | Dimension `employer_verified` | Q5 |
| Bar chart: View to Apply % by Acquisition Channel | Dimension `acquisition_channel` | Q6 |
| Bar chart: Response Rate and Avg Hours by Posting Day Type | Dimension `posted_day_type` | Q7 |
| Time series: Applications by week for a selected city | Dimension `view_week`, add a City drop down control; try Nagpur to see the dip | Q8 |
| Bar chart: View to Apply % by Salary Band | Dimension `salary_band` | Q2 |

#### Page 3: Insights and Recommendations

Text boxes with your findings from Section 14. Each finding uses the same layout so a reader can scan it: heading, evidence (numbers), likely cause, recommendation, how to measure the effect.

### 11.5 Data freshness

Looker Studio caches data. With Google Sheets as the source, changes show up after a short delay (commonly around 15 minutes), or immediately when a viewer refreshes the data. In view mode, use the report menu's Refresh data option. Check the current behavior in your own account, since Looker Studio settings can change. Describe the pipeline as "auto updating from Google Sheets", not "instant real time".

### 11.6 Publish

Use Share > Manage access to create a view only link. Test the link in a private browser window. Add the link to your resume and README. Also export a PDF of the three pages as a backup in case a link fails during an interview.

---

## 12. Live update test (proof that the pipeline works)

Record a 30 to 60 second screen recording and take before and after screenshots.

1. Open the dashboard in view mode and note the headline numbers (Views, Applications, View to Apply %).
2. In the Sheet, make a visible change. Choose one of these:
   - Run `addSimulatedJourneys` manually two or three times (adds about 25 rows each time)
   - Change the `city` of a batch of rows, or change some `applied` values from 0 to 1 in a chosen city
   - Change `hours_to_first_response` for a batch of Delivery & Logistics rows
3. Check the JSON endpoint: the counts should change immediately.
4. In the dashboard, click Refresh data. The scorecards and charts should now change.
5. Save the before and after screenshots, and the recording. Write the exact change you made and the exact number change in the README, for example "Set 200 Tier-3 rows to applied = 1, and View to Apply % for Tier-3 moved from 15.2% to 18.4%".

Keep a short test log in the README:

| Step | Action | Expected result | Actual result |
|---|---|---|---|
| 1 | Run `addSimulatedJourneys` twice | About 50 new rows, Views up by about 50 after refresh | fill in |
| 2 | Change a batch of `applied` values | Applications and View to Apply % change | fill in |
| 3 | Call the JSON endpoint | Numbers match the Sheet | fill in |

---

## 13. SQL validation and practice

Two goals: prove that the dashboard numbers are right (reconciliation), and practice the SQL that analyst interviews test (funnels, window functions, cohorts).

### 13.1 Load the CSVs into SQLite

Use Python for the load, so blank cells become real NULL values. A plain `.import` in the SQLite shell loads blanks as empty text, which skews averages and counts.

```python
import sqlite3
import pandas as pd

con = sqlite3.connect("marketplace.db")
for t in ["seekers", "employers", "jobs", "funnel"]:
    pd.read_csv(f"{t}.csv").to_sql(t, con, if_exists="replace", index=False)
con.close()
```

Open `marketplace.db` in DB Browser for SQLite or the `sqlite3` command line. The queries below were tested on SQLite and use standard syntax that also works in PostgreSQL.

### 13.2 Reconciliation query

```sql
SELECT COUNT(*) AS views,
       SUM(applied) AS applies,
       SUM(recruiter_viewed) AS recruiter_views,
       SUM(responded) AS responses,
       SUM(interviewed) AS interviews,
       SUM(hired) AS hires
FROM funnel;
```

The six numbers must match the `funnel_summary` tab and the dashboard scorecards exactly. Record the match in your README ("dashboard vs SQL: 0 difference on 6 headline metrics"). Do this again after the live update test, using the updated Sheet exported as CSV.

### 13.3 Analysis queries

**Q1. Funnel conversion by city (worst view to apply first)**

```sql
SELECT city, city_tier,
       COUNT(*) AS views,
       SUM(applied) AS applies,
       ROUND(100.0 * SUM(applied) / COUNT(*), 1) AS view_to_apply_pct,
       ROUND(100.0 * SUM(responded) / NULLIF(SUM(applied), 0), 1) AS response_pct,
       ROUND(100.0 * SUM(hired) / NULLIF(SUM(applied), 0), 1) AS hire_pct
FROM funnel
GROUP BY city, city_tier
ORDER BY view_to_apply_pct;
```

**Q2. Week over week change in applications for one city (CTE and LAG)**

```sql
WITH weekly AS (
  SELECT view_week, SUM(applied) AS applies
  FROM funnel
  WHERE city = 'Nagpur'
  GROUP BY view_week
)
SELECT view_week, applies,
       LAG(applies) OVER (ORDER BY view_week) AS prev_week,
       ROUND(100.0 * (applies - LAG(applies) OVER (ORDER BY view_week))
             / LAG(applies) OVER (ORDER BY view_week), 1) AS wow_change_pct
FROM weekly
ORDER BY view_week;
```

**Q3. Best responding employers in each category (ROW_NUMBER, PARTITION BY)**

```sql
WITH emp AS (
  SELECT category, employer_id,
         SUM(applied) AS applies,
         ROUND(100.0 * SUM(responded) / SUM(applied), 1) AS response_pct
  FROM funnel
  GROUP BY category, employer_id
  HAVING SUM(applied) >= 15
),
ranked AS (
  SELECT *,
         ROW_NUMBER() OVER (PARTITION BY category
                            ORDER BY response_pct DESC, applies DESC) AS rn
  FROM emp
)
SELECT category, employer_id, applies, response_pct
FROM ranked
WHERE rn <= 2
ORDER BY category, rn;
```

**Q4. Cumulative hires by week (running total)**

```sql
WITH weekly AS (
  SELECT view_week, SUM(hired) AS hires
  FROM funnel
  GROUP BY view_week
)
SELECT view_week, hires,
       SUM(hires) OVER (ORDER BY view_week) AS cumulative_hires
FROM weekly
ORDER BY view_week;
```

**Q5. Response speed by category**

```sql
SELECT category,
       COUNT(hours_to_first_response) AS responded_apps,
       ROUND(AVG(hours_to_first_response), 1) AS avg_hours,
       ROUND(100.0 * SUM(CASE WHEN hours_to_first_response <= 24 THEN 1 ELSE 0 END)
             / SUM(applied), 1) AS responded_within_24h_pct
FROM funnel
GROUP BY category
ORDER BY avg_hours DESC;
```

**Q6. Seeker cohorts by signup week**

```sql
SELECT signup_week,
       COUNT(DISTINCT seeker_id) AS active_seekers,
       SUM(applied) AS applies,
       ROUND(1.0 * SUM(applied) / COUNT(DISTINCT seeker_id), 2) AS applies_per_seeker
FROM funnel
GROUP BY signup_week
ORDER BY signup_week;
```

Also write two or three of your own on: verified vs unverified employers, acquisition channel, weekday vs weekend. Save all queries in `sql/queries.sql`.

---

## 14. Insights write-up

The insights page is what turns a dashboard into business analysis. Use the same structure for every finding.

### 14.1 Template

| Part | What to write |
|---|---|
| Finding | One sentence with the metric and the segment |
| Evidence | The numbers, the comparison group, and the sample size |
| Likely causes | Two or three hypotheses, marked as hypotheses |
| Recommendation | One specific action an owner could take |
| How to measure | The metric that should move, and what you would compare it against |

### 14.2 Findings to develop (fill in your own final numbers)

| Finding | Evidence to pull | Hypotheses | Example recommendation |
|---|---|---|---|
| Tier-3 cities convert worse from view to apply | View to apply % by tier and city (Q1 above) | Language mismatch in listings, lower trust, less relevant jobs, lower salaries shown | Prioritize regional language listing quality and local job supply in the lowest converting Tier-3 cities, then test |
| Verified employers respond far more than unverified ones | Response rate and hire rate for each group, with counts | Verified employers are more serious or more active | Nudge unverified employers to verify, and rank verified employers higher in seeker results |
| Delivery & Logistics has the slowest response times | Avg hours and % within 24 hours by category | Small fleet operators, phone based hiring, weak recruiter tools | Add a reminder or auto acknowledgement for slow categories, and set response time targets |
| Weekend postings get weaker responses | Response rate and hours, weekday vs weekend | No recruiter coverage on weekends | Schedule weekend job posts for Monday morning visibility, or add weekend recruiter reminders |
| WhatsApp share brings the highest apply rate, paid ads the lowest | View to apply % by channel | Trust from personal referral, poor targeting in ads | Shift some paid budget toward referral and share loops, and tighten ad targeting |
| Nagpur applications dropped sharply for two weeks | Weekly view to apply % and applies for Nagpur, and comparison with similar cities | Tracking issue, supply issue, campaign change, local event | First check data and tracking, then employer supply and channels, then run a short investigation |

For each recommendation, add one line on how you would test it (for example a small experiment with a control group), and mention its expected effect direction. Do not invent an exact percentage lift. Say what you would measure.

Caution on small samples: weekly numbers for a single city are small (tens of applications), so they are noisy. In the Nagpur finding, state the sample size and compare against the city's own normal range.

---

## 15. KPI dictionary

Put this in `docs/kpi_definitions.md` as well. Consistent definitions are a core BA skill.

| KPI | Definition | Formula | Why it matters |
|---|---|---|---|
| Views | Number of seeker job views | Count of funnel rows | Top of funnel demand |
| Applications | Views that became an application | Sum of `applied` | Seeker intent |
| View to Apply % | Share of views that lead to an application | Applications / Views | Listing relevance and trust |
| Recruiter View Rate | Share of applications the recruiter opened | Sum of `recruiter_viewed` / Applications | Employer attention |
| Response Rate | Share of applications that got a recruiter response | Sum of `responded` / Applications | Seeker experience, employer quality |
| Avg Hours to First Response | Average time from apply to first recruiter response | Average of `hours_to_first_response` (responded applications only) | Speed of hiring loop |
| Responded Within 24h % | Share of applications answered within a day | Count with hours <= 24 / Applications | Service level style metric |
| Interview Rate | Share of responses that reach an interview | Sum of `interviewed` / Sum of `responded` | Match quality |
| Hire Rate | Share of applications that end in a hire | Sum of `hired` / Applications | Marketplace outcome |

Definition choices to state clearly: rates are measured against applications unless stated, average response time only includes applications that received a response, and weeks start on Monday.

---

## 16. Repository structure and README

```
hiring-marketplace-analytics/
  README.md
  scripts/
    generate_data.py
  apps_script/
    Code.gs
  sql/
    queries.sql
  docs/
    requirements.md
    kpi_definitions.md
    insights.md
  data/
    (sample CSVs, or a note on how to regenerate them)
  screenshots/
    dashboard_page1.png
    dashboard_page2.png
    dashboard_page3.png
    before_update.png
    after_update.png
  demo/
    live_update_demo.mp4 (or a link)
```

README outline:

1. One paragraph summary and a live dashboard link
2. Screenshots
3. Architecture diagram (Section 4)
4. Business questions and KPIs
5. Data description and how to regenerate it, with a clear "synthetic data" statement
6. How the live update works, and the test log
7. Key findings (three to five)
8. SQL validation and reconciliation result
9. Limitations (synthetic data, Sheets scale, Looker Studio caching, simplified timestamps)
10. Next steps

---

## 17. Timeline and checklist

### 17.1 Four day plan

| Day | Focus | Output |
|---|---|---|
| Day 1 | Generate data, create the Sheet, import tabs, funnel_summary, load SQL and run the reconciliation query | Clean Sheet, SQL results that match |
| Day 2 | Learn Looker Studio basics (morning), build Pages 1 and 2 (afternoon), add calculated fields | Working dashboard, filters, KPIs |
| Day 3 | Apps Script trigger and endpoint, live update test and recording, Page 3 insights | Demo video, before and after screenshots, insights |
| Day 4 | README, docs, resume, LinkedIn post, interview practice, buffer | Repository ready, resume updated |

### 17.2 Minimum version if time is short (about 2 days)

- Data and Sheet (Day 1)
- One page dashboard with six scorecards, funnel, weekly trend, city table and category charts, plus filters
- A manual live update test (edit rows in the Sheet, refresh, screenshot)
- Three findings written up
- Skip the trigger and the endpoint, and add them later

---

## 18. Resume, LinkedIn and outreach

### 18.1 Resume entry

Heading (no dashes):

**Hiring Marketplace Analytics Dashboard | Looker Studio, Google Sheets, Apps Script, SQL, Python**

Bullets (use only what you actually built, and replace the bracketed numbers with your own final numbers):

- Built an auto-updating hiring marketplace dashboard in Looker Studio on a Google Sheets pipeline, with an Apps Script trigger adding records every 15 minutes and a JSON KPI endpoint, tracking the view, apply, response and hire funnel across 21 Tier-2 and Tier-3 cities (synthetic data).
- Generated a 29K record dataset in Python and validated every dashboard KPI against SQL (CTEs, window functions), with headline counts reconciled exactly.
- Diagnosed marketplace issues and wrote recommendations: Tier-3 view to apply gap ([15%] vs [22%]), verified vs unverified employer response gap ([57%] vs [22%]) and slow Delivery & Logistics response ([70] vs [33] average hours).

Short version if space is tight:

- Built a Looker Studio dashboard on an auto-updating Google Sheets and Apps Script pipeline (29K synthetic marketplace records, 21 cities), validated with SQL, with findings and recommendations on conversion, employer response time and channel quality.

Skills line additions (only after building it): Looker Studio, Google Apps Script, SQL (CTEs, window functions), Python.

Space tip: to fit this on a one page resume, shorten the Nivasa project to two lines and tighten the Insurance Claims bullets. Keep the ElectricPe funnel case study and this project as the two headline items.

Note: label the project as synthetic on the resume. Do not describe it as work for Lokal.

### 18.2 LinkedIn post draft

I built a live hiring marketplace analytics dashboard to practice the kind of questions a marketplace business analyst deals with.

Google Sheets holds the data, Apps Script adds new records and serves a KPI endpoint, and Looker Studio shows the funnel from job view to hire across 21 Tier-2 and Tier-3 cities. I validated every number with SQL.

The data is synthetic, but the questions are real: where do seekers drop off, which employers respond slowly, and which channels bring people who actually apply?

Dashboard link and code in the comments. Feedback from anyone working on marketplace analytics is very welcome.

### 18.3 Outreach email (your structure: problem, project, how it helps)

Use this after the dashboard is live. Replace the bracketed parts, and check that the problem statement is something you can defend. It is an assumption about a marketplace like Lokal, not inside knowledge.

Subject: Tracking employer response time in Tier-2 and Tier-3 hiring

Hi [Name],

For a hyperlocal job marketplace, one hard problem is that seekers lose interest when employers take too long to respond, and the delay is often concentrated in a few categories and cities.

I built a Looker Studio dashboard, on a Google Sheets and Apps Script pipeline with SQL validation, that tracks the funnel from job view to hire and breaks response speed down by city, category and employer verification. It uses synthetic data modelled on a vernacular job marketplace.

The same approach could help your team spot slow categories, compare verified and unverified employers, and see which cities need attention, without waiting for a manual report. I have applied for the Business Analyst role and would be glad to walk you through it.

Dashboard: [link]
Code: [GitHub link]

Thanks,
Kalash Jain

---

## 19. Interview preparation

| Question | How to answer |
|---|---|
| Walk me through the project. | Business problem, data, pipeline, dashboard pages, top three findings, and what you would do next. About two minutes. |
| Why synthetic data? Can I trust the findings? | Say plainly that it is synthetic and the patterns were designed in. The value is the method: metric design, segmentation, anomaly detection, validation and recommendations. The same workflow works on real data. |
| How did you define response rate, and why that denominator? | Responses divided by applications, because it reflects what a seeker experiences. Mention the alternative (divide by recruiter views) and when it would be better. |
| Why Looker Studio? What are its limits? | It is free and connects natively to Sheets. Limits: caching delay, no native funnel chart, limited joins and blending, slower with very large Sheets. In production you would use a warehouse such as BigQuery. |
| How does the live update work? | Apps Script trigger appends rows, Sheets stores them, Looker Studio reads the Sheet and refreshes on cache expiry or manual refresh. |
| Tier-3 view to apply is lower. What would you do? | Check data quality first, then segment by language, category, salary and channel. Form hypotheses (language, trust, relevance), then propose a test with a control group and track view to apply %. |
| Applications dropped suddenly in one city. How do you investigate? | Check tracking and data pipeline first. Then decompose by channel, category, employer supply, device and time. Compare with similar cities and with the city's normal range. Then act. |
| How do you prioritize requirements from stakeholders? | Collect and document them, then rank by business impact and effort (MoSCoW or impact vs effort), confirm with stakeholders, and agree on definitions before building. |
| What would you do differently with real data? | Data quality checks, duplicates, bot traffic, time zones, clear metric definitions with owners, a warehouse instead of Sheets, and access controls. |
| What is a window function? Give an example from your project. | A calculation across related rows without collapsing them. Example: LAG for week over week change, ROW_NUMBER to rank employers within a category. |

Practice tips: be ready to write Q1, Q2 and Q3 from Section 13 from memory on a whiteboard, and be able to explain every planted pattern and how you found it.

---

## 20. Stretch goals (only after the core is done)

1. **Natural language analytics layer (the second project idea).** User asks a question, an LLM turns it into a constrained query specification (allowed fields, filters, aggregations), the code runs it on the funnel table, and a chart is drawn. Guardrails: never execute raw model generated SQL without validation, and if the request needs data that is not in the table, ask the user instead of inventing it. This is a good project for Forward Deployed Engineer applications, and it can reuse this dataset.
2. **Anomaly detection.** Flag weeks where a city's view to apply rate falls more than two standard deviations below its own history, and show the flags on the dashboard.
3. **A/B test analysis.** Add an experiment flag to the data, and analyze the impact of a simulated change, such as an auto reminder for slow recruiters.
4. **Forecasting.** Simple weekly trend and moving average forecast for applications and hires.
5. **Move to a warehouse.** Load the data into BigQuery or PostgreSQL and point Looker Studio at it, to talk about scale.

---

## 21. Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| Timestamps show as text in Sheets | Import did not convert values | Re-import with conversion ticked, or format columns P to U as Date time |
| Apps Script adds no rows | Timestamps are not real dates, so rows are skipped | Fix the column formats, then run again |
| Apps Script says the sheet is null | Tab is not named `funnel` | Rename the tab exactly or change `SHEET_NAME` |
| Calculated field returns an error | Field type is Text | Change the field type to Number in the data source |
| Percent shows as a decimal | Output type not set | Set the field type to Percent |
| Dashboard does not change after editing the Sheet | Data cache | Use Refresh data in view mode, wait for cache expiry |
| Looker Studio is slow | Very large Sheet | Keep the funnel tab under about 50,000 rows for this project |
| Charts break after renaming a header | Looker Studio maps fields by name | Rename it back, or reconnect and remap fields |
| SQL numbers differ from the dashboard | Date filter or a blank handling difference | Clear all filters, compare totals first, then segments |
| Web app returns an authorization error | Access is set to "Only myself" and the call is unauthenticated | Open the URL in your signed in browser, or redeploy with wider access for synthetic data |

---

## 22. Final checklist

- [ ] Data generated, and the numbers look like Section 7
- [ ] Sheet has `funnel`, `seekers`, `employers`, `jobs`, `funnel_summary`
- [ ] SQL reconciliation matches the dashboard exactly
- [ ] Looker Studio report has three pages, filters, calculated fields, and a "synthetic data" footer
- [ ] Apps Script trigger and JSON endpoint tested
- [ ] Live update test recorded, with before and after screenshots and a test log
- [ ] Three to five findings written with evidence and recommendations
- [ ] KPI dictionary and requirements documents added
- [ ] GitHub repo with README
- [ ] Dashboard link tested in a private browser window, and a PDF backup exported
- [ ] Resume updated (project entry, skills, no dashes)
- [ ] LinkedIn post drafted
- [ ] Outreach email tailored and sent
- [ ] Interview answers practiced, including SQL Q1 to Q3 from memory
