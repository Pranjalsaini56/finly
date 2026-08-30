import streamlit as st
import pandas as pd
import altair as alt
import os
import base64
from datetime import date

st.set_page_config(page_title="Finly", layout="wide")

DATA_FILE = "my_expenses.csv"
LOGO_FILE = "assets/logo.png"
ICON_FILE = "assets/icon.png"

def get_logo_base64():
    if os.path.exists(LOGO_FILE):
        with open(LOGO_FILE, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return None

def get_icon_base64():
    if os.path.exists(ICON_FILE):
        with open(ICON_FILE, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return None

# --- Styling ---
st.markdown("""
    <style>
/* Distinctive sidebar Finly treatment */
.finly-side-brand {
    display:flex;
    align-items:center;
    justify-content:center;
    min-height:76px;
    margin:2px 2px 22px;
    border-radius:18px;
    background:
        radial-gradient(circle at 50% 0%, rgba(168,85,247,.20), transparent 48%),
        linear-gradient(145deg,#17121f,#0d0f15);
    border:1px solid #2e2540;
    box-shadow:
        0 12px 28px rgba(0,0,0,.30),
        inset 0 1px 0 rgba(255,255,255,.04);
}
.finly-side-brand-word {
    color:#f7f3ff;
    font-size:25px;
    font-weight:800;
    letter-spacing:-1.1px;
    text-shadow:
        0 0 16px rgba(168,85,247,.45),
        0 5px 18px rgba(0,0,0,.55);
}
.finly-side-brand-dot {
    width:7px;
    height:7px;
    border-radius:50%;
    margin-left:7px;
    background:#a855f7;
    box-shadow:0 0 13px rgba(168,85,247,.95);
}

    div.block-container { padding-top: 1.1rem; padding-bottom: 4rem; }

    /* Finora-inspired visual system: deep black/navy surfaces, purple glow, rounded cards */
    .stApp {
        background:
            radial-gradient(circle at 92% 7%, rgba(124,58,237,.24), transparent 24%),
            radial-gradient(circle at 7% 92%, rgba(139,92,246,.16), transparent 28%),
            #090b10;
    }
    div[data-testid="stHeader"] { background: transparent !important; }

    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #12151d, #0d1016);
        padding: 22px; border-radius: 18px;
        border: 1px solid #252b38;
        box-shadow: 0 12px 30px rgba(0,0,0,.28);
    }
    div[data-testid="stMetricLabel"] { color: #8f98aa !important; }
    div[data-testid="stMetricValue"] { color: #f7f7fb !important; }
    hr { border-color: #252b38; margin: 24px 0; }

    .cat-card, .alert-card {
        background: linear-gradient(145deg, #12151d, #0d1016);
        border: 1px solid #252b38; border-radius: 16px;
        padding: 18px 22px; margin-bottom: 14px;
        box-shadow: 0 10px 25px rgba(0,0,0,.20);
        transition: transform .15s ease, box-shadow .15s ease;
    }
    .cat-card:hover, .alert-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 14px 30px rgba(0,0,0,.28);
    }
    .badge {
        display: inline-flex; align-items: center; justify-content: center;
        width: 34px; height: 34px; border-radius: 10px; font-size: 16px; margin-right: 12px;
    }
    .tx-row {
        display: flex; justify-content: space-between; align-items: center;
        padding: 14px 18px; border-radius: 12px; margin-bottom: 7px;
        background: #10131a; border: 1px solid #202531;
    }
    .finly-shell {
        background: linear-gradient(145deg, rgba(18,21,29,.96), rgba(9,11,16,.96));
        border: 1px solid #252b38;
        border-radius: 22px;
        padding: 8px;
        box-shadow: 0 22px 55px rgba(0,0,0,.36);
    }
    .finly-section-title {
        color: #f7f7fb;
        font-size: 18px;
        font-weight: 700;
        letter-spacing: -.2px;
    }
    .finly-muted { color: #8993a6; font-size: 13px; }
    .finly-glow {
        box-shadow: 0 0 0 1px rgba(139,92,246,.10), 0 16px 45px rgba(76,29,149,.18);
    }

    /* Real action buttons (Add Expense, Import, Clear Data) — pill style */
    button[kind="primary"] {
        background: linear-gradient(135deg, #8b5cf6, #6d28d9) !important;
        color: white !important;
        border: none !important;
        border-radius: 999px !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        font-size: 15px !important;
    }
    button[kind="primary"]:hover {
        background: linear-gradient(135deg, #9a6cff, #7c3aed) !important;
        transform: translateY(-1px);
    }

    /* Nav + icon buttons — plain text links, no box, Deloitte-style */
    button[kind="tertiary"] {
        background-color: transparent !important;
        border: none !important;
        color: #cbd5e1 !important;
        font-weight: 500 !important;
        font-size: 15px !important;
        padding: 6px 10px !important;
        box-shadow: none !important;
    }
    button[kind="tertiary"]:hover {
        color: #f8fafc !important;
        text-decoration: underline;
    }

    div[role="radiogroup"] label { border-radius: 999px !important; }

    /* Functional dashboard report buttons */
    div[data-testid="stButton"] button {
        transition: all .18s ease !important;
    }
    div[data-testid="stButton"] button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 20px rgba(124,58,237,.22) !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* ===== FINORA-STYLE FINLY SHELL ===== */

/* ===== FINORA-STYLE FINLY SHELL ===== */
.finly-reference {
    color:#f7f7fb;
}
.finly-dashboard-grid {
    display:grid;
    grid-template-columns:minmax(0,1.45fr) minmax(320px,.9fr);
    gap:18px;
    margin-bottom:18px;
}
.finly-panel {
    background:linear-gradient(145deg,#11141b 0%,#0c0f15 100%);
    border:1px solid #252b36;
    border-radius:20px;
    box-shadow:0 16px 38px rgba(0,0,0,.24);
    overflow:hidden;
}
.finly-welcome-panel {
    min-height:235px;
    padding:30px;
    position:relative;
    background:
        radial-gradient(circle at 78% 50%,rgba(124,58,237,.18),transparent 24%),
        linear-gradient(125deg,#12151b,#0b0e14);
}
.finly-welcome-panel:before {
    content:"";
    position:absolute;
    width:250px;height:250px;
    right:-50px;top:-100px;
    border-radius:50%;
    border:1px solid rgba(139,92,246,.13);
    box-shadow:0 0 70px rgba(124,58,237,.16);
}
.finly-eyebrow {
    color:#a78bfa;
    text-transform:uppercase;
    letter-spacing:1.4px;
    font-size:10px;
    font-weight:700;
}
.finly-welcome-title {
    color:#fafafa;
    font-size:29px;
    line-height:1.15;
    font-weight:750;
    letter-spacing:-.7px;
    margin-top:10px;
}
.finly-welcome-copy {
    color:#8f98a9;
    font-size:14px;
    line-height:1.65;
    max-width:520px;
    margin-top:12px;
}
.finly-purple-button {
    display:inline-block;
    margin-top:20px;
    padding:10px 17px;
    border-radius:10px;
    color:#fff;
    font-size:13px;
    font-weight:650;
    text-decoration:none;
    background:linear-gradient(135deg,#8b45f4,#6726d5);
    box-shadow:0 9px 24px rgba(124,58,237,.25);
}
.finly-balance-card {
    min-height:235px;
    padding:24px 25px;
    position:relative;
    overflow:hidden;
    background:
        radial-gradient(circle at 82% 50%,rgba(255,255,255,.12),transparent 18%),
        linear-gradient(145deg,#974cf2 0%,#7130dc 55%,#5b22c5 100%);
    border:1px solid rgba(196,181,253,.35);
    border-radius:20px;
    box-shadow:0 18px 45px rgba(76,29,149,.30);
}
.finly-balance-card:before,
.finly-balance-card:after {
    content:"";
    position:absolute;
    border-radius:50%;
    border:1px solid rgba(255,255,255,.13);
    pointer-events:none;
}
.finly-balance-card:before {
    width:210px;height:210px;right:-75px;top:35px;
}
.finly-balance-card:after {
    width:150px;height:150px;right:-45px;top:65px;
}
.finly-balance-label {
    color:rgba(255,255,255,.82);
    font-size:12px;
}
.finly-balance-value {
    color:#fff;
    font-size:29px;
    font-weight:750;
    letter-spacing:-.7px;
    margin-top:9px;
    position:relative;
    z-index:2;
}
.finly-balance-status {
    display:inline-block;
    margin-top:10px;
    padding:5px 9px;
    border-radius:999px;
    background:rgba(255,255,255,.88);
    color:#4c1d95;
    font-size:11px;
    font-weight:700;
}
.finly-balance-copy {
    color:rgba(255,255,255,.78);
    font-size:12px;
    line-height:1.5;
    max-width:185px;
    margin-top:11px;
    position:relative;
    z-index:2;
}
.finly-orbit {
    position:absolute;
    right:25px;top:70px;
    width:104px;height:104px;
    border-radius:50%;
    border:1px solid rgba(255,255,255,.20);
    box-shadow:0 0 28px rgba(217,70,239,.28);
}
.finly-orbit:before {
    content:"";
    position:absolute;
    inset:13px;
    border-radius:50%;
    border:7px solid rgba(236,72,153,.50);
    border-left-color:rgba(196,181,253,.88);
    border-bottom-color:rgba(139,92,246,.85);
}
.finly-orbit-icon {
    position:absolute;
    left:35px;top:35px;
    width:34px;height:34px;
    border-radius:11px;
    background:rgba(255,255,255,.12);
    border:1px solid rgba(255,255,255,.2);
    display:flex;align-items:center;justify-content:center;
    font-size:16px;
}
.finly-balance-footer {
    position:absolute;
    left:25px;right:25px;bottom:18px;
    border-top:1px solid rgba(255,255,255,.16);
    padding-top:10px;
    color:rgba(255,255,255,.76);
    font-size:11px;
}
.finly-metric-grid {
    display:grid;
    grid-template-columns:repeat(3,minmax(0,1fr));
    gap:14px;
    margin-bottom:18px;
}
.finly-metric {
    min-height:118px;
    padding:18px 19px;
    position:relative;
    background:linear-gradient(145deg,#11141b,#0d1016);
    border:1px solid #252b36;
    border-radius:17px;
    overflow:hidden;
}
.finly-metric-label {
    color:#8a93a5;
    font-size:11px;
}
.finly-metric-value {
    color:#f8fafc;
    font-size:23px;
    font-weight:700;
    margin-top:7px;
    letter-spacing:-.4px;
}
.finly-metric-trend {
    display:inline-block;
    margin-top:10px;
    padding:4px 7px;
    border-radius:6px;
    background:#181c25;
    color:#8e97a9;
    font-size:10px;
}
.finly-mini-line {
    position:absolute;
    right:12px;bottom:13px;
    width:82px;height:38px;
    opacity:.8;
}
.finly-content-grid {
    display:grid;
    grid-template-columns:minmax(0,1.1fr) minmax(320px,.9fr);
    gap:18px;
    margin-bottom:18px;
}
/* Streamlit containers hold charts/widgets correctly; style the two dashboard cards. */
.st-key-finly-overview-card,
.st-key-finly-recent-card {
    min-height: 360px;
    padding: 20px 21px;
    background: linear-gradient(145deg,#11141b 0%,#0c0f15 100%) !important;
    border: 1px solid #252b36 !important;
    border-radius: 20px !important;
    box-shadow: 0 16px 38px rgba(0,0,0,.24);
}
.st-key-finly-overview-card [data-testid="stVerticalBlock"],
.st-key-finly-recent-card [data-testid="stVerticalBlock"] {
    gap: 0.35rem;
}
.finly-section-card {
    padding:20px 21px;
    min-height:360px;
}
.finly-section-head {
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:10px;
    margin-bottom:14px;
}
.finly-section-head h3 {
    margin:0;
    color:#f4f4f6;
    font-size:17px;
    font-weight:680;
}
.finly-view-all {
    color:#a78bfa;
    font-size:11px;
    text-decoration:none;
}
.finly-recent-row {
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:10px;
    padding:12px 2px;
    border-bottom:1px solid #20242d;
}
.finly-recent-row:last-child { border-bottom:0; }
.finly-recent-left {
    display:flex;
    align-items:center;
    min-width:0;
}
.finly-recent-icon {
    width:34px;height:34px;
    border-radius:11px;
    display:flex;align-items:center;justify-content:center;
    margin-right:10px;
    flex:0 0 auto;
    font-size:13px;
}
.finly-recent-name {
    color:#eef0f5;
    font-size:12px;
    font-weight:600;
    white-space:nowrap;
    overflow:hidden;
    text-overflow:ellipsis;
}
.finly-recent-meta {
    color:#697386;
    font-size:10px;
    margin-top:3px;
}
.finly-recent-amount {
    font-size:12px;
    font-weight:700;
    white-space:nowrap;
}
.finly-bottom-card {
    padding:22px 24px;
    min-height:160px;
    position:relative;
    overflow:hidden;
    background:
        radial-gradient(circle at 82% 50%,rgba(124,58,237,.13),transparent 26%),
        linear-gradient(145deg,#10131a,#0b0e14);
}
.finly-bottom-title {
    color:#8d96a8;
    font-size:12px;
}
.finly-bottom-value {
    color:#f8fafc;
    font-size:28px;
    font-weight:750;
    margin-top:7px;
}
.finly-bottom-copy {
    color:#737d90;
    font-size:12px;
    margin-top:5px;
}
.finly-empty {
    text-align:center;
    padding:60px 20px;
    color:#7f899b;
}
@media (max-width: 900px) {
    .finly-dashboard-grid,.finly-content-grid { grid-template-columns:1fr; }
    .finly-metric-grid { grid-template-columns:1fr; }
}

.stApp {
    background:
        radial-gradient(900px 520px at 94% -8%, rgba(139,92,246,.34), transparent 58%),
        radial-gradient(760px 520px at 5% 108%, rgba(168,85,247,.22), transparent 62%),
        #080a0f !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #101216 0%, #0c0e12 100%) !important;
    border-right: 1px solid #252832 !important;
}
section[data-testid="stSidebar"] > div {
    padding: 1.35rem 1rem 1rem !important;
}
.finora-brand {
    color: #f8f8fb;
    font-size: 31px;
    font-weight: 800;
    letter-spacing: -1.4px;
    padding: 8px 10px 20px;
    text-shadow: 0 6px 22px rgba(139,92,246,.28);
}
.finora-brand-mark {
    color: #a855f7;
    margin-right: 5px;
}
.finora-side-label {
    color: #6f7787;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1.3px;
    padding: 4px 10px 10px;
}
.finora-side-note {
    color: #737b8c;
    font-size: 11px;
    line-height: 1.55;
    padding: 0 10px;
}

/* Main app width and heading */
div.block-container {
    max-width: 1380px !important;
    padding-top: .75rem !important;
    padding-bottom: 3.5rem !important;
}
.finora-page-title {
    color: #f7f7fa;
    font-size: 25px;
    font-weight: 700;
    letter-spacing: -.6px;
    margin: 5px 0 18px 2px;
}
.finora-top-actions {
    display:flex;
    justify-content:flex-end;
    align-items:center;
    gap:10px;
}

/* Hero */
.finora-hero {
    min-height: 205px;
    border-radius: 21px;
    padding: 30px 32px;
    margin: 0 0 18px;
    background:
        radial-gradient(circle at 83% 35%, rgba(139,92,246,.48), transparent 27%),
        radial-gradient(circle at 96% 82%, rgba(59,130,246,.30), transparent 25%),
        linear-gradient(115deg, #11141a 0%, #0c0f14 58%, #171126 100%);
    border: 1px solid #282d38;
    box-shadow: 0 22px 48px rgba(0,0,0,.34);
    position:relative;
    overflow:hidden;
}
.finora-hero:after {
    content:"";
    position:absolute;
    right:-90px;
    top:-130px;
    width:360px;
    height:360px;
    border-radius:50%;
    border:1px solid rgba(196,181,253,.10);
    box-shadow: 0 0 80px rgba(139,92,246,.16);
}
.finora-hero h2 {
    margin:0;
    color:#fafafa;
    font-size:30px;
    letter-spacing:-.8px;
}
.finora-hero p {
    color:#929aaa;
    font-size:14px;
    line-height:1.65;
    max-width:570px;
    margin:12px 0 20px;
}
.finora-eyebrow {
    color:#a78bfa;
    font-size:11px;
    text-transform:uppercase;
    letter-spacing:1.4px;
    font-weight:700;
    margin-bottom:8px;
}

/* Balance card */
.finora-balance {
    min-height:205px;
    border-radius:21px;
    padding:25px 25px 22px;
    background:
        radial-gradient(circle at 86% 12%, rgba(255,255,255,.13), transparent 25%),
        linear-gradient(145deg,#9852f5 0%,#7837e6 55%,#6325d4 100%);
    border:1px solid rgba(255,255,255,.16);
    box-shadow:0 22px 48px rgba(76,29,149,.30);
    color:white;
    position:relative;
    overflow:hidden;
}
.finora-balance:before,
.finora-balance:after {
    content:"";
    position:absolute;
    border-radius:50%;
    border:1px solid rgba(255,255,255,.10);
}
.finora-balance:before { width:220px;height:220px;right:-105px;top:-120px; }
.finora-balance:after { width:170px;height:170px;right:-75px;top:-80px; }
.finora-balance-label { font-size:13px; opacity:.85; }
.finora-balance-value { font-size:31px; font-weight:700; margin-top:8px; letter-spacing:-.7px; }
.finora-balance-meta { font-size:12px; margin-top:12px; opacity:.88; }

/* Cards */
.finora-card {
    background:linear-gradient(145deg,#11141a,#0d1015);
    border:1px solid #252a34;
    border-radius:20px;
    box-shadow:0 16px 36px rgba(0,0,0,.24);
}
.finora-card-title {
    color:#f4f4f6;
    font-size:17px;
    font-weight:650;
}
.finora-card-muted {
    color:#7e8797;
    font-size:12px;
}

/* Transaction rows */
.finora-list-row {
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding:12px 4px;
    border-bottom:1px solid #20242d;
}
.finora-list-row:last-child { border-bottom:0; }
.finora-app-icon {
    width:32px;height:32px;border-radius:10px;
    display:inline-flex;align-items:center;justify-content:center;
    background:#1a1e27;color:#c4b5fd;font-weight:700;font-size:12px;
    margin-right:10px;
}
.finora-positive { color:#a7f3d0; }
.finora-negative { color:#fda4af; }

/* Streamlit controls */
.stButton > button {
    border-radius:10px !important;
}
.stButton > button[kind="primary"] {
    background:linear-gradient(135deg,#9747f5,#7132db) !important;
    border:1px solid #a56af7 !important;
    box-shadow:0 9px 24px rgba(124,58,237,.24) !important;
}
.stTabs [data-baseweb="tab-list"] {
    gap:8px;
    background:transparent;
}
.stTabs [data-baseweb="tab"] {
    background:#0d1015;
    border:1px solid #252a34;
    border-radius:10px;
    padding:7px 16px;
}
.stTabs [aria-selected="true"] {
    background:#f5f5f7 !important;
    color:#101116 !important;
}
</style>
""", unsafe_allow_html=True)

CATEGORY_STYLE = {
    "Food & Dining":       {"icon": "🍽️", "color": "#f97316"},
    "Groceries":           {"icon": "🛒", "color": "#22c55e"},
    "Transport":           {"icon": "🚗", "color": "#3b82f6"},
    "Shopping":            {"icon": "🛍️", "color": "#ec4899"},
    "Housing & Utilities": {"icon": "🏠", "color": "#a855f7"},
    "Subscriptions":       {"icon": "📺", "color": "#06b6d4"},
    "Bills & Recharge":    {"icon": "📱", "color": "#eab308"},
    "Health":              {"icon": "💊", "color": "#ef4444"},
    "Insurance":           {"icon": "🛡️", "color": "#14b8a6"},
    "Entertainment":       {"icon": "🎬", "color": "#8b5cf6"},
    "Income":              {"icon": "💵", "color": "#22c55e"},
    "Cash Withdrawal":     {"icon": "🏧", "color": "#64748b"},
    "Other":               {"icon": "📦", "color": "#94a3b8"},
}
EXPENSE_CATEGORIES = [c for c in CATEGORY_STYLE.keys() if c not in ("Income",)]

def style_for(category):
    return CATEGORY_STYLE.get(category, {"icon": "📦", "color": "#94a3b8"})

def categorize(description):
    desc = description.lower()
    keyword_map = {
        "Subscriptions": ["netflix", "spotify", "hotstar", "prime subscription", "gold membership",
                           "cult.fit", "gym membership"],
        "Food & Dining": ["zomato", "swiggy", "domino", "mcdonald", "cafe", "starbucks", "pizza"],
        "Groceries": ["big bazaar", "dmart", "bigbasket", "zepto", "blinkit", "grocery", "groceries"],
        "Transport": ["uber", "ola", "petrol", "metro", "fuel"],
        "Shopping": ["amazon", "flipkart", "myntra", "ikea"],
        "Housing & Utilities": ["rent", "electricity", "water bill"],
        "Bills & Recharge": ["mobile recharge", "airtel", "jio", "credit card payment"],
        "Health": ["pharmacy", "medical store", "apollo"],
        "Insurance": ["lic", "insurance"],
        "Entertainment": ["pvr", "bookmyshow", "movie"],
        "Income": ["salary"],
        "Cash Withdrawal": ["atm", "cash withdrawal"],
    }
    for category, keywords in keyword_map.items():
        if any(kw in desc for kw in keywords):
            return category
    return "Other"

# --- Load saved data ---
if "expenses" not in st.session_state:
    if os.path.exists(DATA_FILE):
        loaded = pd.read_csv(DATA_FILE)
    else:
        loaded = pd.DataFrame(columns=["Date", "Description", "Amount", "Type", "Category"])
    if "Category" not in loaded.columns:
        loaded["Category"] = loaded["Description"].apply(categorize) if len(loaded) else []
    if "Type" not in loaded.columns:
        loaded["Type"] = loaded["Category"].apply(lambda c: "Income" if c == "Income" else "Expense")
    st.session_state.expenses = loaded

def save_to_disk():
    st.session_state.expenses.to_csv(DATA_FILE, index=False)

if "active_section" not in st.session_state:
    st.session_state.active_section = "Dashboard"
if "welcome_seen" not in st.session_state:
    st.session_state.welcome_seen = False
if "show_full_report" not in st.session_state:
    st.session_state.show_full_report = False

info_sections = ["Who I Am", "What I Do", "My Thinking", "Careers"]

# --- Top navbar: personal information opens as hover/click slide panels ---
logo_b64 = get_logo_base64()
logo_html = (
    f'<img src="data:image/png;base64,{logo_b64}" class="finly-logo-image">'
    if logo_b64
    else '<div class="finly-text-fallback">Finly</div>'
)

icon_b64 = get_icon_base64()
icon_html = (
    f'<img src="data:image/png;base64,{icon_b64}" class="finly-sidebar-icon-image">'
    if icon_b64
    else '<div class="finly-sidebar-icon-fallback">F</div>'
)

st.markdown("""
<style>
.finly-topnav{display:flex !important;align-items:center !important;justify-content:space-between !important;gap:30px;min-height:58px;padding:0 10px 0 4px;background:transparent;border:0;box-shadow:none;position:relative;z-index:1000;}
.finly-top-brand{display:flex;align-items:center;justify-content:flex-start;min-width:170px;height:70px;}
.finly-top-brand img{display:block;width:150px;height:auto;max-height:64px;object-fit:contain;filter:drop-shadow(0 8px 20px rgba(124,58,237,.55)) drop-shadow(0 0 20px rgba(139,92,246,.35));}
.finly-top-links{display:flex;align-items:center;gap:38px;}

.finly-logo-image{display:block !important;} .finly-text-fallback{display:block !important;color:#f8fafc;font-size:24px;font-weight:850;letter-spacing:-1.6px;text-shadow:0 0 16px rgba(139,92,246,.32),0 6px 20px rgba(124,58,237,.24);}
.finly-info{position:relative;height:58px;display:flex;align-items:center;}
.finly-info-label{color:#c9cfdb;font-size:14px;font-weight:500;cursor:pointer;white-space:nowrap;transition:color .18s ease,transform .18s ease;display:flex;align-items:center;gap:9px;}
.finly-info-label:hover{color:#fff;transform:translateY(-1px);}
.finly-nav-icon{width:19px;height:19px;display:inline-flex;align-items:center;justify-content:center;color:#a78bfa;flex:0 0 19px;}
.finly-nav-icon svg{width:19px;height:19px;stroke:currentColor;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;}
.finly-info:hover .finly-nav-icon{color:#c4b5fd;}
.finly-info input{position:absolute;opacity:0;pointer-events:none;}
.finly-slide{position:absolute;top:52px;right:0;width:310px;background:linear-gradient(145deg,#141728,#0b0e17);border:1px solid #34314d;border-radius:15px;padding:18px 19px;box-shadow:0 20px 45px rgba(0,0,0,.48),0 0 35px rgba(124,58,237,.12);opacity:0;visibility:hidden;transform:translateY(-8px);transition:opacity .18s ease,transform .18s ease,visibility .18s ease;}
.finly-info:hover .finly-slide,.finly-info input:checked~.finly-slide{opacity:1;visibility:visible;transform:translateY(0);}
.finly-slide-title{color:#fff;font-size:16px;font-weight:700;margin-bottom:7px;}
.finly-slide-text{color:#929bae;font-size:12px;line-height:1.65;}
.finly-tags{display:flex;flex-wrap:wrap;gap:7px;margin-top:13px;}
.finly-tags span{border:1px solid #393550;background:#171629;color:#cfd3df;border-radius:999px;padding:4px 9px;font-size:10px;}
.finly-quote{margin-top:13px;padding:9px 11px;border-left:2px solid #8b5cf6;background:#171629;color:#cbd1df;font-size:11px;line-height:1.5;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.finly-dashboard-grid{display:grid;grid-template-columns:minmax(0,1.08fr) minmax(390px,.92fr);gap:16px;margin:6px 0 16px;}
.finly-welcome-panel{min-height:310px;padding:30px;position:relative;overflow:hidden;border:1px solid #242b3a;border-radius:18px;background:radial-gradient(circle at 76% 68%,rgba(109,40,217,.25),transparent 24%),linear-gradient(145deg,#0e1422,#0a0e18 78%);box-shadow:0 20px 48px rgba(0,0,0,.28);}
.finly-welcome-panel:after{content:"";position:absolute;right:-90px;bottom:-150px;width:430px;height:260px;background:radial-gradient(ellipse,rgba(124,58,237,.42),transparent 65%);filter:blur(12px);}
.finly-welcome-content{position:relative;z-index:4;}
.finly-eyebrow{color:#8b5cf6;font-size:9px;font-weight:800;letter-spacing:1.5px;}
.finly-welcome-title{color:#f8fafc;font-size:27px;font-weight:760;letter-spacing:-.8px;margin-top:14px;}
.finly-welcome-copy{color:#a0a9bb;font-size:14px;line-height:1.8;margin-top:13px;}
.finly-purple-button{display:inline-block;margin-top:21px;padding:11px 17px;border-radius:9px;background:linear-gradient(135deg,#8b45f4,#6d28d9);color:#fff!important;text-decoration:none;font-size:12px;font-weight:700;box-shadow:0 10px 28px rgba(124,58,237,.28);}
.finly-welcome-visual{position:absolute;right:26px;top:58px;width:280px;height:220px;z-index:3;}
.finly-screen{position:absolute;right:16px;top:4px;width:200px;height:152px;border:1px solid #4b3b73;border-radius:13px;transform:rotate(-7deg);background:linear-gradient(145deg,#18142e,#0c1020);box-shadow:0 18px 45px rgba(0,0,0,.38),0 0 30px rgba(124,58,237,.18);padding:20px 17px;}
.finly-screen svg{position:absolute;left:14px;right:14px;top:42px;width:172px;height:76px;}
.finly-screen-dot{width:7px;height:7px;border-radius:50%;background:#8b5cf6;box-shadow:0 0 12px #8b5cf6;}
.finly-screen-line{position:absolute;height:5px;border-radius:5px;background:#34314e;left:17px;}
.finly-screen-line.l1{width:42px;bottom:26px}.finly-screen-line.l2{width:25px;bottom:15px}.finly-screen-line.l3{width:51px;bottom:15px;left:51px;}
.finly-screen-bar{position:absolute;right:12px;bottom:13px;width:33px;height:18px;border-radius:5px;background:#6d28d9;}
.finly-float-tag{position:absolute;right:-2px;bottom:22px;padding:10px 13px;border:1px solid #493a72;border-radius:9px;background:#191532;color:#5ee6b0;font-size:12px;font-weight:700;transform:rotate(8deg);box-shadow:0 12px 30px rgba(0,0,0,.35);}
.finly-glow-orb{position:absolute;left:8px;bottom:0;width:90px;height:34px;background:radial-gradient(ellipse,rgba(124,58,237,.65),transparent 70%);filter:blur(12px);}
.finly-balance-card{min-height:310px;padding:24px;position:relative;overflow:hidden;border-radius:18px;border:1px solid #6e3fe4;background:radial-gradient(circle at 92% 5%,rgba(255,255,255,.16),transparent 28%),linear-gradient(145deg,#7c3aed 0%,#6126ca 62%,#4c1d95 100%);box-shadow:0 20px 50px rgba(76,29,149,.35);}
.finly-balance-card:before{content:"";position:absolute;width:260px;height:260px;right:-100px;top:-100px;border-radius:50%;border:1px solid rgba(255,255,255,.15);box-shadow:0 0 0 30px rgba(255,255,255,.025),0 0 0 60px rgba(255,255,255,.018);}
.finly-balance-label{color:rgba(255,255,255,.78);font-size:12px;position:relative;z-index:3;}
.finly-balance-menu{position:absolute;right:20px;top:18px;padding:5px 9px;border-radius:8px;color:#ddd2ff;background:rgba(31,15,73,.35);border:1px solid rgba(255,255,255,.12);letter-spacing:2px;font-size:10px;z-index:4;}
.finly-balance-value{color:#fff;font-size:28px;font-weight:780;letter-spacing:-.8px;margin-top:11px;position:relative;z-index:4;}
.finly-balance-status{display:inline-block;margin-top:11px;padding:5px 9px;border-radius:999px;background:#f5ecff;color:#5b21b6;font-size:10px;font-weight:800;position:relative;z-index:4;}
.finly-balance-copy{color:rgba(255,255,255,.78);font-size:11px;line-height:1.55;max-width:210px;margin-top:13px;position:relative;z-index:4;}
.finly-balance-graph{position:absolute;left:18px;right:25px;bottom:70px;height:120px;z-index:2;opacity:.9;}
.finly-balance-graph svg{width:100%;height:100%;}
.finly-balance-orbit{position:absolute;right:25px;top:73px;width:130px;height:130px;z-index:3;}
.orbit-ring{position:absolute;border-radius:50%;border:1px solid rgba(255,255,255,.16);}
.ring-a{inset:0;box-shadow:0 0 28px rgba(236,72,153,.22)}.ring-b{inset:15px;border:6px solid rgba(236,72,153,.42);border-left-color:#c4b5fd;border-bottom-color:#8b5cf6}.ring-c{inset:33px;border:1px dashed rgba(255,255,255,.3);}
.orbit-core{position:absolute;left:48px;top:48px;width:34px;height:34px;border-radius:10px;display:flex;align-items:center;justify-content:center;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.18);color:#fff;box-shadow:0 0 22px rgba(236,72,153,.3);}
.finly-balance-footer{position:absolute;left:23px;right:23px;bottom:17px;padding-top:10px;border-top:1px solid rgba(255,255,255,.14);display:flex;justify-content:space-between;color:rgba(255,255,255,.64);font-size:10px;z-index:4;}
.finly-balance-footer b{color:#fff;}
.finly-balance-only{margin-bottom:16px;}
/* Compact replacement panel shown after the first welcome */
.finly-return-grid{display:grid;grid-template-columns:minmax(0,1.08fr) minmax(390px,.92fr);gap:16px;margin:6px 0 16px;}
.finly-return-card{min-height:310px;padding:30px;position:relative;overflow:hidden;border:1px solid #242b3a;border-radius:18px;background:radial-gradient(circle at 76% 60%,rgba(109,40,217,.24),transparent 25%),linear-gradient(145deg,#0e1422,#0a0e18 78%);box-shadow:0 20px 48px rgba(0,0,0,.28);}
.finly-return-card:before{content:"";position:absolute;right:-80px;top:-120px;width:300px;height:300px;border-radius:50%;border:1px solid rgba(139,92,246,.14);box-shadow:0 0 70px rgba(124,58,237,.18);}
.finly-return-content{position:relative;z-index:2;max-width:390px;}
.finly-return-kicker{color:#8b5cf6;font-size:10px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:12px;}
.finly-return-title{color:#f8fafc;font-size:27px;font-weight:760;letter-spacing:-.8px;line-height:1.15;}
.finly-return-copy{color:#99a3b6;font-size:13px;line-height:1.75;margin-top:12px;}
.finly-return-stat{display:flex;gap:10px;align-items:center;margin-top:22px;}
.finly-return-dot{width:9px;height:9px;border-radius:50%;background:#8b5cf6;box-shadow:0 0 16px #8b5cf6;}
.finly-return-stat span{color:#cbd5e1;font-size:11px;}
.finly-return-visual{position:absolute;right:28px;top:65px;width:235px;height:190px;z-index:1;}
.finly-return-ring{position:absolute;border-radius:50%;border:1px solid rgba(139,92,246,.28);box-shadow:0 0 35px rgba(124,58,237,.12);}
.finly-return-ring.r1{width:150px;height:150px;right:15px;top:5px;}
.finly-return-ring.r2{width:112px;height:112px;right:34px;top:24px;border-color:rgba(236,72,153,.28);}
.finly-return-wallet{position:absolute;right:55px;top:50px;width:92px;height:70px;border-radius:14px;background:linear-gradient(145deg,#30205f,#151126);border:1px solid #5d3ba0;transform:rotate(-7deg);box-shadow:0 20px 40px rgba(0,0,0,.38),0 0 30px rgba(124,58,237,.2);}
.finly-return-wallet:after{content:"";position:absolute;right:12px;top:28px;width:20px;height:14px;border-radius:5px;background:#8b5cf6;box-shadow:0 0 15px rgba(139,92,246,.7);}
.finly-return-orb{position:absolute;width:8px;height:8px;border-radius:50%;background:#a78bfa;box-shadow:0 0 14px #a78bfa;}
.finly-return-orb.o1{right:184px;top:18px}.finly-return-orb.o2{right:5px;top:118px}.finly-return-orb.o3{right:148px;bottom:4px;}
.finly-metric-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-bottom:16px;}
.finly-metric{min-height:102px;padding:18px 17px 15px 74px;position:relative;overflow:hidden;border-radius:16px;border:1px solid #252d3d;background:linear-gradient(145deg,#101520,#0c1018);box-shadow:0 13px 30px rgba(0,0,0,.2);}
.finly-metric-icon{position:absolute;left:18px;top:20px;width:38px;height:38px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:700;}
.metric-income .finly-metric-icon{background:#064e3b;color:#4ade80;border:1px solid #08744f}.metric-expense .finly-metric-icon{background:#4c1728;color:#fb7185;border:1px solid #7f1d3a}.metric-net .finly-metric-icon{background:#2e1065;color:#c4b5fd;border:1px solid #6d28d9}
.finly-metric-label{color:#9ba4b6;font-size:10px}.finly-metric-value{color:#f8fafc;font-size:18px;font-weight:740;margin-top:6px;white-space:nowrap;}
.finly-metric-trend{display:inline-block;margin-top:7px;padding:4px 6px;border-radius:5px;font-size:9px;font-weight:750;background:#111827}.finly-metric-trend span{color:#8b95a7;font-weight:450;margin-left:3px;}
.trend-green{color:#34d399;background:#052e26}.trend-red{color:#fb7185;background:#3a1422}.trend-purple{color:#c4b5fd;background:#251246}
.finly-mini-line{position:absolute;right:9px;bottom:9px;width:82px;height:39px;opacity:.8;}
.finly-section-card{min-height:360px;padding:20px 21px;border-radius:17px;border:1px solid #252d3d;background:linear-gradient(145deg,#101520,#0b0f17);box-shadow:0 14px 34px rgba(0,0,0,.2);}
.finly-section-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}.finly-section-head h3{margin:0;color:#f5f7fb;font-size:16px;font-weight:720;}
.finly-filter{padding:7px 9px;border:1px solid #293042;border-radius:8px;color:#b3bbca;font-size:10px;background:#111722}.finly-view-all{color:#a78bfa;font-size:11px;font-weight:600;}
.finly-legend-row{display:grid;grid-template-columns:10px minmax(70px,1fr) auto auto;gap:7px;align-items:center;margin:12px 0;color:#b8c0ce;font-size:9px}.finly-legend-row b{color:#f3f4f6;font-size:9px}.finly-legend-row>span:last-child{color:#778195}.finly-legend-dot{width:9px;height:9px;border-radius:50%;}
.finly-report-button{width:max-content;margin:8px auto 0;padding:9px 15px;border-radius:8px;border:1px solid #6337b9;color:#a78bfa;font-size:10px;font-weight:700;background:#120d22;}
.finly-recent-row{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:11px 0;border-bottom:1px solid #202633}.finly-recent-row:last-of-type{border-bottom:0;}
.finly-recent-left{display:flex;align-items:center;min-width:0}.finly-recent-icon{width:31px;height:31px;border-radius:50%;display:flex;align-items:center;justify-content:center;margin-right:10px;font-size:12px;flex:0 0 auto}.finly-recent-name{color:#edf0f5;font-size:11px;font-weight:650;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.finly-recent-meta{color:#7c8698;font-size:9px;margin-top:3px}.finly-recent-amount{font-size:11px;font-weight:750;white-space:nowrap;}
@media (max-width:1050px){.finly-dashboard-grid,.finly-return-grid{grid-template-columns:1fr}.finly-welcome-visual{right:10px}}
@media (max-width:760px){.finly-metric-grid{grid-template-columns:1fr}.finly-topnav{gap:16px;overflow-x:auto;justify-content:flex-start}.finly-top-links{gap:18px}.finly-top-brand{min-width:90px}.finly-welcome-visual{opacity:.45}}
</style>
""", unsafe_allow_html=True)

st.markdown(
f"""
<div class="finly-topnav">
<div class="finly-top-brand">{logo_html}</div>
<div class="finly-top-links">
<div class="finly-info">
<input type="checkbox" id="finly-who">
<label class="finly-info-label" for="finly-who"><span class="finly-nav-icon"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="8" r="3.2"></circle><path d="M5.5 20c.7-3.5 3-5.3 6.5-5.3s5.8 1.8 6.5 5.3"></path></svg></span>Who I Am</label>
<div class="finly-slide">
<div class="finly-slide-title">Who I Am</div>
<div class="finly-slide-text">
I'm a student building this AI Finance Controller project to
sharpen my Python, data analysis, and app-building skills.
</div>
<div class="finly-tags"><span>AI</span><span>Python</span><span>Data</span></div>
</div>
</div>

<div class="finly-info">
<input type="checkbox" id="finly-what">
<label class="finly-info-label" for="finly-what"><span class="finly-nav-icon"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m8 8-4 4 4 4"></path><path d="m16 8 4 4-4 4"></path><path d="m14 5-4 14"></path></svg></span>What I Do</label>
<div class="finly-slide">
<div class="finly-slide-title">What I Do</div>
<div class="finly-slide-text">
This app automatically categorizes expenses, flags duplicate
transactions, detects unusual overspending, and visualizes trends.
</div>
<div class="finly-tags"><span>Automation</span><span>Analytics</span><span>Finance</span></div>
</div>
</div>

<div class="finly-info">
<input type="checkbox" id="finly-thinking">
<label class="finly-info-label" for="finly-thinking"><span class="finly-nav-icon"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 18h6"></path><path d="M10 22h4"></path><path d="M8.2 14.8A6.5 6.5 0 1 1 15.8 15c-.9.7-1.5 1.6-1.7 3H9.9c-.2-1.2-.8-2.2-1.7-3.2Z"></path></svg></span>My Thinking</label>
<div class="finly-slide">
<div class="finly-slide-title">My Thinking</div>
<div class="finly-slide-text">
I believe finance tools should be simple enough to use daily,
but smart enough to catch mistakes automatically.
</div>
<div class="finly-quote">Simple enough for daily use. Smart enough to catch mistakes.</div>
</div>
</div>

<div class="finly-info">
<input type="checkbox" id="finly-careers">
<label class="finly-info-label" for="finly-careers"><span class="finly-nav-icon"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="7" width="18" height="13" rx="2"></rect><path d="M8 7V5.5A1.5 1.5 0 0 1 9.5 4h5A1.5 1.5 0 0 1 16 5.5V7"></path><path d="M3 12h18"></path><path d="M10 12v2h4v-2"></path></svg></span>Careers</label>
<div class="finly-slide">
<div class="finly-slide-title">Careers</div>
<div class="finly-slide-text">
Currently exploring internship and entry-level opportunities
in AI, data, and software development.
</div>
<div class="finly-tags"><span>AI/ML</span><span>Data</span><span>Software</span></div>
</div>
</div>
</div>
</div>    """,
    unsafe_allow_html=True
)

st.divider()

# --- Dashboard header ---
if st.session_state.active_section == "Dashboard":
    st.markdown(
        '<div class="finly-main-title">Dashboard</div>',
        unsafe_allow_html=True
    )

# --- Main app navigation: reference-style left rail ---
st.markdown("""
<style>
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#090c18 0%,#0b0d17 100%);border-right:1px solid #252b3a;}
section[data-testid="stSidebar"]>div{padding-top:1.15rem;}
.finora-brand{display:flex;align-items:center;justify-content:flex-start;gap:10px;padding:0 10px 10px;min-height:52px;}
.finora-brand img{display:block;width:32px;height:32px;border-radius:9px;object-fit:contain;object-position:left center;}
.finora-brand-label{color:#b8bfcc;font-size:15px;font-weight:600;letter-spacing:-.2px;}
.finly-main-title{color:#f7f8fc;font-size:26px;font-weight:750;letter-spacing:-.7px;margin:0;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown(
        f'<div class="finora-brand">{icon_html}<span class="finora-brand-label">Finly</span></div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div style="color:#737d90;font-size:11px;line-height:1.45;padding:0 10px 22px;">'
        'Your Personal Finance<br>Companion'
        '</div>',
        unsafe_allow_html=True
    )

    for sec, icon in [
        ("Dashboard", "⌂"),
        ("Transactions", "▣"),
        ("Insights", "◔"),
        ("Settings", "⚙")
    ]:
        active = st.session_state.active_section == sec
        if st.button(
            f"{icon}   {sec}",
            key=f"main_nav_{sec}",
            use_container_width=True,
            type="primary" if active else "tertiary"
        ):
            st.session_state.active_section = sec
            st.rerun()

    st.markdown("<div style='height:210px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="
        margin:0 4px;
        padding:20px 16px;
        border-radius:16px;
        background:linear-gradient(145deg,#1a1237,#100e23);
        border:1px solid #30205b;
        box-shadow:0 12px 30px rgba(76,29,149,.16);
        text-align:center;">
        <div style="font-size:23px;">✦</div>
        <div style="color:#f3e8ff;font-size:14px;font-weight:700;margin-top:7px;">
            Keep tracking.<br>Keep growing.
        </div>
        <div style="color:#858da0;font-size:10px;line-height:1.55;margin-top:9px;">
            Small steps today,<br>big freedom tomorrow.
        </div>
        <div style="color:#8b5cf6;font-size:10px;margin-top:14px;">● • •</div>
    </div>
    """, unsafe_allow_html=True)

# --- Prepare data (used across all sections) ---
df = st.session_state.expenses.copy()
has_data = len(df) > 0
if has_data:
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)
    df = df.sort_values("Date")

    expenses_df = df[df["Type"] == "Expense"].copy()
    income_df = df[df["Type"] == "Income"].copy()
    expenses_only = expenses_df["Amount"].sum()
    income_only = income_df["Amount"].sum()
    net = income_only - expenses_only

    category_totals = expenses_df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
    duplicates = df[df.duplicated(subset=["Date", "Description", "Amount"], keep=False)]

    monthly_cat = expenses_df.groupby(["Month", "Category"])["Amount"].sum().reset_index()
    avg_per_cat = monthly_cat.groupby("Category")["Amount"].mean()
    monthly_cat["Average"] = monthly_cat["Category"].map(avg_per_cat)
    monthly_cat["Overspend"] = monthly_cat["Amount"] > (monthly_cat["Average"] * 1.5)
    flagged = monthly_cat[monthly_cat["Overspend"]]

    months_sorted = sorted(df["Month"].unique())
    trend_html = ""
    if len(months_sorted) >= 2:
        latest, prev = months_sorted[-1], months_sorted[-2]
        latest_spend = expenses_df[expenses_df["Month"] == latest]["Amount"].sum()
        prev_spend = expenses_df[expenses_df["Month"] == prev]["Amount"].sum()
        if prev_spend > 0:
            pct_change = ((latest_spend - prev_spend) / prev_spend) * 100
            arrow = "▲" if pct_change >= 0 else "▼"
            trend_color = "#ef4444" if pct_change >= 0 else "#22c55e"
            trend_html = f'<span style="color:{trend_color}; font-size:13px; font-weight:600;">{arrow} {abs(pct_change):.1f}% vs last month</span>'

section = st.session_state.active_section

# =========================================================
# DASHBOARD
# =========================================================
if section == "Dashboard":
    if has_data:
        recent_dashboard = df.sort_values("Date", ascending=False).head(5)
        balance_status = "On Track" if net >= 0 else "In Deficit"
        balance_status_icon = "✓" if net >= 0 else "↓"
        balance_message = (
            "Your current balance is positive and your recorded income is ahead of spending."
            if net >= 0 else
            "Your spending is currently higher than recorded income. Review your recent activity."
        )

        if not st.session_state.welcome_seen:
            st.markdown(f"""
            <div class="finly-dashboard-grid">
                <div class="finly-welcome-panel">
                    <div class="finly-welcome-content">
                        <div class="finly-eyebrow">FINLY • AI FINANCE CONTROLLER</div>
                        <div class="finly-welcome-title">Welcome back! <span>👋</span></div>
                        <div class="finly-welcome-copy">
                            Track your income and expenses<br>
                            smartly and achieve your goals.
                        </div>
                    </div>
                    <div class="finly-welcome-visual">
                        <div class="finly-screen">
                            <div class="finly-screen-dot"></div>
                            <svg viewBox="0 0 180 90">
                                <path d="M4 66 C18 35,29 74,43 48 S67 72,83 34 S106 67,124 39 S148 61,176 24" fill="none" stroke="#9147ff" stroke-width="3"/>
                            </svg>
                            <div class="finly-screen-line l1"></div><div class="finly-screen-line l2"></div><div class="finly-screen-line l3"></div>
                            <div class="finly-screen-bar"></div>
                        </div>
                        <div class="finly-float-tag">↓ +12.4%</div>
                        <div class="finly-glow-orb"></div>
                    </div>
                </div>
                <div class="finly-balance-card">
                    <div class="finly-balance-label">Current Balance</div><div class="finly-balance-menu">•••</div>
                    <div class="finly-balance-value">Rs. {net:,.2f}</div>
                    <div class="finly-balance-status">{balance_status_icon}&nbsp; {balance_status}</div>
                    <div class="finly-balance-copy">{balance_message}</div>
                    <div class="finly-balance-graph"><svg viewBox="0 0 300 120" preserveAspectRatio="none">
                        <path d="M0 102 C23 87,27 105,47 77 S76 96,91 69 S116 88,133 57 S159 79,177 47 S203 67,220 31 S247 51,265 26 S283 35,300 8" fill="none" stroke="#a855f7" stroke-width="3"/>
                    </svg></div>
                    <div class="finly-balance-orbit"><div class="orbit-ring ring-a"></div><div class="orbit-ring ring-b"></div><div class="orbit-ring ring-c"></div><div class="orbit-core">▣</div></div>
                    <div class="finly-balance-footer"><div><b>↓ {abs(net):,.0f}</b><span> current position</span></div><div><b>{balance_status}</b><span> status</span></div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.session_state.welcome_seen = True
        else:
            st.markdown(f"""
            <div class="finly-return-grid">
                <div class="finly-return-card">
                    <div class="finly-return-content">
                        <div class="finly-return-kicker">FINLY • SMART MONEY</div>
                        <div class="finly-return-title">Your finances,<br>in one clear view.</div>
                        <div class="finly-return-copy">
                            Keep an eye on your spending, understand your trends, and make
                            better decisions with Finly. Your dashboard is ready whenever you are.
                        </div>
                        <div class="finly-return-stat">
                            <span class="finly-return-dot"></span>
                            <span>{len(df)} recorded transactions · Live overview</span>
                        </div>
                    </div>
                    <div class="finly-return-visual">
                        <div class="finly-return-ring r1"></div>
                        <div class="finly-return-ring r2"></div>
                        <div class="finly-return-wallet"></div>
                        <span class="finly-return-orb o1"></span>
                        <span class="finly-return-orb o2"></span>
                        <span class="finly-return-orb o3"></span>
                    </div>
                </div>
                <div class="finly-balance-card">
                    <div class="finly-balance-label">Current Balance</div><div class="finly-balance-menu">•••</div>
                    <div class="finly-balance-value">Rs. {net:,.2f}</div>
                    <div class="finly-balance-status">{balance_status_icon}&nbsp; {balance_status}</div>
                    <div class="finly-balance-copy">{balance_message}</div>
                    <div class="finly-balance-graph"><svg viewBox="0 0 300 120" preserveAspectRatio="none">
                        <path d="M0 102 C23 87,27 105,47 77 S76 96,91 69 S116 88,133 57 S159 79,177 47 S203 67,220 31 S247 51,265 26 S283 35,300 8" fill="none" stroke="#a855f7" stroke-width="3"/>
                    </svg></div>
                    <div class="finly-balance-orbit"><div class="orbit-ring ring-a"></div><div class="orbit-ring ring-b"></div><div class="orbit-ring ring-c"></div><div class="orbit-core">▣</div></div>
                    <div class="finly-balance-footer"><div><b>Current financial position</b></div><div><b>{balance_status}</b></div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="finly-metric-grid">
            <div class="finly-metric metric-income"><div class="finly-metric-icon">⇩</div><div class="finly-metric-label">Total Income</div><div class="finly-metric-value">Rs. {income_only:,.0f}</div><div class="finly-metric-trend trend-green">↓ 8.7% <span>vs last month</span></div><svg class="finly-mini-line" viewBox="0 0 95 45"><path d="M1 40 C12 30,17 37,27 25 S43 34,51 20 S66 28,75 12 S85 18,94 2" fill="none" stroke="#22c55e" stroke-width="2"/></svg></div>
            <div class="finly-metric metric-expense"><div class="finly-metric-icon">⇧</div><div class="finly-metric-label">Total Expenses</div><div class="finly-metric-value">Rs. {expenses_only:,.0f}</div><div class="finly-metric-trend trend-red">↑ 14.2% <span>vs last month</span></div><svg class="finly-mini-line" viewBox="0 0 95 45"><path d="M1 39 C14 32,15 38,27 27 S40 34,50 22 S61 26,72 13 S82 19,94 2" fill="none" stroke="#ec4899" stroke-width="2"/></svg></div>
            <div class="finly-metric metric-net"><div class="finly-metric-icon">▥</div><div class="finly-metric-label">Net Balance</div><div class="finly-metric-value">Rs. {net:,.0f}</div><div class="finly-metric-trend trend-purple">↓ 102.1% <span>vs last month</span></div><svg class="finly-mini-line" viewBox="0 0 95 45"><path d="M1 39 C12 35,18 40,27 27 S41 34,51 19 S66 26,76 11 S87 17,94 2" fill="none" stroke="#8b5cf6" stroke-width="2"/></svg></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div id="financial-overview"></div>', unsafe_allow_html=True)

        overview_df = pd.DataFrame({
            "Type": ["Income", "Expenses"],
            "Amount": [abs(income_only), abs(expenses_only)]
        })
        overview_chart = alt.Chart(overview_df).mark_arc(
            innerRadius=68,
            outerRadius=105
        ).encode(
            theta=alt.Theta("Amount:Q"),
            color=alt.Color(
                "Type:N",
                scale=alt.Scale(
                    domain=["Income", "Expenses"],
                    range=["#8b5cf6", "#ec4899"]
                ),
                legend=None
            ),
            tooltip=[
                alt.Tooltip("Type:N", title="Type"),
                alt.Tooltip("Amount:Q", title="Amount", format=",.0f")
            ]
        ).properties(height=270)

        left_col, right_col = st.columns([1.1, .9], gap="medium")

        with left_col:
            with st.container(border=True, key="finly-overview-card"):
                st.markdown(
                    '<div class="finly-section-head">'
                    '<h3>Financial Overview</h3>'
                    '<span class="finly-filter">This Month&nbsp;⌄</span>'
                    '</div>',
                    unsafe_allow_html=True
                )

                chart_col, legend_col = st.columns([.95, 1.05])

                with chart_col:
                    st.altair_chart(overview_chart, use_container_width=True)

                with legend_col:
                    if len(category_totals) > 0:
                        total_cat = category_totals.sum()
                        for category, amount in category_totals.head(6).items():
                            s = style_for(category)
                            pct = (amount / total_cat * 100) if total_cat else 0
                            st.markdown(
                                f'<div class="finly-legend-row">'
                                f'<span class="finly-legend-dot" style="background:{s["color"]};"></span>'
                                f'<span class="finly-legend-name">{category}</span>'
                                f'<b>Rs. {amount:,.0f}</b>'
                                f'<span>{pct:.1f}%</span>'
                                f'</div>',
                                unsafe_allow_html=True
                            )
                    else:
                        st.markdown(
                            '<div class="finly-muted">No expense categories yet.</div>',
                            unsafe_allow_html=True
                        )

                if st.button("View full report  →", key="view_full_report", use_container_width=False):
                    st.session_state.show_full_report = True
                    st.rerun()

        with right_col:
            with st.container(border=True, key="finly-recent-card"):
                st.markdown(
                    '<div class="finly-section-head">'
                    '<h3>Recent Transactions</h3>'
                    '<span class="finly-view-all">View All</span>'
                    '</div>',
                    unsafe_allow_html=True
                )

                if len(recent_dashboard) > 0:
                    for _, row in recent_dashboard.iterrows():
                        s = style_for(row["Category"])
                        is_income = row["Type"] == "Income"
                        amount_color = "#22c55e" if is_income else "#ff4d6d"
                        sign = "+" if is_income else "-"
                        st.markdown(
                            f'<div class="finly-recent-row">'
                            f'<div class="finly-recent-left">'
                            f'<div class="finly-recent-icon" '
                            f'style="background:{s["color"]}25;'
                            f'border:1px solid {s["color"]}55;'
                            f'color:{s["color"]};">{s["icon"]}</div>'
                            f'<div style="min-width:0;">'
                            f'<div class="finly-recent-name">{str(row["Description"])}</div>'
                            f'<div class="finly-recent-meta">'
                            f'{row["Category"]} · {row["Date"].strftime("%b %d, %Y")}'
                            f'</div></div></div>'
                            f'<div class="finly-recent-amount" style="color:{amount_color};">'
                            f'{sign} Rs. {abs(row["Amount"]):,.0f}'
                            f'</div></div>',
                            unsafe_allow_html=True
                        )
                else:
                    st.markdown(
                        '<div class="finly-empty">No transactions yet.</div>',
                        unsafe_allow_html=True
                    )

                if st.button("View all transactions  →", key="view_all_transactions", use_container_width=False):
                    st.session_state.active_section = "Transactions"
                    st.rerun()

        if st.session_state.show_full_report:
            st.markdown("<div id='full-report'></div>", unsafe_allow_html=True)
            st.markdown("### Full Financial Report")
            report_col1, report_col2, report_col3 = st.columns(3)
            with report_col1:
                st.metric("Total Income", f"Rs. {income_only:,.0f}")
            with report_col2:
                st.metric("Total Expenses", f"Rs. {expenses_only:,.0f}")
            with report_col3:
                st.metric("Net Balance", f"Rs. {net:,.0f}")

            if len(category_totals) > 0:
                report_table = category_totals.reset_index()
                report_table.columns = ["Category", "Amount"]
                report_table["Share"] = (report_table["Amount"] / report_table["Amount"].sum() * 100).round(1).astype(str) + "%"
                st.dataframe(report_table, use_container_width=True, hide_index=True)

            if st.button("Close full report", key="close_full_report", type="secondary"):
                st.session_state.show_full_report = False
                st.rerun()

        st.divider()
        st.subheader("Spend by Category")
        if len(category_totals)>0:
            max_amount=category_totals.max(); total_spend=category_totals.sum()
            for category,amount in category_totals.items():
                s=style_for(category); pct_of_total=(amount/total_spend)*100; bar_pct=amount/max_amount
                st.markdown(f'<div class="cat-card"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;"><div style="display:flex;align-items:center;font-size:15px;font-weight:600;color:#f8fafc;"><span class="badge" style="background-color:{s["color"]}33;">{s["icon"]}</span>{category}</div><div style="font-size:15px;font-weight:700;color:#f8fafc;">Rs. {amount:,.0f} <span style="color:#94a3b8;font-weight:400;font-size:13px;">({pct_of_total:.1f}%)</span></div></div><div style="background-color:#202530;border-radius:6px;height:8px;width:100%;"><div style="background-color:{s["color"]};border-radius:6px;height:8px;width:{bar_pct*100}%;"></div></div></div>',unsafe_allow_html=True)
            st.divider()
            st.subheader("Spending Trend Over Time")
            daily=expenses_df.groupby("Date")["Amount"].sum().reset_index()
            area_chart=alt.Chart(daily).mark_area(line={"color":"#8b5cf6","strokeWidth":2},color=alt.Gradient(gradient="linear",stops=[alt.GradientStop(color="#8b5cf6",offset=0),alt.GradientStop(color="#11141b",offset=1)],x1=1,x2=1,y1=1,y2=0)).encode(x=alt.X("Date:T",title=None),y=alt.Y("Amount:Q",title="Daily Spend (Rs.)"),tooltip=["Date:T","Amount:Q"]).properties(height=280).configure_axis(labelColor="#94a3b8",titleColor="#94a3b8",gridColor="#252b36").configure_view(strokeWidth=0)
            st.altair_chart(area_chart,use_container_width=True)
    else:
        st.markdown("""
        <style>
        .st-key-finly-empty-card {
            position: relative;
            overflow: hidden;
            border-radius: 24px;
            border: 1px solid #2a2140;
            padding: 44px 46px !important;
            background:
                radial-gradient(circle at 88% 12%, rgba(139,92,246,.30), transparent 42%),
                radial-gradient(circle at 8% 92%, rgba(6,182,212,.20), transparent 42%),
                linear-gradient(150deg, #14101f 0%, #0a0b12 70%);
            box-shadow: 0 26px 60px rgba(0,0,0,.35);
        }
        .finly-empty-orb-a {
            position: absolute; width: 300px; height: 300px; border-radius: 50%;
            background: radial-gradient(circle, rgba(139,92,246,.55), transparent 70%);
            filter: blur(24px); top: -110px; right: -90px;
            animation: finly-float 6s ease-in-out infinite;
        }
        .finly-empty-orb-b {
            position: absolute; width: 220px; height: 220px; border-radius: 50%;
            background: radial-gradient(circle, rgba(6,182,212,.45), transparent 70%);
            filter: blur(20px); bottom: -80px; left: -60px;
            animation: finly-float 7s ease-in-out infinite reverse;
        }
        @keyframes finly-float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(18px); }
        }
        .finly-eyebrow2 { position:relative; z-index:2; color:#a78bfa; font-size:11px; font-weight:800; letter-spacing:1.6px; text-transform:uppercase; }
        .finly-empty-heading { position:relative; z-index:2; color:#f8fafc; font-size:30px; font-weight:780; letter-spacing:-.8px; margin-top:12px; line-height:1.2; }
        .finly-empty-sub { position:relative; z-index:2; color:#9aa3b5; font-size:14.5px; line-height:1.75; margin-top:14px; max-width:400px; }

        /* Animated illustration */
        .finly-illust { position:relative; z-index:2; height:220px; display:flex; align-items:flex-end; justify-content:center; gap:14px; padding-bottom:10px; }
        .finly-bar { width: 30px; border-radius: 8px 8px 0 0; background: linear-gradient(180deg, #8b5cf6, #6d28d9); box-shadow: 0 0 22px rgba(139,92,246,.5); animation: finly-grow 2.4s ease-in-out infinite; }
        .finly-bar.b1 { height: 60px; animation-delay: 0s; }
        .finly-bar.b2 { height: 100px; background: linear-gradient(180deg, #06b6d4, #0891b2); box-shadow: 0 0 22px rgba(6,182,212,.5); animation-delay: .3s; }
        .finly-bar.b3 { height: 80px; animation-delay: .6s; }
        .finly-bar.b4 { height: 140px; background: linear-gradient(180deg, #ec4899, #be185d); box-shadow: 0 0 22px rgba(236,72,153,.5); animation-delay: .9s; }
        .finly-bar.b5 { height: 110px; animation-delay: 1.2s; }
        @keyframes finly-grow {
            0%, 100% { transform: scaleY(1); transform-origin: bottom; }
            50% { transform: scaleY(1.12); transform-origin: bottom; }
        }
        .finly-coin { position:absolute; width:34px; height:34px; border-radius:50%; background:linear-gradient(135deg,#fbbf24,#f59e0b); display:flex; align-items:center; justify-content:center; font-size:15px; font-weight:800; color:#78350f; box-shadow:0 8px 18px rgba(245,158,11,.4); animation: finly-drift 5s ease-in-out infinite; }
        .finly-coin.c1 { top: 10px; right: 60px; animation-delay: 0s; }
        .finly-coin.c2 { top: 90px; right: 10px; animation-delay: 1.5s; }
        @keyframes finly-drift {
            0%, 100% { transform: translateY(0) rotate(0deg); }
            50% { transform: translateY(-14px) rotate(8deg); }
        }
        </style>
        """, unsafe_allow_html=True)

        with st.container(border=True, key="finly-empty-card"):
            left, right = st.columns([1.1, .9], gap="large")

            with left:
                st.markdown("""
                    <div class="finly-eyebrow2">FINLY • GET STARTED</div>
                    <div class="finly-empty-heading">Your financial<br>story starts here</div>
                    <div class="finly-empty-sub">
                        Add your first income or expense and Finly will build your
                        financial overview, trends, and insights automatically.
                    </div>
                """, unsafe_allow_html=True)

                st.markdown("<div style='height:22px; position:relative; z-index:2;'></div>", unsafe_allow_html=True)

                b1, b2 = st.columns(2)
                with b1:
                    if st.button("➕  Add Transaction", key="empty_cta_add", type="primary", use_container_width=True):
                        st.session_state.active_section = "Transactions"
                        st.rerun()
                with b2:
                    if st.button("📁  Import / Export", key="empty_cta_import", use_container_width=True):
                        st.session_state.active_section = "Settings"
                        st.rerun()

            with right:
                st.markdown("""
                    <div class="finly-illust">
                        <div class="finly-coin c1">₹</div>
                        <div class="finly-coin c2">$</div>
                        <div class="finly-bar b1"></div>
                        <div class="finly-bar b2"></div>
                        <div class="finly-bar b3"></div>
                        <div class="finly-bar b4"></div>
                        <div class="finly-bar b5"></div>
                    </div>
                """, unsafe_allow_html=True)

# =========================================================
# TRANSACTIONS
# =========================================================
elif section == "Transactions":
    st.subheader("➕ Add a Transaction")
    entry_type = st.radio("Type", ["Expense", "Income"], horizontal=True)

    with st.form("add_entry_form", clear_on_submit=True):
        c1, c2, c3 = st.columns([1, 2, 1])
        with c1:
            entry_date = st.date_input("Date", value=date.today())
        with c2:
            entry_desc = st.text_input(
                "Description",
                placeholder="e.g. Zomato order" if entry_type == "Expense" else "e.g. Salary, Freelance payment"
            )
        with c3:
            entry_amount = st.number_input("Amount (Rs.)", min_value=0.0, step=10.0, format="%.2f")

        if entry_type == "Expense":
            suggested = categorize(entry_desc) if entry_desc else "Other"
            if suggested == "Income":
                suggested = "Other"
            category_choice = st.selectbox(
                "Category (auto-suggested, change if wrong)",
                EXPENSE_CATEGORIES,
                index=EXPENSE_CATEGORIES.index(suggested) if suggested in EXPENSE_CATEGORIES else 0
            )
        else:
            category_choice = "Income"

        submitted = st.form_submit_button(f"Add {entry_type}", type="primary", use_container_width=True)

        if submitted:
            if entry_desc.strip() == "" or entry_amount == 0:
                st.warning("Please fill in description and amount.")
            else:
                new_row = pd.DataFrame([{
                    "Date": entry_date.strftime("%Y-%m-%d"),
                    "Description": entry_desc.strip(),
                    "Amount": entry_amount,
                    "Type": entry_type,
                    "Category": category_choice,
                }])
                st.session_state.expenses = pd.concat([st.session_state.expenses, new_row], ignore_index=True)
                save_to_disk()
                st.success(f"Added {entry_type}: {entry_desc} — Rs. {entry_amount:,.0f}")
                st.rerun()

    st.divider()
    st.subheader("All Transactions")
    if has_data:
        recent = df.sort_values("Date", ascending=False).head(30).reset_index()
        for i, row in recent.iterrows():
            s = style_for(row["Category"])
            is_income = row["Type"] == "Income"
            amount_color = "#22c55e" if is_income else "#f8fafc"
            amount_sign = "+" if is_income else "-"
            row_bg = "#1e293b" if i % 2 == 0 else "#172033"
            st.markdown(f"""
                <div class="tx-row" style="background-color:{row_bg};">
                    <div style="display:flex; align-items:center;">
                        <span class="badge" style="background-color:{s['color']}33;">{s['icon']}</span>
                        <div>
                            <div style="color:#f8fafc; font-size:14px; font-weight:500;">{row['Description']}</div>
                            <div style="color:#64748b; font-size:12px;">{row['Category']} · {row['Date'].strftime('%d %b %Y')}</div>
                        </div>
                    </div>
                    <div style="color:{amount_color}; font-weight:700; font-size:14px;">
                        {amount_sign} Rs. {abs(row['Amount']):,.0f}
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No transactions yet. Add one using the form above.")

# =========================================================
# INSIGHTS
# =========================================================
elif section == "Insights":
    st.subheader("⚠️ Possible Duplicate Entries")
    if has_data and len(duplicates) > 0:
        for _, row in duplicates.iterrows():
            st.markdown(f"""
                <div class="alert-card" style="border-left: 4px solid #ef4444;">
                    <div style="font-weight:700; color:#f8fafc;">⚠️ Duplicate: {row['Description']}</div>
                    <div style="color:#94a3b8; font-size:13px;">{row['Date'].strftime('%d %b %Y')} · Rs. {row['Amount']:,.0f}</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.success("No duplicates found!")

    st.subheader("🚨 Overspending Alerts")
    if has_data and len(flagged) > 0:
        for _, row in flagged.iterrows():
            s = style_for(row["Category"])
            st.markdown(f"""
                <div class="alert-card" style="border-left: 4px solid #eab308;">
                    <div style="font-weight:700; color:#f8fafc;">{s['icon']} {row['Category']} spiked in {row['Month']}</div>
                    <div style="color:#94a3b8; font-size:13px;">Spent Rs. {row['Amount']:,.0f} vs average Rs. {row['Average']:,.0f}</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.success("No unusual overspending detected.")

# =========================================================
# SETTINGS
# =========================================================
elif section == "Settings":
    st.subheader("📁 Bulk Import from CSV")
    file = st.file_uploader("Upload expense CSV (columns: Date, Description, Amount)", type="csv")
    if file:
        uploaded_df = pd.read_csv(file)
        uploaded_df["Category"] = uploaded_df["Description"].apply(categorize)
        uploaded_df["Type"] = uploaded_df["Category"].apply(lambda c: "Income" if c == "Income" else "Expense")
        st.session_state.expenses = pd.concat([st.session_state.expenses, uploaded_df], ignore_index=True)
        save_to_disk()
        st.success(f"Imported {len(uploaded_df)} rows from CSV.")
        st.rerun()

    st.divider()
    st.subheader("⬇️ Export Your Data")
    if has_data:
        csv_data = df[["Date", "Description", "Amount", "Type", "Category"]].to_csv(index=False)
        st.download_button(
            "Download CSV",
            data=csv_data,
            file_name="finly_transactions.csv",
            mime="text/csv",
            type="primary"
        )
    else:
        st.info("No data to export yet.")

    st.divider()
    st.subheader("🗑️ Manage Data")
    if has_data:
        st.write(f"You currently have **{len(df)}** transactions saved.")
        if st.button("Clear All Data", type="primary"):
            st.session_state.expenses = pd.DataFrame(columns=["Date", "Description", "Amount", "Type", "Category"])
            save_to_disk()
            st.rerun()
    else:
        st.info("No data to manage yet.")

# =========================================================
# FOOTER (shown on every section)
# =========================================================
st.markdown("<div style='height:50px'></div>", unsafe_allow_html=True)

st.markdown("""
<style>
.finly-footer {
    background: #050608;
    border-radius: 20px 20px 0 0;
    padding: 46px 44px 30px;
    margin: 0 -1rem;
    border-top: 1px solid #1c202a;
}
.finly-footer-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0,1fr)) auto;
    gap: 36px;
    padding-bottom: 34px;
}
.finly-footer-col h4 {
    color: #f8fafc;
    font-size: 15px;
    font-weight: 700;
    margin: 0 0 16px;
}
.finly-footer-col a, .finly-footer-col div.flink {
    display: block;
    color: #8b93a5;
    font-size: 13.5px;
    line-height: 2.4;
    text-decoration: none;
    cursor: default;
}
.finly-footer-col a:hover { color: #f8fafc; }
.finly-footer-social {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
    min-width: 160px;
}
.finly-footer-social span.label {
    color: #f8fafc;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 14px;
}
.finly-footer-social-icons {
    display: flex;
    gap: 14px;
}
.finly-footer-social-icons a {
    width: 36px; height: 36px;
    border-radius: 50%;
    background: #14171f;
    border: 1px solid #262b38;
    display: flex; align-items: center; justify-content: center;
    color: #cbd5e1;
    transition: all .15s ease;
}
.finly-footer-social-icons a:hover {
    background: linear-gradient(135deg, #8b5cf6, #06b6d4);
    color: white;
    transform: translateY(-2px);
}
.finly-footer-social-icons svg { width: 16px; height: 16px; stroke: currentColor; fill: none; stroke-width: 1.8; }
.finly-footer-divider { border-top: 1px solid #1c202a; margin: 0 0 22px; }
.finly-footer-legal-links {
    display: flex; flex-wrap: wrap; gap: 26px;
    margin-bottom: 20px;
}
.finly-footer-legal-links a {
    color: #cbd5e1; font-size: 13px; font-weight: 600; text-decoration: none;
}
.finly-footer-legal-links a:hover { color: #fff; }
.finly-footer-copyright {
    color: #6b7385; font-size: 12.5px; margin-bottom: 14px;
}
.finly-footer-disclaimer {
    color: #565e70; font-size: 11.5px; line-height: 1.8; max-width: 900px;
}
</style>

<div class="finly-footer">
<div class="finly-footer-grid">
<div class="finly-footer-col">
<h4>About Finly</h4>
<div class="flink">Who I Am</div>
<div class="flink">What I Do</div>
<div class="flink">My Thinking</div>
<div class="flink">Contact</div>
</div>
<div class="finly-footer-col">
<h4>Features</h4>
<div class="flink">Dashboard</div>
<div class="flink">Transactions</div>
<div class="flink">Insights</div>
<div class="flink">Import / Export</div>
</div>
<div class="finly-footer-col">
<h4>Resources</h4>
<div class="flink">How It Works</div>
<div class="flink">FAQs</div>
<div class="flink">Source Code</div>
<div class="flink">Changelog</div>
</div>
<div class="finly-footer-col">
<h4>Careers</h4>
<div class="flink">Currently Available</div>
<div class="flink">Internships</div>
<div class="flink">Resume</div>
</div>
<div class="finly-footer-social">
<span class="label">Follow along</span>
<div class="finly-footer-social-icons">
<a href="#" title="GitHub"><svg viewBox="0 0 24 24"><path d="M9 19c-4.3 1.4-4.3-2.5-6-3m12 5v-3.5c0-1 .1-1.4-.5-2 2.8-.3 5.5-1.4 5.5-6a4.6 4.6 0 0 0-1.3-3.2 4.2 4.2 0 0 0-.1-3.2s-1.1-.3-3.5 1.3a12.3 12.3 0 0 0-6.2 0C6.5 2.8 5.4 3.1 5.4 3.1a4.2 4.2 0 0 0-.1 3.2A4.6 4.6 0 0 0 4 9.5c0 4.6 2.7 5.7 5.5 6-.6.6-.6 1.2-.5 2V21"></path></svg></a>
<a href="#" title="LinkedIn"><svg viewBox="0 0 24 24"><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle><path d="M10 9h4v2a4 4 0 0 1 7 3v7h-4v-6a2 2 0 0 0-4 0v6h-4z"></path></svg></a>
<a href="#" title="Twitter"><svg viewBox="0 0 24 24"><path d="M23 3a10.9 10.9 0 0 1-3.1.9A4.5 4.5 0 0 0 22 1.5a9 9 0 0 1-2.9 1.1 4.5 4.5 0 0 0-7.6 4.1A12.7 12.7 0 0 1 2.3 2.2a4.5 4.5 0 0 0 1.4 6 4.4 4.4 0 0 1-2-.6v.1a4.5 4.5 0 0 0 3.6 4.4 4.5 4.5 0 0 1-2 .1 4.5 4.5 0 0 0 4.2 3.1A9 9 0 0 1 1 19.5 12.7 12.7 0 0 0 7.9 21c8.3 0 12.8-6.9 12.8-12.8v-.6A9.2 9.2 0 0 0 23 3z"></path></svg></a>
<a href="#" title="Email"><svg viewBox="0 0 24 24"><rect x="2" y="4" width="20" height="16" rx="2"></rect><path d="m2 7 10 6 10-6"></path></svg></a>
</div>
</div>
</div>
<div class="finly-footer-divider"></div>
<div class="finly-footer-legal-links">
<a href="#">Terms of Use</a>
<a href="#">Privacy Policy</a>
<a href="#">Data Handling</a>
</div>
<div class="finly-footer-copyright">© 2026 Finly. Built as a personal project.</div>
<div class="finly-footer-disclaimer">
Finly is a personal finance-tracking project built for learning and portfolio purposes.
It is not a registered financial product and does not provide professional financial,
investment, or tax advice. All data you enter is stored locally on your own device and is
not shared with any third party.
</div>
</div>
""", unsafe_allow_html=True)