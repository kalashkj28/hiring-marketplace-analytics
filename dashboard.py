"""
Hiring Marketplace Analytics Dashboard
Built with Streamlit + Plotly
Run: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Hiring Marketplace Analytics",
    page_icon="📊",
    layout="wide",
)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data(ttl=60) # Cache for 60 seconds to allow live updates
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/133YLXhIn7FRXdStSckbObZWCYcNTZZq87FZevoWSgKY/export?format=csv"
    df = pd.read_csv(sheet_url, parse_dates=["view_date", "view_week"])
    return df

df_raw = load_data()

# ── Sidebar filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Filters")

    min_date = df_raw["view_date"].min().date()
    max_date = df_raw["view_date"].max().date()
    date_range = st.date_input("Date Range", value=(min_date, max_date),
                               min_value=min_date, max_value=max_date)

    sel_tier = st.selectbox("City Tier", ["All"] + sorted(df_raw["city_tier"].unique().tolist()))
    sel_city = st.selectbox("City",      ["All"] + sorted(df_raw["city"].unique().tolist()))
    sel_lang = st.selectbox("Language",  ["All"] + sorted(df_raw["language"].unique().tolist()))
    sel_cat  = st.selectbox("Category",  ["All"] + sorted(df_raw["category"].unique().tolist()))
    sel_chan = st.selectbox("Channel",   ["All"] + sorted(df_raw["acquisition_channel"].unique().tolist()))

    st.caption("Data: Jun – Aug 2026 (synthetic)")

# ── Apply filters ─────────────────────────────────────────────────────────────
df = df_raw.copy()
if len(date_range) == 2:
    df = df[(df["view_date"].dt.date >= date_range[0]) &
            (df["view_date"].dt.date <= date_range[1])]
if sel_tier != "All": df = df[df["city_tier"] == sel_tier]
if sel_city != "All": df = df[df["city"]      == sel_city]
if sel_lang != "All": df = df[df["language"]  == sel_lang]
if sel_cat  != "All": df = df[df["category"]  == sel_cat]
if sel_chan != "All": df = df[df["acquisition_channel"] == sel_chan]

# ── KPIs ──────────────────────────────────────────────────────────────────────
views      = len(df)
applies    = int(df["applied"].sum())
rv         = int(df["recruiter_viewed"].sum())
responded  = int(df["responded"].sum())
interviews = int(df["interviewed"].sum())
hires      = int(df["hired"].sum())
vta_pct    = round(100 * applies / views, 1) if views else 0
resp_rate  = round(100 * responded / applies, 1) if applies else 0
hire_rate  = round(100 * hires / applies, 1) if applies else 0
avg_hrs    = round(df["hours_to_first_response"].mean(), 1)
within24   = round(100 * (df["hours_to_first_response"] <= 24).sum() / applies, 1) if applies else 0

# ── Header ────────────────────────────────────────────────────────────────────
st.title("Hiring Marketplace Analytics Dashboard")
st.caption(
    "Tracking the job-seeker journey from view to hire across 21 Tier-2 & Tier-3 cities | "
    "Jun – Aug 2026 | _Synthetic data for portfolio purposes_"
)
st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(["Overview", "Segments", "Insights"])

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE 1 - OVERVIEW
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab1:
    st.subheader("Funnel at a Glance")

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Views",             f"{views:,}")
    c2.metric("Applications",      f"{applies:,}")
    c3.metric("View to Apply %",   f"{vta_pct}%")
    c4.metric("Response Rate",     f"{resp_rate}%")
    c5.metric("Avg Hrs to Respond",f"{avg_hrs}h")
    c6.metric("Hires",             f"{hires:,}")

    st.divider()

    col_left, col_right = st.columns([1, 1.5])

    with col_left:
        st.subheader("Where do seekers drop off?")
        stages = ["Viewed", "Applied", "Recruiter Viewed", "Responded", "Interviewed", "Hired"]
        counts = [views, applies, rv, responded, interviews, hires]
        pcts   = [100,
                  round(100*applies/views, 1) if views else 0,
                  round(100*rv/views, 1) if views else 0,
                  round(100*responded/views, 1) if views else 0,
                  round(100*interviews/views, 1) if views else 0,
                  round(100*hires/views, 1) if views else 0]

        funnel_df = pd.DataFrame({"Stage": stages, "Count": counts, "Pct": pcts})

        fig = go.Figure()
        colors = ["#264653","#2a9d8f","#52b788","#e9c46a","#f4a261","#e76f51"]
        for i, row in funnel_df.iterrows():
            is_large = row["Count"] > 8000
            fig.add_trace(go.Bar(
                x=[row["Count"]], y=[row["Stage"]], orientation="h",
                marker_color=colors[i],
                text=f'{int(row["Count"]):,}  ({row["Pct"]}%)',
                textposition="inside" if is_large else "outside", cliponaxis=False,
                textfont=dict(size=11, color="white" if is_large else "#333"),
                showlegend=False
            ))
        fig.update_layout(
            margin=dict(l=130, r=30, t=40, b=30),
            xaxis=dict(title="Count", showgrid=True, gridcolor="#eee"),
            yaxis=dict(showgrid=False, categoryorder="array",
                       categoryarray=list(reversed(stages))),
            height=300,
            plot_bgcolor="white", paper_bgcolor="white"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("Weekly trend - views and applications")
        weekly = df.groupby("view_week").agg(
            Views=("applied", "count"),
            Applications=("applied", "sum")
        ).reset_index()

        fig2 = px.line(weekly, x="view_week", y=["Views", "Applications"],
                       markers=True,
                       color_discrete_map={"Views": "#264653", "Applications": "#2a9d8f"})
        fig2.update_layout(
            xaxis_title="Week", yaxis_title="Count",
            legend_title="",
            margin=dict(l=10, r=30, t=40, b=10),
            plot_bgcolor="white", paper_bgcolor="white",
            height=300
        )
        fig2.update_xaxes(showgrid=True, gridcolor="#eee")
        fig2.update_yaxes(showgrid=True, gridcolor="#eee")
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Are conversion rates stable week on week?")
    weekly2 = df.groupby("view_week").agg(
        views=("applied","count"), applies=("applied","sum"),
        responded=("responded","sum")
    ).reset_index()
    weekly2["View to Apply %"] = (100 * weekly2["applies"] / weekly2["views"].replace(0,1)).round(1)
    weekly2["Response Rate %"] = (100 * weekly2["responded"] / weekly2["applies"].replace(0,1)).round(1)

    fig3 = px.line(weekly2, x="view_week",
                   y=["View to Apply %", "Response Rate %"],
                   markers=True,
                   color_discrete_map={"View to Apply %":"#264653","Response Rate %":"#e76f51"})
    fig3.update_layout(
        xaxis_title="Week", yaxis_title="%",
        legend_title="",
        margin=dict(l=10, r=30, t=40, b=10),
        plot_bgcolor="white", paper_bgcolor="white",
        height=280
    )
    fig3.update_xaxes(showgrid=True, gridcolor="#eee")
    fig3.update_yaxes(showgrid=True, gridcolor="#eee")
    st.plotly_chart(fig3, use_container_width=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE 2 - SEGMENTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab2:

    # City table
    st.subheader("City-level breakdown (sorted by worst view-to-apply)")
    city_df = df.groupby(["city","city_tier"]).agg(
        Views=("applied","count"), Applications=("applied","sum"),
        Responses=("responded","sum"), Hires=("hired","sum")
    ).reset_index()
    city_df["View to Apply %"] = (100*city_df["Applications"]/city_df["Views"]).round(1)
    city_df["Response Rate %"] = (100*city_df["Responses"]/city_df["Applications"].replace(0,1)).round(1)
    city_df["Hire Rate %"]     = (100*city_df["Hires"]/city_df["Applications"].replace(0,1)).round(1)
    city_df = city_df.sort_values("View to Apply %").reset_index(drop=True)
    city_df.index += 1

    st.dataframe(
        city_df[["city","city_tier","Views","Applications",
                 "View to Apply %","Response Rate %","Hire Rate %"]],
        use_container_width=True,
        column_config={
            "city":           st.column_config.TextColumn("City"),
            "city_tier":      st.column_config.TextColumn("Tier"),
            "Views":          st.column_config.NumberColumn("Views", format="%d"),
            "Applications":   st.column_config.NumberColumn("Applications", format="%d"),
            "View to Apply %":st.column_config.ProgressColumn("View to Apply %", min_value=0, max_value=35, format="%.1f%%"),
            "Response Rate %" :st.column_config.ProgressColumn("Response Rate %", min_value=0, max_value=70, format="%.1f%%"),
            "Hire Rate %":    st.column_config.NumberColumn("Hire Rate %", format="%.1f%%"),
        },
        height=420
    )

    st.divider()
    r2c1, r2c2, r2c3 = st.columns(3)

    with r2c1:
        st.subheader("Tier-2 vs Tier-3 apply rate")
        tier_df = df.groupby("city_tier").agg(v=("applied","count"), a=("applied","sum")).reset_index()
        tier_df["View to Apply %"] = (100*tier_df["a"]/tier_df["v"]).round(1)
        fig = px.bar(tier_df, x="city_tier", y="View to Apply %",
                     text="View to Apply %", color="city_tier",
                     color_discrete_map={"Tier-2":"#2a9d8f","Tier-3":"#e76f51"})
        fig.update_traces(texttemplate="%{text}%", textposition="outside", cliponaxis=False)
        fig.update_layout(showlegend=False, plot_bgcolor="white", paper_bgcolor="white",
                          yaxis=dict(ticksuffix="%", showgrid=True, gridcolor="#eee"),
                          xaxis_title="", margin=dict(t=40,b=10,l=10,r=30))
        st.plotly_chart(fig, use_container_width=True)

    with r2c2:
        st.subheader("Response rate by category")
        cat_df = df.groupby("category").agg(a=("applied","sum"),r=("responded","sum")).reset_index()
        cat_df["Response Rate %"] = (100*cat_df["r"]/cat_df["a"].replace(0,1)).round(1)
        cat_df = cat_df.sort_values("Response Rate %")
        fig = px.bar(cat_df, x="Response Rate %", y="category", orientation="h",
                     text="Response Rate %",
                     color="Response Rate %",
                     color_continuous_scale=["#e76f51","#f4a261","#2a9d8f"])
        fig.update_traces(texttemplate="%{text}%", textposition="outside", cliponaxis=False)
        fig.update_layout(showlegend=False, coloraxis_showscale=False,
                          plot_bgcolor="white", paper_bgcolor="white",
                          xaxis=dict(ticksuffix="%", showgrid=True, gridcolor="#eee"),
                          yaxis_title="", margin=dict(t=40,b=10,l=10,r=30))
        st.plotly_chart(fig, use_container_width=True)

    with r2c3:
        st.subheader("Avg hours to respond by category")
        hrs_df = df.groupby("category")["hours_to_first_response"].mean().round(1).reset_index()
        hrs_df.columns = ["category","Avg Hours"]
        hrs_df = hrs_df.sort_values("Avg Hours", ascending=False)
        fig = px.bar(hrs_df, x="Avg Hours", y="category", orientation="h",
                     text="Avg Hours",
                     color="Avg Hours",
                     color_continuous_scale=["#2a9d8f","#f4a261","#e76f51"])
        fig.update_traces(texttemplate="%{text}h", textposition="outside", cliponaxis=False)
        fig.update_layout(showlegend=False, coloraxis_showscale=False,
                          plot_bgcolor="white", paper_bgcolor="white",
                          xaxis=dict(title="Hours", showgrid=True, gridcolor="#eee"),
                          yaxis_title="", margin=dict(t=40,b=10,l=10,r=30))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    r3c1, r3c2, r3c3 = st.columns(3)

    with r3c1:
        st.subheader("Verified vs unverified employers")
        ver_df = df.groupby("employer_verified").agg(
            a=("applied","sum"), r=("responded","sum"), h=("hired","sum")
        ).reset_index()
        ver_df["Response Rate %"] = (100*ver_df["r"]/ver_df["a"].replace(0,1)).round(1)
        ver_df["Hire Rate %"]     = (100*ver_df["h"]/ver_df["a"].replace(0,1)).round(1)
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Response Rate %", x=ver_df["employer_verified"],
                             y=ver_df["Response Rate %"], marker_color="#2a9d8f",
                             text=ver_df["Response Rate %"], texttemplate="%{text}%",
                             textposition="outside", cliponaxis=False))
        fig.add_trace(go.Bar(name="Hire Rate %", x=ver_df["employer_verified"],
                             y=ver_df["Hire Rate %"], marker_color="#264653",
                             text=ver_df["Hire Rate %"], texttemplate="%{text}%",
                             textposition="outside", cliponaxis=False))
        fig.update_layout(barmode="group",
                          legend=dict(orientation="h", y=-0.2, x=0.1),
                          plot_bgcolor="white", paper_bgcolor="white",
                          yaxis=dict(ticksuffix="%", showgrid=True, gridcolor="#eee"),
                          xaxis_title="Employer Verified",
                          margin=dict(t=40,b=60,l=10,r=30))
        st.plotly_chart(fig, use_container_width=True)

    with r3c2:
        st.subheader("Which channel brings seekers who apply?")
        chan_df = df.groupby("acquisition_channel").agg(v=("applied","count"),a=("applied","sum")).reset_index()
        chan_df["View to Apply %"] = (100*chan_df["a"]/chan_df["v"]).round(1)
        chan_df = chan_df.sort_values("View to Apply %", ascending=True)
        fig = px.bar(chan_df, x="View to Apply %", y="acquisition_channel",
                     orientation="h", text="View to Apply %",
                     color="acquisition_channel",
                     color_discrete_sequence=["#e76f51","#264653","#f4a261","#2a9d8f"])
        fig.update_traces(texttemplate="%{text}%", textposition="outside", cliponaxis=False)
        fig.update_layout(showlegend=False,
                          plot_bgcolor="white", paper_bgcolor="white",
                          xaxis=dict(ticksuffix="%", showgrid=True, gridcolor="#eee"),
                          yaxis_title="", margin=dict(t=40,b=10,l=10,r=30))
        st.plotly_chart(fig, use_container_width=True)

    with r3c3:
        st.subheader("Does posting day affect response?")
        day_df = df.groupby("posted_day_type").agg(
            a=("applied","sum"), r=("responded","sum"),
            h=("hours_to_first_response","mean")
        ).reset_index()
        day_df["Response Rate %"] = (100*day_df["r"]/day_df["a"].replace(0,1)).round(1)
        day_df["Avg Hours"]       = day_df["h"].round(1)
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Response Rate %", x=day_df["posted_day_type"],
                             y=day_df["Response Rate %"], marker_color="#2a9d8f",
                             text=day_df["Response Rate %"], texttemplate="%{text}%",
                             textposition="outside", cliponaxis=False))
        fig.add_trace(go.Bar(name="Avg Hours to Respond", x=day_df["posted_day_type"],
                             y=day_df["Avg Hours"], marker_color="#e76f51",
                             text=day_df["Avg Hours"], texttemplate="%{text}h",
                             textposition="outside", cliponaxis=False))
        fig.update_layout(barmode="group",
                          legend=dict(orientation="h", y=-0.2, x=0),
                          plot_bgcolor="white", paper_bgcolor="white",
                          yaxis=dict(showgrid=True, gridcolor="#eee"),
                          xaxis_title="", margin=dict(t=40,b=60,l=10,r=30))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    r4c1, r4c2 = st.columns([1.8, 1])

    with r4c1:
        st.subheader("Nagpur applications by week - notice the July dip")
        nagpur = df_raw[df_raw["city"] == "Nagpur"].groupby("view_week").agg(
            views=("applied","count"), applies=("applied","sum")
        ).reset_index()
        nagpur["View to Apply %"] = (100*nagpur["applies"]/nagpur["views"]).round(1)

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=nagpur["view_week"], y=nagpur["applies"],
                             name="Applications", marker_color="#2a9d8f",
                             text=nagpur["applies"], textposition="outside", cliponaxis=False),
                      secondary_y=False)
        fig.add_trace(go.Scatter(x=nagpur["view_week"], y=nagpur["View to Apply %"],
                                 mode="lines+markers", name="View to Apply %",
                                 line=dict(color="#e76f51", width=2, dash="dot"),
                                 marker=dict(size=6)),
                      secondary_y=True)
        fig.add_vrect(x0="2026-07-10", x1="2026-07-27",
                      fillcolor="#e76f51", opacity=0.07,
                      annotation_text="Dip", annotation_position="top left",
                      line_width=0)
        fig.update_layout(legend=dict(orientation="h", y=-0.2),
                          plot_bgcolor="white", paper_bgcolor="white",
                          margin=dict(t=40,b=60,l=10,r=30), height=320)
        fig.update_yaxes(title_text="Applications", secondary_y=False,
                         showgrid=True, gridcolor="#eee")
        fig.update_yaxes(title_text="View to Apply %", secondary_y=True,
                         ticksuffix="%", showgrid=False)
        st.plotly_chart(fig, use_container_width=True)

    with r4c2:
        st.subheader("Salary band vs apply rate")
        sal_order = ["<12k","12-18k","18-25k","25k+"]
        sal_df = df.groupby("salary_band").agg(v=("applied","count"),a=("applied","sum")).reset_index()
        sal_df["View to Apply %"] = (100*sal_df["a"]/sal_df["v"]).round(1)
        sal_df["salary_band"] = pd.Categorical(sal_df["salary_band"], categories=sal_order, ordered=True)
        sal_df = sal_df.sort_values("salary_band")
        fig = px.bar(sal_df, x="salary_band", y="View to Apply %",
                     text="View to Apply %",
                     color="View to Apply %",
                     color_continuous_scale=["#e76f51","#f4a261","#2a9d8f"])
        fig.update_traces(texttemplate="%{text}%", textposition="outside", cliponaxis=False)
        fig.update_layout(showlegend=False, coloraxis_showscale=False,
                          plot_bgcolor="white", paper_bgcolor="white",
                          xaxis_title="Salary Band",
                          yaxis=dict(ticksuffix="%", showgrid=True, gridcolor="#eee"),
                          margin=dict(t=40,b=10,l=10,r=30), height=320)
        st.plotly_chart(fig, use_container_width=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE 3 - INSIGHTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab3:
    st.subheader("Key findings and what I'd recommend")
    st.caption(
        "These are the six most interesting patterns I found in the data. "
        "Numbers are from the SQL queries - cross-checked against the dashboard above."
    )

    # Pre-compute numbers
    t2 = df_raw[df_raw["city_tier"]=="Tier-2"]
    t3 = df_raw[df_raw["city_tier"]=="Tier-3"]
    t2_vta = round(100*t2["applied"].sum()/len(t2), 1)
    t3_vta = round(100*t3["applied"].sum()/len(t3), 1)

    vr = df_raw[df_raw["employer_verified"]=="Yes"]
    uv = df_raw[df_raw["employer_verified"]=="No"]
    ver_r = round(100*vr["responded"].sum()/vr["applied"].sum(), 1)
    uvr_r = round(100*uv["responded"].sum()/uv["applied"].sum(), 1)

    dl_h  = round(df_raw[df_raw["category"]=="Delivery & Logistics"]["hours_to_first_response"].mean(), 1)
    sal_h = round(df_raw[df_raw["category"]=="Sales"]["hours_to_first_response"].mean(), 1)

    wkd = df_raw[df_raw["posted_day_type"]=="Weekday"]
    wke = df_raw[df_raw["posted_day_type"]=="Weekend"]
    wkd_r = round(100*wkd["responded"].sum()/wkd["applied"].sum(), 1)
    wke_r = round(100*wke["responded"].sum()/wke["applied"].sum(), 1)

    wa  = df_raw[df_raw["acquisition_channel"]=="WhatsApp Share"]
    pa  = df_raw[df_raw["acquisition_channel"]=="Paid Ads"]
    wa_v = round(100*wa["applied"].sum()/len(wa), 1)
    pa_v = round(100*pa["applied"].sum()/len(pa), 1)

    findings = [
        {
            "title": "1. Tier-3 cities apply at a much lower rate",
            "numbers": f"Tier-2: **{t2_vta}%** view-to-apply vs Tier-3: **{t3_vta}%** - a gap of {round(t2_vta-t3_vta,1)} percentage points",
            "why": "Likely reasons: listings may not be in local languages, fewer verified employers (lower trust), and less relevant job supply in smaller cities.",
            "recommendation": "Start by auditing the 3-4 worst Tier-3 cities - check if listings have a language version in the seeker's preferred language. If not, that's probably the first thing to fix.",
            "measure": "Track View to Apply % for the pilot cities week on week."
        },
        {
            "title": "2. Verified employers respond 2.5x more than unverified ones",
            "numbers": f"Verified: **{ver_r}%** response rate | Unverified: **{uvr_r}%** - a massive {round(ver_r-uvr_r,1)}pp gap",
            "why": "Verified employers are probably more serious about hiring. Unverified might be posting jobs without actually being ready to hire.",
            "recommendation": "Add an in-app prompt after a job goes live: 'Complete verification to rank higher in seeker search results.' Also consider suppressing unverified postings from top search results.",
            "measure": "Response rate for newly verified employers - compare the 30 days before and after verification."
        },
        {
            "title": "3. Delivery & Logistics is the slowest category to respond",
            "numbers": f"D&L avg: **{dl_h}h** to first response vs Sales: **{sal_h}h** - more than 2x slower",
            "why": "These are usually small fleet operators or local businesses. They probably check the app once a day at most, and don't have a dedicated HR team.",
            "recommendation": "Send an auto-acknowledgement to the seeker within 1 hour of applying (so they don't feel ignored). Nudge the recruiter with a notification at 24h if they haven't responded.",
            "measure": "% of D&L applications responded to within 24h. Currently this is very low."
        },
        {
            "title": "4. Weekend job postings get weaker recruiter response",
            "numbers": f"Weekday postings: **{wkd_r}%** response rate | Weekend: **{wke_r}%** - {round(wkd_r-wke_r,1)}pp lower",
            "why": "Recruiters (especially at small businesses) probably don't check the app on weekends. Applications pile up and some seekers move on before Monday.",
            "recommendation": "If an employer posts on a Saturday/Sunday, push their job live on Monday morning instead. This ensures the posting gets recruiter attention when they're actually online.",
            "measure": "Compare response rate for weekend-posted jobs that are 'delayed to Monday' vs live immediately."
        },
        {
            "title": "5. WhatsApp Share brings the most intent-driven seekers",
            "numbers": f"WhatsApp Share: **{wa_v}%** view-to-apply | Paid Ads: **{pa_v}%** - a {round(wa_v-pa_v,1)}pp gap",
            "why": "When a friend shares a job on WhatsApp, there's an implicit endorsement. Seekers from paid ads are often just browsing and not ready to apply.",
            "recommendation": "Invest more in referral/share loops - 'Share this job with a friend' inside the app. For paid ads, tighten targeting to city + language + category instead of broad demographics.",
            "measure": "Cost per application by channel. WhatsApp referral CAA is almost certainly lower than paid ads."
        },
        {
            "title": "6. Nagpur had a sharp 2-week dip in July (needs investigation)",
            "numbers": f"Nagpur view-to-apply dropped to ~6-9% in weeks of Jul 13 and Jul 20, vs its normal range of 17-30%",
            "why": "Could be a tracking/data issue, a paused campaign, a drop in employer supply, or something local. Other comparable cities (Nashik, Patna) did not show the same dip.",
            "recommendation": "Before assuming it's demand-side - check the data pipeline first. Then break down by channel and category to isolate where the drop came from.",
            "measure": "Watch Nagpur's weekly view-to-apply % for the next 4 weeks. If it normalises, it was probably a one-time event."
        }
    ]

    for f in findings:
        with st.expander(f["title"], expanded=True):
            st.markdown(f"**Numbers:** {f['numbers']}")
            st.markdown(f"**Why this is happening (hypothesis):** {f['why']}")
            st.markdown(f"**What I'd recommend:** {f['recommendation']}")
            st.markdown(f"**How to measure the impact:** {f['measure']}")

    st.divider()
    st.caption(
        "All data is synthetic - generated with Python (seed=42). "
        "Patterns were designed into the dataset to simulate real marketplace dynamics. "
        "Dashboard validated against SQL queries - headline numbers match exactly."
    )
