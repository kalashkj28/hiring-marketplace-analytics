# Business Requirements

## Context

A vernacular, hyperlocal job marketplace connects job seekers and employers in Tier-2 and Tier-3 cities across frontline roles (Sales, Customer Support, Delivery, Operations, Telecalling, Retail, Back Office). Growth depends on seekers finding relevant jobs in their language, applying, and employers responding quickly enough to keep seekers engaged.

## Business Questions

| # | Question | Metric | Dashboard location |
|---|---|---|---|
| Q1 | How healthy is the overall hiring funnel? | Views, applies, recruiter views, responses, interviews, hires, stage conversion | Page 1 funnel + scorecards |
| Q2 | Which cities and tiers convert worst from view to apply? | View to Apply % by city and tier | Page 2 city table |
| Q3 | Are employers responding fast enough? | Response rate, avg hours to first response, % within 24h | Page 1 scorecards, Page 2 category charts |
| Q4 | Which job categories have slow or weak hiring outcomes? | Response rate, hours to response, hire rate by category | Page 2 |
| Q5 | Do verified employers perform better? | Response rate and hire rate, verified vs unverified | Page 2 |
| Q6 | Which acquisition channels bring seekers who actually apply? | View to Apply % by channel | Page 2 |
| Q7 | Does the posting day matter? | Response rate and response time, weekday vs weekend | Page 2 |
| Q8 | Is anything changing suddenly? | Weekly applies and View to Apply %, by city | Page 1 trend, Page 2 city trend |

## Stakeholders

| Stakeholder | What they care about |
|---|---|
| Product | Funnel drop-off, language and city experience |
| Growth & Marketing | Channel quality, seeker activation |
| Recruiter Success / Operations | Employer response time, verified employer quality, category-level delays |
| Leadership | Hires, conversion, trends |

## Requirements (MoSCoW)

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
| R11 | Natural language query layer | Could |
