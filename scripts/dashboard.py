import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import subprocess
import time

st.set_page_config(page_title="Mkn Ops", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #0E1117 !important;
        color: #E0E0E0 !important;
    }
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"], [data-testid="stMetric"] {
        background-color: #161B22 !important;
        color: #E0E0E0 !important;
        border-radius: 8px;
        padding: 10px;
    }
    .stTabs [data-baseweb="tab-list"] {
        background-color: #0E1117 !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #888888 !important;
        background-color: transparent !important;
    }
    .stTabs [aria-selected="true"] {
        color: #007BFF !important;
        border-bottom: 2px solid #007BFF !important;
    }
    div.stButton > button {
        width: 100%; height: 4.5rem; font-size: 1.5rem !important;
        font-weight: bold !important; border-radius: 8px; border: none;
    }
    .stButton button[kind="primary"] {
        background-color: #007BFF !important;
        color: white !important;
    }
    .stButton button[kind="secondary"] {
        background-color: #21262D !important;
        color: #FF4B4B !important;
        border: 1px solid #30363D !important;
        height: 3rem !important;
        font-size: 1rem !important;
    }
    h1, h2, h3, h4, h5, h6, p, span, label {
        color: #E0E0E0 !important;
    }
    [data-testid="stDataFrame"] {
        background-color: #161B22 !important;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def get_engine():
    try:
        U, P, H, PRT, D = "admini_user", "mkn_e4444rRbdunwpbwEfb-e-w32221-dXcvv0i_ZAQPm2-1-_324", "postgres", "5432", "n8n_dbdb"
        return create_engine(f"postgresql+psycopg2://{U}:{P}@{H}:{PRT}/{D}")
    except: return None

engine = get_engine()

def fetch_data():
    if engine is None: return pd.DataFrame()
    try: return pd.read_sql("SELECT * FROM telemetry ORDER BY processed_at DESC LIMIT 1000", engine)
    except: return pd.DataFrame()

st.markdown("# 🏭 Mkn Industrial OS")
st.caption("v2.5.0-stable | Distributed Cluster Monitoring")

col_btn1, col_btn2 = st.columns([3, 1])

with col_btn1:
    if st.button("🚀 TRIGGER SYSTEM STRESS TEST", type="primary"):
        subprocess.Popen(["python3", "scripts/stress_test.py"], shell=False)
        st.toast("Stress Sequence Initialized", icon="🔥")

with col_btn2:
    if st.button("🗑️ RESET CLUSTER", type="secondary"):
        try:
            with engine.connect() as conn:
                conn.execute(text("TRUNCATE TABLE telemetry;"))
                conn.commit()
            st.toast("Database Cleared", icon="🗑️")
            time.sleep(0.5)
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

st.divider()

@st.fragment(run_every=2)
def live_dashboard():
    df = fetch_data()
    if df.empty:
        st.info("Awaiting telemetry link...")
        return

    m1, m2, m3 = st.columns(3)
    m1.metric("Ingested Events", len(df))
    w_col = 'worker_name' if 'worker_name' in df.columns else 'processed_by'
    nodes = df[w_col].nunique() if w_col in df.columns else 1
    m2.metric("Cluster Nodes", f"{nodes} Active")
    m3.metric("System Heartbeat", time.strftime('%H:%M:%S'))

    t1, t2 = st.tabs(["TELEMETRY", "CLUSTER LOAD"])

    with t1:
        if 'status' in df.columns:
            st.bar_chart(df['status'].value_counts(), color="#10B981", height=380)

    with t2:
        if w_col in df.columns:
            st.bar_chart(df[w_col].value_counts(), color="#3B82F6", height=380)

    st.markdown("### 📝 Node Activity Logs")
    cols = [c for c in [w_col, 'temperature', 'status', 'processed_at'] if c in df.columns]
    st.dataframe(df[cols].head(10), use_container_width=True, hide_index=True)

live_dashboard()
