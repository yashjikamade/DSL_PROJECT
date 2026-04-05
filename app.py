import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SpendSage · Smart Expense Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=Figtree:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #f5f3ef !important;
    color: #1a1a1a !important;
    font-family: 'Figtree', sans-serif !important;
}
[data-testid="stAppViewContainer"] > .main { background: #f5f3ef !important; }
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none; }
.block-container { 
    padding: 0 2.5rem 4rem !important; 
    max-width: 1280px !important; 
}

/* ── Topbar ── */
.topbar {
    background: #1a1a1a;
    padding: 0 3rem;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 0 -2.5rem 2.5rem;
    position: sticky;
    top: 0;
    z-index: 100;
}
.topbar-logo {
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 800;
    color: #fff;
    letter-spacing: -0.03em;
}
.topbar-logo span { color: #c8f06e; }
.topbar-nav {
    display: flex;
    gap: 2rem;
    font-size: 13px;
    color: #888;
    font-weight: 500;
}
.topbar-badge {
    background: #c8f06e;
    color: #1a1a1a;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 100px;
    letter-spacing: 0.04em;
}

/* ── Hero ── */
.hero {
    background: #1a1a1a;
    border-radius: 24px;
    padding: 3.5rem 4rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    align-items: center;
}
.hero-eyebrow {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #c8f06e;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.hero-eyebrow::before {
    content: '';
    width: 24px;
    height: 2px;
    background: #c8f06e;
    border-radius: 2px;
}
.hero-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 3.4rem !important;
    font-weight: 800 !important;
    color: #ffffff !important;
    line-height: 1.05 !important;
    letter-spacing: -0.04em !important;
    margin-bottom: 20px !important;
}
.hero-title .accent { color: #c8f06e; }
.hero-desc {
    color: #888;
    font-size: 15px;
    line-height: 1.65;
    max-width: 420px;
}
.hero-stats {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
}
.hstat {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.4rem 1.5rem;
}
.hstat-num {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #c8f06e;
    line-height: 1;
    margin-bottom: 6px;
}
.hstat-label {
    font-size: 12px;
    color: #666;
    font-weight: 500;
}
.hero-decor {
    position: absolute;
    top: -80px; right: -80px;
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(200,240,110,0.06) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}

/* ── Section header ── */
.sec-header {
    display: flex;
    align-items: baseline;
    gap: 12px;
    margin-bottom: 1.2rem;
    margin-top: 0.5rem;
}
.sec-title {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: #1a1a1a;
    letter-spacing: -0.02em;
}
.sec-line {
    flex: 1;
    height: 1px;
    background: #e8e4dc;
}
.sec-count {
    font-size: 11px;
    color: #aaa;
    font-weight: 600;
    letter-spacing: 0.06em;
}

/* ── Card ── */
.card {
    background: #ffffff;
    border: 1px solid #e8e4dc;
    border-radius: 20px;
    padding: 1.8rem 2rem;
    margin-bottom: 1rem;
}
.card-dark {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 20px;
    padding: 1.8rem 2rem;
    margin-bottom: 1rem;
}

/* ── Number input overrides ── */
[data-testid="stNumberInput"] {
    margin-bottom: 0 !important;
}
[data-testid="stNumberInput"] label {
    font-size: 12px !important;
    font-weight: 600 !important;
    color: #666 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    font-family: 'Figtree', sans-serif !important;
    margin-bottom: 6px !important;
}
[data-testid="stNumberInput"] input {
    background: #f8f6f2 !important;
    border: 1.5px solid #e8e4dc !important;
    border-radius: 12px !important;
    color: #1a1a1a !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    font-family: 'Syne', sans-serif !important;
    padding: 12px 16px !important;
    transition: border-color 0.2s !important;
}
[data-testid="stNumberInput"] input:focus {
    border-color: #1a1a1a !important;
    box-shadow: 0 0 0 3px rgba(26,26,26,0.06) !important;
    outline: none !important;
}
[data-testid="stNumberInput"] button {
    background: #f8f6f2 !important;
    border: 1.5px solid #e8e4dc !important;
    color: #666 !important;
    border-radius: 10px !important;
}

/* ── Input group label ── */
.input-group {
    margin-bottom: 1.4rem;
}
.input-icon-label {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    font-weight: 600;
    color: #444;
    margin-bottom: 6px;
}
.input-emoji { font-size: 16px; }

/* ── Allocation bar ── */
.alloc-bar-wrap {
    background: #f8f6f2;
    border: 1px solid #e8e4dc;
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    margin: 1rem 0;
}
.alloc-bar-top {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 10px;
}
.alloc-label { font-size: 12px; color: #999; font-weight: 500; }
.alloc-amount { font-family: 'Syne', sans-serif; font-size: 18px; font-weight: 700; color: #1a1a1a; }
.alloc-of { font-size: 13px; color: #bbb; font-weight: 400; }
.alloc-track { background: #e8e4dc; border-radius: 8px; height: 8px; overflow: hidden; }
.alloc-fill { height: 8px; border-radius: 8px; transition: width 0.4s ease; }
.alloc-pct { font-size: 11px; color: #bbb; margin-top: 6px; font-weight: 500; }

/* ── Metric cards ── */
.metrics-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.mcard {
    background: #fff;
    border: 1px solid #e8e4dc;
    border-radius: 18px;
    padding: 1.4rem 1.5rem;
    position: relative;
    overflow: hidden;
}
.mcard-accent {
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 18px 18px 0 0;
}
.mcard-label {
    font-size: 11px;
    font-weight: 600;
    color: #aaa;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 10px;
    margin-top: 4px;
}
.mcard-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.7rem;
    font-weight: 800;
    color: #1a1a1a;
    line-height: 1;
    letter-spacing: -0.03em;
}
.mcard-sub {
    font-size: 11px;
    color: #bbb;
    margin-top: 6px;
    font-weight: 500;
}

/* ── Alert ── */
.alert {
    border-radius: 14px;
    padding: 14px 18px;
    font-size: 13px;
    margin-bottom: 1rem;
    display: flex;
    align-items: flex-start;
    gap: 12px;
    line-height: 1.55;
    font-weight: 500;
}
.alert-success { background: #f0fdf4; border: 1px solid #bbf7d0; color: #166534; }
.alert-warning { background: #fffbeb; border: 1px solid #fde68a; color: #92400e; }
.alert-danger  { background: #fef2f2; border: 1px solid #fecaca; color: #991b1b; }
.alert-info    { background: #eff6ff; border: 1px solid #bfdbfe; color: #1e40af; }

/* ── Progress bars (breakdown) ── */
.bk-row { margin-bottom: 16px; }
.bk-meta { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 5px; }
.bk-name { font-size: 13px; font-weight: 600; color: #333; }
.bk-amt  { font-size: 13px; font-weight: 700; color: #1a1a1a; }
.bk-pct  { font-size: 11px; color: #bbb; margin-left: 6px; }
.bk-track { background: #f0ede8; border-radius: 6px; height: 7px; overflow: hidden; }
.bk-fill  { height: 7px; border-radius: 6px; }

/* ── Tip card ── */
.tip {
    background: #f8f6f2;
    border-left: 3px solid #1a1a1a;
    border-radius: 0 12px 12px 0;
    padding: 12px 16px;
    font-size: 13px;
    color: #444;
    margin-bottom: 10px;
    line-height: 1.6;
}

/* ── Health score ── */
.score-ring-wrap {
    text-align: center;
    padding: 2rem 1.5rem;
}
.score-number {
    font-family: 'Syne', sans-serif;
    font-size: 5rem;
    font-weight: 800;
    line-height: 1;
    letter-spacing: -0.05em;
}
.score-grade {
    display: inline-block;
    padding: 6px 18px;
    border-radius: 100px;
    font-size: 13px;
    font-weight: 700;
    margin-top: 10px;
    letter-spacing: 0.06em;
}
.score-bar-bg { background: #f0ede8; border-radius: 10px; height: 10px; overflow: hidden; margin: 16px 0 8px; }
.score-bar-fill { height: 10px; border-radius: 10px; }

/* ── What-if ── */
.wi-result {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin: 1.5rem 0;
}

/* ── Tab overrides ── */
[data-baseweb="tab-list"] {
    background: #ffffff !important;
    border: 1px solid #e8e4dc !important;
    border-radius: 14px !important;
    padding: 5px !important;
    gap: 3px !important;
    margin-bottom: 1.5rem !important;
}
[data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 10px !important;
    color: #999 !important;
    font-family: 'Figtree', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    padding: 9px 22px !important;
    transition: all 0.2s !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    background: #1a1a1a !important;
    color: #fff !important;
}
[data-baseweb="tab-highlight"],
[data-baseweb="tab-border"] { display: none !important; }

/* ── Button ── */
.stButton > button {
    background: #1a1a1a !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 16px 28px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    font-family: 'Syne', sans-serif !important;
    letter-spacing: -0.01em !important;
    width: 100% !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #333 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.15) !important;
}

/* ── Divider ── */
hr { border-color: #e8e4dc !important; }

/* ── Footer ── */
.footer {
    text-align: center;
    color: #ccc;
    font-size: 12px;
    margin-top: 4rem;
    padding-top: 1.5rem;
    border-top: 1px solid #e8e4dc;
    font-weight: 500;
    letter-spacing: 0.04em;
}

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Model ─────────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    df = pd.read_csv("monthly_spending_dataset_2020_2025.csv")
    X = df[['Income (₹)', 'Savings (₹)', 'Rent (₹)', 'Groceries (₹)', 'Transportation (₹)']]
    y = df['Total Expenditure (₹)']
    m = LinearRegression()
    m.fit(X, y)
    return m

model = load_model()

def run_prediction(income, savings, rent, groceries, transport):
    return max(float(model.predict([[income, savings, rent, groceries, transport]])[0]), 0)

CAT_COLORS = {
    "Rent":          "#1a1a1a",
    "Groceries":     "#4ade80",
    "Transport":     "#facc15",
    "Utilities":     "#60a5fa",
    "Dining Out":    "#f97316",
    "Entertainment": "#e879f9",
    "Medical":       "#22d3ee",
    "Savings":       "#c8f06e",
}

PLOT_BG   = "rgba(0,0,0,0)"
FONT_CLR  = "#999"
GRID_CLR  = "rgba(0,0,0,0.05)"


# ── Topbar ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <div class="topbar-logo">Spend<span>Sage</span></div>
    <div class="topbar-nav">
        <span>Dashboard</span>
        <span>Insights</span>
        <span>Reports</span>
    </div>
    <div class="topbar-badge">ML POWERED</div>
</div>
""", unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-decor"></div>
    <div class="hero-grid">
        <div>
            <div class="hero-eyebrow">Intelligent Finance</div>
            <div class="hero-title">Know where your<br>money <span class="accent">goes.</span></div>
            <p class="hero-desc">
                SpendSage uses machine learning trained on 5 years of Indian household
                data to predict your monthly expenses, score your financial health,
                and surface personalised savings opportunities.
            </p>
        </div>
        <div class="hero-stats">
            <div class="hstat">
                <div class="hstat-num">60K</div>
                <div class="hstat-label">Training data points</div>
            </div>
            <div class="hstat">
                <div class="hstat-num">99.1%</div>
                <div class="hstat-label">Model accuracy (R²)</div>
            </div>
            <div class="hstat">
                <div class="hstat-num">5 yrs</div>
                <div class="hstat-label">Historical data range</div>
            </div>
            <div class="hstat">
                <div class="hstat-num">4</div>
                <div class="hstat-label">Analysis modules</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "  ◈  Input & Predict  ",
    "  ▦  Breakdown  ",
    "  ◎  What-If Simulator  ",
    "  ◉  Health Score  ",
])


# ─── TAB 1 ────────────────────────────────────────────────────────────────────
with tab1:

    # ── Income card ──
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="sec-header"><div class="sec-title">Monthly Income</div><div class="sec-line"></div><div class="sec-count">₹ INR</div></div>', unsafe_allow_html=True)

    income = st.number_input(
        "Monthly Income (₹)", min_value=0, max_value=10_000_000,
        value=100_000, step=1_000, format="%d", label_visibility="collapsed",
        key="ni_income"
    )

    if income < 30_000:    tier, tc = "Entry Level", "#f59e0b"
    elif income < 75_000:  tier, tc = "Mid Level",   "#3b82f6"
    elif income < 2_00_000:tier, tc = "Upper Mid",   "#10b981"
    else:                  tier, tc = "High Earner", "#c8f06e"

    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;margin-top:10px;">
        <div>
            <div style="font-family:'Syne',sans-serif;font-size:2.2rem;font-weight:800;
                        color:#1a1a1a;letter-spacing:-0.04em;line-height:1;">
                ₹{income:,}
            </div>
            <div style="font-size:12px;color:#aaa;margin-top:4px;font-weight:500;">per month</div>
        </div>
        <div style="background:{tc}18;border:1.5px solid {tc}44;color:{tc};
               font-size:12px;font-weight:700;padding:8px 16px;border-radius:100px;
               letter-spacing:0.06em;text-transform:uppercase;">{tier}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Expense inputs ──
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="sec-header"><div class="sec-title">Monthly Expenses</div><div class="sec-line"></div><div class="sec-count">8 categories</div></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")

    with c1:
        st.markdown('<div style="font-size:11px;font-weight:700;color:#aaa;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:10px;">Essential</div>', unsafe_allow_html=True)
        rent = st.number_input(
            "🏠 Rent / EMI (₹)", min_value=0, max_value=500_000,
            value=20_000, step=500, format="%d", key="ni_rent"
        )
        groceries = st.number_input(
            "🛒 Groceries (₹)", min_value=0, max_value=100_000,
            value=8_000, step=250, format="%d", key="ni_groc"
        )
        utilities = st.number_input(
            "💡 Utilities (₹)", min_value=0, max_value=50_000,
            value=2_500, step=100, format="%d", key="ni_util"
        )
        medical = st.number_input(
            "🏥 Medical (₹)", min_value=0, max_value=100_000,
            value=1_500, step=100, format="%d", key="ni_med"
        )

    with c2:
        st.markdown('<div style="font-size:11px;font-weight:700;color:#aaa;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:10px;">Lifestyle</div>', unsafe_allow_html=True)
        transport = st.number_input(
            "🚗 Transportation (₹)", min_value=0, max_value=100_000,
            value=3_000, step=250, format="%d", key="ni_trans"
        )
        dining = st.number_input(
            "🍽️ Dining Out (₹)", min_value=0, max_value=100_000,
            value=4_000, step=250, format="%d", key="ni_dining"
        )
        entertainment = st.number_input(
            "🎬 Entertainment (₹)", min_value=0, max_value=50_000,
            value=2_000, step=100, format="%d", key="ni_ent"
        )
        savings = st.number_input(
            "🏦 Monthly Savings (₹)", min_value=0, max_value=1_000_000,
            value=15_000, step=500, format="%d", key="ni_sav"
        )

    # ── Live allocation bar ──
    manual_total = rent + groceries + utilities + medical + transport + dining + entertainment + savings
    pct_alloc = min(manual_total / income * 100, 100) if income > 0 else 0
    bar_color = "#ef4444" if pct_alloc > 90 else "#f59e0b" if pct_alloc > 70 else "#22c55e"

    st.markdown(f"""
    <div class="alloc-bar-wrap" style="margin-top:1rem;">
        <div class="alloc-bar-top">
            <span class="alloc-label">Budget allocated</span>
            <span class="alloc-amount">₹{manual_total:,}
                <span class="alloc-of">/ ₹{income:,}</span>
            </span>
        </div>
        <div class="alloc-track">
            <div class="alloc-fill" style="width:{pct_alloc:.1f}%;background:{bar_color};"></div>
        </div>
        <div class="alloc-pct">{pct_alloc:.1f}% of income allocated across all categories</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Predict button ──
    if st.button("◈  Analyse My Spending", use_container_width=True):
        pred = run_prediction(income, savings, rent, groceries, transport)
        st.session_state.update({
            "pred": pred, "income": income, "savings": savings,
            "rent": rent, "groceries": groceries, "transport": transport,
            "utilities": utilities, "dining": dining,
            "entertainment": entertainment, "medical": medical,
        })
        st.markdown(f"""
        <div class="alert alert-success" style="margin-top:1rem;">
            <span style="font-size:18px;">✦</span>
            <span>Prediction complete — your estimated monthly spend is
            <strong style="font-size:15px;">₹{pred:,.0f}</strong>.
            Open <strong>Breakdown</strong> for your full analysis.</span>
        </div>
        """, unsafe_allow_html=True)


# ─── TAB 2 ────────────────────────────────────────────────────────────────────
with tab2:
    if "pred" not in st.session_state:
        st.markdown('<div class="alert alert-info" style="margin-top:1rem;"><span>ℹ️</span><span>Run a prediction in <strong>Input & Predict</strong> first.</span></div>', unsafe_allow_html=True)
    else:
        pred          = st.session_state["pred"]
        income        = st.session_state["income"]
        savings       = st.session_state["savings"]
        rent          = st.session_state["rent"]
        groceries     = st.session_state["groceries"]
        transport     = st.session_state["transport"]
        utilities     = st.session_state["utilities"]
        dining        = st.session_state["dining"]
        entertainment = st.session_state["entertainment"]
        medical       = st.session_state["medical"]

        ratio  = pred / income * 100 if income > 0 else 0
        remain = income - pred

        # ── Metrics ──
        st.markdown('<div class="metrics-row">', unsafe_allow_html=True)
        metric_data = [
            ("Predicted Expense",  f"₹{pred:,.0f}",             "ML model output",           "#1a1a1a"),
            ("Remaining Income",   f"₹{abs(remain):,.0f}",      "surplus" if remain >= 0 else "deficit", "#22c55e" if remain >= 0 else "#ef4444"),
            ("Expense Ratio",      f"{ratio:.1f}%",             "of monthly income",          "#22c55e" if ratio < 70 else "#f59e0b" if ratio < 90 else "#ef4444"),
            ("Annual Surplus",     f"₹{max(remain,0)*12:,.0f}", "projected over 12 months",  "#c8f06e"),
        ]
        cols = st.columns(4, gap="small")
        for col, (lbl, val, sub, color) in zip(cols, metric_data):
            col.markdown(f"""
            <div class="mcard">
                <div class="mcard-accent" style="background:{color};"></div>
                <div class="mcard-label">{lbl}</div>
                <div class="mcard-value">{val}</div>
                <div class="mcard-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

        # ── Status alert ──
        if ratio > 90:
            st.markdown('<div class="alert alert-danger"><span>🚨</span><span><strong>Critical:</strong> Spending over 90% of income — immediate action needed to avoid debt.</span></div>', unsafe_allow_html=True)
        elif ratio > 70:
            st.markdown(f'<div class="alert alert-warning"><span>⚠️</span><span><strong>Caution:</strong> {ratio:.1f}% expense ratio. Reduce by ₹{pred - income*0.70:,.0f} to reach the healthy 70% threshold.</span></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="alert alert-success"><span>✅</span><span><strong>Healthy:</strong> Your {ratio:.1f}% expense ratio is well within safe limits. Keep it up.</span></div>', unsafe_allow_html=True)

        # ── Charts ──
        cat_vals = {
            "Rent": rent, "Groceries": groceries, "Transport": transport,
            "Utilities": utilities, "Dining Out": dining,
            "Entertainment": entertainment, "Medical": medical, "Savings": savings,
        }
        df_c = pd.DataFrame([
            {"Category": k, "Amount": v, "Color": CAT_COLORS[k]}
            for k, v in cat_vals.items() if v > 0
        ]).sort_values("Amount", ascending=False)
        total_entered = df_c["Amount"].sum()

        left_col, right_col = st.columns([3, 2], gap="large")

        with left_col:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="sec-header"><div class="sec-title">Spending by Category</div><div class="sec-line"></div></div>', unsafe_allow_html=True)
            for _, row in df_c.iterrows():
                pct = row["Amount"] / total_entered * 100 if total_entered > 0 else 0
                st.markdown(f"""
                <div class="bk-row">
                    <div class="bk-meta">
                        <span class="bk-name">{row['Category']}</span>
                        <span class="bk-amt">₹{row['Amount']:,}<span class="bk-pct">({pct:.1f}%)</span></span>
                    </div>
                    <div class="bk-track">
                        <div class="bk-fill" style="width:{pct:.1f}%;background:{row['Color']};"></div>
                    </div>
                </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with right_col:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="sec-header"><div class="sec-title">Distribution</div><div class="sec-line"></div></div>', unsafe_allow_html=True)
            fig_pie = go.Figure(go.Pie(
                labels=df_c["Category"], values=df_c["Amount"],
                hole=0.6,
                marker_colors=df_c["Color"].tolist(),
                textinfo="percent",
                textfont=dict(size=11, family="Figtree"),
                hovertemplate="<b>%{label}</b><br>₹%{value:,}<br>%{percent}<extra></extra>",
            ))
            fig_pie.update_layout(
                paper_bgcolor=PLOT_BG, plot_bgcolor=PLOT_BG,
                margin=dict(l=0, r=0, t=0, b=0), height=260,
                showlegend=True,
                legend=dict(
                    font=dict(size=11, color="#999", family="Figtree"),
                    bgcolor="rgba(0,0,0,0)", x=1, y=0.5
                ),
                annotations=[dict(
                    text=f"<b>₹{total_entered:,}</b>",
                    x=0.38, y=0.5,
                    font=dict(size=13, color="#1a1a1a", family="Syne"),
                    showarrow=False
                )],
            )
            st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Tips ──
        tips = []
        if rent > income * 0.35:
            tips.append(f"🏠 <strong>Rent</strong> is {rent/income*100:.0f}% of income (target &lt;30%). A flatmate or relocation could save ₹{rent - income*0.30:,.0f}/month.")
        if dining > income * 0.10:
            tips.append(f"🍽️ <strong>Dining Out</strong> at {dining/income*100:.0f}% of income is high. Cooking at home 3–4x/week could free ₹{dining*0.4:,.0f}/month.")
        if savings < income * 0.20:
            tips.append(f"🏦 <strong>Savings</strong> is below the 20% rule. Automate ₹{income*0.20 - savings:,.0f} more each payday to close the gap.")
        if entertainment > income * 0.07:
            tips.append(f"🎬 <strong>Entertainment</strong> ({entertainment/income*100:.0f}%) is elevated. Audit subscriptions and cancel unused ones.")
        if medical > income * 0.08:
            tips.append(f"🏥 High <strong>Medical</strong> spend ({medical/income*100:.0f}%). A health insurance plan could reduce out-of-pocket costs significantly.")
        if transport > income * 0.12:
            tips.append(f"🚗 <strong>Transport</strong> ({transport/income*100:.0f}%) is above ideal. Public transit or carpooling could reduce this.")

        if tips:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="sec-header"><div class="sec-title">Personalised Recommendations</div><div class="sec-line"></div></div>', unsafe_allow_html=True)
            for t in tips:
                st.markdown(f'<div class="tip">{t}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)


# ─── TAB 3 ────────────────────────────────────────────────────────────────────
with tab3:
    if "pred" not in st.session_state:
        st.markdown('<div class="alert alert-info" style="margin-top:1rem;"><span>ℹ️</span><span>Run a prediction first to unlock the simulator.</span></div>', unsafe_allow_html=True)
    else:
        income    = st.session_state["income"]
        orig = {
            "Rent":          st.session_state["rent"],
            "Groceries":     st.session_state["groceries"],
            "Transport":     st.session_state["transport"],
            "Utilities":     st.session_state["utilities"],
            "Dining Out":    st.session_state["dining"],
            "Entertainment": st.session_state["entertainment"],
            "Medical":       st.session_state["medical"],
        }
        orig_total = sum(orig.values())

        st.markdown('<div class="alert alert-info"><span>◎</span><span>Adjust the values below your current spending to simulate how cuts in each category affect your monthly and annual savings.</span></div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="sec-header"><div class="sec-title">Adjust Category Spending</div><div class="sec-line"></div></div>', unsafe_allow_html=True)

        new_vals = {}
        w1, w2 = st.columns(2, gap="large")
        for i, (cat, val) in enumerate(orig.items()):
            with (w1 if i % 2 == 0 else w2):
                new_vals[cat] = st.number_input(
                    f"{cat} (₹)", min_value=0, max_value=max(val * 2, 1000),
                    value=val, step=100, format="%d", key=f"wi_{cat}"
                )
        st.markdown('</div>', unsafe_allow_html=True)

        new_total     = sum(new_vals.values())
        monthly_saved = orig_total - new_total
        annual_saved  = monthly_saved * 12

        cols4 = st.columns(4, gap="small")
        wi_cards = [
            ("New Monthly Total",  f"₹{new_total:,}",        f"was ₹{orig_total:,}",          "#1a1a1a"),
            ("Monthly Saving",     f"₹{monthly_saved:,}",    "freed up each month",           "#22c55e" if monthly_saved >= 0 else "#ef4444"),
            ("Annual Saving",      f"₹{annual_saved:,}",     "projected over 12 months",      "#c8f06e" if annual_saved >= 0 else "#ef4444"),
            ("New Expense Ratio",  f"{new_total/income*100:.1f}%", "of monthly income",       "#22c55e" if new_total/income < 0.7 else "#f59e0b"),
        ]
        for col, (lbl, val, sub, color) in zip(cols4, wi_cards):
            col.markdown(f"""
            <div class="mcard">
                <div class="mcard-accent" style="background:{color};"></div>
                <div class="mcard-label">{lbl}</div>
                <div class="mcard-value">{val}</div>
                <div class="mcard-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

        diffs  = [orig[c] - new_vals[c] for c in orig]
        colors = ["#22c55e" if d >= 0 else "#ef4444" for d in diffs]

        fig_wf = go.Figure(go.Bar(
            x=list(orig.keys()), y=diffs,
            marker_color=colors,
            text=[f"₹{d:+,}" for d in diffs],
            textposition="outside",
            textfont=dict(size=11, color="#999", family="Figtree"),
        ))
        fig_wf.update_layout(
            paper_bgcolor=PLOT_BG,
            plot_bgcolor="#fafaf8",
            font=dict(family="Figtree", color="#999"),
            margin=dict(l=10, r=10, t=30, b=10), height=280,
            title=dict(
                text="Savings per category — green: reduced  ·  red: increased",
                font=dict(size=12, color="#aaa", family="Figtree"), x=0
            ),
            xaxis=dict(showgrid=False, color="#bbb"),
            yaxis=dict(
                showgrid=True, gridcolor=GRID_CLR,
                zeroline=True, zerolinecolor="rgba(0,0,0,0.1)", color="#bbb"
            ),
        )
        st.plotly_chart(fig_wf, use_container_width=True, config={"displayModeBar": False})

        if monthly_saved > 0:
            st.markdown(f"""<div class="alert alert-success">
                <span>🎯</span>
                <span>These adjustments free up <strong>₹{monthly_saved:,}/month</strong> — that's
                <strong>₹{annual_saved:,}/year</strong>. Over 5 years, that's ₹{annual_saved*5:,}
                — enough to build a solid emergency fund or investment corpus.</span>
            </div>""", unsafe_allow_html=True)


# ─── TAB 4 ────────────────────────────────────────────────────────────────────
with tab4:
    if "pred" not in st.session_state:
        st.markdown('<div class="alert alert-info" style="margin-top:1rem;"><span>ℹ️</span><span>Run a prediction first to generate your Financial Health Score.</span></div>', unsafe_allow_html=True)
    else:
        pred          = st.session_state["pred"]
        income        = st.session_state["income"]
        savings       = st.session_state["savings"]
        rent          = st.session_state["rent"]
        dining        = st.session_state["dining"]
        entertainment = st.session_state["entertainment"]

        def clamp(v): return max(0.0, min(float(v), 20.0))

        sav_rate  = savings / income if income > 0 else 0
        exp_ratio = pred / income if income > 0 else 1
        rent_r    = rent / income if income > 0 else 1
        disc      = (dining + entertainment) / income if income > 0 else 1
        buffer    = (income - pred) / income if income > 0 else 0

        s1 = clamp(sav_rate / 0.20 * 20)
        s2 = clamp((1 - exp_ratio) / 0.30 * 20)
        s3 = clamp((1 - rent_r / 0.35) * 20)
        s4 = clamp((1 - disc / 0.17) * 20)
        s5 = clamp(buffer / 0.10 * 20)
        score = int(s1 + s2 + s3 + s4 + s5)

        if score >= 80:   grade, gc, gl = "A", "#22c55e", "Excellent"
        elif score >= 65: grade, gc, gl = "B", "#3b82f6", "Good"
        elif score >= 50: grade, gc, gl = "C", "#f59e0b", "Fair"
        elif score >= 35: grade, gc, gl = "D", "#f97316", "Needs Work"
        else:             grade, gc, gl = "F", "#ef4444", "Critical"

        left_col, right_col = st.columns([1, 2], gap="large")

        with left_col:
            st.markdown(f"""
            <div class="card" style="text-align:center;padding:2.5rem 1.5rem;">
                <div style="font-size:11px;font-weight:700;color:#aaa;text-transform:uppercase;
                            letter-spacing:0.1em;margin-bottom:16px;">Financial Health Score</div>
                <div class="score-number" style="color:{gc};">{score}</div>
                <div style="font-size:13px;color:#bbb;margin:4px 0 14px;">out of 100</div>
                <div class="score-grade" style="background:{gc}18;border:1.5px solid {gc}44;color:{gc};">
                    Grade {grade} &nbsp;·&nbsp; {gl}
                </div>
                <div class="score-bar-bg">
                    <div class="score-bar-fill" style="width:{score}%;background:{gc};"></div>
                </div>
                <div style="font-size:11px;color:#ccc;margin-top:4px;">{score}/100 overall</div>
            </div>
            """, unsafe_allow_html=True)

        with right_col:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="sec-header"><div class="sec-title">Score Breakdown</div><div class="sec-line"></div></div>', unsafe_allow_html=True)

            breakdown = [
                ("Savings Rate",        s1, f"{sav_rate*100:.1f}% saved (target ≥ 20%)",              "#22c55e"),
                ("Expense Control",     s2, f"{exp_ratio*100:.1f}% expense ratio (target < 70%)",     "#3b82f6"),
                ("Rent Burden",         s3, f"{rent/income*100:.1f}% on rent (target < 30%)",         "#8b5cf6"),
                ("Discretionary Spend", s4, f"{disc*100:.1f}% on dining + entertainment",             "#f97316"),
                ("Monthly Buffer",      s5, f"₹{max(income-pred,0):,} left after all expenses",       "#06b6d4"),
            ]
            for name, sc, detail, color in breakdown:
                pct = sc / 20 * 100
                st.markdown(f"""
                <div class="bk-row">
                    <div class="bk-meta">
                        <span class="bk-name">{name}</span>
                        <span style="font-size:13px;font-weight:700;color:{color};">{int(sc)}/20</span>
                    </div>
                    <div style="font-size:11px;color:#bbb;margin-bottom:6px;">{detail}</div>
                    <div class="bk-track">
                        <div class="bk-fill" style="width:{pct:.1f}%;background:{color};"></div>
                    </div>
                </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Radar ──
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="sec-header"><div class="sec-title">Financial Profile Radar</div><div class="sec-line"></div></div>', unsafe_allow_html=True)

        r_cats = ["Savings Rate", "Expense Control", "Rent Burden", "Discretionary", "Buffer"]
        r_vals = [s1/20*100, s2/20*100, s3/20*100, s4/20*100, s5/20*100]
        r_vals_c = r_vals + [r_vals[0]]
        r_cats_c = r_cats + [r_cats[0]]

        fig_r = go.Figure()
        fig_r.add_trace(go.Scatterpolar(
            r=[100]*6, theta=r_cats_c, fill="toself",
            fillcolor="rgba(0,0,0,0.02)",
            line=dict(color="rgba(0,0,0,0.08)", width=1),
            showlegend=False,
        ))
        fig_r.add_trace(go.Scatterpolar(
            r=r_vals_c, theta=r_cats_c, fill="toself",
            fillcolor="rgba(26,26,26,0.08)",
            line=dict(color="#1a1a1a", width=2.5),
            marker=dict(size=8, color="#c8f06e", line=dict(color="#1a1a1a", width=2)),
            showlegend=False,
        ))
        fig_r.update_layout(
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(
                    visible=True, range=[0, 100],
                    tickfont=dict(size=9, color="#bbb", family="Figtree"),
                    gridcolor=GRID_CLR
                ),
                angularaxis=dict(
                    tickfont=dict(size=12, color="#666", family="Figtree"),
                    gridcolor=GRID_CLR
                ),
            ),
            paper_bgcolor=PLOT_BG,
            margin=dict(l=50, r=50, t=20, b=20),
            height=320,
        )
        st.plotly_chart(fig_r, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    SpendSage &nbsp;·&nbsp; Smart Expense Intelligence
    &nbsp;·&nbsp; Powered by Scikit-learn &amp; Streamlit
    &nbsp;·&nbsp; Model trained on 2020–2025 Indian household data
</div>
""", unsafe_allow_html=True)