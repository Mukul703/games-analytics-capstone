import streamlit as st
import plotly.express as px
from db_connection import run_query

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Tennis Analytics Dashboard",
    layout="wide"
)

# ======================================================
# GLOBAL BLUE GRADIENT THEME + UI STYLING
# ======================================================
st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(135deg, #e3f2fd, #f8fbff);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d47a1, #1976d2);
}
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* KPI cards */
.kpi-card {
    background: linear-gradient(135deg, #2196f3, #1e88e5);
    padding: 26px;
    border-radius: 18px;
    box-shadow: 0 10px 24px rgba(0,0,0,0.18);
    text-align: center;
    color: white;
}
.kpi-title {
    font-size: 15px;
    opacity: 0.9;
}
.kpi-value {
    font-size: 40px;
    font-weight: 700;
}

/* Section spacing */
.section-gap {
    margin-top: 30px;
}

/* Tables */
thead tr th {
    background-color: #e3f2fd !important;
    color: #0d47a1 !important;
}

/* Slider color */
.css-1cypcdb {
    color: #1976d2 !important;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# SIDEBAR NAVIGATION
# ======================================================
st.sidebar.title("🎾 Tennis Analytics")

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Home",
        "📊 Dashboard Overview",
        "🔍 Search & Filter Competitors",
        "👤 Competitor Details",
        "🌍 Country-wise Analysis",
        "🏆 Leaderboards"
    ]
)

# ======================================================
# HOME PAGE
# ======================================================
if page == "🏠 Home":
    st.title("🎾 Tennis SportRadar Analytics Dashboard")

    st.markdown("""
    ### 📌 Problem Statement
    The objective of this project is to analyze tennis competitors,
    rankings, and competition data using a relational SQL database
    and present actionable insights through an interactive dashboard.

    ### 🎯 Business Use Cases
    - Competitor performance analysis
    - Ranking & points-based insights
    - Country-wise tennis dominance
    - Decision support for sports analytics

    ### 🛠 Tech Stack
    - **Database**: MySQL  
    - **Backend**: Python  
    - **Frontend**: Streamlit  
    - **Visualization**: Plotly  
    """)

# ======================================================
# DASHBOARD OVERVIEW
# ======================================================
elif page == "📊 Dashboard Overview":
    st.title("📊 Dashboard Overview")

    query = """
    SELECT
        COUNT(DISTINCT c.competitor_id) AS total_competitors,
        COUNT(DISTINCT c.country) AS total_countries,
        MAX(cr.points) AS highest_points
    FROM competitors c
    JOIN competitor_rankings cr
        ON c.competitor_id = cr.competitor_id;
    """
    df = run_query(query)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Competitors</div>
            <div class="kpi-value">{df['total_competitors'][0]}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Countries Represented</div>
            <div class="kpi-value">{df['total_countries'][0]}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Highest Points Scored</div>
            <div class="kpi-value">{df['highest_points'][0]}</div>
        </div>
        """, unsafe_allow_html=True)

# ======================================================
# SEARCH & FILTER COMPETITORS (POINTS INCLUDED)
# ======================================================
elif page == "🔍 Search & Filter Competitors":
    st.title("🔍 Search & Filter Competitors")

    query = """
    SELECT
        c.name,
        c.country,
        cr.rank,
        cr.points
    FROM competitors c
    JOIN competitor_rankings cr
        ON c.competitor_id = cr.competitor_id;
    """
    df = run_query(query)

    col1, col2, col3, col4 = st.columns([3, 3, 2, 2])

    with col1:
        name_filter = st.text_input("Search by Competitor Name")

    with col2:
        country_filter = st.text_input("Filter by Country")

    with col3:
        rank_range = st.slider(
            "Rank Range",
            int(df["rank"].min()),
            int(df["rank"].max()),
            (int(df["rank"].min()), int(df["rank"].max()))
        )

    with col4:
        points_range = st.slider(
            "Points Threshold",
            int(df["points"].min()),
            int(df["points"].max()),
            (int(df["points"].min()), int(df["points"].max()))
        )

    if name_filter:
        df = df[df["name"].str.contains(name_filter, case=False)]

    if country_filter:
        df = df[df["country"].str.contains(country_filter, case=False)]

    df = df[
        (df["rank"] >= rank_range[0]) &
        (df["rank"] <= rank_range[1]) &
        (df["points"] >= points_range[0]) &
        (df["points"] <= points_range[1])
    ]

    st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

# ======================================================
# COMPETITOR DETAILS VIEWER
# ======================================================
elif page == "👤 Competitor Details":
    st.title("👤 Competitor Details")

    names_df = run_query("SELECT name FROM competitors ORDER BY name;")
    selected_name = st.selectbox("Select Competitor", names_df["name"])

    query = f"""
    SELECT
        c.name,
        c.country,
        cr.rank,
        cr.movement,
        cr.points,
        cr.competitions_played
    FROM competitors c
    JOIN competitor_rankings cr
        ON c.competitor_id = cr.competitor_id
    WHERE c.name = '{selected_name}';
    """
    df = run_query(query)
    st.table(df)

# ======================================================
# COUNTRY-WISE ANALYSIS (AVG POINTS)
# ======================================================
elif page == "🌍 Country-wise Analysis":
    st.title("🌍 Country-wise Analysis")

    query = """
    SELECT
        c.country,
        COUNT(DISTINCT c.competitor_id) AS total_competitors,
        ROUND(AVG(cr.points), 2) AS avg_points
    FROM competitors c
    JOIN competitor_rankings cr
        ON c.competitor_id = cr.competitor_id
    GROUP BY c.country
    ORDER BY avg_points DESC;
    """
    df = run_query(query)

    fig = px.bar(
        df,
        x="country",
        y="avg_points",
        title="Average Points by Country",
        color="avg_points",
        color_continuous_scale="Blues"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df, use_container_width=True)

# ======================================================
# LEADERBOARDS
# ======================================================
elif page == "🏆 Leaderboards":
    st.title("🏆 Leaderboards")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏅 Top Ranked Competitors")
        df_rank = run_query("""
        SELECT
            c.name,
            cr.rank,
            c.country
        FROM competitors c
        JOIN competitor_rankings cr
            ON c.competitor_id = cr.competitor_id
        ORDER BY cr.rank
        LIMIT 10;
        """)
        st.dataframe(df_rank, use_container_width=True)

    with col2:
        st.subheader("🔥 Highest Points")
        df_points = run_query("""
        SELECT
            c.name,
            cr.points,
            c.country
        FROM competitors c
        JOIN competitor_rankings cr
            ON c.competitor_id = cr.competitor_id
        ORDER BY cr.points DESC
        LIMIT 10;
        """)
        st.dataframe(df_points, use_container_width=True)
