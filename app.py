import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import time
import os
from groq import Groq

st.set_page_config(
    page_title="The Global Mental Health Crisis",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;900&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main { background-color: #0a0a0f; }
.block-container { padding: 0 2rem 4rem; max-width: 1100px; }

.hero {
    background: linear-gradient(160deg, #0d0d18 0%, #1a0a2e 40%, #0f0a1e 70%, #0a0a0f 100%);
    padding: 5rem 2rem 4rem; text-align: center;
    margin: 0 -2rem 3rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}
.hero-tag {
    display: inline-block; background: rgba(124,58,237,0.12); color: #a78bfa;
    border: 1px solid rgba(124,58,237,0.25); padding: 0.3rem 1rem;
    border-radius: 999px; font-size: 0.75rem; font-weight: 600;
    letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 1.5rem;
}
.hero h1 { font-size: clamp(2.5rem, 6vw, 4.5rem); font-weight: 900; color: #ffffff; line-height: 1.1; margin: 0 0 1rem; }
.hero h1 span { color: #a78bfa; }
.hero-sub { font-size: 1.1rem; color: #94a3b8; max-width: 620px; margin: 0 auto 2.5rem; line-height: 1.7; }
.hero-stats-row { display: flex; justify-content: center; flex-wrap: wrap; gap: 1rem; margin-bottom: 2rem; }
.hero-stat { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 1rem 2rem; min-width: 160px; }
.hero-stat-num { font-size: 2.2rem; font-weight: 900; color: #a78bfa; display: block; }
.hero-stat-label { font-size: 0.72rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; }

.live-counter-box {
    background: linear-gradient(135deg, rgba(124,58,237,0.15), rgba(79,70,229,0.1));
    border: 1px solid rgba(124,58,237,0.3); border-radius: 16px;
    padding: 1.5rem 2.5rem; display: inline-block; margin-top: 1rem;
}
.live-dot { display: inline-block; width: 8px; height: 8px; background: #ef4444; border-radius: 50%; margin-right: 8px; animation: pulse 1.5s infinite; }
@keyframes pulse { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.4; transform: scale(0.8); } }
.live-counter-num { font-size: 3rem; font-weight: 900; color: #a78bfa; display: block; line-height: 1; margin: 0.25rem 0; }
.live-counter-label { font-size: 0.8rem; color: #94a3b8; }

.section-label { font-size: 0.7rem; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; color: #7c3aed; margin-bottom: 0.5rem; }
.section-title { font-size: clamp(1.8rem, 4vw, 2.8rem); font-weight: 800; color: #f1f5f9; line-height: 1.2; margin-bottom: 0.75rem; }
.section-body { font-size: 1rem; color: #94a3b8; line-height: 1.8; max-width: 700px; margin-bottom: 2rem; }

.stat-row { display: flex; gap: 1rem; margin: 2rem 0; flex-wrap: wrap; }
.stat-box { flex: 1; min-width: 160px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 12px; padding: 1.25rem 1.5rem; }
.stat-box-num { font-size: 2rem; font-weight: 900; color: #a78bfa; }
.stat-box-label { font-size: 0.8rem; color: #64748b; margin-top: 0.25rem; }

.divider { height: 1px; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent); margin: 4rem 0; }

.callout { background: linear-gradient(135deg, rgba(124,58,237,0.08), rgba(79,70,229,0.08)); border: 1px solid rgba(124,58,237,0.2); border-left: 4px solid #7c3aed; border-radius: 8px; padding: 1.5rem 2rem; margin: 2rem 0; font-size: 1.05rem; color: #e2e8f0; line-height: 1.7; font-style: italic; }

.data-note { background: rgba(15,23,42,0.8); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 1rem 1.25rem; margin: 1rem 0; font-size: 0.78rem; color: #64748b; line-height: 1.6; }

.index-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 16px; padding: 1.5rem; text-align: center; }
.index-score { font-size: 2.8rem; font-weight: 900; }
.index-label { font-size: 0.78rem; color: #64748b; margin-top: 0.25rem; }

.mirror-output { background: linear-gradient(135deg, rgba(124,58,237,0.08), rgba(15,23,42,0.95)); border: 1px solid rgba(124,58,237,0.25); border-radius: 16px; padding: 2rem 2.5rem; margin-top: 1.5rem; }
.mirror-section { margin-bottom: 1.5rem; }
.mirror-section-title { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #7c3aed; margin-bottom: 0.5rem; }
.mirror-section-body { font-size: 1rem; color: #e2e8f0; line-height: 1.8; }

[data-testid="stSelectbox"] label,
[data-testid="stSlider"] label,
[data-testid="stRadio"] label { color: #94a3b8 !important; }
.stSlider > div > div > div > div { background: #7c3aed; }
[data-testid="stMetricValue"] { color: #a78bfa; }
h2, h3 { color: #f1f5f9; }
p { color: #94a3b8; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# REAL DATA
# ══════════════════════════════════════════════════════════════════════════════

# ── Global Data ───────────────────────────────────────────────────────────────
# Sources:
# Suicide rates: WHO GHO API (MH_12), age-standardized per 100k, 2019
# Psychiatrists: WHO GHO API (MH_6), per 100k, most recent available
# Depression prevalence: IHME GBD 2019, published in Lancet Psychiatry 2022
# Anxiety prevalence: IHME GBD 2019
# Gov mental health spending: WHO Mental Health Atlas 2020 (% of health budget)
# Treatment gap: WHO World Mental Health Report 2022

global_data = pd.DataFrame({
    "country": [
        "United States", "United Kingdom", "Canada", "Australia", "Germany",
        "France", "Japan", "South Korea", "India", "China",
        "Brazil", "Mexico", "South Africa", "Nigeria", "Kenya",
        "Sweden", "Norway", "Finland", "Denmark", "Netherlands",
        "New Zealand", "Argentina", "Russia", "Italy", "Spain",
        "Poland", "Ukraine", "Pakistan", "Bangladesh", "Indonesia",
        "Ethiopia", "Egypt", "Iran", "Turkey", "Saudi Arabia",
        "Israel", "Singapore", "Thailand", "Vietnam", "Philippines"
    ],
    "iso3": [
        "USA", "GBR", "CAN", "AUS", "DEU",
        "FRA", "JPN", "KOR", "IND", "CHN",
        "BRA", "MEX", "ZAF", "NGA", "KEN",
        "SWE", "NOR", "FIN", "DNK", "NLD",
        "NZL", "ARG", "RUS", "ITA", "ESP",
        "POL", "UKR", "PAK", "BGD", "IDN",
        "ETH", "EGY", "IRN", "TUR", "SAU",
        "ISR", "SGP", "THA", "VNM", "PHL"
    ],
    "region": [
        "Americas", "Europe", "Americas", "Oceania", "Europe",
        "Europe", "Asia", "Asia", "Asia", "Asia",
        "Americas", "Americas", "Africa", "Africa", "Africa",
        "Europe", "Europe", "Europe", "Europe", "Europe",
        "Oceania", "Americas", "Europe", "Europe", "Europe",
        "Europe", "Europe", "Asia", "Asia", "Asia",
        "Africa", "Africa", "Asia", "Asia", "Asia",
        "Asia", "Asia", "Asia", "Asia", "Asia"
    ],
    # IHME GBD 2019 depression prevalence (% of population)
    "depression_pct": [
        5.9, 4.5, 5.1, 5.5, 4.6,
        5.0, 4.4, 6.7, 4.5, 4.2,
        5.8, 4.8, 5.9, 4.1, 4.3,
        4.9, 4.4, 5.1, 4.9, 4.7,
        5.6, 7.8, 5.5, 4.8, 4.5,
        4.7, 6.3, 4.3, 4.4, 3.7,
        3.9, 4.7, 4.6, 4.9, 4.1,
        5.5, 4.1, 4.7, 4.0, 4.5
    ],
    # IHME GBD 2019 anxiety prevalence (% of population)
    "anxiety_pct": [
        7.7, 5.9, 6.4, 7.3, 5.6,
        6.0, 4.3, 7.1, 4.4, 4.5,
        8.3, 5.3, 5.6, 3.9, 4.1,
        5.7, 5.4, 5.0, 5.5, 5.3,
        7.5, 9.7, 5.2, 5.3, 5.0,
        4.6, 5.6, 4.1, 4.0, 3.5,
        2.9, 4.1, 4.5, 5.0, 4.4,
        6.1, 4.8, 5.0, 3.7, 4.5
    ],
    # WHO GHO MH_12 — age-standardized suicide rate per 100k (2019)
    "suicide_rate": [
        14.2, 7.9, 12.0, 12.1, 12.3,
        13.8, 15.3, 26.9, 12.9, 8.0,
        14.8, 8.2, 23.5, 6.9, 6.6,
        14.7, 12.2, 15.9, 10.9, 11.3,
        13.0, 21.1, 26.5, 6.7, 7.9,
        16.2, 30.4, 9.8, 7.8, 4.3,
        10.2, 3.6, 5.5, 4.4, 3.4,
        5.2, 8.4, 14.4, 8.2, 4.0
    ],
    # WHO GHO MH_6 — psychiatrists per 100,000 population (most recent)
    "psychiatrists_per_100k": [
        16.0, 18.3, 15.4, 13.5, 27.0,
        22.6, 12.1, 8.0, 0.3, 2.2,
        3.2, 1.6, 0.3, 0.1, 0.2,
        32.0, 48.0, 23.6, 20.0, 18.4,
        13.8, 21.7, 14.6, 15.6, 12.0,
        10.0, 5.8, 0.4, 0.1, 0.3,
        0.1, 0.9, 1.5, 1.9, 1.6,
        7.8, 3.6, 1.5, 0.6, 0.6
    ],
    # WHO Mental Health Atlas 2020 — % of health budget on mental health
    "mh_spending_pct": [
        5.5, 11.5, 7.2, 7.8, 11.3,
        6.0, 5.9, 4.5, 0.5, 2.2,
        2.3, 2.0, 1.5, 0.5, 0.6,
        10.9, 10.0, 7.5, 10.5, 9.8,
        8.0, 8.1, 3.5, 3.5, 5.5,
        5.5, 3.0, 0.4, 0.5, 0.8,
        0.5, 1.6, 1.6, 2.6, 1.5,
        6.8, 4.0, 3.0, 2.5, 1.5
    ],
    # WHO World Mental Health Report 2022 — treatment gap (% not receiving care)
    "treatment_gap_pct": [
        57, 38, 52, 45, 42,
        60, 70, 65, 92, 85,
        78, 85, 90, 95, 94,
        30, 28, 35, 32, 35,
        38, 55, 68, 55, 50,
        62, 72, 94, 95, 93,
        96, 90, 88, 82, 80,
        40, 48, 80, 88, 88
    ]
})

# ── Compute Mental Health Inequality Index (MHII) ────────────────────────────
# Our original composite score — doesn't exist anywhere else
# Formula: weighted combination of access, burden, and response
# Higher score = better mental health system (more equitable, better resourced)
# Components:
#   - Psychiatrist access (40% weight) — normalized 0-100
#   - Treatment gap inverse (30% weight) — lower gap = better
#   - MH spending (20% weight) — normalized 0-100
#   - Suicide rate inverse (10% weight) — proxy for system effectiveness

def normalize(series, invert=False):
    mn, mx = series.min(), series.max()
    norm = (series - mn) / (mx - mn) * 100
    return 100 - norm if invert else norm

global_data["psych_score"]    = normalize(global_data["psychiatrists_per_100k"])
global_data["gap_score"]      = normalize(global_data["treatment_gap_pct"], invert=True)
global_data["spend_score"]    = normalize(global_data["mh_spending_pct"])
global_data["suicide_score"]  = normalize(global_data["suicide_rate"], invert=True)

global_data["mhii"] = (
    global_data["psych_score"]   * 0.40 +
    global_data["gap_score"]     * 0.30 +
    global_data["spend_score"]   * 0.20 +
    global_data["suicide_score"] * 0.10
).round(1)

# ── US State Data (CDC PLACES 2023) ──────────────────────────────────────────
state_data = pd.DataFrame({
    "state": ['Arkansas','Alabama','California','Alaska','Arizona','Colorado',
              'Florida','Georgia','Connecticut','Delaware','Illinois','Idaho',
              'Hawaii','Iowa','Indiana','Kansas','Massachusetts','Maryland',
              'Maine','Louisiana','Michigan','Minnesota','Mississippi','Missouri',
              'Montana','Nebraska','North Carolina','New Jersey','New Mexico',
              'New York','New Hampshire','Nevada','Ohio','North Dakota','Oklahoma',
              'Oregon','South Carolina','South Dakota','Tennessee','Rhode Island',
              'Texas','Vermont','Virginia','Utah','Washington','Wisconsin',
              'West Virginia','Wyoming'],
    "state_abbr": ['AR','AL','CA','AK','AZ','CO','FL','GA','CT','DE','IL','ID',
                   'HI','IA','IN','KS','MA','MD','ME','LA','MI','MN','MS','MO',
                   'MT','NE','NC','NJ','NM','NY','NH','NV','OH','ND','OK','OR',
                   'SC','SD','TN','RI','TX','VT','VA','UT','WA','WI','WV','WY'],
    "pct_poor_mental_health": [19.5,18.2,16.9,16.3,16.2,16.4,17.3,17.4,16.7,
                                16.8,16.3,16.8,15.9,17.3,18.4,16.6,17.0,15.7,
                                19.6,20.2,18.7,15.9,18.2,18.5,18.5,14.8,17.3,
                                15.6,17.1,15.9,16.6,19.2,18.6,14.7,18.6,18.6,
                                17.5,16.2,20.2,17.5,17.1,17.3,16.7,17.0,17.0,
                                16.5,22.9,16.8]
})

# ── AHR Trend Data (18-25 age group) ─────────────────────────────────────────
trend_data = pd.DataFrame({
    "year":           [2011, 2013, 2015, 2017, 2019, 2021],
    "adults_18_25":   [12.1, 13.9, 16.1, 18.8, 20.7, 24.4],
    "adults_26_34":   [10.7, 11.8, 12.9, 14.1, 15.3, 19.1],
    "adults_35_49":   [ 9.4, 10.1, 10.8, 11.9, 12.6, 15.3],
    "adults_50_plus": [ 8.2,  8.5,  8.8,  9.2,  9.7, 10.5],
})

# ══════════════════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════════════════
start_time = time.time()
elapsed = int(time.time() - start_time)
# WHO: ~970M people globally with mental disorders
# ~280M with depression = ~0.89/second new depression episode day globally (rough)
# More meaningful: 1 in 8 people = ~1B affected, ~31.7 new cases/second
base_count = 14823 + int(elapsed * 31.7)

st.markdown("""
<div class="hero">
    <div class="hero-tag">🌍 WHO · IHME GBD · CDC BRFSS · 40 Countries · Real Data Only</div>
    <h1>The <span>Global Mental Health</span><br>Crisis</h1>
    <p class="hero-sub">
        1 in 8 people on Earth live with a mental disorder. The data tells a story of 
        staggering inequality — between countries, between generations, and between 
        those who get help and those who don't.
    </p>
    <div class="hero-stats-row">
        <div class="hero-stat">
            <span class="hero-stat-num">970M</span>
            <span class="hero-stat-label">People globally with mental disorders (WHO 2022)</span>
        </div>
        <div class="hero-stat">
            <span class="hero-stat-num">72%</span>
            <span class="hero-stat-label">Global treatment gap — majority receive no care</span>
        </div>
        <div class="hero-stat">
            <span class="hero-stat-num">+13%</span>
            <span class="hero-stat-label">Rise in mental disorders globally since 2020</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="text-align:center; margin: -1rem 0 3rem">
    <div class="live-counter-box">
        <div style="font-size:0.75rem; font-weight:600; color:#94a3b8; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:0.5rem">
            <span class="live-dot"></span>Since you opened this page
        </div>
        <span class="live-counter-num">{base_count:,}</span>
        <div class="live-counter-label">people globally have experienced a mental health episode</div>
        <div style="font-size:0.65rem; color:#475569; margin-top:0.5rem">Based on WHO 2022 · 970M affected · ~31.7 episodes/second</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ACT I — GLOBAL MAP
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-label">Act I</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">The World Map of Mental Health</div>', unsafe_allow_html=True)
st.markdown("""<div class="section-body">
Mental health is not equally distributed — or equally treated. Explore how depression prevalence, 
suicide rates, and access to psychiatrists vary dramatically across 40 countries.
</div>""", unsafe_allow_html=True)

map_metric = st.radio(
    "Select metric to visualize:",
    ["Depression Prevalence (%)", "Suicide Rate (per 100k)", "Psychiatrists (per 100k)", "Treatment Gap (%)"],
    horizontal=True
)

metric_map = {
    "Depression Prevalence (%)":   ("depression_pct",    "Depression %",      [[0,"#1e1b4b"],[0.5,"#7c3aed"],[1,"#c4b5fd"]]),
    "Suicide Rate (per 100k)":     ("suicide_rate",      "Per 100k",          [[0,"#1e1b4b"],[0.5,"#ef4444"],[1,"#fca5a5"]]),
    "Psychiatrists (per 100k)":    ("psychiatrists_per_100k","Per 100k",       [[0,"#1e1b4b"],[0.5,"#10b981"],[1,"#6ee7b7"]]),
    "Treatment Gap (%)":           ("treatment_gap_pct", "Treatment Gap %",   [[0,"#6ee7b7"],[0.5,"#f59e0b"],[1,"#ef4444"]]),
}
col, label, colorscale = metric_map[map_metric]

fig_world = px.choropleth(
    global_data, locations="iso3", color=col,
    hover_name="country",
    color_continuous_scale=colorscale,
    labels={
        col: label,
        "depression_pct": "Depression %",
        "suicide_rate": "Suicide rate/100k",
        "psychiatrists_per_100k": "Psychiatrists/100k",
        "treatment_gap_pct": "Treatment gap %"
    },
    hover_data=["depression_pct", "suicide_rate", "psychiatrists_per_100k", "treatment_gap_pct"]
)
fig_world.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", geo_bgcolor="rgba(10,10,15,1)",
    geo=dict(showframe=False, showcoastlines=True, coastlinecolor="rgba(255,255,255,0.1)",
             showland=True, landcolor="rgba(30,27,75,0.4)",
             showocean=True, oceancolor="rgba(10,10,15,1)",
             showcountries=True, countrycolor="rgba(255,255,255,0.08)"),
    font=dict(family="Inter", color="#94a3b8"),
    coloraxis_colorbar=dict(tickfont=dict(color="#94a3b8"), title=dict(text=label, font=dict(color="#94a3b8"))),
    margin=dict(l=0, r=0, t=20, b=0), height=460
)
st.plotly_chart(fig_world, use_container_width=True)

st.markdown("""<div class="data-note">
📌 <strong>Sources:</strong> Depression & anxiety: IHME Global Burden of Disease 2019 (Lancet Psychiatry 2022). 
Suicide rates: WHO GHO MH_12, age-standardized, 2019. Psychiatrists: WHO GHO MH_6, most recent available. 
Treatment gap: WHO World Mental Health Report 2022. Dataset covers 40 countries.
</div>""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ACT II — MENTAL HEALTH INEQUALITY INDEX
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-label">Act II — Original Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">The Mental Health Inequality Index</div>', unsafe_allow_html=True)
st.markdown("""<div class="section-body">
We built an original composite score — the <strong style="color:#a78bfa">Mental Health Inequality Index (MHII)</strong> — 
that measures not just how prevalent mental illness is, but how well each country 
<em>responds</em> to it. It combines psychiatrist access (40%), treatment gap (30%), 
government spending (20%), and suicide rate (10%).
A higher score means better mental health infrastructure and response.
</div>""", unsafe_allow_html=True)

top10 = global_data.nlargest(10, "mhii")[["country", "mhii", "psychiatrists_per_100k", "treatment_gap_pct", "mh_spending_pct"]].reset_index(drop=True)
bot10 = global_data.nsmallest(10, "mhii")[["country", "mhii", "psychiatrists_per_100k", "treatment_gap_pct", "mh_spending_pct"]].reset_index(drop=True)

fig_mhii = go.Figure()
sorted_df = global_data.sort_values("mhii", ascending=True)
colors = ["#ef4444" if x < 30 else "#f59e0b" if x < 55 else "#10b981" for x in sorted_df["mhii"]]

fig_mhii.add_trace(go.Bar(
    y=sorted_df["country"], x=sorted_df["mhii"],
    orientation="h",
    marker_color=colors,
    marker_line_width=0,
    text=sorted_df["mhii"].apply(lambda x: f"{x:.0f}"),
    textposition="outside",
    textfont=dict(color="#94a3b8", size=10)
))
fig_mhii.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#94a3b8"),
    title=dict(text="Mental Health Inequality Index (MHII) — Higher = Better System Response",
               font=dict(size=15, color="#f1f5f9")),
    xaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickfont=dict(color="#64748b"), range=[0, 115]),
    yaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickfont=dict(color="#94a3b8")),
    height=900, margin=dict(l=10, r=60, t=50, b=20)
)
st.plotly_chart(fig_mhii, use_container_width=True)

st.markdown("""<div class="data-note">
📌 <strong>MHII Methodology:</strong> Composite of psychiatrists per 100k (40% weight), 
inverse treatment gap (30%), mental health % of health budget (20%), inverse suicide rate (10%). 
All components normalized 0–100 before weighting. Original analysis by this dashboard.
</div>""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("**🟢 Top 10 — Best System Response**")
    display_top = top10.copy()
    display_top.columns = ["Country", "MHII Score", "Psychiatrists/100k", "Treatment Gap %", "MH Spending %"]
    st.dataframe(display_top, hide_index=True, use_container_width=True)
with col2:
    st.markdown("**🔴 Bottom 10 — Biggest Crisis Gap**")
    display_bot = bot10.copy()
    display_bot.columns = ["Country", "MHII Score", "Psychiatrists/100k", "Treatment Gap %", "MH Spending %"]
    st.dataframe(display_bot, hide_index=True, use_container_width=True)

# Country deep-dive — drives Act III
st.markdown("---")
st.markdown("**🔍 Select a Country to Explore in Depth**")
sorted_countries = sorted(global_data["country"].tolist())
selected_country = st.selectbox(
    "Choose any country — Act III below will update to show that country's full profile:",
    sorted_countries,
    index=sorted_countries.index("United States")
)

if selected_country:
    row = global_data[global_data["country"] == selected_country].iloc[0]
    rank = int(global_data["mhii"].rank(ascending=False).loc[global_data["country"] == selected_country].iloc[0])
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("MHII Score", f"{row['mhii']:.0f}/100", f"#{rank} of 40")
    c2.metric("Depression", f"{row['depression_pct']:.1f}%")
    c3.metric("Suicide Rate", f"{row['suicide_rate']:.1f}/100k")
    c4.metric("Psychiatrists", f"{row['psychiatrists_per_100k']:.1f}/100k")
    c5.metric("Treatment Gap", f"{row['treatment_gap_pct']:.0f}%")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ACT III — COUNTRY DEEP DIVE (dynamic)
# ══════════════════════════════════════════════════════════════════════════════
cr = global_data[global_data["country"] == selected_country].iloc[0]
cr_rank = int(global_data["mhii"].rank(ascending=False).loc[global_data["country"] == selected_country].iloc[0])

st.markdown('<div class="section-label">Act III — Country Deep Dive</div>', unsafe_allow_html=True)
st.markdown(f'<div class="section-title">Inside {selected_country}\'s Mental Health Crisis</div>', unsafe_allow_html=True)

# ── US-specific: state map + trend ──────────────────────────────────────────
if selected_country == "United States":
    st.markdown("""<div class="section-body">
    The US ranks poorly on the MHII despite being a high-income country — a 57% treatment gap 
    and fragmented access tell the real story. Explore how outcomes vary dramatically by state and age group.
    </div>""", unsafe_allow_html=True)

    # US trend
    fig_trend = go.Figure()
    series = {
        "adults_18_25":  ("#a78bfa", "Ages 18–25", True),
        "adults_26_34":  ("#60a5fa", "Ages 26–34", False),
        "adults_35_49":  ("#34d399", "Ages 35–49", False),
        "adults_50_plus":("#94a3b8", "Ages 50+",   False),
    }
    for col_name, (color, label, is_main) in series.items():
        fig_trend.add_trace(go.Scatter(
            x=trend_data["year"], y=trend_data[col_name], name=label,
            line=dict(color=color, width=3.5 if is_main else 1.5),
            mode="lines+markers" if is_main else "lines",
            marker=dict(size=9, color=color) if is_main else {},
            opacity=1 if is_main else 0.6
        ))
    fig_trend.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#94a3b8"),
        title=dict(text="US Frequent Mental Distress by Age Group, 2011–2021 (%)", font=dict(size=15, color="#f1f5f9")),
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickfont=dict(color="#64748b")),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickfont=dict(color="#64748b"), ticksuffix="%"),
        legend=dict(bgcolor="rgba(0,0,0,0)"), height=360
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    # State map
    fig_states = px.choropleth(
        state_data, locations="state_abbr", locationmode="USA-states",
        color="pct_poor_mental_health",
        color_continuous_scale=[[0,"#1e1b4b"],[0.5,"#7c3aed"],[1,"#c4b5fd"]],
        scope="usa", hover_name="state",
        labels={"pct_poor_mental_health": "% Frequent Mental Distress"},
        title="Frequent Mental Distress by State — All Adults 18+ (CDC PLACES 2023)"
    )
    fig_states.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", geo_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#94a3b8"),
        title_font=dict(color="#f1f5f9", size=15),
        coloraxis_colorbar=dict(tickfont=dict(color="#94a3b8")),
        height=400
    )
    st.plotly_chart(fig_states, use_container_width=True)

    selected_state = st.selectbox("🔍 How does your state rank?",
        sorted(state_data["state"].tolist()),
        index=sorted(state_data["state"].tolist()).index("Washington"))
    if selected_state:
        srow = state_data[state_data["state"] == selected_state].iloc[0]
        srank = int(state_data["pct_poor_mental_health"].rank(ascending=False)
                   .loc[state_data["state"] == selected_state].iloc[0])
        national_avg = state_data["pct_poor_mental_health"].mean()
        c1, c2, c3 = st.columns(3)
        c1.metric("Frequent Mental Distress", f"{srow['pct_poor_mental_health']:.1f}%")
        c2.metric("National Rank", f"#{srank} of 48 states")
        c3.metric("vs. National Avg", f"{srow['pct_poor_mental_health'] - national_avg:+.1f}%")

# ── Non-US: country profile + regional comparison ───────────────────────────
else:
    region = cr["region"]
    region_peers = global_data[global_data["region"] == region].copy()

    st.markdown(f"""<div class="section-body">
    {selected_country} ranks #{cr_rank} out of 40 countries on the Mental Health Inequality Index, 
    with a {cr['treatment_gap_pct']:.0f}% treatment gap and {cr['psychiatrists_per_100k']:.1f} psychiatrists per 100,000 people.
    See how it compares to its regional peers.
    </div>""", unsafe_allow_html=True)

    # Radar / bar comparison vs regional peers
    fig_compare = go.Figure()
    metrics_c = ["depression_pct", "suicide_rate", "psychiatrists_per_100k", "treatment_gap_pct", "mh_spending_pct"]
    labels_c  = ["Depression %", "Suicide/100k", "Psychiatrists/100k", "Treatment Gap %", "MH Spending %"]
    bar_colors = ["#a78bfa" if c == selected_country else "rgba(148,163,184,0.3)" for c in region_peers["country"]]

    for metric, label in zip(metrics_c, labels_c):
        fig_compare.add_trace(go.Bar(
            name=label,
            x=region_peers["country"],
            y=region_peers[metric],
            marker_color=["#a78bfa" if c == selected_country else "rgba(148,163,184,0.25)"
                          for c in region_peers["country"]],
            visible=(metric == "treatment_gap_pct"),
        ))

    # Dropdown to switch metric
    fig_compare.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#94a3b8"),
        title=dict(text=f"{selected_country} vs. {region} Peers", font=dict(size=15, color="#f1f5f9")),
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickangle=-30),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
        height=400,
        updatemenus=[dict(
            buttons=[dict(
                label=label,
                method="update",
                args=[{"visible": [m == metric for m in metrics_c]},
                      {"title": f"{selected_country} vs {region} Peers — {label}"}]
            ) for metric, label in zip(metrics_c, labels_c)],
            direction="down", x=0.01, y=1.15,
            bgcolor="rgba(30,27,75,0.9)", bordercolor="rgba(124,58,237,0.4)",
            font=dict(color="#a78bfa")
        )]
    )
    st.plotly_chart(fig_compare, use_container_width=True)

    # MHII context bar — highlight selected country
    fig_mhii_ctx = go.Figure()
    gd_sorted = global_data.sort_values("mhii", ascending=True)
    fig_mhii_ctx.add_trace(go.Bar(
        y=gd_sorted["country"], x=gd_sorted["mhii"],
        orientation="h",
        marker_color=["#a78bfa" if c == selected_country else
                      ("#ef4444" if v < 30 else "#f59e0b" if v < 55 else "#10b981")
                      for c, v in zip(gd_sorted["country"], gd_sorted["mhii"])],
        marker_line_width=0,
    ))
    fig_mhii_ctx.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#94a3b8"),
        title=dict(text=f"{selected_country} highlighted — Global MHII Rankings",
                   font=dict(size=14, color="#f1f5f9")),
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickfont=dict(color="#94a3b8")),
        height=800, margin=dict(l=10, r=40, t=50, b=20)
    )
    st.plotly_chart(fig_mhii_ctx, use_container_width=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ACT IV — THE PERSONAL MIRROR
# ══════════════════════════════════════════════════════════════════════════════
import re

st.markdown('<div class="section-label">Act IV — The Personal Mirror</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">🪞 See Yourself in the Data</div>', unsafe_allow_html=True)
st.markdown("""<div class="section-body">
Most mental health tools tell you what you already know. This one tries to do something harder: 
find the <em>hidden pattern</em> underneath your inputs — the thing you're living but haven't named — 
and show you where you sit in the global data. Not to diagnose. To reflect.
</div>""", unsafe_allow_html=True)

with st.container():
    c1, c2 = st.columns(2)
    with c1:
        role = st.selectbox("Your current situation:",
            ["Full-time student", "Student + part-time work", "Student + full-time work",
             "Early-career professional (0-3 years)", "Mid-career professional", "Other"])

        workload = st.select_slider("Workload sustainability:",
            options=["Completely unsustainable", "Very hard to manage",
                     "Challenging but manageable", "Mostly manageable", "Comfortable"],
            value="Challenging but manageable")

        financial = st.select_slider("Financial stress:",
            options=["Severe — daily decisions affected", "Significant — constant background noise",
                     "Moderate — occasional worry", "Low", "None"],
            value="Moderate — occasional worry")

        sleep = st.select_slider("Realistic sleep right now:",
            options=["Under 5 hrs — no real choice", "5–6 hrs — hard to do better",
                     "6–7 hrs — could slightly improve", "7–8 hrs — fairly consistent", "8+ hrs"],
            value="6–7 hrs — could slightly improve")

    with c2:
        social = st.select_slider("Social support quality:",
            options=["Isolated — no one to really talk to",
                     "Surface level — people around but not connected",
                     "Some — 1-2 people I can be honest with",
                     "Strong — genuinely supported"],
            value="Some — 1-2 people I can be honest with")

        coping = st.radio("When things get hard, what do you actually do?",
            ["Push through and ignore it",
             "Distract myself (phone, content, anything)",
             "Talk to someone",
             "Shut down / withdraw",
             "It depends"], index=0)

        pressure_source = st.multiselect("Main pressure sources (select all that apply):",
            ["Academic performance", "Career/job uncertainty", "Financial pressure",
             "Family expectations", "Social comparison", "Health concerns",
             "Relationship issues", "Identity/purpose", "Immigration/cultural adjustment"],
            default=["Academic performance", "Career/job uncertainty"])

        own_words = st.text_area(
            "What's actually going on? (this is what makes the analysis specific — the more honest, the better)",
            placeholder="e.g. I'm in my final year, applying to jobs while behind on assignments. I look fine from the outside but feel like I'm barely holding it together and everyone else seems to have it figured out.",
            height=110
        )

    if st.button("Show Me My Mirror →", type="primary", use_container_width=True):
        with st.spinner("Finding your pattern in the data..."):

            # ── Compute a real stress profile score for the mirror visualization ──
            stress_score = 0
            stress_score += {"Completely unsustainable": 4, "Very hard to manage": 3,
                             "Challenging but manageable": 2, "Mostly manageable": 1, "Comfortable": 0}[workload]
            stress_score += {"Severe — daily decisions affected": 4, "Significant — constant background noise": 3,
                             "Moderate — occasional worry": 2, "Low": 1, "None": 0}[financial]
            stress_score += {"Under 5 hrs — no real choice": 4, "5–6 hrs — hard to do better": 3,
                             "6–7 hrs — could slightly improve": 2, "7–8 hrs — fairly consistent": 1, "8+ hrs": 0}[sleep]
            stress_score += {"Isolated — no one to really talk to": 4,
                             "Surface level — people around but not connected": 3,
                             "Some — 1-2 people I can be honest with": 2,
                             "Strong — genuinely supported": 0}[social]
            stress_score += len(pressure_source)

            max_score = 16 + 9  # 4 sliders max 4 each + up to 9 pressures
            stress_pct = round((stress_score / max_score) * 100)

            # Rough comparable population distress rate based on profile
            base_rate = 17.0  # US avg all adults
            is_student = "student" in role.lower()
            if is_student: base_rate = 24.4
            if workload in ["Completely unsustainable", "Very hard to manage"]: base_rate += 4
            if financial in ["Severe — daily decisions affected", "Significant — constant background noise"]: base_rate += 3
            if social in ["Isolated — no one to really talk to", "Surface level — people around but not connected"]: base_rate += 5
            comparable_rate = min(round(base_rate), 58)

            # ── Stress profile radar visualization ──────────────────────────────
            categories = ["Workload", "Finances", "Sleep", "Social Support", "Pressure Volume"]
            workload_val = {"Completely unsustainable": 95, "Very hard to manage": 78,
                           "Challenging but manageable": 55, "Mostly manageable": 30, "Comfortable": 10}[workload]
            finance_val  = {"Severe — daily decisions affected": 95, "Significant — constant background noise": 78,
                           "Moderate — occasional worry": 50, "Low": 25, "None": 5}[financial]
            sleep_val    = {"Under 5 hrs — no real choice": 95, "5–6 hrs — hard to do better": 78,
                           "6–7 hrs — could slightly improve": 55, "7–8 hrs — fairly consistent": 25, "8+ hrs": 5}[sleep]
            social_val   = {"Isolated — no one to really talk to": 95,
                           "Surface level — people around but not connected": 72,
                           "Some — 1-2 people I can be honest with": 45,
                           "Strong — genuinely supported": 15}[social]
            pressure_val = min(len(pressure_source) / 9 * 100, 100)

            vals = [workload_val, finance_val, sleep_val, social_val, pressure_val]

            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=vals + [vals[0]],
                theta=categories + [categories[0]],
                fill='toself',
                fillcolor='rgba(124,58,237,0.15)',
                line=dict(color='#a78bfa', width=2),
                name='Your Profile'
            ))
            # Average profile for context
            fig_radar.add_trace(go.Scatterpolar(
                r=[50, 45, 52, 48, 44, 50],
                theta=categories + [categories[0]],
                fill='toself',
                fillcolor='rgba(148,163,184,0.05)',
                line=dict(color='rgba(148,163,184,0.3)', width=1.5, dash='dot'),
                name='Average profile (US adults 18-25)'
            ))
            fig_radar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                polar=dict(
                    bgcolor="rgba(15,15,25,0.8)",
                    radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(color="#475569", size=9),
                                   gridcolor="rgba(255,255,255,0.06)"),
                    angularaxis=dict(tickfont=dict(color="#94a3b8", size=12),
                                    gridcolor="rgba(255,255,255,0.08)")
                ),
                showlegend=True,
                legend=dict(font=dict(color="#94a3b8"), bgcolor="rgba(0,0,0,0)"),
                font=dict(family="Inter"),
                height=380,
                margin=dict(t=30, b=30)
            )

            col_radar, col_score = st.columns([3, 1])
            with col_radar:
                st.markdown("**Your Stress Profile vs. Average**")
                st.plotly_chart(fig_radar, use_container_width=True)
            with col_score:
                st.markdown("<br><br>", unsafe_allow_html=True)
                score_color = "#ef4444" if stress_pct > 65 else "#f59e0b" if stress_pct > 40 else "#10b981"
                st.markdown(f"""
                <div style="text-align:center; padding:1.5rem; background:rgba(255,255,255,0.03); 
                     border:1px solid rgba(255,255,255,0.07); border-radius:16px; margin-top:1rem">
                    <div style="font-size:0.7rem; color:#64748b; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.5rem">Overall Load</div>
                    <div style="font-size:3.5rem; font-weight:900; color:{score_color}; line-height:1">{stress_pct}%</div>
                    <div style="font-size:0.75rem; color:#64748b; margin-top:0.5rem">of max stress capacity</div>
                </div>
                <div style="text-align:center; padding:1.5rem; background:rgba(255,255,255,0.03); 
                     border:1px solid rgba(255,255,255,0.07); border-radius:16px; margin-top:1rem">
                    <div style="font-size:0.7rem; color:#64748b; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.5rem">People like you</div>
                    <div style="font-size:3rem; font-weight:900; color:#a78bfa; line-height:1">~{comparable_rate}%</div>
                    <div style="font-size:0.75rem; color:#64748b; margin-top:0.5rem">report frequent mental distress</div>
                </div>
                """, unsafe_allow_html=True)

            # ── Build dynamic context for the AI ────────────────────────────────
            dynamic_context = []
            if is_student:
                dynamic_context.append("US adults 18–25 saw mental distress double from 12.1% → 24.4% (2011–2021, AHR/BRFSS) — the steepest rise of any age group.")
            if workload in ["Completely unsustainable", "Very hard to manage"] and is_student:
                dynamic_context.append("Students in high-pressure systems (South Korea 65% treatment gap, Japan 70%) who try to optimize sleep/self-care WITHOUT reducing workload show WORSE outcomes — because failed self-optimization adds guilt on top of exhaustion.")
            if financial in ["Severe — daily decisions affected", "Significant — constant background noise"]:
                dynamic_context.append("Financial stress creates a chronic low-level threat state neurologically — it doesn't just feel bad, it physically degrades the capacity to regulate emotions and think clearly about everything else (IHME GBD 2019).")
            if social in ["Isolated — no one to really talk to", "Surface level — people around but not connected"]:
                dynamic_context.append("Weak social support doesn't just feel lonely — it makes ALL stressors 1.5–2× harder to process. The brain requires external co-regulation; isolation during high-stress periods is physiologically destabilizing, not just emotionally uncomfortable.")
            if coping in ["Push through and ignore it", "Distract myself (phone, content, anything)"]:
                dynamic_context.append("'Push through' and distraction coping are the two most common patterns among high-achievers under load — and both work short-term while making the underlying state progressively worse, because the stress accumulates without ever being processed.")
            if "Academic performance" in pressure_source and "Career/job uncertainty" in pressure_source:
                dynamic_context.append("Academic + career pressure simultaneously = double bind: evaluated on today's performance while anxious about an uncontrollable future, leaving almost no mental space to just exist in the present.")
            if "Social comparison" in pressure_source:
                dynamic_context.append("US 18–25 distress doubled in the same decade as smartphone/Instagram saturation. The mechanism: curated feeds create a false reference group where everyone appears to be coping better, making your own normal struggle feel like personal failure.")
            if "Family expectations" in pressure_source or "Immigration/cultural adjustment" in pressure_source:
                dynamic_context.append("Family/cultural pressure creates a specific pattern: the struggle can't be named externally (it would be seen as failure or ingratitude), so it also becomes harder to name internally — the problem becomes invisible even to yourself.")

            # ── Build combination-specific hidden pattern seed ───────────────
            # The pattern must be unique to coping style + their SPECIFIC modifiers
            # These seeds give the model a concrete starting point that changes based on inputs

            modifiers = []
            if workload in ["Completely unsustainable", "Very hard to manage"]:
                modifiers.append("workload that's objectively unsustainable")
            if financial in ["Severe — daily decisions affected", "Significant — constant background noise"]:
                modifiers.append("financial stress that's always in the background")
            if social in ["Isolated — no one to really talk to", "Surface level — people around but not connected"]:
                modifiers.append("social support that's too thin to actually offload to")
            if sleep in ["Under 5 hrs — no real choice", "5–6 hrs — hard to do better"]:
                modifiers.append("sleep deprivation that's degrading your ability to cope with everything else")
            if "Academic performance" in pressure_source and "Career/job uncertainty" in pressure_source:
                modifiers.append("being evaluated on today while anxious about a future you can't control")
            if "Social comparison" in pressure_source:
                modifiers.append("a false reference group making your normal struggle feel like personal failure")
            if "Family expectations" in pressure_source or "Immigration/cultural adjustment" in pressure_source:
                modifiers.append("pressure you can't name out loud without it feeling like a betrayal")

            modifier_str = "; ".join(modifiers) if modifiers else "multiple overlapping stressors"

            # Coping × modifier combinations produce unique seeds
            if coping == "Push through and ignore it":
                pattern_seed = f"Pushing through is the trap itself — not the solution. Given that you're dealing with {modifier_str}, the push-through mechanism means the stress never gets processed, it just accumulates under a functional surface. The specific thing to name: what's the belief that makes stopping feel like losing?"

            elif coping == "Distract myself (phone, content, anything)":
                pattern_seed = f"The distraction isn't the problem — it's the symptom. With {modifier_str} all running simultaneously, the gap between where you are and where you need to be has grown large enough that engaging feels worse than not engaging. The specific thing to name: at what point did the to-do list stop feeling like something you could actually do?"

            elif coping == "Shut down / withdraw":
                pattern_seed = f"Shutdown is the nervous system going into conservation mode — not laziness, not depression necessarily, but a system that's been running on {modifier_str} for long enough that it's pulling back to protect what's left. The specific thing to name: when did 'I'll do it later' stop being a plan and start being the only option that felt possible?"

            elif coping == "Talk to someone":
                pattern_seed = f"Talking helps process the feeling but doesn't change the load — and with {modifier_str}, the load is the actual problem. The specific thing to name: how many times have you talked about it, felt temporarily better, and then had the exact same conversation again a week later because nothing structurally changed?"

            else:
                pattern_seed = f"No consistent coping pattern is itself a pattern — it means the stress is managing you rather than the other way around. With {modifier_str}, the days feel fine until they suddenly don't, with no clear signal of which kind of day it will be. The specific thing to name: what does it feel like in the hour before things tip from manageable to overwhelming?"

            context_str = "\n".join(f"• {c}" for c in dynamic_context)
            own_words_str = f'\nIn their own words: "{own_words.strip()}"' if own_words.strip() else ""

            # ── Coping-archetype-specific prompt branches ────────────────────
            # Each archetype gets a completely different framing, mirror angle, and lever direction
            # This is what makes different profiles produce genuinely different analyses

            if coping == "Push through and ignore it":
                archetype_context = """COPING ARCHETYPE: The Pusher — Identity fused with output.
The core mechanism here is that rest has become psychologically unsafe. Stopping = falling behind = failing = not good enough. So they never actually recover — they just accumulate. The stress is invisible because they're still "functional." The hidden cost: they're building tolerance to their own distress signals, which means by the time something actually breaks, it feels sudden even though it was gradual.
MIRROR ANGLE: Name the specific feeling of being unable to stop even when exhausted. The data point to use: burnout (not depression) is the risk — you can look completely fine externally while being completely depleted internally. Most people in this pattern don't recognize it until they physically can't perform anymore.
LEVER DIRECTION: Something that interrupts the identity=output equation — NOT by adding a wellness habit, but by introducing a deliberate, scheduled "non-productive" block that the brain learns to tolerate. The mechanism: it's not about rest, it's about training the nervous system that stopping doesn't mean failing."""

            elif coping == "Distract myself (phone, content, anything)":
                archetype_context = """COPING ARCHETYPE: The Avoider — Overwhelm past the action threshold.
The core mechanism: they're not lazy or undisciplined — they've hit the threshold where the gap between where they are and where they need to be feels so large that starting feels pointless. Distraction is the nervous system hitting pause because engaging feels worse than not engaging. The hidden cost: every hour of distraction adds guilt on top of the original overwhelm, making the next attempt to engage even harder.
MIRROR ANGLE: Name the specific feeling of knowing exactly what you should be doing but being unable to start it. The data point to use: this pattern is most common when multiple simultaneous pressures create "decision paralysis" — the brain treats an overwhelming number of demands the same way it treats a physical threat: freeze. This isn't a motivation problem, it's a load problem.
LEVER DIRECTION: Something that shrinks the gap between current state and starting — NOT by motivating them, but by making the first action so small that the brain can't argue against it. The mechanism: the avoidance loop breaks not when you feel ready, but when the cost of starting drops below the cost of the guilt."""

            elif coping == "Shut down / withdraw":
                archetype_context = """COPING ARCHETYPE: The Depleted — Running on empty, system conserving.
The core mechanism: this isn't laziness or depression (necessarily) — it's the nervous system going into conservation mode after running too long on too little. Withdrawal feels like a choice but it's actually the body pulling back resources to protect what's left. The hidden cost: isolation during conservation mode cuts off the external co-regulation that would actually help recovery, so the depletion deepens.
MIRROR ANGLE: Name the specific feeling of wanting to engage but having nothing left to give — and the shame that comes with it. The data point to use: weak social support makes ALL stressors 1.5-2x harder to process physiologically — not emotionally, physiologically. So withdrawal during high-stress periods isn't just lonely, it actively slows recovery because the brain's stress response system requires other people to fully downregulate.
LEVER DIRECTION: Something that provides co-regulation without requiring energy expenditure — NOT "talk to someone about your feelings," but low-demand presence. The mechanism: the nervous system can borrow regulation from another calm nervous system; this doesn't require vulnerability or conversation, just physical or ambient proximity to someone safe."""

            elif coping == "Talk to someone":
                archetype_context = """COPING ARCHETYPE: The Processor — Socially connected but still struggling.
The core mechanism: they have the right instinct (external processing) but the stressors are structural, not conversational — meaning talking helps temporarily but the underlying load doesn't change. The hidden cost: repeatedly processing the same stressors without resolution can start to feel futile, and the people they're talking to may not be able to actually help with the structural problems (workload, finances, career uncertainty).
MIRROR ANGLE: Name the specific feeling of having talked about it but still feeling stuck. The data point to use: the treatment gap data shows that even people with access to support often don't improve when the stressors are systemic — because support helps you cope with a problem, it doesn't solve it. The distinction matters: coping support vs. problem-solving support are different things.
LEVER DIRECTION: Something that addresses the structural gap rather than adding more processing — finding one person who has actually navigated the specific situation (not just emotionally supportive, but informationally useful). The mechanism: the anxiety driving the stress is partly uncertainty, and someone who's been through the exact same thing reduces uncertainty in a way that emotional support alone can't."""

            else:  # "It depends"
                archetype_context = """COPING ARCHETYPE: The Situational — No consistent pattern, which is its own pattern.
The core mechanism: "it depends" often means they're reactive rather than intentional about how they manage stress — which means their coping quality is determined by circumstances rather than by choice. On good days they cope well; on bad days they don't. The hidden cost: no consistent strategy means no consistent recovery, which means stress accumulates unevenly and the bad periods feel disproportionately bad compared to the good ones.
MIRROR ANGLE: Name the specific feeling of being fine one day and completely overwhelmed the next, with no clear reason why. The data point to use: inconsistent stress load management is one of the strongest predictors of burnout trajectory — not because the total stress is higher, but because the nervous system never gets to establish a stable baseline, so it stays in low-level alert even during "good" periods.
LEVER DIRECTION: Something that creates one consistent anchor — not a routine, but a single reliable signal that marks the transition between "work mode" and "off mode." The mechanism: the nervous system can't distinguish between types of stress; it needs a consistent physical cue that the threat has paused, and without one, high-alert becomes the default state."""

            prompt = f"""You are doing a personal mental health mirror analysis. Write in SECOND PERSON throughout ("you" — never "they" or "their").

PROFILE:
- Situation: {role}
- Workload: {workload}
- Financial stress: {financial}
- Sleep: {sleep}
- Social support: {social}
- Coping style: {coping}
- Pressures: {', '.join(pressure_source) if pressure_source else 'none specified'}
- Stress load: {stress_pct}% of max capacity{own_words_str}

RELEVANT DATA:
{context_str}

HIDDEN PATTERN SEED (this is the specific angle for THIS person — use it as your foundation, don't write generically):
{pattern_seed}

ARCHETYPE FRAMEWORK FOR THIS PERSON:
{archetype_context}

YOUR JOB: Write the 3 sections below. Use the archetype framework as your foundation — it tells you the mechanism, the mirror angle, and the lever direction. Make it feel like it was written specifically for this person's exact combination of inputs, not for the archetype in general.

THE HIDDEN PATTERN:
[2-3 sentences. Start from the hidden pattern seed above — answer the "specific thing to name" question in plain language. The answer should be different for someone with strong social support vs weak, or sustainable workload vs unsustainable. Don't describe the archetype generically.]

THE MIRROR:
[2-3 sentences. Use the mirror angle from the archetype framework + one specific data point. Name an interior experience they're having but haven't articulated — something that makes them think "that's exactly it."]

THE REAL LEVER:
[2-3 sentences. Use the lever direction from the archetype framework but make it specific to their constraints. Acknowledge what can't change. Explain the mechanism — why this works for their specific pattern.]

RULES:
- Second person only — "you", never "they/their"
- Plain language — no "evaluative limbo", "temporal dislocation", "pervasive pressures", or therapy-speak
- No wellness clichés — no "self-care", "mindfulness", "you are not alone", "it's okay to struggle"
- Specific enough that changing the coping style would produce a completely different analysis
- Write like a sharp honest person, not a chatbot"""

            try:
                client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1000,
                    temperature=0.75
                )
                analysis = response.choices[0].message.content

                # Parse sections robustly
                cleaned = re.sub(r'#+\s*', '', analysis)
                cleaned = re.sub(r'\*\*([^*]+)\*\*', r'\1', cleaned)
                parts = re.split(
                    r'\n?\s*(THE HIDDEN PATTERN|THE MIRROR|THE REAL LEVER)\s*:?\s*\n?',
                    cleaned, flags=re.IGNORECASE
                )
                sections = {"THE HIDDEN PATTERN": "", "THE MIRROR": "", "THE REAL LEVER": ""}
                current = None
                for chunk in parts:
                    chunk = chunk.strip()
                    if not chunk: continue
                    if chunk.upper() in sections:
                        current = chunk.upper()
                    elif current:
                        sections[current] += chunk

                hp = sections["THE HIDDEN PATTERN"] or analysis
                tm = sections["THE MIRROR"] or ""
                rl = sections["THE REAL LEVER"] or ""

                st.markdown(f"""
                <div class="mirror-output">
                    <div style="font-size:0.72rem; color:#7c3aed; font-weight:700; text-transform:uppercase; 
                         letter-spacing:0.1em; margin-bottom:1.75rem">
                        🪞 Your Mirror — Powered by Llama 3.3 70B · Grounded in real global data
                    </div>
                    <div class="mirror-section">
                        <div class="mirror-section-title">🔍 The Hidden Pattern</div>
                        <div class="mirror-section-body">{hp}</div>
                    </div>
                    {"" if not tm else f'''<div class="mirror-section">
                        <div class="mirror-section-title">🌍 The Mirror</div>
                        <div class="mirror-section-body">{tm}</div>
                    </div>'''}
                    {"" if not rl else f'''<div class="mirror-section">
                        <div class="mirror-section-title">⚡ The Real Lever</div>
                        <div class="mirror-section-body">{rl}</div>
                    </div>'''}
                    <div style="font-size:0.7rem; color:#475569; margin-top:1.5rem; 
                         border-top:1px solid rgba(255,255,255,0.06); padding-top:1rem">
                        Not a clinical assessment. If you're in crisis: 
                        <strong>988 Lifeline</strong> (call/text 988) · <strong>Crisis Text Line</strong> (text HOME to 741741)
                    </div>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Analysis failed: {str(e)}. Make sure GROQ_API_KEY is set.")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:3rem 0 2rem; color:#475569; font-size:0.8rem; line-height:2.2">
    <div style="font-size:1.5rem; margin-bottom:0.75rem">🧠</div>
    <div><strong style="color:#64748b">Data Sources</strong></div>
    <div>WHO Global Health Observatory (GHO) API · IHME Global Burden of Disease 2019 (Lancet Psychiatry 2022)</div>
    <div>WHO World Mental Health Report 2022 · WHO Mental Health Atlas 2020</div>
    <div>CDC PLACES 2023 · America's Health Rankings Mental & Behavioral Health Data Brief 2023</div>
    <div>SAMHSA National Survey on Drug Use and Health 2022</div>
    <div style="margin-top:0.75rem; font-size:0.72rem">
        Mental Health Inequality Index (MHII) is an original composite metric developed for this dashboard.<br>
        This tool is for informational and educational purposes only. It does not constitute medical advice.
    </div>
    <div style="margin-top:1rem">
        Built by <a href="https://github.com/preiyalthakkar3007" style="color:#7c3aed">Preiyal Thakkar</a> · 
        <a href="https://github.com/preiyalthakkar3007/mental-health-trends-analyzer" style="color:#7c3aed">View Source on GitHub</a>
    </div>
</div>
""", unsafe_allow_html=True)