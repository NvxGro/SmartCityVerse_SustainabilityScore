import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(
    page_title="Smart City Sustainability Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    background-color: #111111 !important;
    color: #e0e0e0 !important;
}

.main, .block-container {
    background-color: #111111 !important;
}

.block-container {
    padding: 1.5rem 2rem 2rem 2rem;
    max-width: 1400px;
}

/* Header */
.dash-header {
    background: #1a1a1a;
    border-radius: 14px;
    padding: 1.2rem 2rem;
    margin-bottom: 1.2rem;
    border: 1px solid #2a5c3a;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.dash-title    { font-size: 22px; font-weight: 700; color: #a8e6b8; margin: 0; }
.dash-subtitle { font-size: 13px; color: #6b9b78; margin: 2px 0 0; }
.live-badge {
    background: #1a2e1f; color: #6fcf8a;
    font-size: 12px; font-weight: 500;
    padding: 5px 14px; border-radius: 20px;
    border: 1px solid #2a5c3a;
}

/* Cards — universal */
.kpi-card, .chart-card, .score-card, .filter-bar, .insights-wrap {
    background: #1a1a1a;
    border-radius: 14px;
    border: 1px solid #2a5c3a;
    padding: 1.2rem 1.3rem;
}
.score-card { text-align: center; padding: 1.5rem; }

/* KPI */
.kpi-icon-wrap {
    width: 36px; height: 36px; border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; margin-bottom: 0.7rem;
    background: #1f2e22;
}
.kpi-val  { font-size: 28px; font-weight: 700; color: #a8e6b8; line-height: 1.1; }
.kpi-name { font-size: 11px; color: #6b9b78; margin-top: 3px; font-weight: 500;
            text-transform: uppercase; letter-spacing: 0.05em; }
.kpi-sub  { font-size: 12px; color: #557a61; margin-top: 2px; }
.trend-up   { color: #66bb6a; font-size: 12px; font-weight: 600; }
.trend-down { color: #ef5350; font-size: 12px; font-weight: 600; }

/* Score status pills */
.score-label {
    font-size: 11px; font-weight: 600; color: #6b9b78;
    letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.5rem;
}
.score-status {
    display: inline-block; font-size: 13px; font-weight: 500;
    padding: 5px 18px; border-radius: 20px; margin-top: 0.5rem;
}
.score-status-good     { background:#1a2e1f; color:#66bb6a; border:1px solid #2a5c3a; }
.score-status-moderate { background:#2a2010; color:#ffb74d; border:1px solid #5c4a1a; }
.score-status-poor     { background:#2a1010; color:#ef5350; border:1px solid #5c2a2a; }

/* Section labels */
.section-label {
    font-size: 11px; font-weight: 600; color: #557a61;
    letter-spacing: 0.08em; text-transform: uppercase;
    margin: 1.2rem 0 0.6rem;
}

/* Insights */
.insight-card {
    background: #1f1f1f;
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    border-left: 4px solid #4caf50;
    margin-bottom: 0.5rem;
}
.insight-card.blue  { border-left-color: #42a5f5; }
.insight-card.amber { border-left-color: #ffa726; }
.insight-card.teal  { border-left-color: #26c6a6; }
.insight-lbl  { font-size: 10px; font-weight: 600; color: #6b9b78;
                text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 2px; }
.insight-val  { font-size: 18px; font-weight: 700; color: #a8e6b8; }
.insight-desc { font-size: 11px; color: #557a61; margin-top: 2px; }

/* Filter bar */
.filter-bar { margin-bottom: 1.2rem; }

/* Streamlit widget overrides */
div[data-testid="stSelectbox"] label,
div[data-testid="stDateInput"] label {
    color: #6b9b78 !important; font-size: 12px !important;
}
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stDateInput"] > div > div {
    background-color: #222 !important;
    border: 1px solid #2a5c3a !important;
    border-radius: 8px !important;
    color: #e0e0e0 !important;
}
div[data-testid="stExpander"] {
    background: #1a1a1a !important;
    border: 1px solid #2a5c3a !important;
    border-radius: 14px !important;
}

#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    df = pd.read_csv("data/smart_city_sustainability.csv", parse_dates=["Date"])
    return df

df = load_data()

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="dash-header">
  <div>
    <p class="dash-title">Smart City Sustainability Dashboard</p>
    <p class="dash-subtitle">Urban Analytics & Sustainability Insights — India 2023</p>
  </div>
  <span class="live-badge">Dataset: 2023 · 5 Cities · 1,825 Records</span>
</div>
""", unsafe_allow_html=True)

# ── FILTERS ───────────────────────────────────────────────────────────────────
st.markdown('<div class="filter-bar">', unsafe_allow_html=True)
col_f1, col_f2, col_f3 = st.columns([2, 2, 3])
with col_f1:
    cities = ["All Cities"] + sorted(df["City"].unique().tolist())
    selected_city = st.selectbox("Select City", cities)
with col_f2:
    months = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
              7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
    month_options = ["All Months"] + [months[m] for m in sorted(df["Date"].dt.month.unique())]
    selected_month = st.selectbox("Select Month", month_options)
with col_f3:
    date_range = st.date_input(
        "Date Range",
        value=(df["Date"].min().date(), df["Date"].max().date()),
        min_value=df["Date"].min().date(),
        max_value=df["Date"].max().date(),
    )
st.markdown('</div>', unsafe_allow_html=True)

# ── APPLY FILTERS ─────────────────────────────────────────────────────────────
filtered = df.copy()
if selected_city != "All Cities":
    filtered = filtered[filtered["City"] == selected_city]
if selected_month != "All Months":
    month_num = {v: k for k, v in months.items()}[selected_month]
    filtered = filtered[filtered["Date"].dt.month == month_num]
if len(date_range) == 2:
    filtered = filtered[
        (filtered["Date"].dt.date >= date_range[0]) &
        (filtered["Date"].dt.date <= date_range[1])
    ]
if filtered.empty:
    st.warning("No data for the selected filters.")
    st.stop()

# ── KPIs ──────────────────────────────────────────────────────────────────────
avg_sus     = round(filtered["Sustainability_Score"].mean(), 1)
avg_aqi     = round(filtered["AQI"].mean(), 1)
avg_traffic = round(filtered["Traffic_Congestion_Pct"].mean(), 1)
avg_energy  = round(filtered["Energy_Consumption_MWh"].mean(), 1)
avg_recycle = round(filtered["Waste_Recycled_Pct"].mean(), 1)

def sus_label(s):
    if s >= 60: return "Good", "score-status-good"
    elif s >= 40: return "Moderate", "score-status-moderate"
    else: return "Poor", "score-status-poor"

def aqi_label(a):
    if a <= 50: return "Good"
    elif a <= 100: return "Satisfactory"
    elif a <= 200: return "Moderate"
    elif a <= 300: return "Poor"
    else: return "Very Poor"

sus_text, sus_cls = sus_label(avg_sus)

# ── CHART LAYOUT DEFAULTS ─────────────────────────────────────────────────────
DARK_LAYOUT = dict(
    paper_bgcolor="#1a1a1a",
    plot_bgcolor="#1a1a1a",
    font=dict(family="Poppins", size=11, color="#a0a0a0"),
    margin=dict(t=30, b=30, l=40, r=20),
    height=240,
    legend=dict(
        orientation="h", yanchor="bottom", y=1.02,
        xanchor="right", x=1, font_size=10,
        bgcolor="rgba(0,0,0,0)", font_color="#a0a0a0"
    ),
    xaxis=dict(showgrid=False, linecolor="#2a2a2a", tickcolor="#444", color="#888"),
    yaxis=dict(gridcolor="#222", linecolor="#2a2a2a", tickcolor="#444", color="#888"),
)

COLORS = {
    "Mumbai": "#4caf50", "Delhi": "#ef5350",
    "Bangalore": "#42a5f5", "Chennai": "#ff7043", "Hyderabad": "#ab47bc"
}

# ── SCORE + KPI ROW ───────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Sustainability Overview</p>', unsafe_allow_html=True)
col_s, col_k1, col_k2, col_k3, col_k4 = st.columns([1.4, 1, 1, 1, 1])

with col_s:
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_sus,
        number={"font": {"size": 40, "family": "Poppins", "color": "#a8e6b8"}, "suffix": ""},
        gauge={
            "axis": {"range": [0, 100], "tickfont": {"size": 10, "color": "#555"}, "tickcolor": "#333"},
            "bar": {"color": "#4caf50", "thickness": 0.28},
            "bgcolor": "#1a1a1a",
            "borderwidth": 0,
            "steps": [
                {"range": [0,  40],  "color": "#2a1515"},
                {"range": [40, 60],  "color": "#2a2010"},
                {"range": [60, 100], "color": "#1a2e1f"},
            ],
            "threshold": {
                "line": {"color": "#66bb6a", "width": 3},
                "thickness": 0.8, "value": avg_sus
            }
        }
    ))
    fig_gauge.update_layout(
        height=200, margin=dict(t=20, b=10, l=20, r=20),
        paper_bgcolor="#1a1a1a", plot_bgcolor="#1a1a1a",
        font={"family": "Poppins"},
    )
    st.markdown('<div class="score-card">', unsafe_allow_html=True)
    st.markdown('<p class="score-label">Sustainability Score</p>', unsafe_allow_html=True)
    st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})
    st.markdown(f'<span class="score-status {sus_cls}">{sus_text}</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

kpis = [
    ("", f"{avg_aqi}", "AQI Score",         aqi_label(avg_aqi), "↑" if avg_aqi > 150 else "↓", avg_aqi > 150),
    ("", f"{avg_traffic}%", "Traffic Congestion", "Avg load",    "↑" if avg_traffic > 60 else "↓", avg_traffic > 60),
    ("", f"{avg_energy}", "Energy (MWh)",    "Monthly avg",       "↑" if avg_energy > 500 else "↓", avg_energy > 500),
    ("", f"{avg_recycle}%", "Recycling Rate","Waste recycled",    "↑" if avg_recycle > 55 else "↓", avg_recycle <= 55),
]
for col, (icon, val, name, sub, arrow, is_bad) in zip([col_k1,col_k2,col_k3,col_k4], kpis):
    trend_cls = "trend-down" if is_bad else "trend-up"
    with col:
        st.markdown(f"""
        <div class="kpi-card">
          <div class="kpi-icon-wrap">{icon}</div>
          <div style="display:flex;align-items:baseline;justify-content:space-between">
            <span class="kpi-val">{val}</span>
            <span class="{trend_cls}">{arrow}</span>
          </div>
          <div class="kpi-name">{name}</div>
          <div class="kpi-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

# ── CHARTS ────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Analytics</p>', unsafe_allow_html=True)
col_c1, col_c2 = st.columns(2)

with col_c1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("**AQI Trend — Monthly Average**")
    aqi_monthly = filtered.groupby([filtered["Date"].dt.to_period("M"), "City"])["AQI"].mean().reset_index()
    aqi_monthly["Date"] = aqi_monthly["Date"].astype(str)
    fig1 = px.line(aqi_monthly, x="Date", y="AQI", color="City",
                   color_discrete_map=COLORS, markers=True)
    fig1.update_traces(line_width=2, marker_size=4)
    fig1.update_layout(**DARK_LAYOUT)
    fig1.add_hline(y=100, line_dash="dot", line_color="#444",
                   annotation_text="Safe limit", annotation_font_size=9,
                   annotation_font_color="#666")
    st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with col_c2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("**Traffic Congestion — Monthly %**")
    traffic_monthly = filtered.groupby([filtered["Date"].dt.to_period("M"), "City"])["Traffic_Congestion_Pct"].mean().reset_index()
    traffic_monthly["Date"] = traffic_monthly["Date"].astype(str)
    fig2 = px.bar(traffic_monthly, x="Date", y="Traffic_Congestion_Pct",
                  color="City", barmode="group", color_discrete_map=COLORS)
    fig2.update_layout(**DARK_LAYOUT)
    fig2.update_traces(marker_line_width=0)
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

col_c3, col_c4 = st.columns(2)

with col_c3:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("**Energy Consumption — Monthly MWh**")
    energy_monthly = filtered.groupby([filtered["Date"].dt.to_period("M"), "City"])["Energy_Consumption_MWh"].mean().reset_index()
    energy_monthly["Date"] = energy_monthly["Date"].astype(str)
    fig3 = px.area(energy_monthly, x="Date", y="Energy_Consumption_MWh",
                   color="City", color_discrete_map=COLORS)
    fig3.update_traces(line_width=1.5)
    fig3.update_layout(**DARK_LAYOUT)
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with col_c4:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("**Waste Management — Average Split**")
    recycled  = round(filtered["Waste_Recycled_Pct"].mean(), 1)
    landfill  = round(filtered["Waste_Landfill_Pct"].mean(), 1)
    composted = round(filtered["Waste_Composted_Pct"].mean(), 1)
    fig4 = go.Figure(go.Pie(
        labels=["Recycled", "Landfill", "Composted"],
        values=[recycled, landfill, composted],
        hole=0.62,
        marker_colors=["#4caf50", "#ef5350", "#66bb6a"],
        marker_line=dict(color="#1a1a1a", width=2),
        textinfo="label+percent",
        textfont=dict(size=11, color="#ccc"),
        hovertemplate="%{label}: %{value:.1f}%<extra></extra>",
    ))
    fig4.update_layout(
        paper_bgcolor="#1a1a1a", plot_bgcolor="#1a1a1a",
        font=dict(family="Poppins", size=11, color="#a0a0a0"),
        margin=dict(t=30, b=10, l=10, r=10),
        height=240,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15,
                    font_size=10, bgcolor="rgba(0,0,0,0)", font_color="#a0a0a0"),
        showlegend=True,
    )
    st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ── INSIGHTS ──────────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Key Insights</p>', unsafe_allow_html=True)

worst_city_aqi    = filtered.groupby("City")["AQI"].mean().idxmax()
worst_aqi_val     = round(filtered.groupby("City")["AQI"].mean().max(), 1)
best_recycle_city = filtered.groupby("City")["Waste_Recycled_Pct"].mean().idxmax()
best_recycle_val  = round(filtered.groupby("City")["Waste_Recycled_Pct"].mean().max(), 1)
peak_energy_city  = filtered.groupby("City")["Energy_Consumption_MWh"].mean().idxmax()
peak_energy_val   = round(filtered.groupby("City")["Energy_Consumption_MWh"].mean().max(), 1)
best_sus_city     = filtered.groupby("City")["Sustainability_Score"].mean().idxmax()
best_sus_val      = round(filtered.groupby("City")["Sustainability_Score"].mean().max(), 1)

col_i1, col_i2, col_i3, col_i4 = st.columns(4)
insights = [
    (col_i1, "",      "Highest Pollution",  worst_city_aqi,    f"Avg AQI: {worst_aqi_val}"),
    (col_i2, "blue",  "Best Recycling",     best_recycle_city, f"Recycles {best_recycle_val}% of waste"),
    (col_i3, "amber", "Peak Energy Use",    peak_energy_city,  f"Avg {peak_energy_val} MWh/month"),
    (col_i4, "teal",  "Top Sustainability", best_sus_city,     f"Score: {best_sus_val}/100"),
]
for col, cls, lbl, val, desc in insights:
    with col:
        st.markdown(f"""
        <div class="insight-card {cls}">
          <div class="insight-lbl">{lbl}</div>
          <div class="insight-val">{val}</div>
          <div class="insight-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# ── RAW DATA ──────────────────────────────────────────────────────────────────
with st.expander("View Raw Data"):
    display_df = filtered.copy()
    display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")
    st.dataframe(
        display_df.sort_values("Date", ascending=False).reset_index(drop=True),
        use_container_width=True, height=300,
    )
    st.download_button(
        label="Download Filtered Data as CSV",
        data=display_df.to_csv(index=False).encode("utf-8"),
        file_name="smart_city_filtered.csv",
        mime="text/csv",
    )

st.markdown("""
<div style="text-align:center;padding:1.5rem 0 0.5rem;color:#333;font-size:12px;">
  Smart City Sustainability Dashboard · Urban Analytics Project · 2024
</div>
""", unsafe_allow_html=True)
