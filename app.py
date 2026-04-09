import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(
    page_title="Expense Intelligence · Dashboard",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── dark mode ─────────────────────────────────────────────────
if "dark" not in st.session_state:
    st.session_state["dark"] = False
dk = st.session_state["dark"]

# ── colour tokens ─────────────────────────────────────────────
if dk:
    PAGE   = "#0e1117"
    S1     = "#161b27"
    S2     = "#1c2338"
    S3     = "#222a40"
    BD     = "#2a3350"
    BDS    = "#1f2940"
    T1     = "#eef1ff"
    T2     = "#7b8db8"
    T3     = "#3d4f73"
    INP    = "#0e1117"
    INP_BD = "#2a3350"
    NAV    = "#090d18"
    NAV_BD = "#141b2d"
    HERO   = "linear-gradient(150deg,#0a0e1c 0%,#0e1528 60%,#080c18 100%)"
    HBD    = "rgba(99,102,241,0.15)"
    SBG    = "rgba(99,102,241,0.06)"
    SBR    = "rgba(99,102,241,0.12)"
    PBG    = "rgba(0,0,0,0)"
    GBG    = "#161b27"
    GRD    = "rgba(255,255,255,0.04)"
    SHD    = "none"
    AG_B,AG_R,AG_T = "rgba(34,197,94,0.08)","rgba(34,197,94,0.2)","#4ade80"
    AY_B,AY_R,AY_T = "rgba(234,179,8,0.08)","rgba(234,179,8,0.2)","#fbbf24"
    AR_B,AR_R,AR_T = "rgba(239,68,68,0.08)","rgba(239,68,68,0.2)","#f87171"
    AN_B,AN_R,AN_T = "rgba(99,102,241,0.08)","rgba(99,102,241,0.2)","#a5b4fc"
    TI,TL  = "☀", "Light"
else:
    PAGE   = "#f5f7ff"
    S1     = "#ffffff"
    S2     = "#edf0ff"
    S3     = "#e2e6f8"
    BD     = "#c9d0ed"
    BDS    = "#dde2f5"
    T1     = "#0d1135"
    T2     = "#4a5580"
    T3     = "#9aa3c8"
    INP    = "#f5f7ff"
    INP_BD = "#c9d0ed"
    NAV    = "#0d1135"
    NAV_BD = "#162040"
    HERO   = "linear-gradient(150deg,#0d1135 0%,#141c45 60%,#0a0e28 100%)"
    HBD    = "rgba(99,102,241,0.2)"
    SBG    = "rgba(255,255,255,0.06)"
    SBR    = "rgba(255,255,255,0.1)"
    PBG    = "rgba(0,0,0,0)"
    GBG    = "#edf0ff"
    GRD    = "rgba(0,0,0,0.04)"
    SHD    = "0 1px 3px rgba(13,17,53,0.08)"
    AG_B,AG_R,AG_T = "#f0fdf4","#bbf7d0","#15803d"
    AY_B,AY_R,AY_T = "#fffbeb","#fde68a","#78350f"
    AR_B,AR_R,AR_T = "#fef2f2","#fecaca","#7f1d1d"
    AN_B,AN_R,AN_T = "#eef2ff","#c7d2fe","#3730a3"
    TI,TL  = "☽", "Dark"

IN  = "#6366f1"   # indigo primary
IN2 = "#4f46e5"   # indigo deep
IN3 = "#818cf8"   # indigo light
IN4 = "#e0e7ff"   # indigo pale

CAT = {
    "Rent":          "#6366f1",
    "Groceries":     "#10b981",
    "Transport":     "#f59e0b",
    "Utilities":     "#8b5cf6",
    "Dining Out":    "#f97316",
    "Entertainment": "#ec4899",
    "Medical":       "#06b6d4",
    "Savings":       "#22c55e",
}

def safe_int(val, default=0):
    try:
        v = str(val).replace(",","").replace("₹","").strip()
        return max(0, int(float(v))) if v else default
    except:
        return default

# ── CSS ───────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&family=DM+Mono:wght@400;500&display=swap');

*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0;}}

html,body,[data-testid="stAppViewContainer"]{{
  background:{PAGE}!important;color:{T1}!important;
  font-family:'DM Sans',system-ui,sans-serif!important;
}}
[data-testid="stAppViewContainer"]>.main{{background:{PAGE}!important;}}
[data-testid="stHeader"]{{display:none!important;}}
[data-testid="stToolbar"]{{display:none!important;}}
.block-container{{padding:0 2rem 6rem!important;max-width:1240px!important;}}

/* NAV */
.nav{{
  background:{NAV};border-bottom:1px solid {NAV_BD};
  height:58px;display:flex;align-items:center;
  justify-content:space-between;padding:0 2.5rem;
  margin:0 -2rem 2.5rem;position:sticky;top:0;z-index:1000;
}}
.nav-brand{{
  display:flex;align-items:center;gap:12px;
  font-size:14px;font-weight:600;color:rgba(255,255,255,0.85);
  letter-spacing:0.01em;
}}
.nav-icon{{
  width:32px;height:32px;border-radius:8px;
  background:linear-gradient(135deg,{IN2},{IN});
  display:flex;align-items:center;justify-content:center;
  font-size:16px;box-shadow:0 3px 12px rgba(99,102,241,0.4);
}}
.nav-sep{{width:1px;height:20px;background:rgba(255,255,255,0.1);}}
.nav-sub{{font-size:12px;color:rgba(255,255,255,0.3);font-weight:400;letter-spacing:0.04em;}}
.nav-r{{display:flex;align-items:center;gap:10px;}}
.nav-badge{{
  font-size:10px;font-weight:700;color:{IN3};
  background:rgba(99,102,241,0.12);border:1px solid rgba(99,102,241,0.22);
  padding:4px 10px;border-radius:5px;letter-spacing:0.1em;text-transform:uppercase;
}}

/* HERO */
.hero{{
  background:{HERO};border:1px solid {HBD};border-radius:18px;
  padding:2.8rem 3.5rem;margin-bottom:2rem;
  position:relative;overflow:hidden;
}}
.hg1{{
  position:absolute;top:-100px;right:-80px;width:380px;height:380px;
  background:radial-gradient(circle,rgba(99,102,241,0.1) 0%,transparent 65%);
  border-radius:50%;pointer-events:none;
}}
.hg2{{
  position:absolute;bottom:-60px;left:20%;width:220px;height:220px;
  background:radial-gradient(circle,rgba(99,102,241,0.05) 0%,transparent 70%);
  border-radius:50%;pointer-events:none;
}}
.hero-grid{{display:grid;grid-template-columns:1.2fr 0.8fr;gap:3rem;align-items:center;position:relative;}}
.hero-kicker{{
  font-size:10px;font-weight:700;letter-spacing:0.22em;text-transform:uppercase;
  color:{IN3};margin-bottom:14px;display:flex;align-items:center;gap:10px;
}}
.hero-kicker::before{{content:'';width:22px;height:1.5px;background:{IN3};border-radius:2px;}}
.hero-h1{{
  font-family:'DM Sans',sans-serif!important;font-size:2.65rem!important;
  font-weight:700!important;color:#fff!important;line-height:1.12!important;
  letter-spacing:-0.025em!important;margin-bottom:14px!important;
}}
.hero-h1 .hl{{
  background:linear-gradient(90deg,{IN3} 0%,#c4b5fd 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}}
.hero-desc{{font-size:14px;color:rgba(255,255,255,0.38);line-height:1.75;max-width:400px;}}
.hstats{{display:grid;grid-template-columns:1fr 1fr;gap:10px;}}
.hstat{{
  background:{SBG};border:1px solid {SBR};border-radius:12px;padding:1.2rem 1.4rem;
}}
.hstat-n{{
  font-family:'DM Mono',monospace;font-size:1.6rem;font-weight:500;
  color:{IN3};line-height:1;margin-bottom:4px;letter-spacing:-0.02em;
}}
.hstat-l{{font-size:11px;color:rgba(255,255,255,0.3);font-weight:500;letter-spacing:0.03em;}}

/* SECTION HEAD */
.sh{{display:flex;align-items:center;gap:12px;margin-bottom:1.2rem;}}
.sh-t{{
  font-size:11px;font-weight:700;color:{T3};
  letter-spacing:0.12em;text-transform:uppercase;white-space:nowrap;
}}
.sh-r{{flex:1;height:1px;background:{BDS};}}
.sh-b{{
  font-size:10px;font-weight:700;color:{IN};
  background:rgba(99,102,241,0.08);border:1px solid rgba(99,102,241,0.16);
  padding:2px 9px;border-radius:4px;letter-spacing:0.09em;
  text-transform:uppercase;white-space:nowrap;
}}

/* CARD */
.card{{
  background:{S1};border:1px solid {BD};border-radius:14px;
  padding:1.6rem 1.8rem;margin-bottom:1.2rem;box-shadow:{SHD};
}}

/* TEXT INPUTS — clean type-in fields */
[data-testid="stTextInput"] label{{
  font-size:11px!important;font-weight:700!important;color:{T3}!important;
  text-transform:uppercase!important;letter-spacing:0.1em!important;
  font-family:'DM Sans',sans-serif!important;margin-bottom:4px!important;
}}
[data-testid="stTextInput"] input{{
  background:{INP}!important;border:1px solid {INP_BD}!important;
  border-radius:9px!important;color:{T1}!important;
  font-size:16px!important;font-weight:600!important;
  font-family:'DM Mono',monospace!important;
  padding:11px 14px!important;
  transition:border-color 0.15s,box-shadow 0.15s!important;
  box-shadow:{SHD}!important;
}}
[data-testid="stTextInput"] input:focus{{
  border-color:{IN}!important;
  box-shadow:0 0 0 3px rgba(99,102,241,0.14)!important;outline:none!important;
}}
[data-testid="stTextInput"] input::placeholder{{color:{T3}!important;font-weight:400!important;}}

/* INCOME DISPLAY */
.inc-panel{{
  display:flex;align-items:center;justify-content:space-between;
  background:{S2};border:1px solid {BDS};
  border-left:3px solid {IN};border-radius:0 10px 10px 0;
  padding:13px 18px;margin-top:10px;
}}
.inc-v{{
  font-family:'DM Mono',monospace;font-size:1.9rem;font-weight:500;
  color:{T1};letter-spacing:-0.03em;line-height:1;
}}
.inc-s{{font-size:10px;color:{T3};margin-top:3px;text-transform:uppercase;letter-spacing:0.1em;}}
.tier-tag{{
  font-size:11px;font-weight:700;padding:5px 12px;
  border-radius:5px;text-transform:uppercase;letter-spacing:0.08em;
}}

/* GROUP HEAD */
.grp{{
  font-size:10px;font-weight:700;color:{T3};text-transform:uppercase;
  letter-spacing:0.16em;padding:10px 0;
  border-bottom:1px solid {BDS};margin-bottom:14px;
  display:flex;align-items:center;gap:8px;
}}
.grp-bar{{width:3px;height:13px;background:{IN};border-radius:2px;}}

/* ALLOC BAR */
.alloc{{
  background:{S2};border:1px solid {BDS};border-radius:12px;
  padding:1rem 1.4rem;margin-top:1rem;
}}
.alloc-top{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:9px;}}
.alloc-lbl{{font-size:11px;color:{T3};font-weight:600;letter-spacing:0.1em;text-transform:uppercase;}}
.alloc-n{{font-family:'DM Mono',monospace;font-size:15px;font-weight:600;color:{T1};}}
.alloc-of{{font-size:12px;color:{T3};margin-left:4px;}}
.alloc-trk{{background:{S3};border-radius:3px;height:4px;overflow:hidden;}}
.alloc-fill{{height:4px;border-radius:3px;transition:width 0.4s ease;}}
.alloc-note{{font-size:11px;color:{T3};margin-top:5px;}}

/* KPI CARDS */
.kpi{{
  background:{S1};border:1px solid {BD};border-radius:13px;
  padding:1.2rem 1.4rem;position:relative;overflow:hidden;box-shadow:{SHD};
}}
.kpi::before{{
  content:'';position:absolute;left:0;top:0;bottom:0;
  width:3px;border-radius:13px 0 0 13px;background:var(--ac);
}}
.kpi-l{{font-size:10px;font-weight:700;color:{T3};text-transform:uppercase;letter-spacing:0.12em;margin-bottom:9px;}}
.kpi-v{{font-family:'DM Mono',monospace;font-size:1.45rem;font-weight:500;color:{T1};line-height:1;letter-spacing:-0.02em;}}
.kpi-s{{font-size:11px;color:{T3};margin-top:5px;}}

/* ALERTS */
.alert{{
  display:flex;align-items:flex-start;gap:11px;border-radius:10px;
  padding:12px 16px;font-size:13px;line-height:1.55;
  font-weight:500;margin-bottom:1rem;
}}
.ai{{font-size:13px;flex-shrink:0;margin-top:1px;}}
.ag{{background:{AG_B};border:1px solid {AG_R};color:{AG_T};}}
.ay{{background:{AY_B};border:1px solid {AY_R};color:{AY_T};}}
.ar{{background:{AR_B};border:1px solid {AR_R};color:{AR_T};}}
.an{{background:{AN_B};border:1px solid {AN_R};color:{AN_T};}}

/* BARS */
.pb{{margin-bottom:16px;}}
.pb-top{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:4px;}}
.pb-name{{font-size:13px;font-weight:500;color:{T1};}}
.pb-val{{font-family:'DM Mono',monospace;font-size:12px;font-weight:500;color:{T1};}}
.pb-pct{{font-size:11px;color:{T3};margin-left:4px;}}
.pb-trk{{background:{S3};border-radius:3px;height:4px;overflow:hidden;}}
.pb-fill{{height:4px;border-radius:3px;}}

/* TIP */
.tip{{
  display:flex;gap:11px;align-items:flex-start;
  background:{S2};border:1px solid {BDS};border-left:3px solid {IN};
  border-radius:0 10px 10px 0;padding:12px 15px;
  font-size:13px;color:{T2};margin-bottom:9px;line-height:1.6;
}}
.tip-i{{font-size:14px;flex-shrink:0;margin-top:1px;}}

/* SCORE */
.score-wrap{{text-align:center;padding:2.2rem 1.4rem;}}
.score-n{{
  font-family:'DM Mono',monospace;font-size:5rem;font-weight:500;
  line-height:1;letter-spacing:-0.05em;
}}
.score-of{{font-size:13px;color:{T3};margin:3px 0 12px;}}
.score-chip{{
  display:inline-block;padding:5px 18px;border-radius:5px;
  font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;
}}
.score-bg{{background:{S3};border-radius:3px;height:5px;overflow:hidden;margin:16px 0 5px;}}
.score-bar{{height:5px;border-radius:3px;}}

/* TABS */
[data-baseweb="tab-list"]{{
  background:{S1}!important;border:1px solid {BD}!important;
  border-radius:11px!important;padding:4px!important;
  gap:2px!important;margin-bottom:1.75rem!important;box-shadow:{SHD}!important;
}}
[data-baseweb="tab"]{{
  background:transparent!important;border-radius:8px!important;
  color:{T3}!important;font-family:'DM Sans',sans-serif!important;
  font-size:13px!important;font-weight:600!important;
  padding:8px 20px!important;transition:all 0.15s!important;
}}
[aria-selected="true"][data-baseweb="tab"]{{
  background:linear-gradient(135deg,{IN2},{IN})!important;color:#fff!important;
  box-shadow:0 2px 10px rgba(99,102,241,0.35)!important;
}}
[data-baseweb="tab-highlight"],[data-baseweb="tab-border"]{{display:none!important;}}

/* BUTTON */
.stButton>button{{
  background:linear-gradient(135deg,{IN2} 0%,{IN} 100%)!important;
  color:#fff!important;border:none!important;border-radius:10px!important;
  padding:14px 24px!important;font-size:14px!important;font-weight:600!important;
  font-family:'DM Sans',sans-serif!important;width:100%!important;
  box-shadow:0 3px 14px rgba(99,102,241,0.35)!important;
  transition:all 0.2s!important;letter-spacing:0.01em!important;
}}
.stButton>button:hover{{
  box-shadow:0 6px 22px rgba(99,102,241,0.5)!important;
  transform:translateY(-1px)!important;
}}

/* TOGGLE */
.tog{{
  font-size:12px;font-weight:600;color:rgba(255,255,255,0.4);
  background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);
  border-radius:6px;padding:6px 12px;cursor:pointer;
  font-family:'DM Sans',sans-serif;letter-spacing:0.02em;
  white-space:nowrap;
}}

/* VALIDATION HINT */
.val-hint{{
  font-size:11px;color:#f87171;margin-top:3px;margin-left:2px;
  font-family:'DM Sans',sans-serif;
}}

#MainMenu,footer,header{{visibility:hidden;}}
hr{{border-color:{BDS}!important;}}
.footer{{
  text-align:center;color:{T3};font-size:11px;margin-top:5rem;
  padding-top:1.5rem;border-top:1px solid {BDS};
  letter-spacing:0.08em;text-transform:uppercase;font-weight:500;
}}
</style>
""", unsafe_allow_html=True)

# ── model ─────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    df = pd.read_csv("monthly_spending_dataset_2020_2025.csv")
    X  = df[["Income (₹)","Savings (₹)","Rent (₹)","Groceries (₹)",
             "Transportation (₹)","Utilities (₹)","Dining Out (₹)","Entertainment (₹)"]]
    y  = df["Total Expenditure (₹)"]
    m  = LinearRegression(); m.fit(X, y); return m

model = load_model()

def ml_predict(inc,sav,rent,groc,tr,util,din,ent):
    return max(float(model.predict([[inc,sav,rent,groc,tr,util,din,ent]])[0]),0)

def field(label, key, default, hint="e.g. 25000"):
    val = st.text_input(label, value=str(default), placeholder=hint, key=key)
    n   = safe_int(val, default)
    if val.strip() and n == 0 and val.strip() not in ("0",""):
        st.markdown('<div class="val-hint">Enter a valid number</div>', unsafe_allow_html=True)
    return n

# ── NAV ───────────────────────────────────────────────────────
nc1, nc2 = st.columns([11, 1])
with nc1:
    st.markdown(f"""
    <div class="nav">
      <div class="nav-brand">
        <div class="nav-icon">◆</div>
        Expense Intelligence
        <div class="nav-sep"></div>
        <div class="nav-sub">Personal Finance Dashboard</div>
      </div>
      <div class="nav-r">
        <div class="nav-badge">ML Engine</div>
      </div>
    </div>""", unsafe_allow_html=True)
with nc2:
    st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
    if st.button(f"{TI} {TL}", key="tog"):
        st.session_state["dark"] = not dk; st.rerun()

# ── HERO ──────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <div class="hg1"></div><div class="hg2"></div>
  <div class="hero-grid">
    <div>
      <div class="hero-kicker">ML-Powered Finance Analytics</div>
      <div class="hero-h1">Predict your spending.<br><span class="hl">Control your future.</span></div>
      <p class="hero-desc">
        Machine learning trained on 60,000+ Indian household records predicts
        your monthly expenses with 99.1% accuracy — then shows exactly
        where to cut back and save more.
      </p>
    </div>
    <div class="hstats">
      <div class="hstat"><div class="hstat-n">60K+</div><div class="hstat-l">Training records</div></div>
      <div class="hstat"><div class="hstat-n">99.1%</div><div class="hstat-l">R² accuracy</div></div>
      <div class="hstat"><div class="hstat-n">5 yrs</div><div class="hstat-l">Data coverage</div></div>
      <div class="hstat"><div class="hstat-n">8</div><div class="hstat-l">Expense categories</div></div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────
t1,t2,t3,t4 = st.tabs([
    "  Input & Predict  ",
    "  Breakdown  ",
    "  What-If Simulator  ",
    "  Health Score  ",
])

# ══════════════════════════════════════════════════════════════
# TAB 1 — INPUT
# ══════════════════════════════════════════════════════════════
with t1:
    st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)
    main_col, side_col = st.columns([3,1], gap="large")

    with main_col:
        # income
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<div class="sh"><div class="sh-t">Monthly Income</div><div class="sh-r"></div><div class="sh-b">Step 1 of 2</div></div>', unsafe_allow_html=True)
        income_raw = st.text_input("Take-home income per month (₹)", value="100000",
                                   placeholder="e.g. 85000", key="inc_raw")
        income = safe_int(income_raw, 100000)

        if   income < 30_000:  tier,tc,tbg = "Entry Level","#f59e0b","rgba(245,158,11,0.08)"
        elif income < 75_000:  tier,tc,tbg = "Mid Level",  "#3b82f6","rgba(59,130,246,0.08)"
        elif income < 200_000: tier,tc,tbg = "Upper Mid",  IN,       f"rgba(99,102,241,0.08)"
        else:                  tier,tc,tbg = "High Earner","#a78bfa","rgba(167,139,250,0.08)"

        st.markdown(f"""
        <div class="inc-panel">
          <div>
            <div class="inc-v">₹{income:,}</div>
            <div class="inc-s">per month · take-home</div>
          </div>
          <div class="tier-tag" style="background:{tbg};border:1px solid {tc}33;color:{tc};">{tier}</div>
        </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # expenses
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<div class="sh"><div class="sh-t">Monthly Expenses</div><div class="sh-r"></div><div class="sh-b">Step 2 of 2</div></div>', unsafe_allow_html=True)

        c1,c2 = st.columns(2, gap="large")
        with c1:
            st.markdown('<div class="grp"><span class="grp-bar"></span>Essential</div>', unsafe_allow_html=True)
            rent      = field("Rent / EMI (₹)",    "r_raw",  20000, "e.g. 15000")
            groceries = field("Groceries (₹)",     "g_raw",   8000, "e.g. 6000")
            utilities = field("Utilities (₹)",     "u_raw",   2500, "e.g. 2000")
            medical   = field("Medical (₹)",       "m_raw",   1500, "e.g. 1000")
        with c2:
            st.markdown('<div class="grp"><span class="grp-bar"></span>Discretionary</div>', unsafe_allow_html=True)
            transport     = field("Transport (₹)",     "t_raw",   3000, "e.g. 2500")
            dining        = field("Dining Out (₹)",    "d_raw",   4000, "e.g. 3000")
            entertainment = field("Entertainment (₹)", "e_raw",   2000, "e.g. 1500")
            savings       = field("Savings (₹)",       "s_raw",  15000, "e.g. 10000")

        manual  = rent+groceries+utilities+medical+transport+dining+entertainment+savings
        pct_all = min(manual/income*100,100) if income>0 else 0
        bc      = "#ef4444" if pct_all>90 else "#f59e0b" if pct_all>70 else IN

        st.markdown(f"""
        <div class="alloc">
          <div class="alloc-top">
            <span class="alloc-lbl">Allocated</span>
            <span class="alloc-n">₹{manual:,}<span class="alloc-of"> / ₹{income:,}</span></span>
          </div>
          <div class="alloc-trk">
            <div class="alloc-fill" style="width:{pct_all:.1f}%;background:{bc};"></div>
          </div>
          <div class="alloc-note">{pct_all:.1f}% of income budgeted across all categories</div>
        </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        if st.button("◆  Run Prediction", use_container_width=True):
            # Total expenditure = everything the user entered EXCEPT savings
            pred = ml_predict(income,savings,rent,groceries,transport,utilities,dining,entertainment)
            st.session_state.update({
                "pred":pred,"income":income,"savings":savings,
                "rent":rent,"groceries":groceries,"transport":transport,
                "utilities":utilities,"dining":dining,
                "entertainment":entertainment,"medical":medical,
            })
            st.markdown(f"""
            <div class="alert ag" style="margin-top:1rem;">
              <span class="ai">✓</span>
              <span>Analysis complete. Your total monthly expenditure is
              <strong style="font-family:'DM Mono',monospace;font-size:15px;">
              ₹{pred:,.0f}</strong>. Open <strong>Breakdown</strong> for the full report.</span>
            </div>""", unsafe_allow_html=True)

    # live summary panel
    with side_col:
        st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)
        remain_now = income - manual
        pct_now    = pct_all
        bc2        = "#ef4444" if pct_now>90 else "#f59e0b" if pct_now>70 else IN
        s_bg       = "rgba(239,68,68,0.08)" if pct_now>90 else "rgba(99,102,241,0.08)" if pct_now>70 else "rgba(34,197,94,0.08)"
        s_c        = "#ef4444" if pct_now>90 else IN if pct_now>70 else "#22c55e"
        s_t        = "Over Budget" if pct_now>90 else "Watch Spend" if pct_now>70 else "On Track"

        rows = [
            ("Income",       f"₹{income:,}"),
            ("Rent",         f"₹{rent:,}"),
            ("Groceries",    f"₹{groceries:,}"),
            ("Transport",    f"₹{transport:,}"),
            ("Utilities",    f"₹{utilities:,}"),
            ("Dining",       f"₹{dining:,}"),
            ("Entertain.",   f"₹{entertainment:,}"),
            ("Medical",      f"₹{medical:,}"),
            ("Savings",      f"₹{savings:,}"),
        ]
        rows_html = "".join(f"""
        <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:9px;">
          <span style="font-size:12px;font-weight:500;color:{T2};">{lb}</span>
          <span style="font-family:'DM Mono',monospace;font-size:13px;font-weight:500;color:{T1};">{vl}</span>
        </div>""" for lb,vl in rows)

        st.markdown(f"""
        <div style="background:{S2};border:1px solid {BDS};border-radius:14px;
                    padding:1.4rem 1.5rem;position:sticky;top:80px;">
          <div style="font-size:10px;font-weight:700;color:{T3};
                      text-transform:uppercase;letter-spacing:0.14em;margin-bottom:14px;
                      display:flex;align-items:center;gap:8px;">
            <span style="width:6px;height:6px;border-radius:50%;background:{IN};
                          box-shadow:0 0 8px {IN};display:inline-block;"></span>
            Live Summary
          </div>
          {rows_html}
          <div style="height:1px;background:{BDS};margin:12px 0;"></div>
          <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:8px;">
            <span style="font-size:12px;font-weight:500;color:{T2};">Budgeted</span>
            <span style="font-family:'DM Mono',monospace;font-size:13px;font-weight:500;color:{T1};">₹{manual:,}</span>
          </div>
          <div style="background:{S3};border-radius:3px;height:4px;overflow:hidden;margin-bottom:8px;">
            <div style="width:{min(pct_now,100):.1f}%;height:4px;background:{bc2};border-radius:3px;"></div>
          </div>
          <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:12px;">
            <span style="font-size:12px;font-weight:500;color:{T2};">Remaining</span>
            <span style="font-family:'DM Mono',monospace;font-size:13px;font-weight:600;
                         color:{'#22c55e' if remain_now>=0 else '#ef4444'};">
              ₹{remain_now:,}
            </span>
          </div>
          <div style="background:{s_bg};border:1px solid {s_c}22;color:{s_c};
                      font-size:11px;font-weight:700;text-align:center;
                      padding:7px 10px;border-radius:7px;letter-spacing:0.06em;">
            {s_t}
          </div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 2 — BREAKDOWN
# ══════════════════════════════════════════════════════════════
with t2:
    if "pred" not in st.session_state:
        st.markdown(f'<div class="alert an" style="margin-top:1.5rem;"><span class="ai">ℹ</span><span>Complete <strong>Input & Predict</strong> first.</span></div>', unsafe_allow_html=True)
    else:
        pred=st.session_state["pred"]; income=st.session_state["income"]
        savings=st.session_state["savings"]; rent=st.session_state["rent"]
        groceries=st.session_state["groceries"]; transport=st.session_state["transport"]
        utilities=st.session_state["utilities"]; dining=st.session_state["dining"]
        entertainment=st.session_state["entertainment"]; medical=st.session_state["medical"]
        ratio=pred/income*100 if income>0 else 0
        remain=income-pred

        cols_k=st.columns(4,gap="small")
        kpis=[
            ("Predicted Spend",  f"₹{pred:,.0f}",          "ML model output",                IN),
            ("Net Remaining",    f"₹{abs(remain):,.0f}",   "surplus" if remain>=0 else "deficit","#22c55e" if remain>=0 else "#ef4444"),
            ("Expense Ratio",    f"{ratio:.1f}%",          "of monthly income",              IN if ratio<70 else "#f59e0b" if ratio<90 else "#ef4444"),
            ("Annual Surplus",   f"₹{max(remain,0)*12:,.0f}","12-month projection",          "#3b82f6"),
        ]
        for col,(lb,vl,sb,ac) in zip(cols_k,kpis):
            col.markdown(f"""
            <div class="kpi" style="--ac:{ac};">
              <div class="kpi-l">{lb}</div>
              <div class="kpi-v">{vl}</div>
              <div class="kpi-s">{sb}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        if ratio>90:
            st.markdown(f'<div class="alert ar"><span class="ai">!</span><span><strong>Critical:</strong> Expenditure exceeds 90% of income. Immediate review required.</span></div>', unsafe_allow_html=True)
        elif ratio>70:
            st.markdown(f'<div class="alert ay"><span class="ai">△</span><span><strong>Caution:</strong> {ratio:.1f}% ratio. Reduce by ₹{pred-income*0.70:,.0f} to hit the 70% benchmark.</span></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="alert ag"><span class="ai">✓</span><span><strong>On track:</strong> {ratio:.1f}% expense ratio — within healthy limits.</span></div>', unsafe_allow_html=True)

        cat_map={"Rent":rent,"Groceries":groceries,"Transport":transport,
                 "Utilities":utilities,"Dining Out":dining,
                 "Entertainment":entertainment,"Medical":medical,"Savings":savings}
        df_c=(pd.DataFrame([{"Category":k,"Amount":v,"Color":CAT[k]}
                             for k,v in cat_map.items() if v>0])
                .sort_values("Amount",ascending=False))
        tot=df_c["Amount"].sum()

        lc,rc=st.columns([3,2],gap="large")
        with lc:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f'<div class="sh"><div class="sh-t">Category Breakdown</div><div class="sh-r"></div></div>', unsafe_allow_html=True)
            for _,row in df_c.iterrows():
                p=row["Amount"]/tot*100 if tot>0 else 0
                st.markdown(f"""
                <div class="pb">
                  <div class="pb-top">
                    <span class="pb-name">{row['Category']}</span>
                    <span class="pb-val">₹{row['Amount']:,}<span class="pb-pct">{p:.1f}%</span></span>
                  </div>
                  <div class="pb-trk">
                    <div class="pb-fill" style="width:{p:.1f}%;background:{row['Color']};"></div>
                  </div>
                </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with rc:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f'<div class="sh"><div class="sh-t">Distribution</div><div class="sh-r"></div></div>', unsafe_allow_html=True)
            figp=go.Figure(go.Pie(
                labels=df_c["Category"],values=df_c["Amount"],hole=0.65,
                marker_colors=df_c["Color"].tolist(),textinfo="percent",
                textfont=dict(size=10,family="DM Sans"),
                hovertemplate="<b>%{label}</b><br>₹%{value:,}<br>%{percent}<extra></extra>",
            ))
            figp.update_layout(
                paper_bgcolor=PBG,plot_bgcolor=PBG,
                margin=dict(l=0,r=0,t=0,b=0),height=256,showlegend=True,
                legend=dict(font=dict(size=11,color=T2,family="DM Sans"),
                            bgcolor="rgba(0,0,0,0)",x=1,y=0.5,xanchor="left"),
                annotations=[dict(text=f"₹{tot:,}",x=0.35,y=0.5,
                    font=dict(size=12,color=T1,family="DM Mono"),showarrow=False)],
            )
            st.plotly_chart(figp,use_container_width=True,config={"displayModeBar":False})
            st.markdown('</div>', unsafe_allow_html=True)

        tips=[]
        if rent>income*0.35:
            tips.append(("🏠",f"<strong>Rent</strong> is {rent/income*100:.0f}% of income.",f"Target &lt;30%. A flatmate or relocation saves ₹{rent-income*0.30:,.0f}/month."))
        if dining>income*0.10:
            tips.append(("🍽",f"<strong>Dining Out</strong> at {dining/income*100:.0f}% is elevated.",f"Cooking at home 3–4× weekly recovers ₹{dining*0.4:,.0f}/month."))
        if savings<income*0.20:
            tips.append(("🏦",f"<strong>Savings</strong> below the 20% rule.",f"Automate ₹{income*0.20-savings:,.0f} more per payday."))
        if entertainment>income*0.07:
            tips.append(("📺",f"<strong>Entertainment</strong> ({entertainment/income*100:.0f}%) above threshold.",f"Audit subscriptions and cancel unused ones."))
        if medical>income*0.08:
            tips.append(("🏥",f"High <strong>Medical</strong> spend ({medical/income*100:.0f}%).",f"A health plan could cut out-of-pocket costs."))
        if transport>income*0.12:
            tips.append(("🚗",f"<strong>Transport</strong> ({transport/income*100:.0f}%) above 12%.",f"Public transit or carpooling could help."))
        if tips:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f'<div class="sh"><div class="sh-t">Recommendations</div><div class="sh-r"></div></div>', unsafe_allow_html=True)
            for ico,head,body in tips:
                st.markdown(f'<div class="tip"><span class="tip-i">{ico}</span><span>{head} {body}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 3 — WHAT-IF
# ══════════════════════════════════════════════════════════════
with t3:
    if "pred" not in st.session_state:
        st.markdown(f'<div class="alert an" style="margin-top:1.5rem;"><span class="ai">ℹ</span><span>Run a prediction first.</span></div>', unsafe_allow_html=True)
    else:
        income=st.session_state["income"]
        orig={
            "Rent":st.session_state["rent"],"Groceries":st.session_state["groceries"],
            "Transport":st.session_state["transport"],"Utilities":st.session_state["utilities"],
            "Dining Out":st.session_state["dining"],"Entertainment":st.session_state["entertainment"],
            "Medical":st.session_state["medical"],
        }
        ot=sum(orig.values())

        st.markdown(f'<div class="alert an"><span class="ai">◎</span><span>Adjust values to model the impact on your monthly and annual surplus.</span></div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<div class="sh"><div class="sh-t">Scenario Builder</div><div class="sh-r"></div><div class="sh-b">Simulator</div></div>', unsafe_allow_html=True)
        nv={}
        w1,w2=st.columns(2,gap="large")
        for i,(cat,val) in enumerate(orig.items()):
            with (w1 if i%2==0 else w2):
                raw=st.text_input(f"{cat} (₹)",value=str(val),
                                  placeholder=f"e.g. {val}",key=f"wi_{cat}")
                nv[cat]=safe_int(raw,val)
        st.markdown('</div>', unsafe_allow_html=True)

        nt=sum(nv.values()); ms=ot-nt; yr=ms*12
        kc4=st.columns(4,gap="small")
        wi4=[
            ("New Monthly Total", f"₹{nt:,}",       f"was ₹{ot:,}",                         IN),
            ("Monthly Saving",    f"₹{abs(ms):,}",  "freed up" if ms>=0 else "extra spend",  "#22c55e" if ms>=0 else "#ef4444"),
            ("Annual Saving",     f"₹{abs(yr):,}",  "12-month projection",                   "#3b82f6" if yr>=0 else "#ef4444"),
            ("New Ratio",         f"{nt/income*100:.1f}%","of income",                       IN if nt/income<0.7 else "#f59e0b"),
        ]
        for col,(lb,vl,sb,ac) in zip(kc4,wi4):
            col.markdown(f"""
            <div class="kpi" style="--ac:{ac};">
              <div class="kpi-l">{lb}</div>
              <div class="kpi-v">{vl}</div>
              <div class="kpi-s">{sb}</div>
            </div>""", unsafe_allow_html=True)

        diffs=[orig[c]-nv[c] for c in orig]
        fig2=go.Figure(go.Bar(
            x=list(orig.keys()),y=diffs,
            marker_color=["#22c55e" if d>=0 else "#ef4444" for d in diffs],
            text=[f"₹{d:+,}" for d in diffs],textposition="outside",
            textfont=dict(size=11,color=T2,family="DM Sans"),
        ))
        fig2.update_layout(
            paper_bgcolor=PBG,plot_bgcolor=GBG,
            font=dict(family="DM Sans",color=T2),
            margin=dict(l=8,r=8,t=30,b=8),height=260,
            title=dict(text="Reduction per category  ·  green = saving  ·  red = increased",
                       font=dict(size=11,color=T3,family="DM Sans"),x=0),
            xaxis=dict(showgrid=False,color=T3,linecolor=BD),
            yaxis=dict(showgrid=True,gridcolor=GRD,zeroline=True,zerolinecolor=BD,color=T3),
        )
        st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})

        if ms>0:
            st.markdown(f"""<div class="alert ag">
              <span class="ai">↑</span>
              <span>This scenario frees <strong>₹{ms:,}/month</strong> —
              <strong>₹{yr:,}/year</strong>. Over 5 years: <strong>₹{yr*5:,}</strong>.</span>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 4 — HEALTH SCORE
# ══════════════════════════════════════════════════════════════
with t4:
    if "pred" not in st.session_state:
        st.markdown(f'<div class="alert an" style="margin-top:1.5rem;"><span class="ai">ℹ</span><span>Run a prediction first.</span></div>', unsafe_allow_html=True)
    else:
        pred=st.session_state["pred"]; income=st.session_state["income"]
        savings=st.session_state["savings"]; rent=st.session_state["rent"]
        dining=st.session_state["dining"]; entertainment=st.session_state["entertainment"]

        def cl(v): return max(0.0,min(float(v),20.0))
        sr=savings/income if income>0 else 0
        er=pred/income    if income>0 else 1
        rr=rent/income    if income>0 else 1
        dr=(dining+entertainment)/income if income>0 else 1
        buf=(income-pred)/income         if income>0 else 0

        s1=cl(sr/0.20*20); s2=cl((1-er)/0.30*20)
        s3=cl((1-rr/0.35)*20); s4=cl((1-dr/0.17)*20)
        s5=cl(buf/0.10*20)
        score=int(s1+s2+s3+s4+s5)

        if   score>=80: g,gc,gl="A","#22c55e","Excellent"
        elif score>=65: g,gc,gl="B","#3b82f6","Good"
        elif score>=50: g,gc,gl="C",IN,       "Fair"
        elif score>=35: g,gc,gl="D","#f97316","Needs Attention"
        else:           g,gc,gl="F","#ef4444","Critical"

        lc,rc=st.columns([1,2],gap="large")
        with lc:
            st.markdown(f"""
            <div class="card score-wrap">
              <div style="font-size:10px;font-weight:700;color:{T3};
                          text-transform:uppercase;letter-spacing:0.15em;margin-bottom:18px;">
                Financial Health Score
              </div>
              <div class="score-n" style="color:{gc};">{score}</div>
              <div class="score-of">out of 100</div>
              <div class="score-chip"
                   style="background:{gc}12;border:1px solid {gc}33;color:{gc};">
                Grade {g} &nbsp;·&nbsp; {gl}
              </div>
              <div class="score-bg">
                <div class="score-bar"
                     style="width:{score}%;background:linear-gradient(90deg,{IN2},{gc});
                            box-shadow:0 0 10px {gc}55;"></div>
              </div>
              <div style="font-size:11px;color:{T3};margin-top:5px;">{score} / 100 overall</div>
            </div>""", unsafe_allow_html=True)

        with rc:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f'<div class="sh"><div class="sh-t">Score Components</div><div class="sh-r"></div></div>', unsafe_allow_html=True)
            bk=[
                ("Savings Rate",    s1,f"{sr*100:.1f}% saved  ·  target ≥ 20%",          "#22c55e"),
                ("Expense Control", s2,f"{er*100:.1f}% expense ratio  ·  target < 70%",   "#3b82f6"),
                ("Rent Burden",     s3,f"{rr*100:.1f}% on rent  ·  target < 30%",         "#8b5cf6"),
                ("Discretionary",   s4,f"{dr*100:.1f}%  dining + entertainment",           "#f97316"),
                ("Monthly Buffer",  s5,f"₹{max(income-pred,0):,} remaining after expenses","#06b6d4"),
            ]
            for nm,sc,det,col in bk:
                p=sc/20*100
                st.markdown(f"""
                <div class="pb">
                  <div class="pb-top">
                    <span class="pb-name">{nm}</span>
                    <span style="font-family:'DM Mono',monospace;font-size:12px;
                                 font-weight:600;color:{col};">{int(sc)}/20</span>
                  </div>
                  <div style="font-size:11px;color:{T3};margin-bottom:5px;">{det}</div>
                  <div class="pb-trk">
                    <div class="pb-fill" style="width:{p:.1f}%;background:{col};
                         box-shadow:0 0 5px {col}44;"></div>
                  </div>
                </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<div class="sh"><div class="sh-t">Financial Profile Radar</div><div class="sh-r"></div></div>', unsafe_allow_html=True)
        rc_=["Savings Rate","Expense Control","Rent Burden","Discretionary","Buffer"]
        rv_=[s1/20*100,s2/20*100,s3/20*100,s4/20*100,s5/20*100]
        rv_+=rv_[:1]; rc_+=rc_[:1]

        figr=go.Figure()
        figr.add_trace(go.Scatterpolar(
            r=[100]*6,theta=rc_,fill="toself",
            fillcolor="rgba(99,102,241,0.03)",
            line=dict(color=BD,width=1),showlegend=False,
        ))
        figr.add_trace(go.Scatterpolar(
            r=rv_,theta=rc_,fill="toself",
            fillcolor="rgba(99,102,241,0.12)",
            line=dict(color=IN,width=2),
            marker=dict(size=7,color=IN,line=dict(color=S1,width=2)),
            showlegend=False,
        ))
        figr.update_layout(
            polar=dict(
                bgcolor=PBG,
                radialaxis=dict(visible=True,range=[0,100],
                    tickfont=dict(size=9,color=T3,family="DM Mono"),gridcolor=GRD),
                angularaxis=dict(tickfont=dict(size=11,color=T2,family="DM Sans"),gridcolor=GRD),
            ),
            paper_bgcolor=PBG,margin=dict(l=50,r=50,t=20,b=20),height=310,
        )
        st.plotly_chart(figr,use_container_width=True,config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
  Expense Intelligence Platform &nbsp;|&nbsp;
  Scikit-learn ML Engine &nbsp;|&nbsp;
  2020–2025 Dataset &nbsp;|&nbsp; 60K+ Records
</div>""", unsafe_allow_html=True)
