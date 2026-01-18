import json
import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


def apply_4k_plotly_theme(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#EAF0FF", size=13),
        title=dict(font=dict(size=18, color="#FFFFFF")),
        margin=dict(l=10, r=10, t=60, b=10),
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        showline=False,
        tickfont=dict(color="rgba(234,240,255,0.75)")
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.06)",
        zeroline=False,
        tickfont=dict(color="rgba(234,240,255,0.75)")
    )

    return fig



# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="UIDAI Migration & Urbanization Tracker",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)
#---------------------
# Custom CSS Theme
#----------------------------
st.markdown("""
<style>

/* -----------------------------
   4K DARK + SOFT NEON THEME
----------------------------- */

.stApp{
    background:
        radial-gradient(circle at 12% 18%, rgba(0,245,255,0.10), transparent 40%),
        radial-gradient(circle at 88% 82%, rgba(124,255,0,0.08), transparent 45%),
        radial-gradient(circle at 50% 50%, rgba(255,255,255,0.03), transparent 55%),
        #060A12;
    color: #EAF0FF;
}

/* Main container spacing */
.block-container{
    padding-top: 1rem;
    padding-bottom: 2rem;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background: rgba(10, 14, 26, 0.92);
    border-right: 1px solid rgba(0,245,255,0.10);
    box-shadow: 0px 0px 28px rgba(0,0,0,0.65);
}


/* Sidebar slide-in animation */
section[data-testid="stSidebar"] {
    animation: sidebarSlide 0.6s ease-in-out;
}

@keyframes sidebarSlide {
    from {
        transform: translateX(-25px);
        opacity: 0;
    }
    to {
        transform: translateX(0px);
        opacity: 1;
    }
}

/* Sidebar button hover animation */
.stButton > button {
    transition: all 0.25s ease-in-out !important;
}

/* Hover glow + lift */
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0px 0px 18px rgba(0,245,255,0.18);
    border: 1px solid rgba(0,245,255,0.35);
}

/* Click animation */
.stButton > button:active {
    transform: scale(0.98);
    box-shadow: 0px 0px 10px rgba(124,255,0,0.18);
}

/* Smooth sidebar expanders */
div[data-testid="stExpander"] {
    transition: all 0.3s ease-in-out;
}


           

/* Sidebar headings */
section[data-testid="stSidebar"] h2{
    font-size: 18px !important;
    margin-bottom: 10px !important;
    color: rgba(234,240,255,0.95) !important;
    letter-spacing: 0.3px;
}

/* Sidebar labels */
section[data-testid="stSidebar"] label{
    font-size: 13.5px !important;
    color: rgba(234,240,255,0.78) !important;
}

/* Metrics cards (premium glass) */
div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 14px 14px;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    box-shadow: 0px 8px 30px rgba(0,0,0,0.35);
}
div[data-testid="stMetric"] * {
    color: #EAF0FF !important;
}
.glass-card{
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(0,245,255,0.12);
    border-radius: 22px;

    padding: 18px 18px;   /* ✅ this is the main improvement */
    margin-top: 14px;
    margin-bottom: 14px;

    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);

    box-shadow: 0px 10px 35px rgba(0,0,0,0.55),
                0px 0px 18px rgba(0,245,255,0.06);
}



/* Button styling (matte + subtle neon glow) */
.stButton > button{
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(0,245,255,0.16);
    border-radius: 14px;
    color: rgba(234,240,255,0.92);
    padding: 0.55rem 1rem;
    transition: 0.2s ease-in-out;
    box-shadow: 0px 0px 14px rgba(0,245,255,0.05);
}

.stButton > button:hover{
    border: 1px solid rgba(0,245,255,0.30);
    box-shadow:
        0px 0px 20px rgba(0,245,255,0.10),
        0px 0px 28px rgba(124,255,0,0.06);
    transform: translateY(-1px);
}

/* Divider line */
hr{
    border: none !important;
    height: 1px !important;
    background: linear-gradient(
        90deg,
        rgba(0,245,255,0.00),
        rgba(0,245,255,0.20),
        rgba(124,255,0,0.10),
        rgba(0,245,255,0.00)
    ) !important;
    margin: 18px 0px !important;
}

/* Remove white background from plotly charts */
.js-plotly-plot .plotly, .js-plotly-plot .plotly div{
    background: rgba(0,0,0,0) !important;
}

/* Streamlit default header/footer hide (clean look) */
header{visibility:hidden;}
footer{visibility:hidden;}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# Load Data (PATH FIXED)
# -----------------------------


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_data
def load_state_month():
    path = os.path.join(BASE_DIR, "..", "data", "dashboard_state_month.csv")
    df = pd.read_csv(path)
    df["month"] = pd.to_datetime(df["month"], errors="coerce")
    return df

@st.cache_data
def load_district_month():
    path = os.path.join(BASE_DIR, "..", "data", "dashboard_district_month.csv")
    df = pd.read_csv(path)
    df["month"] = pd.to_datetime(df["month"], errors="coerce")
    return df

@st.cache_data
def load_geojson():
    path = os.path.join(BASE_DIR, "india_states.geojson")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


state_df = load_state_month()
dist_df = load_district_month()
india_geo = load_geojson()

# -----------------------------
# Logo Setup (MUST be before header)
# -----------------------------
import base64

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_path = os.path.join(BASE_DIR, "..", "assets", "aadhaar_transparent.png")
logo_base64 = get_base64(logo_path)

# -----------------------------
# Sidebar Navigation (FINAL)
# -----------------------------
chosen_state = None
chosen_district = None


# -----------------------------
# Navigation (Buttons 2x2)
# -----------------------------
st.sidebar.markdown("## 🧭 Navigation")

row1 = st.sidebar.columns(2)
row2 = st.sidebar.columns(2)

with row1[0]:
    india_btn = st.sidebar.button("🇮🇳 India", use_container_width=True)

with row1[1]:
    state_btn = st.sidebar.button("🏙️ State", use_container_width=True)

with row2[0]:
    dist_btn = st.sidebar.button("📍 District", use_container_width=True)

with row2[1]:
    age_btn = st.sidebar.button("👥 Age", use_container_width=True)

if "page" not in st.session_state:
    st.session_state.page = "🇮🇳 India Overview"

if india_btn:
    st.session_state.page = "🇮🇳 India Overview"
elif state_btn:
    st.session_state.page = "🏙️ State Deep Dive"
elif dist_btn:
    st.session_state.page = "📍 District Drilldown"
elif age_btn:
    st.session_state.page = "👥 Age Migration"

page = st.session_state.page
st.sidebar.markdown("---")






# -----------------------------
# Time Filter (FINAL)
# -----------------------------
st.sidebar.markdown("## ⏳ Time Window")

min_m = state_df["month"].min()
max_m = state_df["month"].max()

preset = st.sidebar.selectbox(
    "Quick Preset",
    ["Full Range", "Last 3 Months", "Last 6 Months"],
    index=0
)

if preset == "Last 3 Months":
    start = (max_m - pd.DateOffset(months=3)).to_pydatetime()
    end = max_m.to_pydatetime()
elif preset == "Last 6 Months":
    start = (max_m - pd.DateOffset(months=6)).to_pydatetime()
    end = max_m.to_pydatetime()
else:
    start = min_m.to_pydatetime()
    end = max_m.to_pydatetime()

time_range = st.sidebar.slider(
    "Select range",
    min_value=min_m.to_pydatetime(),
    max_value=max_m.to_pydatetime(),
    value=(start, end)
)

st.sidebar.caption(f"📅 **{time_range[0].date()} → {time_range[1].date()}**")

# Apply global filters
state_df_f = state_df[
    (state_df["month"] >= pd.to_datetime(time_range[0])) &
    (state_df["month"] <= pd.to_datetime(time_range[1]))
].copy()

dist_df_f = dist_df[
    (dist_df["month"] >= pd.to_datetime(time_range[0])) &
    (dist_df["month"] <= pd.to_datetime(time_range[1]))
].copy()

st.sidebar.markdown("---")

# -----------------------------
# Page Specific Filters (FINAL)
# -----------------------------
st.sidebar.markdown("## 🎛️ Filters")

if page == "🏙️ State Deep Dive":
    with st.sidebar.expander("🏙️ State Filter", expanded=True):
        states = sorted(state_df_f["state"].dropna().unique())
        chosen_state = st.selectbox("Select State/UT", states)

elif page == "📍 District Drilldown":
    with st.sidebar.expander("📍 District Filter", expanded=True):
        states = sorted(dist_df_f["state"].dropna().unique())
        chosen_state = st.selectbox("Select State/UT", states)

        districts = sorted(
            dist_df_f[dist_df_f["state"] == chosen_state]["district"].dropna().unique()
        )
        chosen_district = st.selectbox("Select District", districts)

elif page == "👥 Age Migration":
    with st.sidebar.expander("👥 Demographics Filter", expanded=True):
        states = sorted(state_df_f["state"].dropna().unique())
        chosen_state = st.selectbox("Select State/UT", ["All India"] + states)

st.sidebar.markdown("---")

# -----------------------------
# Sidebar Live Snapshot
# -----------------------------
st.sidebar.markdown("## ⚡ Live Snapshot")
st.sidebar.metric("States/UTs", f"{state_df_f['state'].nunique()}")
st.sidebar.metric("Total Activity", f"{state_df_f['activity_total'].sum():,.0f}")

# -----------------------------
# Header
# -----------------------------
# -----------------------------
# HEADER (FINAL CLEAN)
# -----------------------------
# -----------------------------
# HEADER (FINAL CLEAN)
# -----------------------------
import base64

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ✅ Correct path: assets folder is outside dashboard
logo_path = os.path.join(BASE_DIR, "..", "assets", "aadhaar_transparent.png")

# ✅ create logo_base64 FIRST
logo_base64 = get_base64(logo_path)

st.markdown("""
<style>
.header-wrap{
    display:flex;
    justify-content:center;
    align-items:center;
    gap:18px;
    padding:10px 0px 6px 0px;
    margin-bottom:10px;
}

.header-logo img{
    height:65px;
    width:auto;
    background:transparent !important;
    border:none !important;
    outline:none !important;
    box-shadow:none !important;
    filter: drop-shadow(0px 0px 10px rgba(0,245,255,0.22));
}

.header-text{
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:flex-start;
}

.header-title{
    font-size:48px;
    font-weight:900;
    color:#E6EAF2;
    line-height:1.05;
    margin:0;
}

.header-sub{
    font-size:14px;
    color:rgba(230,234,242,0.70);
    margin-top:4px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="header-wrap">
    <div class="header-logo">
        <img src="data:image/png;base64,{logo_base64}">
    </div>
    <div class="header-text">
        <div class="header-title">UIDAI Migration & Urbanization Tracker</div>
        <div class="header-sub">Migration Proxy + Urbanization Hotspots | UIDAI Hackathon 2026</div>
    </div>
</div>
""", unsafe_allow_html=True)


# -----------------------------
# TOP NAVIGATION BAR (1 x 4 Tiles)
# -----------------------------
st.markdown("""
<style>
.nav-btn button{
    width:100%;
    border-radius:16px !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    background: rgba(255,255,255,0.06) !important;
    color: rgba(230,234,242,0.92) !important;
    font-weight: 700 !important;
    padding: 10px 14px !important;
    transition: 0.2s ease-in-out;
}

.nav-btn button:hover{
    background: rgba(255,255,255,0.10) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
}

.nav-active button{
    background: rgba(255,255,255,0.14) !important;
    border: 1px solid rgba(255,255,255,0.22) !important;
}
</style>
""", unsafe_allow_html=True)

# Default page
if "page" not in st.session_state:
    st.session_state.page = "🇮🇳 India Overview"

col1, col2, col3, col4 = st.columns(4)

def nav_button(label, page_name, col):
    active_class = "nav-active" if st.session_state.page == page_name else ""
    with col:
        st.markdown(f"<div class='nav-btn {active_class}'>", unsafe_allow_html=True)
        clicked = st.button(label, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if clicked:
        st.session_state.page = page_name

nav_button("🇮🇳 India Overview", "🇮🇳 India Overview", col1)
nav_button("🏙️ State Deep Dive", "🏙️ State Deep Dive", col2)
nav_button("📍 District Drilldown", "📍 District Drilldown", col3)
nav_button("👥 Age Migration", "👥 Age Migration", col4)

page = st.session_state.page




# ============================
# 🇮🇳 INDIA OVERVIEW PAGE
# ============================
if page == "🇮🇳 India Overview":

    st.markdown("## 🗺️ India Overview: Migration & Urbanization Signals (Proxy)")

    # KPIs
    total_activity = state_df_f["activity_total"].sum()
    avg_growth = state_df_f["growth_pct"].mean()
    states_covered = state_df_f["state"].nunique()

    rank_tmp = (
        state_df_f.groupby("state", as_index=False)
        .agg(avg_migration=("migration_index", "mean"))
    )
    pos_pct = (rank_tmp["avg_migration"] > 0).mean() * 100

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📌 Total Activity", f"{total_activity:,.0f}")
    c2.metric("📌 States with + Migration Signal", f"{pos_pct:.1f}%")
    c3.metric("📌 Avg Growth %", f"{avg_growth*100:.2f}%")
    c4.metric("🗺️ States/UTs Covered", f"{states_covered}")

    st.divider()

    # Ranking table
    rank = (
        state_df_f.groupby("state", as_index=False)
        .agg(
            avg_migration=("migration_index", "mean"),
            total_activity=("activity_total", "sum"),
            avg_growth=("growth_pct", "mean"),
        )
        .sort_values("avg_migration", ascending=False)
    )

    # -----------------------------
    # GEOJSON FIX (Missing states)
    # -----------------------------
    geo_states = set([f["properties"]["NAME_1"] for f in india_geo["features"]])
    rank["state_map"] = rank["state"]

    fix_map = {
    # UTs / name variants
    "Andaman and Nicobar Islands": "Andaman and Nicobar",
    "Dadra and Nagar Haveli and Daman and Diu": "Dadra and Nagar Haveli",
    "Puducherry": "Pondicherry",
    "Pondicherry": "Pondicherry",

    # Delhi variants
    "Delhi": "Delhi",
    "NCT of Delhi": "Delhi",

    # Older census naming (common in GeoJSON)
    "Odisha": "Orissa",
    "Orissa": "Orissa",

    "Uttarakhand": "Uttaranchal",
    "Uttaranchal": "Uttaranchal",

    # Some GeoJSONs still have combined/old naming
    "Jammu & Kashmir": "Jammu and Kashmir",
    "Jammu and Kashmir": "Jammu and Kashmir",
    "Ladakh": "Jammu and Kashmir",
}


    rank["state_map"] = rank["state_map"].replace(fix_map)

    missing = sorted(list(set(rank["state_map"].unique()) - geo_states))
   

    # Choropleth Map
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    fig_map = px.choropleth(
        rank,
        geojson=india_geo,
        locations="state_map",
        featureidkey="properties.NAME_1",
        color="avg_migration",
        hover_name="state",
        hover_data={"total_activity":":,.0f", "avg_growth":":.2%"},
        color_continuous_scale="Turbo",
        title="India Migration Inflow Signal (Proxy) — State Boundaries"
    )

    # BLACK outlines
    fig_map.update_traces(
        marker_line_width=1.2,
        marker_line_color="rgba(0,0,0,1)"
    )

    # Remove white background
    fig_map.update_geos(
        fitbounds="locations",
        visible=False,
        bgcolor="rgba(0,0,0,0)",
        showframe=False,
        showcoastlines=False
    )

    fig_map.update_layout(
        height=520,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=50, b=0),
        font=dict(color="#E6EAF2"),
        coloraxis_colorbar=dict(
            bgcolor="rgba(0,0,0,0)",
            outlinecolor="rgba(0,245,255,0.35)"
        )
    )

    st.plotly_chart(fig_map, use_container_width=True, config={"scrollZoom": True})
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # Top In vs Out migration
    left, right = st.columns([0.55, 0.45])

    with left:
        st.markdown("### 🏆 Top In-Migration States (Proxy)")
        fig_in = px.bar(
            rank.head(12),
            x="avg_migration",
            y="state",
            orientation="h",
            title="Top Positive Migration Index (Z)"
        )
        fig_in.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E6EAF2"),
            height=420,
            margin=dict(l=10, r=10, t=50, b=10)
        )
        fig_in = apply_4k_plotly_theme(fig_in)
        st.plotly_chart(fig_in, use_container_width=True)

    with right:
        st.markdown("### 📉 Top Out-Migration States (Proxy)")
        fig_out = px.bar(
            rank.tail(12).sort_values("avg_migration", ascending=True),
            x="avg_migration",
            y="state",
            orientation="h",
            title="Top Negative Migration Index (Z)"
        )
        fig_out.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E6EAF2"),
            height=420,
            margin=dict(l=10, r=10, t=50, b=10)
        )
        fig_in = apply_4k_plotly_theme(fig_in)
        st.plotly_chart(fig_out, use_container_width=True)

    st.divider()

    import plotly.graph_objects as go

    st.divider()

    st.markdown("## 🔀 Migration Flow (Proxy): Source → Destination")
    st.caption(
    "This Sankey shows a proxy flow model built from migration index signals. "
    "It does NOT represent actual individual migration routes."
)

# 1) Prepare state-level migration signal
    flow_rank = (
     state_df_f.groupby("state", as_index=False)
    .agg(mig=("migration_index", "mean"))
)

# Split into outflow (negative) and inflow (positive)
    sources = flow_rank[flow_rank["mig"] < 0].copy()
    targets = flow_rank[flow_rank["mig"] > 0].copy()

# If not enough data
    if len(sources) < 2 or len(targets) < 2:
      st.warning("Not enough variation in migration index to generate Sankey flow.")
    else:
    # Convert signal strength to positive weights
     sources["out_strength"] = sources["mig"].abs()
    targets["in_strength"] = targets["mig"].abs()

    # Take Top-N to keep Sankey clean
    # Take Top-N to keep Sankey clean (BONUS slider)
    TOP_N = st.slider("Number of states in flow chart", 5, 15, 10)

    sources = sources.sort_values("out_strength", ascending=False).head(TOP_N)
    targets = targets.sort_values("in_strength", ascending=False).head(TOP_N)


    # Normalize weights
    sources["out_w"] = sources["out_strength"] / sources["out_strength"].sum()
    targets["in_w"] = targets["in_strength"] / targets["in_strength"].sum()

    # Build proxy flows: each source distributes to each target
    links = []
    for _, s in sources.iterrows():
        for _, t in targets.iterrows():
            value = float(s["out_w"] * t["in_w"])  # proxy distribution
            links.append((s["state"], t["state"], value))

    link_df = pd.DataFrame(links, columns=["source", "target", "value"])

    # Scale values for better visualization
    link_df["value_scaled"] = link_df["value"] * 1000

    # Create Sankey nodes 
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)


    all_nodes = list(pd.unique(link_df[["source", "target"]].values.ravel()))
    node_index = {name: i for i, name in enumerate(all_nodes)}

    sankey_source = link_df["source"].map(node_index)
    sankey_target = link_df["target"].map(node_index)
    sankey_value = link_df["value_scaled"]

    fig_sankey = go.Figure(
        data=[
            go.Sankey(
                arrangement="snap",
                node=dict(
                    pad=18,
                    thickness=18,
                    line=dict(color="rgba(0,0,0,0.8)", width=0.6),
                    label=all_nodes,
                    color="rgba(0,245,255,0.25)"
                ),
                link=dict(
                    source=sankey_source,
                    target=sankey_target,
                    value=sankey_value,
                    color="rgba(124,255,0,0.18)"
                ),
            )
        ]
    )

    fig_sankey.update_layout(
        title="Migration Flow Sankey (Proxy): Outflow → Inflow States",
        font=dict(color="#E6EAF2"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=650,
        margin=dict(l=10, r=10, t=60, b=10),
    )
    fig_in = apply_4k_plotly_theme(fig_in)
    
    
    st.plotly_chart(fig_sankey, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Urbanization Hotspots Scatter
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)


    st.markdown("### 🌆 Urbanization Hotspots (High Activity + High Migration)")
    hotspots = rank.copy()
    hotspots["growth_pct_num"] = hotspots["avg_growth"] * 100

    fig_hot = px.scatter(
        hotspots,
        x="total_activity",
        y="avg_migration",
        size="total_activity",
        color="growth_pct_num",
        hover_name="state",
        title="Urbanization Hotspots: Activity vs Migration Index",
        labels={
            "total_activity": "Total Activity",
            "avg_migration": "Avg Migration Index (Z)",
            "growth_pct_num": "Avg Growth %"
        }
    )

    fig_hot.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E6EAF2"),
        height=520
    )
    fig_hot = apply_4k_plotly_theme(fig_hot)
    st.plotly_chart(fig_hot, use_container_width=True)
    

    st.markdown('</div>', unsafe_allow_html=True)


    st.divider()

    # India trend
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)


    st.markdown("### 📆 India Trend")
    india_trend = (
        state_df_f.groupby("month", as_index=False)
        .agg(activity_total=("activity_total", "sum"),
             migration_index=("migration_index", "mean"))
    )

    fig3 = px.line(india_trend, x="month", y="activity_total", markers=True)
    fig3.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E6EAF2"),
        title="India-wide Aadhaar Activity Trend"
    )
    fig_in = apply_4k_plotly_theme(fig_in)
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.divider()

    

    # Heatmap
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)


    st.markdown("### 🌡️ Migration Signal Heatmap (State × Month)")
    heat_df = state_df_f.groupby(["state", "month"], as_index=False).agg(
        mig=("migration_index", "mean")
    )

    heat_pivot = heat_df.pivot(index="state", columns="month", values="mig").fillna(0)

    fig_heat = px.imshow(
        heat_pivot,
        aspect="auto",
        title="Migration Index (Z) Heatmap — State vs Month",
    )

    fig_heat.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E6EAF2"),
        height=650,
        margin=dict(l=10, r=10, t=60, b=10)
    )
    fig_in = apply_4k_plotly_theme(fig_in)

    st.plotly_chart(fig_heat, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    
    


    # Top Movers
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    st.markdown("### 🚀 Top Movers (Month-on-Month Change)")

    mom = state_df_f.groupby(["state", "month"], as_index=False).agg(
        mig=("migration_index", "mean")
    )
    mom = mom.sort_values(["state", "month"])
    mom["mom_change"] = mom.groupby("state")["mig"].diff()

    latest_month = mom["month"].max()
    mom_latest = mom[mom["month"] == latest_month].dropna(subset=["mom_change"]).copy()

    top_gainers = mom_latest.sort_values("mom_change", ascending=False).head(10)
    top_losers = mom_latest.sort_values("mom_change", ascending=True).head(10)

    colA, colB = st.columns(2)

    with colA:
        st.markdown("#### 🟢 Fastest Rising States")
        fig_gain = px.bar(
            top_gainers,
            x="mom_change",
            y="state",
            orientation="h",
            title=f"Top Gainers — {latest_month.date()}",
        )
        fig_gain.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E6EAF2"),
            height=420,
            margin=dict(l=10, r=10, t=60, b=10)
        )
        fig_gain = apply_4k_plotly_theme(fig_gain)
        st.plotly_chart(fig_gain, use_container_width=True)

    with colB:
        st.markdown("#### 🔴 Fastest Falling States")
        fig_lose = px.bar(
            top_losers.sort_values("mom_change", ascending=True),
            x="mom_change",
            y="state",
            orientation="h",
            title=f"Top Losers — {latest_month.date()}",
        )
        fig_lose.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E6EAF2"),
            height=420,
            margin=dict(l=10, r=10, t=60, b=10)
        )
        fig_in = apply_4k_plotly_theme(fig_in)
        st.plotly_chart(fig_lose, use_container_width=True)
       
        st.markdown('</div>', unsafe_allow_html=True)


    st.caption("MoM change shows sudden spikes/drops in migration signal (proxy). Useful for detecting emerging hotspots.")

    st.info("⚠️ Migration Index is a proxy based on Aadhaar activity growth patterns (not individual tracking).")

    st.markdown("### ⬇️ Download Clean Data")
    st.download_button(
        "Download State-Month CSV",
        data=state_df.to_csv(index=False),
        file_name="dashboard_state_month.csv"
    )
    st.download_button(
        "Download District-Month CSV",
        data=dist_df.to_csv(index=False),
        file_name="dashboard_district_month.csv"
    )

# ============================
# 🏙️ STATE DEEP DIVE
# ============================



elif page == "🏙️ State Deep Dive":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)


    st.subheader("🏙️ State Deep Dive")

    if chosen_state is None:
        st.info("Select a state from the sidebar.")
        st.stop()

    s_df = state_df_f[state_df_f["state"] == chosen_state].copy()

    c1, c2, c3 = st.columns(3)
    c1.metric("📊 Total Activity", f"{s_df['activity_total'].sum():,.0f}")
    c2.metric("📌 Avg Migration Index", f"{s_df['migration_index'].mean():.2f}")
    c3.metric("📈 Avg Growth %", f"{(s_df['growth_pct'].mean()*100):.2f}%")

    st.divider()

    fig = px.line(
        s_df,
        x="month",
        y="activity_total",
        markers=True,
        title=f"{chosen_state}: Activity Trend"
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E6EAF2")
    )
    fig_in = apply_4k_plotly_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📍 Top Districts by Activity")
    d_df = dist_df_f[dist_df_f["state"] == chosen_state].copy()

    d_rank = (
        d_df.groupby("district", as_index=False)
        .agg(total_activity=("activity_total", "sum"))
        .sort_values("total_activity", ascending=False)
        .head(15)
    )

    fig2 = px.bar(
        d_rank,
        x="total_activity",
        y="district",
        orientation="h",
        title="Top Districts (Activity)"
    )
    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E6EAF2")
    )
    fig2 = apply_4k_plotly_theme(fig2)
    st.plotly_chart(fig2, use_container_width=True)
    

    st.markdown('</div>', unsafe_allow_html=True)



    import plotly.graph_objects as go

    st.divider()
    st.markdown("### 🔀 State Migration Flow (Proxy)")
    st.caption(
        "This Sankey shows a proxy origin/destination flow around the selected state using migration index signals. "
        "It does NOT represent actual person-level migration routes."
    )

    flow_rank = (
        state_df_f.groupby("state", as_index=False)
        .agg(mig=("migration_index", "mean"))
    )

    # --- Selected state value ---
    selected_row = flow_rank[flow_rank["state"] == chosen_state]
    if selected_row.empty:
        st.warning("Selected state not found in dataset.")
        st.stop()

    selected_mig = float(selected_row["mig"].iloc[0])

    # --- Build sources & targets ---
    sources = flow_rank[flow_rank["mig"] < 0].copy()
    targets = flow_rank[flow_rank["mig"] > 0].copy()

    TOP_N = st.slider("Number of connected states", 5, 15, 10)

    # --- If all mig values are 0 (or too small) ---
    if sources.empty and targets.empty:
        st.warning("⚠️ Sankey cannot be generated because migration_index values are mostly 0 in this time window.")
        st.info("Try expanding the time range or check if migration_index column has positive/negative values.")
        st.stop()

    # --- Build link_df ---
    if selected_mig < 0:
        # Outflow proxy: selected -> positive states
        targets = targets.sort_values("mig", ascending=False).head(TOP_N)

        if targets.empty:
            st.warning("No positive migration states found to connect.")
            st.stop()

        targets["w"] = targets["mig"].abs()
        targets["w"] = targets["w"] / targets["w"].sum()

        link_df = pd.DataFrame({
            "source": [chosen_state] * len(targets),
            "target": targets["state"].tolist(),
            "value": (targets["w"] * 1000).tolist()
        })

        title_flow = f"Outflow Proxy: {chosen_state} → Top Inflow States"

    else:
        # Inflow proxy: negative states -> selected
        sources = sources.sort_values("mig", ascending=True).head(TOP_N)

        if sources.empty:
            st.warning("No negative migration states found to connect.")
            st.stop()

        sources["w"] = sources["mig"].abs()
        sources["w"] = sources["w"] / sources["w"].sum()

        link_df = pd.DataFrame({
            "source": sources["state"].tolist(),
            "target": [chosen_state] * len(sources),
            "value": (sources["w"] * 1000).tolist()
        })

        title_flow = f"Inflow Proxy: Top Outflow States → {chosen_state}"

    # --- Final check ---
    if link_df.empty:
        st.warning("Sankey links are empty. Nothing to plot.")
        st.stop()

    # --- Build Sankey ---
    nodes = list(pd.unique(link_df[["source", "target"]].values.ravel()))
    node_index = {name: i for i, name in enumerate(nodes)}

    fig_state_flow = go.Figure(
    data=[
        go.Sankey(
            arrangement="snap",
            node=dict(
                pad=18,
                thickness=18,
                line=dict(color="rgba(0,0,0,1)", width=0.8),
                label=nodes,

                # ✅ Neon cyan nodes (like your theme)
                color="rgba(0,245,255,0.22)",
            ),
            link=dict(
                source=link_df["source"].map(node_index),
                target=link_df["target"].map(node_index),
                value=link_df["value"],

                # ✅ Neon green flow (like your theme)
                color="rgba(124,255,0,0.22)",
            ),
        )
    ]
    )

    fig_state_flow.update_layout(
        title=title_flow,
        font=dict(color="#E6EAF2"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=520,
        margin=dict(l=10, r=10, t=60, b=10),
    )


    
    fig_in = apply_4k_plotly_theme(fig_in)
    st.plotly_chart(fig_state_flow, use_container_width=True)



    

# ============================
# 📍 DISTRICT DRILLDOWN
# ============================
elif page == "📍 District Drilldown":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)


    st.subheader("📍 District Drilldown (State → District)")

    if chosen_state is None or chosen_district is None:
        st.info("Select a state and district from the sidebar.")
        st.stop()

    dd = dist_df_f[
        (dist_df_f["state"] == chosen_state) &
        (dist_df_f["district"] == chosen_district)
    ].copy()

    c1, c2, c3 = st.columns(3)
    c1.metric("📊 Total Activity", f"{dd['activity_total'].sum():,.0f}")
    c2.metric("👶 0–5 Total", f"{dd['age_0_5'].sum():,.0f}")
    c3.metric("🧑 18+ Total", f"{dd['age_18_greater'].sum():,.0f}")

    st.divider()

    fig = px.line(
        dd,
        x="month",
        y="activity_total",
        markers=True,
        title=f"{chosen_district}, {chosen_state}: Trend"
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E6EAF2")
    )
    fig_in = apply_4k_plotly_theme(fig)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ============================
# 👥 AGE MIGRATION
# ============================
elif page == "👥 Age Migration":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)


    st.subheader("👥 Age Activity Insights (Proxy, Not Direct Migration)")
    st.caption(
        "This section shows Aadhaar activity by age group. Higher 0–5 does NOT mean kids migrate alone — "
        "it reflects enrolment/updates linked to family movement & service drives."
    )

    if chosen_state is None:
        st.info("Select All India or a state from the sidebar.")
        st.stop()

    if chosen_state == "All India":
        temp = state_df_f.groupby("month", as_index=False).agg(
            age_0_5=("age_0_5", "sum"),
            age_5_17=("age_5_17", "sum"),
            age_18_greater=("age_18_greater", "sum"),
        )
        title = "India Aadhaar Activity by Age Group (Proxy)"
    else:
        temp = (
            state_df_f[state_df_f["state"] == chosen_state]
            .groupby("month", as_index=False)
            .agg(
                age_0_5=("age_0_5", "sum"),
                age_5_17=("age_5_17", "sum"),
                age_18_greater=("age_18_greater", "sum"),
            )
        )
        title = f"{chosen_state} Aadhaar Activity by Age Group (Proxy)"

    long = temp.melt(id_vars="month", var_name="age_group", value_name="count")

    fig = px.line(long, x="month", y="count", color="age_group", markers=True, title=title)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E6EAF2"),
        height=520
    )
    fig_in = apply_4k_plotly_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.markdown("### 🧑‍💼 Working-Age Migration Signal (Proxy)")
    st.caption("Adult Share % = 18+ / (0–5 + 5–17 + 18+). Higher % suggests stronger working-age movement updates (proxy).")

    temp2 = temp.copy()
    temp2["total_age_activity"] = temp2["age_0_5"] + temp2["age_5_17"] + temp2["age_18_greater"]

    temp2["adult_share_pct"] = np.where(
        temp2["total_age_activity"] > 0,
        (temp2["age_18_greater"] / temp2["total_age_activity"]) * 100,
        0
    )

    fig_adult = px.area(
        temp2,
        x="month",
        y="adult_share_pct",
        markers=True,
        title="Adult Share % of Aadhaar Activity (18+ / Total) — Migration Proxy"
    )

    fig_adult.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E6EAF2"),
        height=420,
        yaxis_title="Adult Share (%)",
        margin=dict(l=10, r=10, t=60, b=10)
    )
    fig_in = apply_4k_plotly_theme(fig_in)
    st.plotly_chart(fig_adult, use_container_width=True)

    st.divider()

    st.markdown("### 🧩 Age Contribution Share (Proxy)")

    age_totals = {
        "0–5": float(temp["age_0_5"].sum()),
        "5–17": float(temp["age_5_17"].sum()),
        "18+": float(temp["age_18_greater"].sum()),
    }

    age_share = pd.DataFrame({
        "age_group": list(age_totals.keys()),
        "count": list(age_totals.values())
    })

    fig_age = px.pie(
        age_share,
        names="age_group",
        values="count",
        hole=0.55,
        title="Age Group Share in Aadhaar Activity (Proxy)"
    )

    fig_age.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E6EAF2"),
        height=420
    )
    fig_in = apply_4k_plotly_theme(fig_in)
    st.plotly_chart(fig_age, use_container_width=True)
    

    st.markdown('</div>', unsafe_allow_html=True)


    st.success(
        "Interpretation: Adult Share % rising = stronger working-age movement signal (proxy). "
        "0–5 spikes often indicate enrolment/service drives + family-linked updates."
    )