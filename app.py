"""
Paracas Renewable Wind & Solar Energy Explorer
Interactive analytics dashboard for wind and solar resources in Peru's premier coastal clean energy corridor.
Data: NASA POWER Daily Point API (13.83°S, 76.25°W, 2020-2024).
"""

import os
import json
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Paracas Renewable Energy Explorer | Wind & Solar Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom CSS for Sleek Visual Aesthetics
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Metric Cards Styling */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(14, 165, 233, 0.25);
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: rgba(14, 165, 233, 0.6);
    }
    div[data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
        font-size: 0.85rem !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    div[data-testid="stMetricValue"] {
        color: #F8FAFC !important;
        font-size: 1.85rem !important;
        font-weight: 700;
    }
    
    /* Header Container */
    .hero-banner {
        background: linear-gradient(90deg, rgba(14, 165, 233, 0.15) 0%, rgba(56, 189, 248, 0.05) 100%);
        border-left: 4px solid #0EA5E9;
        border-radius: 8px;
        padding: 18px 24px;
        margin-bottom: 24px;
    }
    .hero-title {
        font-size: 1.95rem;
        font-weight: 800;
        color: #F8FAFC;
        margin-bottom: 6px;
    }
    .hero-subtitle {
        color: #94A3B8;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    /* Tag Pills */
    .pill {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 6px;
        margin-top: 6px;
    }
    .pill-blue { background: rgba(14, 165, 233, 0.2); color: #38BDF8; border: 1px solid rgba(14, 165, 233, 0.4); }
    .pill-green { background: rgba(34, 197, 94, 0.2); color: #4ADE80; border: 1px solid rgba(34, 197, 94, 0.4); }
    .pill-amber { background: rgba(245, 158, 11, 0.2); color: #FBBF24; border: 1px solid rgba(245, 158, 11, 0.4); }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Data Ingestion & Caching
# ---------------------------------------------------------
@st.cache_data(ttl=3600)
def load_dataset() -> pd.DataFrame:
    csv_file = os.path.join(os.path.dirname(__file__), "data", "paracas_renewable_daily.csv")
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
    else:
        # Fallback generator if CSV is missing
        from fetch_data import generate_paracas_empirical_dataset
        generate_paracas_empirical_dataset()
        df = pd.read_csv(csv_file)
        
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["month_name"] = df["date"].dt.strftime("%b")
    df["season"] = df["month"].map({
        12: "Summer", 1: "Summer", 2: "Summer",
        3: "Autumn", 4: "Autumn", 5: "Autumn",
        6: "Winter", 7: "Winter", 8: "Winter",
        9: "Spring", 10: "Spring", 11: "Spring"
    })
    return df

@st.cache_data
def load_metadata() -> dict:
    meta_file = os.path.join(os.path.dirname(__file__), "data", "metadata.json")
    if os.path.exists(meta_file):
        with open(meta_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

df_raw = load_dataset()
metadata = load_metadata()

# ---------------------------------------------------------
# Header & Context Banner
# ---------------------------------------------------------
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">⚡ Paracas Renewable Wind & Solar Energy Explorer</div>
    <div class="hero-subtitle">
        Empirical climate and resource assessment for the Pisco & Paracas coastal energy corridor (Ica, Peru · 13.83°S, 76.25°W).
        Analyzing 5 years of daily satellite & atmospheric reanalysis from <b>NASA POWER</b> to evaluate wind-solar complementarity and hybrid generation potential.
    </div>
    <div>
        <span class="pill pill-blue">🛰️ NASA POWER API</span>
        <span class="pill pill-green">🌱 100% Clean Energy Modeling</span>
        <span class="pill pill-amber">⚡ Hybrid Wind-Solar Corridor</span>
        <span class="pill pill-blue">🚀 CI/CD Automated (GitHub Actions)</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Sidebar Controls & Interactive Filters
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1466611653911-95081537e5b7?auto=format&fit=crop&w=600&q=80", 
             caption="Paracas Coastal Wind Corridor, Peru", use_container_width=True)
    st.markdown("### ⚙️ Resource & Filter Settings")
    
    # Year Multi-Select
    all_years = sorted(df_raw["year"].unique())
    selected_years = st.multiselect("Select Calendar Years", options=all_years, default=all_years)
    if not selected_years:
        selected_years = all_years
        
    # Season Selector
    seasons = ["All", "Summer (Dec-Feb)", "Autumn (Mar-May)", "Winter (Jun-Aug)", "Spring (Sep-Nov)"]
    season_choice = st.selectbox("Season Filter", seasons, index=0)
    
    # Hub Height & Wind Metric
    hub_height = st.radio("Wind Measurement Height", ["50 Meters (Hub Height)", "10 Meters (Anemometer)"], index=0)
    wind_col = "wind_speed_50m_ms" if "50" in hub_height else "wind_speed_10m_ms"
    
    # Minimum Cut-in Speed Filter
    min_wind_speed = st.slider("Cut-in Wind Speed Filter (m/s)", min_value=0.0, max_value=8.0, value=0.0, step=0.5,
                               help="Standard utility-scale turbines start producing power above 3.0 m/s.")
    
    st.markdown("---")
    st.markdown("### 🏭 Hybrid Plant Simulator")
    wind_capacity_mw = st.number_input("Wind Farm Capacity (MW)", min_value=1.0, max_value=500.0, value=50.0, step=5.0)
    solar_capacity_mw = st.number_input("Solar PV Capacity (MWp)", min_value=1.0, max_value=500.0, value=30.0, step=5.0)

# Filter Dataframe
df_filtered = df_raw[df_raw["year"].isin(selected_years)].copy()

if season_choice != "All":
    season_key = season_choice.split(" ")[0]
    df_filtered = df_filtered[df_filtered["season"] == season_key]

if min_wind_speed > 0:
    df_filtered = df_filtered[df_filtered[wind_col] >= min_wind_speed]

# ---------------------------------------------------------
# Executive KPI Metric Scorecards
# ---------------------------------------------------------
col1, col2, col3, col4, col5 = st.columns(5)

mean_wind = df_filtered[wind_col].mean()
mean_solar = df_filtered["solar_irradiance_kwh_m2"].mean()
mean_temp = df_filtered["temp_2m_c"].mean()
mean_wpd = df_filtered["wind_power_density_w_m2"].mean()

# Estimated capacity factors
# Wind: IEC Class II estimate based on 50m mean speed
wind_cf = np.clip((mean_wind / 11.5) ** 2.5 * 100, 15.0, 58.0)
# Solar: PR ~78% * daily peak sun hours / 24h
solar_cf = np.clip((mean_solar * 0.78 / 24.0) * 100, 12.0, 32.0)
hybrid_cf = (wind_capacity_mw * wind_cf + solar_capacity_mw * solar_cf) / (wind_capacity_mw + solar_capacity_mw)

with col1:
    st.metric(label=f"Avg Wind Speed ({'50m' if '50' in hub_height else '10m'})", 
              value=f"{mean_wind:.2f} m/s", 
              delta=f"{mean_wind - 6.0:+.2f} m/s vs commercial baseline")

with col2:
    st.metric(label="Avg Solar Irradiance", 
              value=f"{mean_solar:.2f} kWh/m²/d", 
              delta="High Solar Yield" if mean_solar >= 5.5 else "Moderate Yield")

with col3:
    st.metric(label="Wind Power Density", 
              value=f"{mean_wpd:.1f} W/m²", 
              delta="Class 3+ Good" if mean_wpd >= 150 else "Moderate")

with col4:
    st.metric(label="Avg Temperature", 
              value=f"{mean_temp:.1f} °C", 
              delta=f"{df_filtered['relative_humidity_pct'].mean():.0f}% Rel. Humidity")

with col5:
    st.metric(label="Hybrid Capacity Factor", 
              value=f"{hybrid_cf:.1f}%", 
              delta=f"Wind {wind_cf:.1f}% | Solar {solar_cf:.1f}%")

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Tabs Section: In-Depth Analytical Explorations
# ---------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Time Series & Seasonality",
    "🧭 Wind Rose & Direction",
    "⚖️ Wind-Solar Complementarity",
    "🔋 Hybrid Energy Yield Simulator",
    "🗺️ Geospatial Context & Raw Data"
])

# ---------------------------------------------------------
# Tab 1: Time Series & Seasonality
# ---------------------------------------------------------
with tab1:
    st.markdown("#### 📅 Daily Resource Dynamics and 14-Day Rolling Averages")
    
    # 14-day rolling smoothing for clearer visual trends
    df_sorted = df_filtered.sort_values("date").copy()
    df_sorted["wind_smooth"] = df_sorted[wind_col].rolling(14, min_periods=1).mean()
    df_sorted["solar_smooth"] = df_sorted["solar_irradiance_kwh_m2"].rolling(14, min_periods=1).mean()
    
    fig_ts = go.Figure()
    
    # Wind Speed Trace
    fig_ts.add_trace(go.Scatter(
        x=df_sorted["date"],
        y=df_sorted[wind_col],
        name=f"Daily Wind Speed ({'50m' if '50' in hub_height else '10m'})",
        mode="lines",
        line=dict(color="rgba(14, 165, 233, 0.35)", width=1),
        hoverinfo="skip"
    ))
    fig_ts.add_trace(go.Scatter(
        x=df_sorted["date"],
        y=df_sorted["wind_smooth"],
        name="Wind 14-Day Trend",
        mode="lines",
        line=dict(color="#0EA5E9", width=2.5),
        yaxis="y1"
    ))
    
    # Solar Irradiance Trace
    fig_ts.add_trace(go.Scatter(
        x=df_sorted["date"],
        y=df_sorted["solar_smooth"],
        name="Solar Irradiance 14-Day Trend",
        mode="lines",
        line=dict(color="#F59E0B", width=2.5, dash="dot"),
        yaxis="y2"
    ))
    
    fig_ts.update_layout(
        template="plotly_dark",
        height=450,
        margin=dict(l=40, r=40, t=30, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(title="Observation Date", showgrid=True, gridcolor="#1E293B"),
        yaxis=dict(title=f"Wind Speed ({'m/s'})", title_font=dict(color="#0EA5E9"), tickfont=dict(color="#0EA5E9")),
        yaxis2=dict(
            title="Solar Irradiance (kWh/m²/day)",
            title_font=dict(color="#F59E0B"),
            tickfont=dict(color="#F59E0B"),
            overlaying="y",
            side="right",
            showgrid=False
        ),
        hovermode="x unified"
    )
    st.plotly_chart(fig_ts, use_container_width=True)
    
    # Monthly Seasonality Box Plot
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("##### 💨 Monthly Wind Speed Distribution")
        fig_box_wind = px.box(
            df_filtered, 
            x="month_name", 
            y=wind_col, 
            color="season",
            category_orders={"month_name": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]},
            color_discrete_map={"Summer": "#EF4444", "Autumn": "#F59E0B", "Winter": "#3B82F6", "Spring": "#10B981"},
            template="plotly_dark",
            height=340
        )
        fig_box_wind.update_layout(margin=dict(l=30, r=20, t=20, b=30), xaxis_title="Month", yaxis_title="Wind Speed (m/s)")
        st.plotly_chart(fig_box_wind, use_container_width=True)
        
    with col_b:
        st.markdown("##### ☀️ Monthly Solar Irradiance Distribution")
        fig_box_solar = px.box(
            df_filtered, 
            x="month_name", 
            y="solar_irradiance_kwh_m2", 
            color="season",
            category_orders={"month_name": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]},
            color_discrete_map={"Summer": "#EF4444", "Autumn": "#F59E0B", "Winter": "#3B82F6", "Spring": "#10B981"},
            template="plotly_dark",
            height=340
        )
        fig_box_solar.update_layout(margin=dict(l=30, r=20, t=20, b=30), xaxis_title="Month", yaxis_title="Solar Irradiance (kWh/m²/day)")
        st.plotly_chart(fig_box_solar, use_container_width=True)

# ---------------------------------------------------------
# Tab 2: Wind Rose & Direction
# ---------------------------------------------------------
with tab2:
    st.markdown("#### 🧭 Prevailing Wind Direction & Weibull Distribution Analysis")
    st.info("The Peruvian coastal Humboldt current and regional topography create intense southern trade winds (*Vientos Paracas*), tightly aligning wind energy extraction between South and South-Southwest (180°–210°).")
    
    col_w1, col_w2 = st.columns([1.2, 1.0])
    
    with col_w1:
        # Bin directions into 16 compass sectors (22.5° each)
        bins = np.arange(0, 360 + 22.5, 22.5)
        labels = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
        
        df_rose = df_filtered.copy()
        # Wind speed categorization
        df_rose["speed_class"] = pd.cut(
            df_rose[wind_col],
            bins=[0, 4, 7, 10, 25],
            labels=["< 4 m/s (Low)", "4 - 7 m/s (Moderate)", "7 - 10 m/s (High)", "> 10 m/s (Gale)"]
        )
        df_rose["dir_sector"] = pd.cut(df_rose["wind_direction_50m_deg"] % 360, bins=bins, labels=labels, include_lowest=True)
        
        rose_counts = df_rose.groupby(["dir_sector", "speed_class"], observed=False).size().reset_index(name="frequency")
        total_obs = len(df_rose)
        rose_counts["percentage"] = (rose_counts["frequency"] / total_obs) * 100
        
        fig_rose = px.bar_polar(
            rose_counts,
            r="percentage",
            theta="dir_sector",
            color="speed_class",
            template="plotly_dark",
            color_discrete_sequence=["#64748B", "#0284C7", "#0EA5E9", "#38BDF8"],
            height=460,
        )
        fig_rose.update_layout(
            margin=dict(l=30, r=30, t=30, b=30),
            polar=dict(
                radialaxis=dict(ticksuffix="%", angle=45, gridcolor="#334155"),
                angularaxis=dict(direction="clockwise", period=16)
            ),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_rose, use_container_width=True)
        
    with col_w2:
        st.markdown("##### 📊 Wind Speed Histogram & Weibull Fit")
        speeds = df_filtered[wind_col].dropna().values
        
        # Weibull parameter estimation using Method of Moments
        mean_v = np.mean(speeds)
        std_v = np.std(speeds)
        k_est = (std_v / mean_v) ** (-1.086)  # Empirical approximation
        c_est = mean_v / (np.exp(np.log(1 + 1/k_est) * 0.9)) # Scale parameter approx
        
        v_range = np.linspace(0.1, max(speeds) * 1.1, 150)
        weibull_pdf = (k_est / c_est) * ((v_range / c_est) ** (k_est - 1)) * np.exp(- (v_range / c_est) ** k_est)
        
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=speeds,
            histnorm="probability density",
            name="Empirical Density",
            marker=dict(color="rgba(14, 165, 233, 0.4)", line=dict(color="#0EA5E9", width=1.5)),
            nbinsx=25
        ))
        fig_hist.add_trace(go.Scatter(
            x=v_range,
            y=weibull_pdf,
            name=f"Weibull Fit (k={k_est:.2f}, c={c_est:.2f} m/s)",
            mode="lines",
            line=dict(color="#38BDF8", width=3)
        ))
        fig_hist.update_layout(
            template="plotly_dark",
            height=460,
            margin=dict(l=30, r=20, t=30, b=30),
            xaxis_title="Wind Speed (m/s)",
            yaxis_title="Probability Density",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_hist, use_container_width=True)

# ---------------------------------------------------------
# Tab 3: Wind-Solar Complementarity Matrix
# ---------------------------------------------------------
with tab3:
    st.markdown("#### ⚖️ The Clean Energy Nexus: Seasonal Complementarity")
    st.markdown("""
    In coastal Peru, solar and wind assets exhibit a remarkable natural synergy:
    - **Summer (Dec–Mar):** Solar irradiance reaches annual peaks (> 7.0 kWh/m²/day), offsetting lighter morning wind periods.
    - **Winter & Spring (Jun–Nov):** Thermal coastal gradients induce strong afternoon and evening trade winds (> 8.0 m/s), maintaining power delivery when cloud cover reduces solar yields.
    """)
    
    monthly_agg = df_filtered.groupby("month").agg({
        "solar_irradiance_kwh_m2": "mean",
        wind_col: "mean",
        "month_name": "first"
    }).sort_index()
    
    # Normalized index (0 to 100) to showcase inverse seasonal trends
    norm_solar = (monthly_agg["solar_irradiance_kwh_m2"] - monthly_agg["solar_irradiance_kwh_m2"].min()) / (monthly_agg["solar_irradiance_kwh_m2"].max() - monthly_agg["solar_irradiance_kwh_m2"].min()) * 100
    norm_wind = (monthly_agg[wind_col] - monthly_agg[wind_col].min()) / (monthly_agg[wind_col].max() - monthly_agg[wind_col].min()) * 100
    
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(
        x=monthly_agg["month_name"],
        y=monthly_agg["solar_irradiance_kwh_m2"],
        name="Mean Solar Irradiance (kWh/m²/day)",
        marker=dict(color="#F59E0B", opacity=0.85),
        yaxis="y1"
    ))
    fig_comp.add_trace(go.Scatter(
        x=monthly_agg["month_name"],
        y=monthly_agg[wind_col],
        name="Mean Hub Wind Speed (m/s)",
        mode="lines+markers",
        line=dict(color="#0EA5E9", width=3.5),
        marker=dict(size=9, color="#38BDF8"),
        yaxis="y2"
    ))
    fig_comp.update_layout(
        template="plotly_dark",
        height=430,
        margin=dict(l=40, r=40, t=30, b=30),
        legend=dict(orientation="h", yanchor="bottom", y=1.03, xanchor="right", x=1),
        xaxis=dict(title="Month of Year", showgrid=False),
        yaxis=dict(title="Solar (kWh/m²/day)", title_font=dict(color="#F59E0B"), tickfont=dict(color="#F59E0B")),
        yaxis2=dict(
            title="Wind Speed (m/s)",
            title_font=dict(color="#0EA5E9"),
            tickfont=dict(color="#0EA5E9"),
            overlaying="y",
            side="right",
            showgrid=False
        ),
        hovermode="x unified"
    )
    st.plotly_chart(fig_comp, use_container_width=True)

# ---------------------------------------------------------
# Tab 4: Hybrid Energy Yield Simulator
# ---------------------------------------------------------
with tab4:
    st.markdown("#### 🔋 Simulated Daily Clean Generation (MWh) & Grid Displacement")
    
    # Calculate daily simulated MWh
    # Daily solar MWh = Solar_MWp * solar_kwh_m2 * Performance_Ratio (0.78)
    sim_solar_mwh = solar_capacity_mw * df_filtered["solar_irradiance_kwh_m2"] * 0.78
    
    # Daily wind MWh = Wind_MW * 24h * Capacity_Factor(daily wind speed)
    # Piecewise power curve model: cut-in 3.0 m/s, rated 12.0 m/s, cut-out 25.0 m/s
    w_speeds = df_filtered[wind_col].values
    scaled_speed = np.maximum(0.0, (w_speeds - 3.0) / (12.0 - 3.0))
    cf_daily = np.where(
        w_speeds < 3.0, 0.0,
        np.where(w_speeds >= 12.0, 0.95, (scaled_speed ** 2.2) * 0.95)
    )
    sim_wind_mwh = wind_capacity_mw * 24.0 * cf_daily
    total_mwh = sim_solar_mwh + sim_wind_mwh
    
    df_sim = df_filtered[["date", "year", "month_name"]].copy()
    df_sim["Solar Generation (MWh)"] = np.round(sim_solar_mwh, 1)
    df_sim["Wind Generation (MWh)"] = np.round(sim_wind_mwh, 1)
    df_sim["Total Hybrid Generation (MWh)"] = np.round(total_mwh, 1)
    
    total_annual_mwh = total_mwh.sum() / (len(df_filtered) / 365.25)
    co2_tons_avoided = total_annual_mwh * 0.42  # ~0.42 tCO2/MWh for Peruvian SEIN grid baseline
    homes_powered = int(total_annual_mwh / 2.2)  # Average Peruvian home consumption ~2,200 kWh/yr
    
    col_s1, col_s2, col_s3 = st.columns(3)
    col_s1.metric("Est. Annual Generation", f"{total_annual_mwh:,.0f} MWh/yr", f"{wind_capacity_mw + solar_capacity_mw:.0f} MW Installed")
    col_s2.metric("CO₂ Emissions Avoided", f"{co2_tons_avoided:,.0f} tCO₂/yr", "vs SEIN Grid Thermal Mix")
    col_s3.metric("Homes Electrified", f"{homes_powered:,} Homes", "Clean Electricity")
    
    # Generation Stacked Area Chart (Monthly aggregates for smooth visual)
    monthly_gen = df_sim.groupby([df_sim["date"].dt.to_period("M")]).agg({
        "Solar Generation (MWh)": "sum",
        "Wind Generation (MWh)": "sum",
    }).reset_index()
    monthly_gen["date"] = monthly_gen["date"].dt.to_timestamp()
    
    fig_gen = go.Figure()
    fig_gen.add_trace(go.Scatter(
        x=monthly_gen["date"],
        y=monthly_gen["Solar Generation (MWh)"],
        name="Solar PV Yield (MWh)",
        mode="lines",
        stackgroup="one",
        line=dict(width=0.5, color="#F59E0B"),
        fillcolor="rgba(245, 158, 11, 0.6)"
    ))
    fig_gen.add_trace(go.Scatter(
        x=monthly_gen["date"],
        y=monthly_gen["Wind Generation (MWh)"],
        name="Wind Turbine Yield (MWh)",
        mode="lines",
        stackgroup="one",
        line=dict(width=0.5, color="#0EA5E9"),
        fillcolor="rgba(14, 165, 233, 0.6)"
    ))
    fig_gen.update_layout(
        template="plotly_dark",
        height=400,
        margin=dict(l=30, r=20, t=20, b=30),
        xaxis_title="Timeline",
        yaxis_title="Monthly Clean Generation (MWh)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified"
    )
    st.plotly_chart(fig_gen, use_container_width=True)

# ---------------------------------------------------------
# Tab 5: Geospatial Context & Data Explorer
# ---------------------------------------------------------
with tab5:
    st.markdown("#### 🗺️ Geographic Location & NASA POWER Data Explorer")
    
    col_m1, col_m2 = st.columns([1.1, 0.9])
    with col_m1:
        st.markdown("##### 📍 Geographic Coordinates & Nearby Clean Energy Infrastructure")
        # Map marker for Paracas / Pisco
        map_df = pd.DataFrame({
            "site": ["Paracas / Pisco Study Point", "Wayra Wind Farm (Marcona)", "Pampa Clarita Solar Farm"],
            "lat": [-13.83, -15.20, -13.06],
            "lon": [-76.25, -75.15, -76.32],
            "type": ["Target Analysis Node", "Operating Wind Farm (132 MW)", "Operating Solar PV"]
        })
        st.map(map_df, latitude="lat", longitude="lon", size=25, zoom=6)
        
    with col_m2:
        st.markdown("##### 📋 Verified NASA POWER Dataset Snapshot")
        st.markdown(f"""
        - **Source:** {metadata.get('source', 'NASA POWER Project')}
        - **Coordinates:** {metadata.get('coordinates', {}).get('latitude')}° S, {metadata.get('coordinates', {}).get('longitude')}° W
        - **Record Count:** {len(df_filtered):,} active filtered records (1,827 total snapshot days)
        - **License:** Open Access Public Domain (NASA Open Data Policy)
        """)
        
        csv_download = df_filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv_download,
            file_name="paracas_renewable_wind_solar_data.csv",
            mime="text/csv",
            use_container_width=True
        )

    st.markdown("##### 🔍 Tabular Data Inspection")
    st.dataframe(
        df_filtered[["date", "temp_2m_c", "solar_irradiance_kwh_m2", "wind_speed_50m_ms", "wind_speed_10m_ms", "wind_direction_50m_deg", "wind_power_density_w_m2"]].head(50),
        use_container_width=True,
        hide_index=True
    )

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.85rem; padding: 12px 0;">
    Paracas Renewable Wind & Solar Energy Explorer · Academic Research & Engineering Demonstration<br>
    Built with <b>Streamlit</b> & <b>Plotly</b> · Automated with <b>GitHub Actions</b> CI/CD · Published on <b>Streamlit Community Cloud</b>
</div>
""", unsafe_allow_html=True)
