# Insights and Recommendations

> **Note:** All data is synthetic. The patterns were designed into the dataset. The value is the method: metric design, segmentation, anomaly detection, validation, and recommendation. The same workflow applies to real data.

---

## Finding 1 — Tier-3 cities convert worse from view to apply

**Finding:** View to Apply % in Tier-3 cities (~X%) is significantly lower than Tier-2 cities (~X%), a gap of roughly X percentage points.

**Evidence:**
- Tier-2 cities: ~22% view to apply (from SQL Q1 / dashboard Page 2)
- Tier-3 cities: ~15% view to apply
- Sample: [fill in] views across [fill in] cities

**Likely causes (hypotheses):**
1. Language mismatch — job listings may not be available in the seeker's preferred language in smaller cities
2. Lower trust — fewer verified employers in Tier-3, reducing seeker confidence
3. Less relevant jobs — lower salary bands and fewer category options in smaller cities

**Recommendation:** Prioritize regional language listing quality and local job supply in the lowest-converting Tier-3 cities. Test language-matched listing display vs. Hindi-default in a controlled pilot.

**How to measure:** Track View to Apply % for Tier-3 cities in the pilot vs. a control group of similar Tier-3 cities. Expect uplift in apply rate within 4 weeks.

---

## Finding 2 — Verified employers respond far more than unverified ones

**Finding:** Verified employers have a response rate of ~57% vs. ~22% for unverified employers — a 2.5x difference.

**Evidence:**
- Verified: ~57% response rate, ~X% hire rate (from SQL Bonus Q7 / dashboard Page 2)
- Unverified: ~22% response rate, ~X% hire rate
- Sample: [fill in] applications to verified, [fill in] to unverified employers

**Likely causes (hypotheses):**
1. Verified employers are more serious about hiring — verification signals commitment
2. Verified employers are larger companies with dedicated recruiters
3. Unverified employers may be posting jobs without active intent to hire

**Recommendation:** Nudge unverified employers to complete verification (in-app prompt after posting). Rank verified employers higher in seeker search results to improve seeker experience.

**How to measure:** Compare response rate and hire rate for newly verified employers (pre/post verification). Track verification completion rate as a leading indicator.

---

## Finding 3 — Delivery & Logistics has the slowest response times

**Finding:** Delivery & Logistics takes an average of ~70 hours to first response vs. ~33 hours for Sales — more than 2x slower. Only ~X% of Delivery & Logistics applications get a response within 24 hours.

**Evidence:**
- Delivery & Logistics: avg ~70 hrs, ~X% within 24h
- Sales: avg ~33 hrs, ~X% within 24h
- Sample: [fill in] responded applications in D&L

**Likely causes (hypotheses):**
1. Small fleet operators tend to hire via phone — they may not check the app frequently
2. Recruiter tooling is weaker for logistics employers
3. High volume of applicants causes delayed triage

**Recommendation:** Add an auto-acknowledgement message for Delivery & Logistics applications (within 1 hour of apply) and a nudge to the recruiter at 24h if no response. Set category-level response time targets.

**How to measure:** Track avg hours to first response and % within 24h for D&L month-over-month. Seeker dropout rate (applied but never heard back) as a secondary metric.

---

## Finding 4 — Weekend postings get weaker recruiter response

**Finding:** Jobs posted on weekends have a ~9 percentage point lower response rate than weekday postings (~37% vs. ~46%).

**Evidence:**
- Weekday postings: ~46% response rate, avg ~X hrs
- Weekend postings: ~37% response rate, avg ~X hrs
- Sample: [fill in] weekend applications vs [fill in] weekday

**Likely causes (hypotheses):**
1. Recruiters are not active on weekends — no coverage policy
2. Weekend applications sit unread until Monday, reducing seeker confidence
3. Smaller employers (who post on weekends) have less structured recruiting

**Recommendation:** Schedule weekend job posts to go live on Monday morning instead, or add a weekend recruiter reminder notification. Test with a subset of employers.

**How to measure:** Response rate and avg hours for jobs posted on Monday (from a weekend draft) vs. jobs posted live on weekends. Compare over 4-week windows.

---

## Finding 5 — WhatsApp Share brings the highest apply rate; Paid Ads the lowest

**Finding:** Seekers who joined via WhatsApp Share apply at ~1.3x the base rate, while Paid Ads seekers apply at ~0.8x — a gap of ~X percentage points in View to Apply %.

**Evidence:**
- WhatsApp Share: ~X% view to apply
- Paid Ads: ~X% view to apply
- Organic Search: ~X%, Referral: ~X%
- Sample: [fill in] views per channel

**Likely causes (hypotheses):**
1. WhatsApp share is a trust-based referral — the sender endorses the platform
2. Paid Ads attract lower-intent seekers who are browsing rather than actively job hunting
3. Ad targeting may not be precise enough for hyperlocal frontline jobs

**Recommendation:** Shift some paid budget toward referral and share loops (in-app "share with a friend" feature). Tighten Paid Ads targeting to city, language, and category before scaling.

**How to measure:** View to Apply % and Cost Per Application by channel. Track share loop conversion and referral volume as leading indicators.

---

## Finding 6 — Nagpur applications dropped sharply for two weeks

**Finding:** Nagpur's weekly View to Apply % fell to ~6–9% during weeks of 11–25 July 2026, compared to its normal range of ~17–30%. Applications in those weeks dropped by approximately X.

**Evidence:**
- Normal Nagpur weeks: ~17–30% view to apply, ~X applications/week
- Dip weeks (day 40–54): ~6–9% view to apply
- Sample: [fill in] views in Nagpur during dip vs. [fill in] baseline
- Similar cities (Nashik, Pune) showed no corresponding dip in the same period

**Likely causes (hypotheses — investigate in this order):**
1. **Data / tracking issue** — check if a source change or tagging error affected Nagpur-specific views
2. **Campaign pause** — a Nagpur-specific paid or WhatsApp campaign may have been paused
3. **Local supply shock** — employer posting volume may have dropped for a local reason (holiday, event)
4. **Seeker-side issue** — device or login issues for Nagpur users

**Recommendation:** Before acting, confirm the data pipeline and tracking are clean. Then decompose by channel, category, and employer supply in those two weeks. Run a short investigation (1–2 days) before deciding whether to re-activate a campaign.

**How to measure:** Track weekly View to Apply % for Nagpur for the next 4 weeks. If normal, the issue was temporary. If it persists, escalate the investigation to demand side (employer supply) and supply side (seeker acquisition).

> **Caution on small samples:** Weekly numbers for a single city can be in the tens of applications. State the sample size and compare against the city's own historical range, not a national average.
