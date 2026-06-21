import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─────────────────────────────────────────────
# PAGE CONFIGURATION & ENTERPRISE THEME
# ─────────────────────────────────────────────
st.set_page_config(page_title="App Voice of Customer Analytics", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family:'Inter', sans-serif; background:#0f172a; color: #e2e8f0; }
    .stApp { background:#0f172a; }
    
    /* Executive KPI Cards */
    .metric-card { background:#1e293b; border:1px solid #334155; border-radius:6px; padding:1.25rem; margin-bottom:1rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
    .metric-title { color:#94a3b8; font-size:0.8rem; font-weight:600; text-transform:uppercase; letter-spacing:0.05em; }
    .metric-value { color:#f8fafc; font-size:2.2rem; font-weight:700; margin-top:0.4rem; letter-spacing:-0.02em; }
    
    /* Streamlit Table Styling Overrides to match theme */
    .stDataFrame { background-color: #1e293b; border-radius: 6px; }
    [data-testid="stTable"] { background-color: #1e293b; border-radius: 6px; }
    [data-testid="stTable"] th { background-color: #0f172a !important; color: #94a3b8 !important; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 0.05em; border-bottom: 1px solid #334155 !important; }
    [data-testid="stTable"] td { color: #e2e8f0 !important; font-size: 0.9rem; border-bottom: 1px solid #334155 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA ACQUISITION
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        return pd.read_csv("analyzed_reviews.csv")
    except FileNotFoundError:
        return None

df = load_data()

# ─────────────────────────────────────────────
# DASHBOARD UI: HEADER & KPIs
# ─────────────────────────────────────────────
st.markdown("<h1 style='color:#f8fafc; font-size:1.8rem; margin-bottom:0;'>VOICE OF CUSTOMER: COMPETITIVE NLP INTELLIGENCE</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#94a3b8; font-size:0.9rem; text-transform:uppercase; letter-spacing:0.05em;'>Uncovering the Choice Drivers Behind App Switching</p>", unsafe_allow_html=True)
st.markdown("<hr style='border-color:#334155; margin-top:0.5rem; margin-bottom:1.5rem;'>", unsafe_allow_html=True)

if df is None:
    st.error("SYSTEM ERROR: Data file not found. Please run the NLP engine first.")
    st.stop()

# Calculate high-level metrics
total_reviews = len(df)
avg_bank_score = df[df['App_Type'] == 'Traditional Bank']['Score'].mean()
avg_fintech_score = df[df['App_Type'] == 'Digital Fintech']['Score'].mean()
top_theme = df['Topic_Name'].mode()[0]

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Total Processed Reviews</div><div class='metric-value'>{total_reviews:,}</div></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Traditional Bank Avg Score</div><div class='metric-value' style='color:#ef4444;'>{avg_bank_score:.1f} / 5.0</div></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Digital Fintech Avg Score</div><div class='metric-value' style='color:#10b981;'>{avg_fintech_score:.1f} / 5.0</div></div>", unsafe_allow_html=True)
with c4:
    # Safely format the top theme name by taking the words after the colon
    clean_top_theme = top_theme.split(': ')[1] if ':' in top_theme else top_theme
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Most Discussed Theme</div><div class='metric-value' style='font-size:1.4rem; padding-top:0.6rem;'>{clean_top_theme.title()}</div></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DASHBOARD UI: VISUALIZATIONS
# ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown("<h3 style='color:#f8fafc; font-size:1.0rem; text-transform:uppercase; letter-spacing:0.05em;'>Overall Theme Distribution</h3>", unsafe_allow_html=True)
    
    theme_counts = df['Topic_Name'].value_counts().reset_index()
    theme_counts.columns = ['Theme', 'Volume']
    
    # Clean theme names for better visual display
    theme_counts['Theme_Short'] = theme_counts['Theme'].apply(lambda x: x.split(': ')[1].title() if ':' in x else x)
    
    fig_donut = px.pie(
        theme_counts, 
        values='Volume', 
        names='Theme_Short',
        hole=0.6,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_donut.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(color='#94a3b8', size=11)),
        margin=dict(l=0, r=0, t=20, b=0)
    )
    st.plotly_chart(fig_donut, use_container_width=True)

with col_right:
    st.markdown("<h3 style='color:#f8fafc; font-size:1.0rem; text-transform:uppercase; letter-spacing:0.05em;'>The Battleground: Banks vs. Fintechs</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; font-size:0.85rem;'>Percentage of complaints/reviews mapped to each theme by sector.</p>", unsafe_allow_html=True)
    
    # Calculate what percentage of a sector's reviews fall into each topic
    sector_topic = df.groupby(['App_Type', 'Topic_Name']).size().reset_index(name='Count')
    sector_totals = df.groupby('App_Type').size().reset_index(name='Total')
    sector_topic = pd.merge(sector_topic, sector_totals, on='App_Type')
    sector_topic['Percentage'] = (sector_topic['Count'] / sector_topic['Total']) * 100
    
    sector_topic['Theme_Short'] = sector_topic['Topic_Name'].apply(lambda x: x.split(': ')[1].title() if ':' in x else x)
    
    fig_bar = px.bar(
        sector_topic, 
        x='Percentage', 
        y='Theme_Short', 
        color='App_Type',
        barmode='group',
        orientation='h',
        color_discrete_map={
            "Traditional Bank": "#ef4444", 
            "Digital Fintech": "#10b981"
        }
    )
    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title="% of Total Reviews", showgrid=True, gridcolor='#334155', tickfont=dict(color='#94a3b8')),
        yaxis=dict(title="", showgrid=False, tickfont=dict(color='#f8fafc')),
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="left", x=0, font=dict(color='#94a3b8', size=11), title=""),
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ─────────────────────────────────────────────
# DASHBOARD UI: QUALITATIVE DATA EXPLORER
# ─────────────────────────────────────────────
st.markdown("<h3 style='color:#f8fafc; font-size:1.1rem; text-transform:uppercase; letter-spacing:0.05em; margin-top:2rem;'>Qualitative Evidence Explorer</h3>", unsafe_allow_html=True)
st.markdown("<p style='color:#94a3b8; font-size:0.9rem; margin-bottom: 1rem;'>Read the raw, unedited voice of the customer filtered by the AI's discovered themes.</p>", unsafe_allow_html=True)

# Let the user filter the dataframe
col_filter1, col_filter2 = st.columns(2)
with col_filter1:
    selected_theme = st.selectbox("Filter by Theme:", df['Topic_Name'].unique())
with col_filter2:
    selected_sector = st.selectbox("Filter by Sector:", ["All"] + list(df['App_Type'].unique()))

# Apply filters
filtered_df = df[df['Topic_Name'] == selected_theme]
if selected_sector != "All":
    filtered_df = filtered_df[filtered_df['App_Type'] == selected_sector]

# Display the top 10 most relevant reviews (sorting by lowest score first to see complaints)
display_df = filtered_df[['App_Category', 'Score', 'Review_Content']].sort_values(by='Score').head(10)

# Rename columns for the display table
display_df.columns = ["App Name", "Star Rating", "Raw Customer Review"]

st.dataframe(display_df, use_container_width=True, hide_index=True)