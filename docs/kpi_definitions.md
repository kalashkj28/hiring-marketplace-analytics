# KPI Dictionary

> Consistent definitions are a core BA skill. Every metric in the dashboard uses exactly the definition below.

| KPI | Definition | Formula | Why it matters |
|---|---|---|---|
| **Views** | Number of seeker job views (one row in the funnel table = one view) | `COUNT(journey_id)` | Top-of-funnel demand signal |
| **Applications** | Views that became an application | `SUM(applied)` | Seeker intent and listing relevance |
| **View to Apply %** | Share of views that lead to an application | `Applications / Views` | Core relevance and trust metric |
| **Recruiter View Rate** | Share of applications the recruiter opened | `SUM(recruiter_viewed) / Applications` | Employer attention signal |
| **Response Rate** | Share of applications that got a recruiter response | `SUM(responded) / Applications` | Seeker experience and employer quality |
| **Avg Hours to First Response** | Average time from application to first recruiter response | `AVG(hours_to_first_response)` — **responded applications only** | Speed of the hiring loop |
| **Responded Within 24h %** | Share of applications answered within one day | `COUNT(hours_to_first_response <= 24) / Applications` | Service-level metric |
| **Interview Rate** | Share of responses that reach an interview | `SUM(interviewed) / SUM(responded)` | Match quality signal |
| **Hire Rate** | Share of applications that end in a hire | `SUM(hired) / Applications` | Primary marketplace outcome |

## Definition choices (state these clearly in interviews)

- All rates use **Applications as the denominator** unless explicitly stated otherwise.
- **Avg Hours to First Response** only includes applications that received a response — blank `hours_to_first_response` rows are excluded from the average.
- All weeks start on **Monday** (`view_week`, `signup_week`).
- **Hired** means an offer was made — not necessarily the seeker's first day.
- Data covers 90 days: 1 June 2026 to 29 August 2026 (synthetic).
