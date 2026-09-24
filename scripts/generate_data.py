"""
Synthetic data generator for a hyperlocal job marketplace analytics project.
Creates four CSVs: seekers, employers, jobs, funnel (flat table used by the dashboard).
All data is simulated. Run: python scripts/generate_data.py
Output CSVs are written to the data/ folder.
"""
import numpy as np
import pandas as pd
import os

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
    "company_size": rng.choice(["1 to 10", "11 to 50", "51 to 200", "200+"], N_EMPLOYERS, p=[0.35, 0.35, 0.2, 0.1]),
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
    hrs = float("nan")
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

# Write to data/ folder
os.makedirs("data", exist_ok=True)
seekers.to_csv("data/seekers.csv", index=False)
employers.to_csv("data/employers.csv", index=False)
jobs.to_csv("data/jobs.csv", index=False)
funnel.to_csv("data/funnel.csv", index=False)

print("Data generated successfully!")
print(f"   seekers  : {len(seekers):,} rows")
print(f"   employers: {len(employers):,} rows")
print(f"   jobs     : {len(jobs):,} rows")
print(f"   funnel   : {len(funnel):,} rows")
print("\nQuick validation:")
print(f"   Total views          : {len(funnel):,}")
print(f"   Total applications   : {funnel['applied'].sum():,}")
print(f"   View to Apply %      : {100 * funnel['applied'].sum() / len(funnel):.1f}%")
print(f"   Total responses      : {funnel['responded'].sum():,}")
print(f"   Total hires          : {funnel['hired'].sum():,}")
tier_stats = funnel.groupby("city_tier")["applied"].agg(["sum", "count"])
tier_stats["pct"] = (100 * tier_stats["sum"] / tier_stats["count"]).round(1)
print("\n   View to Apply % by Tier:")
for tier, row in tier_stats.iterrows():
    print(f"     {tier}: {row['pct']}%")
print("\nCSVs written to data/ folder.")
