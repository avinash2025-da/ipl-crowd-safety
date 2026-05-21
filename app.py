"""
IPL Crowd Safety Management Dashboard — Streamlit
Run: streamlit run app.py
Install: pip install streamlit pandas numpy plotly openpyxl cohere matplotlib
"""

import os
import io
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import cohere

# ─────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IPL Crowd Safety Management Center",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

PHASE_ORDER = ["Pre-match", "First innings", "Break", "Second innings", "Exit phase"]

# ─────────────────────────────────────────────────────────
# THEMES — Redesigned with comfortable Intermediate Slate-Slate-Gray colors
# ─────────────────────────────────────────────────────────
THEMES = {
    "Intro": {
        "bg": "#1E293B", "sidebar": "#0F172A", "card": "#334155",
        "accent": "#38BDF8", "accent_lt": "#475569", "accent2": "#93C5FD",
        "text": "#FAFAFA", "text2": "#94A3B8", "border": "#475569",
        "plot_bg": "#334155", "paper_bg": "#1E293B", "grid": "#475569",
        "legend_rgba": "rgba(30,41,59,0.92)",
        "palette": ["#38BDF8", "#0EA5E9", "#FBBF24", "#34D399", "#F87171", "#A78BFA"],
        "crit_col": "#F87171", "warn_col": "#FBBF24", "ok_col": "#34D399", "info_col": "#38BDF8",
    },
    "Overview": {
        "bg": "#F8FAFC", "sidebar": "#F1F5F9", "card": "#FFFFFF",
        "accent": "#4F46E5", "accent_lt": "#EEF2FF", "accent2": "#312E81",
        "text": "#0F172A", "text2": "#64748B", "border": "#E2E8F0",
        "plot_bg": "#FFFFFF", "paper_bg": "#F8FAFC", "grid": "#F1F5F9",
        "legend_rgba": "rgba(248,250,252,0.92)",
        "palette": ["#4F46E5", "#0ea5e9", "#F59E0B", "#10B981", "#EF4444", "#8B5CF6"],
        "crit_col": "#EF4444", "warn_col": "#F59E0B", "ok_col": "#10B981", "info_col": "#4F46E5",
    },
    "Crowd Flow": {
        "bg": "#F0F9FF", "sidebar": "#E0F2FE", "card": "#FFFFFF",
        "accent": "#0284C7", "accent_lt": "#F0F9FF", "accent2": "#0C4A6E",
        "text": "#0F172A", "text2": "#64748B", "border": "#BAE6FD",
        "plot_bg": "#FFFFFF", "paper_bg": "#F0F9FF", "grid": "#E0F2FE",
        "legend_rgba": "rgba(240,249,255,0.92)",
        "palette": ["#0284C7", "#38bdf8", "#F59E0B", "#10B981", "#8B5CF6", "#EF4444"],
        "crit_col": "#EF4444", "warn_col": "#F59E0B", "ok_col": "#10B981", "info_col": "#0284C7",
    },
    "Medical & Heat": {
        "bg": "#FFF5F5", "sidebar": "#FFE3E3", "card": "#FFFFFF",
        "accent": "#E03131", "accent_lt": "#FFF5F5", "accent2": "#9C1C1C",
        "text": "#2B1B1B", "text2": "#7A6565", "border": "#FFC9C9",
        "plot_bg": "#FFFFFF", "paper_bg": "#FFF5F5", "grid": "#FFE3E3",
        "legend_rgba": "rgba(255,245,245,0.92)",
        "palette": ["#E03131", "#ff8787", "#F97316", "#8B5CF6", "#3B82F6", "#10B981"],
        "crit_col": "#E03131", "warn_col": "#F97316", "ok_col": "#10B981", "info_col": "#8B5CF6",
    },
    "Security": {
        "bg": "#FFFBEB", "sidebar": "#FEF3C7", "card": "#FFFFFF",
        "accent": "#D97706", "accent_lt": "#FEF3C7", "accent2": "#B45309",
        "text": "#1C1007", "text2": "#6B7280", "border": "#FCD34D",
        "plot_bg": "#FFFFFF", "paper_bg": "#FFFBEB", "grid": "#FFFCF0",
        "legend_rgba": "rgba(255,251,235,0.92)",
        "palette": ["#D97706", "#F59E0B", "#3B82F6", "#10B981", "#8B5CF6", "#EF4444"],
        "crit_col": "#EF4444", "warn_col": "#D97706", "ok_col": "#10B981", "info_col": "#3B82F6",
    },
    "Resource Planning": {
        "bg": "#F4FBF7", "sidebar": "#E6F4EA", "card": "#FFFFFF",
        "accent": "#0F5132", "accent_lt": "#E6F4EA", "accent2": "#0A3622",
        "text": "#1A2521", "text2": "#60716A", "border": "#C3E6CB",
        "plot_bg": "#FFFFFF", "paper_bg": "#F4FBF7", "grid": "#E6F4EA",
        "legend_rgba": "rgba(244,251,247,0.92)",
        "palette": ["#0F5132", "#198754", "#8B5CF6", "#0ea5e9", "#F59E0B", "#EF4444"],
        "crit_col": "#EF4444", "warn_col": "#F59E0B", "ok_col": "#0F5132", "info_col": "#0ea5e9",
    },
    "Risk Matrix": {
        "bg": "#FAFAFA", "sidebar": "#F4F4F5", "card": "#FFFFFF",
        "accent": "#E03131", "accent_lt": "#FFE3E3", "accent2": "#9C1C1C",
        "text": "#18181B", "text2": "#71717A", "border": "#E4E4E7",
        "plot_bg": "#FFFFFF", "paper_bg": "#FAFAFA", "grid": "#F4F4F5",
        "legend_rgba": "rgba(250,250,250,0.92)",
        "palette": ["#E03131", "#F97316", "#FBBF24", "#10B981", "#3B82F6", "#8B5CF6"],
        "crit_col": "#E03131", "warn_col": "#F97316", "ok_col": "#10B981", "info_col": "#3B82F6",
    },
    "Ask AI": {
        "bg": "#F9F8FF", "sidebar": "#F3F0FF", "card": "#FFFFFF",
        "accent": "#735BF2", "accent_lt": "#F3F0FF", "accent2": "#3B2EA6",
        "text": "#1E1743", "text2": "#7D759F", "border": "#E5E1FC",
        "plot_bg": "#FFFFFF", "paper_bg": "#F9F8FF", "grid": "#F3F0FF",
        "legend_rgba": "rgba(249,248,255,0.92)",
        "palette": ["#735BF2", "#907EFC", "#F59E0B", "#10B981", "#EF4444", "#3B82F6"],
        "crit_col": "#EF4444", "warn_col": "#F59E0B", "ok_col": "#10B981", "info_col": "#735BF2",
    },
}

PAGES = [
    ("🚀", "Intro"),
    ("🏠", "Overview"),
    ("🌊", "Crowd Flow"),
    ("🏥", "Medical & Heat"),
    ("🔒", "Security"),
    ("📦", "Resource Planning"),
    ("🚨", "Risk Matrix"),
    ("💬", "Ask AI"),
]

# Initialize active page state
if "active_page" not in st.session_state:
    st.session_state.active_page = "Intro"


# ─────────────────────────────────────────────────────────
# DATA LOAD
# ─────────────────────────────────────────────────────────
@st.cache_data
def load_all():
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

    def _read(fname):
        path = os.path.join(base, fname)
        if not os.path.exists(path):
            st.error(f"❌ Missing file: data/{fname}")
            st.stop()
        return pd.read_excel(path)

    ops     = _read("fact_operations_main.xlsx")
    inc     = _read("fact_incidents.xlsx")
    evt     = _read("fact_events.xlsx")
    zone    = _read("dim_zone.xlsx")
    stadium = _read("dim_stadium.xlsx")

    for df in [ops, inc, evt, zone, stadium]:
        df.columns = df.columns.str.strip().str.lower()

    ops = ops.merge(zone[["zone_id", "zone_name", "zone_type"]], on="zone_id", how="left")

    zone_s = zone[["zone_id", "stadium_id"]].merge(
        stadium[["stadium_id", "stadium_name"]], on="stadium_id", how="left"
    )
    ops = ops.merge(zone_s[["zone_id", "stadium_name"]], on="zone_id", how="left")

    evt_cols = ["event_id", "season_year", "is_final_match", "total_attendance"]
    ops = ops.merge(evt[evt_cols], on="event_id", how="left")

    ops["heat_risk_index"]      = ops["temperature_celsius"] * 0.7 + ops["humidity_percent"] * 0.3
    ops["occupancy_pct"]        = ops["occupancy_rate"] * 100
    ops["capacity_breach"]      = (ops["occupancy_rate"] >= 0.55).astype(int)
    ops["staff_adequacy_ratio"] = np.where(
        ops["people_count"] > 0,
        ops["required_staff"] / ops["people_count"] * 1000, 0
    )

    ops["occupancy_risk_band"] = pd.cut(
        ops["occupancy_rate"],
        bins=[-np.inf, 0.45, 0.60, 0.70, np.inf],
        labels=["Low", "Moderate", "High", "Critical"]
    )

    ops["queue_stress"] = pd.cut(
        ops["avg_queue_wait_time"],
        bins=[-np.inf, 10, 20, 25, np.inf],
        labels=["Acceptable under 10 min", "Moderate 10-20 min",
                "High 20-25 min", "Extreme 25+ min"]
    )

    q75 = evt["total_attendance"].quantile(0.75)
    q40 = evt["total_attendance"].quantile(0.40)
    evt["match_category"] = np.select(
        [evt["is_final_match"] == 1,
         evt["total_attendance"] >= q75,
         evt["total_attendance"] >= q40],
        ["Final Match", "High Attendance Match", "Moderate Attendance Match"],
        default="Regular Match"
    )
    ops = ops.merge(evt[["event_id", "match_category"]], on="event_id", how="left")
    ops["match_category"] = ops["match_category"].fillna("Regular Match")

    inc = inc.merge(evt[["event_id", "season_year"]], on="event_id", how="left")
    inc = inc.merge(zone_s[["zone_id", "stadium_name"]], on="zone_id", how="left")

    return ops, inc


try:
    ops, inc = load_all()
except Exception as e:
    st.error(f"❌ Data load error: {e}")
    st.stop()


# ─────────────────────────────────────────────────────────
# CSS — with draggable sidebar resizer & centered Layout
# ─────────────────────────────────────────────────────────
def inject_css(t):
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Sora:wght@600;700;800&display=swap');

html, body, [class*="css"] {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
.stApp {{ background-color: {t['bg']}; color: {t['text']}; }}
.block-container {{ padding-top: 4.2rem; padding-bottom: 2rem; max-width: 1580px; }}

/* ── Draggable/Resizable Sidebar ── */
section[data-testid="stSidebar"] {{
    background-color: {t['sidebar']};
    border-right: 3px solid {t['border']};
    min-width: 200px !important;
    max-width: 420px !important;
    resize: horizontal;
    overflow: auto;
    position: relative;
}}
section[data-testid="stSidebar"]::after {{
    content: '⠿';
    position: absolute;
    top: 50%;
    right: 4px;
    transform: translateY(-50%);
    font-size: 18px;
    color: {t['border']};
    cursor: col-resize;
    pointer-events: none;
    opacity: 0.6;
}}
section[data-testid="stSidebar"] * {{ color: {t['text']} !important; }}
section[data-testid="stSidebar"] .stButton > button {{
    width: 100% !important; text-align: left !important;
    background: {t['card']} !important; border: 1px solid {t['border']} !important;
    border-radius: 12px !important; padding: 10px 14px !important;
    font-size: 13px !important; font-weight: 700 !important;
    color: {t['text']} !important; margin-bottom: 5px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
    transition: all 0.18s ease !important;
}}
section[data-testid="stSidebar"] .stButton > button:hover {{
    background: {t['accent_lt']} !important;
    border-color: {t['accent']} !important;
    color: {t['accent2']} !important;
    transform: translateX(2px) !important;
}}

/* ── Centered Page Header Layout ── */
.dash-header {{
    background: linear-gradient(120deg, {t['card']} 60%, {t['accent_lt']});
    border: 1px solid {t['border']}; border-top: 5px solid {t['accent']};
    border-radius: 18px; padding: 26px 28px 24px;
    margin-bottom: 24px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.05);
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}}
.dash-icon {{ font-size: 44px; line-height: 1; margin-bottom: 12px; }}
.dash-title {{
    font-family: 'Sora', sans-serif; font-size: 26px; font-weight: 800;
    color: {t['text']}; margin: 0 0 8px 0; letter-spacing: -0.3px;
}}
.dash-sub {{ font-size: 13px; color: {t['text2']}; margin: 0; max-width: 800px; line-height: 1.5; }}

/* ── Centered KPI Card Layout ── */
.kpi-card {{
    background: {t['card']}; border: 1px solid {t['border']};
    border-radius: 16px; padding: 22px 16px 18px;
    min-height: 110px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    position: relative; overflow: hidden;
    margin-bottom: 16px;
    text-align: center;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
}}
.kpi-card::before {{
    content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 4px;
}}
.kpi-info::before  {{ background: linear-gradient(90deg, {t['info_col']}, {t['accent2']}); }}
.kpi-warn::before  {{ background: linear-gradient(90deg, {t['warn_col']}, #FBBF24); }}
.kpi-crit::before  {{ background: linear-gradient(90deg, {t['crit_col']}, #F87171); }}
.kpi-ok::before    {{ background: linear-gradient(90deg, {t['ok_col']}, #34D399); }}

.kpi-label {{
    font-size: 10px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1px; color: {t['text2']}; margin-bottom: 10px;
    text-align: center; width: 100%;
}}
.kpi-val {{
    font-family: 'Sora', sans-serif; font-size: 30px; font-weight: 800;
    color: {t['text']}; line-height: 1; text-align: center;
}}
.kpi-sub {{
    font-size: 10px; color: {t['text2']}; margin-top: 8px;
    text-align: center; width: 100%;
}}

.sec-lbl {{
    font-family: 'Sora', sans-serif; font-size: 12px; font-weight: 700;
    color: {t['accent2']}; text-transform: uppercase; letter-spacing: 0.9px;
    margin: 22px 0 12px 0; padding-bottom: 6px;
    border-bottom: 2px solid {t['accent_lt']};
}}

/* ── AI Section Header & Banner (at the absolute bottom of each page) ── */
.ai-section-divider {{
    margin: 40px 0 16px 0;
    padding: 14px 20px;
    background: linear-gradient(90deg, {t['accent_lt']}, transparent);
    border-left: 5px solid {t['accent']};
    border-radius: 10px;
    font-family: 'Sora', sans-serif;
    font-size: 14px; font-weight: 800;
    color: {t['accent2']};
    letter-spacing: 0.5px;
}}
.ai-card {{
    background: {t["card"]}; border: 1px solid {t["border"]}; border-radius: 18px;
    padding: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    margin-bottom: 14px; color: {t["text"]};
}}
.ai-mini-card {{
    background: {t["card"]}; border: 1px solid {t["border"]};
    border-left: 5px solid {t["accent"]}; border-radius: 14px;
    padding: 14px; margin-bottom: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    text-align: center;
}}
.ai-metric {{
    font-size: 28px; font-weight: 800; color: {t["text"]};
    font-family: 'Sora', sans-serif; text-align: center;
}}
.ai-label {{
    font-size: 11px; text-transform: uppercase; font-weight: 700;
    letter-spacing: 0.7px; color: {t["text2"]}; text-align: center;
}}
.ai-status-critical {{ color: #DC2626; font-weight: 700; font-size: 12px; text-align: center; }}
.ai-status-warning  {{ color: #F59E0B; font-weight: 700; font-size: 12px; text-align: center; }}
.ai-status-good     {{ color: #10B981; font-weight: 700; font-size: 12px; text-align: center; }}

.insight-pill {{
    display: inline-block; padding: 6px 14px; border-radius: 999px;
    font-size: 11px; font-weight: 700; margin-bottom: 10px;
    background: {t["accent_lt"]}; color: {t["accent2"]};
}}

div[data-testid="stPlotlyChart"] > div {{
    border-radius: 14px !important; border: 1px solid {t['border']} !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
}}
[data-testid="stDataFrame"] {{
    border-radius: 12px; border: 1px solid {t['border']}; overflow: hidden;
}}

::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: {t['bg']}; }}
::-webkit-scrollbar-thumb {{ background: {t['border']}; border-radius: 3px; }}
hr {{ border-color: {t['border']} !important; opacity: 0.6; }}
</style>

<script>
// Resize controller script
(function() {{
    function initSidebarResize() {{
        var sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
        if (!sidebar) return;
        sidebar.style.resize = 'horizontal';
        sidebar.style.overflow = 'auto';
        sidebar.style.minWidth = '200px';
        sidebar.style.maxWidth = '450px';
    }}
    setTimeout(initSidebarResize, 800);
}})();
</script>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────
def kpi_card(label, value, style="info", sub=""):
    sub_html = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    st.markdown(f"""
<div class="kpi-card kpi-{style}">
  <div class="kpi-label">{label}</div>
  <div class="kpi-val">{value}</div>
  {sub_html}
</div>""", unsafe_allow_html=True)


def page_header(icon, title, subtitle):
    st.markdown(f"""
<div class="dash-header">
  <div class="dash-icon">{icon}</div>
  <div class="dash-title">{title}</div>
  <div class="dash-sub">{subtitle}</div>
</div>""", unsafe_allow_html=True)


def sec_label(text):
    st.markdown(f'<div class="sec-lbl">{text}</div>', unsafe_allow_html=True)


def ai_section_header(text):
    st.markdown(f'<div class="ai-section-divider">{text}</div>', unsafe_allow_html=True)


def get_cohere_key():
    """Retrieves Cohere API key from st.secrets first, then os.environ."""
    # Try secrets
    try:
        key = st.secrets.get("COHERE_API_KEY", "")
        if key:
            return key
    except Exception:
        pass
    # Try environment variable
    key = os.environ.get("COHERE_API_KEY", "")
    if key:
        return key
    return ""


def extract_cohere_text(response):
    """Safely extracts text response across different Cohere SDK versions and shapes."""
    if hasattr(response, "text") and response.text:
        return response.text
    elif isinstance(response, dict) and "text" in response:
        return response["text"]
    elif hasattr(response, "generations") and response.generations:
        return response.generations[0].text
    elif hasattr(response, "reply") and response.reply:
        return response.reply
    else:
        return str(response)


def generate_cohere_insights(summary_text, page_name, temperature_value=0.4, token_value=700):
    api_key = get_cohere_key()
    if not api_key:
        return (
            "⚠️ Cohere API key not configured.\n\n"
            "To enable AI insights:\n"
            "1. Go to Streamlit Cloud → your app → Settings → Secrets\n"
            "2. Add: `COHERE_API_KEY = \"your_key_here\"`\n"
            "3. Get your key free at: https://dashboard.cohere.com/api-keys"
        )
    try:
        co = cohere.Client(api_key)
        prompt = f"""
You are a world-class professional IPL stadium crowd safety analyst and operations control director.
Provide a highly specialized, context-aware analysis based exactly on the dashboard parameters and telemetry of page "{page_name}".

STADIUM DATA SUMMARY:
{summary_text}

Analyze the data and structure your answer into these clean Markdown sections:
1. **📌 Key Operational Insights**: Core trends and metrics that require attention based on current values.
2. **⚠️ Critical Risks & Hotspots**: Risks regarding densities, heat variables, emergency response speeds, or unauthorized attempts.
3. **✅ Priority Action Blueprint**: Tactical tasks to deploy operation coordinators, paramedics, or safety barricades right now.

Be extremely domain-oriented. Cite specific stands, metrics, and phases when possible. Keep the language authoritative, professional, and practical.
"""
        response = co.chat(
            model="command-r-plus-08-2024",
            message=prompt,
            temperature=temperature_value,
            max_tokens=token_value,
        )
        return extract_cohere_text(response)
    except Exception as e:
        return f"❌ Cohere insight generation failed: {e}"


def ask_ai_question(question, context_text, temperature_value=0.3, token_value=500):
    api_key = get_cohere_key()
    if not api_key:
        return "⚠️ Cohere API key not configured."
    try:
        co = cohere.Client(api_key)
        prompt = f"""
You are an expert AI Operations Advisor inside an IPL Crowd Safety Dashboard.
Answer the user's operational query with professional authority, grounding your response heavily in the provided raw dataset context under STADIUM FIELD CONTEXT, combined with your expert domain knowledge of stadium crowd management.

STADIUM FIELD CONTEXT:
{context_text}

USER OPERATIONAL QUESTION:
{question}

Provide actionable, metrics-backed stadium control tasks. Be direct, comprehensive, and concise. Reference specific stands/metrics from the context if relevant.
"""
        response = co.chat(
            model="command-r-plus-08-2024",
            message=prompt,
            temperature=temperature_value,
            max_tokens=token_value,
        )
        return extract_cohere_text(response)
    except Exception as e:
        return f"❌ Q&A failed: {e}"


def sfig(fig, t, h=320):
    fig.update_layout(
        height=h,
        paper_bgcolor=t["paper_bg"],
        plot_bgcolor=t["plot_bg"],
        font=dict(color=t["text"], family="Plus Jakarta Sans", size=12),
        title_font=dict(color=t["text"], size=14, family="Sora"),
        title_x=0.03,
        legend=dict(
            bgcolor=t["legend_rgba"], bordercolor=t["border"], borderwidth=1,
            font=dict(color=t["text2"], size=11),
        ),
        margin=dict(l=35, r=20, t=55, b=35),
        colorway=t["palette"],
    )
    fig.update_xaxes(
        gridcolor=t["grid"], zerolinecolor=t["grid"], linecolor=t["border"],
        tickfont=dict(color=t["text2"]), title_font=dict(color=t["text2"]),
    )
    fig.update_yaxes(
        gridcolor=t["grid"], zerolinecolor=t["grid"], linecolor=t["border"],
        tickfont=dict(color=t["text2"]), title_font=dict(color=t["text2"]),
    )
    return fig


def safe_norm(series):
    min_val, max_val = series.min(), series.max()
    if pd.isna(min_val) or pd.isna(max_val) or max_val == min_val:
        return pd.Series(0, index=series.index)
    return ((series - min_val) / (max_val - min_val)) * 100


def add_advanced_risk_features(df):
    df = df.copy()
    df["security_total"] = (
        df["security_incidents"].fillna(0)
        + df["unauthorized_entry_attempts"].fillna(0)
        + df["counterfeit_ticket_cases"].fillna(0)
        + df["fan_ejections"].fillna(0)
    )
    df["risk_score"] = (
        safe_norm(df["crowd_pressure_index"].fillna(0)) * 0.25
        + safe_norm(df["bottleneck_risk_score"].fillna(0)) * 0.25
        + safe_norm(df["avg_queue_wait_time"].fillna(0)) * 0.15
        + safe_norm(df["ambulance_response_time"].fillna(0)) * 0.15
        + safe_norm(df["heat_risk_index"].fillna(0)) * 0.10
        + safe_norm(df["security_total"].fillna(0)) * 0.10
    ).round(2)
    df["risk_band"] = pd.cut(
        df["risk_score"], bins=[-1, 40, 70, 101],
        labels=["Safe", "Monitor", "Critical"]
    )
    df["risk_reason"] = np.select(
        [df["bottleneck_risk_score"] >= 70,
         df["ambulance_response_time"] >= 10,
         df["avg_queue_wait_time"] >= 20,
         df["heat_risk_index"] >= df["heat_risk_index"].quantile(0.75),
         df["security_total"] >= df["security_total"].quantile(0.75)],
        ["High bottleneck risk", "Delayed medical response", "Long queue wait time",
         "High heat exposure", "High security activity"],
        default="Normal operating condition"
    )
    df["recommended_action"] = np.select(
        [df["risk_reason"] == "High bottleneck risk",
         df["risk_reason"] == "Delayed medical response",
         df["risk_reason"] == "Long queue wait time",
         df["risk_reason"] == "High heat exposure",
         df["risk_reason"] == "High security activity"],
        ["Add barricades and redirect crowd flow",
         "Deploy extra medical team and ambulance support",
         "Open additional gates and improve queue control",
         "Provide water points and cooling zones",
         "Increase security staff and access checks"],
        default="Continue monitoring"
    )
    return df


def create_risk_priority_matrix(df):
    cols = ["stadium_name", "zone_name", "zone_type", "phase",
            "risk_score", "risk_band", "risk_reason", "recommended_action",
            "people_count", "avg_queue_wait_time", "ambulance_response_time",
            "bottleneck_risk_score", "heat_risk_index"]
    available_cols = [c for c in cols if c in df.columns]
    matrix = df[available_cols].sort_values("risk_score", ascending=False).head(15).copy()
    matrix.rename(columns={
        "stadium_name": "Stadium", "zone_name": "Zone", "zone_type": "Zone Type",
        "phase": "Phase", "risk_score": "Risk Score", "risk_band": "Risk Band",
        "risk_reason": "Main Risk Reason", "recommended_action": "Recommended Action",
        "people_count": "People Count", "avg_queue_wait_time": "Queue Wait",
        "ambulance_response_time": "Ambulance Response",
        "bottleneck_risk_score": "Bottleneck Score", "heat_risk_index": "Heat Risk",
    }, inplace=True)
    return matrix


def create_anomaly_table(df):
    metrics = ["avg_queue_wait_time", "ambulance_response_time", "bottleneck_risk_score",
               "crowd_pressure_index", "heat_risk_index", "security_total", "medical_incidents"]
    temp = df.copy()
    existing_metrics = [m for m in metrics if m in temp.columns]
    anomaly_flags = []
    for metric in existing_metrics:
        threshold = temp[metric].quantile(0.90)
        flag_col = f"{metric}_anomaly"
        temp[flag_col] = temp[metric] >= threshold
        anomaly_flags.append(flag_col)
    temp["anomaly_count"] = temp[anomaly_flags].sum(axis=1)
    temp["anomaly_reason"] = temp.apply(
        lambda row: ", ".join([
            metric.replace("_", " ").title()
            for metric in existing_metrics
            if row.get(f"{metric}_anomaly", False)
        ]), axis=1
    )
    anomalies = temp[temp["anomaly_count"] > 0].copy()
    cols = ["stadium_name", "zone_name", "zone_type", "phase",
            "anomaly_count", "anomaly_reason", "risk_score",
            "avg_queue_wait_time", "ambulance_response_time",
            "bottleneck_risk_score", "heat_risk_index"]
    available_cols = [c for c in cols if c in anomalies.columns]
    anomalies = anomalies[available_cols].sort_values(
        ["anomaly_count", "risk_score"], ascending=False
    ).head(15)
    anomalies.rename(columns={
        "stadium_name": "Stadium", "zone_name": "Zone", "zone_type": "Zone Type",
        "phase": "Phase", "anomaly_count": "Anomaly Count", "anomaly_reason": "Anomaly Reason",
        "risk_score": "Risk Score", "avg_queue_wait_time": "Queue Wait",
        "ambulance_response_time": "Ambulance Response",
        "bottleneck_risk_score": "Bottleneck Score", "heat_risk_index": "Heat Risk",
    }, inplace=True)
    return anomalies


def dataframe_to_csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8")


# ─────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div style="text-align:center;padding:12px 0 20px 0;">
  <div style="font-size:36px; margin-bottom:8px;">🏏</div>
  <div style="font-family:'Sora',sans-serif;font-size:16px;font-weight:800;color:#F8F8FF;">
    IPL Crowd Safety
  </div>
  <div style="font-size:10px;letter-spacing:1.2px;font-weight:700;color:#94A3B8;margin-top:4px;text-transform:uppercase;">
    Stadium Operations Command
  </div>
</div>""", unsafe_allow_html=True)

    # Sidebar Page Selection Navigation
    for icon, name in PAGES:
        # Give active tab visual feedback using static key and conditional label
        is_active = (st.session_state.active_page == name)
        label_text = f"{icon}  {name}   ◀" if is_active else f"{icon}  {name}"
        if st.button(label_text, key=f"nav_{name}"):
            st.session_state.active_page = name
            st.rerun()

    st.markdown("<hr style='margin:16px 0; opacity:0.3;'>", unsafe_allow_html=True)

    # Active filters sidebar block: Only render when NOT on the Welcome Intro page!
    if st.session_state.active_page != "Intro":
        st.markdown(
            '<p style="font-size:10px;font-weight:800;letter-spacing:1px;margin:0 0 10px 0;color:#94A3B8;text-transform:uppercase;">FILTER TELEMETRY</p>',
            unsafe_allow_html=True)

        all_stadiums = sorted(ops["stadium_name"].dropna().unique())
        sel_stadium  = st.multiselect("Stadium Venue",  all_stadiums, default=all_stadiums, key="f_stad")
        sel_phase    = st.multiselect("Match Phase",    PHASE_ORDER,  default=PHASE_ORDER,  key="f_ph")
        all_years    = sorted(ops["season_year"].dropna().astype(int).unique())
        sel_year     = st.multiselect("Season Year",    all_years,    default=all_years,    key="f_yr")
        all_zones    = sorted(ops["zone_type"].dropna().unique())
        sel_zone     = st.multiselect("Zone Category",  all_zones,    default=all_zones,    key="f_zt")
        all_cats     = sorted(ops["match_category"].dropna().unique())
        sel_cat      = st.multiselect("Match Category", all_cats,     default=all_cats,     key="f_mc")

        st.markdown("<hr style='margin:16px 0; opacity:0.3;'>", unsafe_allow_html=True)
        st.markdown(
            '<p style="font-size:10px;font-weight:800;letter-spacing:1px;margin:0 0 10px 0;color:#94A3B8;text-transform:uppercase;">COHERE AI TUNING</p>',
            unsafe_allow_html=True)
        ai_temperature = st.slider("Model Temperature", 0.0, 1.0, 0.4, 0.1)
        ai_max_tokens  = st.slider("Max Response Tokens", 100, 2000, 750, 100)
    else:
        # Dummy fallbacks for the initial page load when data filtering is not yet needed
        all_stadiums = sorted(ops["stadium_name"].dropna().unique())
        sel_stadium  = all_stadiums
        sel_phase    = PHASE_ORDER
        all_years    = sorted(ops["season_year"].dropna().astype(int).unique())
        sel_year     = all_years
        all_zones    = sorted(ops["zone_type"].dropna().unique())
        sel_zone     = all_zones
        all_cats     = sorted(ops["match_category"].dropna().unique())
        sel_cat      = all_cats
        ai_temperature = 0.4
        ai_max_tokens  = 750


# ─────────────────────────────────────────────────────────
# RENDER PAGES
# ─────────────────────────────────────────────────────────
page = st.session_state.active_page
t    = THEMES[page]
inject_css(t)

# ═══════════════════════════════════════════════════════════
# PAGE 0 — INTRO LANDING PAGE (Clean Intermediate Blue-Slate Theme)
# ═══════════════════════════════════════════════════════════
if page == "Intro":
    st.markdown(f"""
<div class="intro-hero" style="background: linear-gradient(135deg, {t['bg']} 0%, {t['sidebar']} 100%); border: 1px solid {t['border']}; box-shadow: 0 10px 30px rgba(0,0,0,0.3); border-radius: 24px; padding: 40px; margin-bottom: 30px; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center;">
  <div class="intro-badge" style="background: rgba(56,189,248,0.15); border: 1px solid {t['accent']}; color: {t['accent']}; padding: 6px 14px; border-radius: 999px; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 18px;">🏏 Stadium Command Operations Suite</div>
  <h1 class="intro-title" style="color: {t['text']}; font-family: 'Sora', sans-serif; font-size: 36px; font-weight: 800; line-height: 1.25; margin-bottom: 12px;">IPL Crowd Safety<br><span style="background: linear-gradient(90deg, {t['accent']}, {t['accent2']}); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Management Control Platform</span></h1>
  <p class="intro-desc" style="color: {t['text2']}; max-width: 780px; font-size: 14px; line-height: 1.6; margin: 0 auto;">
    An advanced executive analytics console engineered to support stadium commanders, safety directors, and logistics staff. 
    Monitor human densities, thermal thresholds, emergency paramedic transit parameters, and security occurrences across multi-season IPL venues.
  </p>
</div>
""", unsafe_allow_html=True)

    total_records = len(ops)
    total_stadiums = ops["stadium_name"].nunique()
    total_zones = ops["zone_name"].nunique() if "zone_name" in ops.columns else 0
    total_years = ops["season_year"].nunique()

    # Center statistics row
    st.markdown(f"""
    <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-bottom: 30px;">
        <div style="background: {t['card']}; border: 1px solid {t['border']}; border-radius: 16px; padding: 18px 24px; min-width: 160px; text-align: center;">
            <span style="font-family: 'Sora', sans-serif; font-size: 26px; font-weight: 800; color: {t['accent']}; display: block;">{total_records:,}</span>
            <span style="font-size: 10px; font-weight: 700; color: {t['text2']}; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 4px; display: block;">Audit Data Points</span>
        </div>
        <div style="background: {t['card']}; border: 1px solid {t['border']}; border-radius: 16px; padding: 18px 24px; min-width: 160px; text-align: center;">
            <span style="font-family: 'Sora', sans-serif; font-size: 26px; font-weight: 800; color: {t['accent']}; display: block;">{total_stadiums}</span>
            <span style="font-size: 10px; font-weight: 700; color: {t['text2']}; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 4px; display: block;">Major Venues</span>
        </div>
        <div style="background: {t['card']}; border: 1px solid {t['border']}; border-radius: 16px; padding: 18px 24px; min-width: 160px; text-align: center;">
            <span style="font-family: 'Sora', sans-serif; font-size: 26px; font-weight: 800; color: {t['accent']}; display: block;">{total_zones}</span>
            <span style="font-size: 10px; font-weight: 700; color: {t['text2']}; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 4px; display: block;">Mapped Zones</span>
        </div>
        <div style="background: {t['card']}; border: 1px solid {t['border']}; border-radius: 16px; padding: 18px 24px; min-width: 160px; text-align: center;">
            <span style="font-family: 'Sora', sans-serif; font-size: 26px; font-weight: 800; color: {t['accent']}; display: block;">{total_years}</span>
            <span style="font-size: 10px; font-weight: 700; color: {t['text2']}; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 4px; display: block;">IPL Seasons</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    sec_label("Interactive Dashboard Modules Guide")

    # Beautiful module grid explaining EXACTLY what each page is for
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style="background: {t['card']}; border: 1px solid {t['border']}; border-radius: 18px; padding: 22px 20px; min-height: 180px;">
            <span style="font-size: 30px; margin-bottom: 10px; display: block;">🏠</span>
            <div style="font-family: 'Sora', sans-serif; font-size: 15px; font-weight: 800; color: {t['text']}; margin-bottom: 8px;">Executive Overview</div>
            <div style="font-size: 12px; color: {t['text2']}; line-height: 1.6;">Compile critical safety, crowd pressure, medical incident occurrences, and capacity breach indicators into a fast executive command deck.</div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        st.markdown(f"""
        <div style="background: {t['card']}; border: 1px solid {t['border']}; border-radius: 18px; padding: 22px 20px; min-height: 180px;">
            <span style="font-size: 30px; margin-bottom: 10px; display: block;">📦</span>
            <div style="font-family: 'Sora', sans-serif; font-size: 15px; font-weight: 800; color: {t['text']}; margin-bottom: 8px;">Logistical Resource Planner</div>
            <div style="font-size: 12px; color: {t['text2']}; line-height: 1.6;">Proactively schedule security marshals, temporary physical barricades, and paramedic teams according to real-time risk scores.</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="background: {t['card']}; border: 1px solid {t['border']}; border-radius: 18px; padding: 22px 20px; min-height: 180px;">
            <span style="font-size: 30px; margin-bottom: 10px; display: block;">🌊</span>
            <div style="font-family: 'Sora', sans-serif; font-size: 15px; font-weight: 800; color: {t['text']}; margin-bottom: 8px;">Crowd Flow & Congestion</div>
            <div style="font-size: 12px; color: {t['text2']}; line-height: 1.6;">Monitor gate wait queue benchmarks, zone loading patterns, and bottleneck risk ratios from pre-match gates opening to post-match exit.</div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        st.markdown(f"""
        <div style="background: {t['card']}; border: 1px solid {t['border']}; border-radius: 18px; padding: 22px 20px; min-height: 180px;">
            <span style="font-size: 30px; margin-bottom: 10px; display: block;">🚨</span>
            <div style="font-family: 'Sora', sans-serif; font-size: 15px; font-weight: 800; color: {t['text']}; margin-bottom: 8px;">Risk Decision Matrix</div>
            <div style="font-size: 12px; color: {t['text2']}; line-height: 1.6;">Leverages advanced multi-metric weighted equations to identify and isolate critical safety vulnerabilities across complex stadium coordinates.</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="background: {t['card']}; border: 1px solid {t['border']}; border-radius: 18px; padding: 22px 20px; min-height: 180px;">
            <span style="font-size: 30px; margin-bottom: 10px; display: block;">🏥</span>
            <div style="font-family: 'Sora', sans-serif; font-size: 15px; font-weight: 800; color: {t['text']}; margin-bottom: 8px;">Medical & Heat Stress</div>
            <div style="font-size: 12px; color: {t['text2']}; line-height: 1.6;">Assess ambient humidity, wet-bulb heat scores, ambulance transit times, and medical emergency incident statistics to protect critical stands.</div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        st.markdown(f"""
        <div style="background: {t['card']}; border: 1px solid {t['border']}; border-radius: 18px; padding: 22px 20px; min-height: 180px;">
            <span style="font-size: 30px; margin-bottom: 10px; display: block;">💬</span>
            <div style="font-family: 'Sora', sans-serif; font-size: 15px; font-weight: 800; color: {t['text']}; margin-bottom: 8px;">Ask AI Dialog Center</div>
            <div style="font-size: 12px; color: {t['text2']}; line-height: 1.6;">Type natural questions or query ready presets to extract immediate, clear operations recommendations powered by Cohere Command models.</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(56,189,248,0.1), rgba(30,41,59,0.8)); border: 1px solid {t['border']}; border-radius: 20px; padding: 28px; text-align: center;">
        <div style="font-family: 'Sora', sans-serif; font-size: 20px; font-weight: 800; color: {t['text']}; margin-bottom: 10px;">🚀 Launch Stadium Command Control</div>
        <p style="font-size: 13px; color: {t['accent2']}; margin-bottom: 0;">Navigate to dashboard indicators using the <b>🏠 Overview</b> button located in the sidebar menu. Filter by year, phase, or specific stands to focus safely.</p>
    </div>
    """, unsafe_allow_html=True)

    st.stop()


# ─────────────────────────────────────────────────────────
# FILTER CHECKS (Defensive stop)
# ─────────────────────────────────────────────────────────
f = ops[
    ops["stadium_name"].isin(sel_stadium) &
    ops["phase"].isin(sel_phase) &
    ops["season_year"].astype(int).isin(sel_year) &
    ops["zone_type"].isin(sel_zone) &
    ops["match_category"].isin(sel_cat)
].copy()

if f.empty:
    st.warning("⚠️ No data for the selected filters. Please widen your selection in the custom sidebar.")
    st.stop()

f["phase_cat"] = pd.Categorical(f["phase"], categories=PHASE_ORDER, ordered=True)

inc_f = inc[
    inc["stadium_name"].isin(sel_stadium) &
    inc["season_year"].astype(int).isin(sel_year)
].copy() if "stadium_name" in inc.columns and "season_year" in inc.columns else inc.copy()

f             = add_advanced_risk_features(f)
risk_matrix   = create_risk_priority_matrix(f)
anomaly_table = create_anomaly_table(f)

# ─────────────────────────────────────────────────────────
# KPI SCORES CALCULATIONS
# ─────────────────────────────────────────────────────────
safety_risk         = round(f["crowd_pressure_index"].mean() * 0.40
                            + f["bottleneck_risk_score"].mean() * 0.35
                            + f["avg_queue_wait_time"].mean() * 0.25, 2)
overall_risk_score  = round(f["risk_score"].mean(), 2)
critical_zone_count = int((f["risk_band"] == "Critical").sum())
monitor_zone_count  = int((f["risk_band"] == "Monitor").sum())
med_rate            = round(f["medical_incidents"].sum() / max(f["people_count"].sum(), 1) * 1000, 2)
cap_breach          = round(f["capacity_breach"].mean() * 100, 2)
amb_resp            = round(f["ambulance_response_time"].mean(), 2)
avg_queue           = round(f["avg_queue_wait_time"].mean(), 2)
avg_pressure        = round(f["crowd_pressure_index"].mean(), 2)
avg_bottleneck      = round(f["bottleneck_risk_score"].mean(), 2)
avg_heat            = round(f["heat_risk_index"].mean(), 2)
high_risk_zones     = int(f[f["bottleneck_risk_score"] >= 70]["zone_id"].nunique())
delayed_med         = int(f[f["ambulance_response_time"] >= 10]["zone_id"].nunique())
res_rate = round(
    inc_f[inc_f["status"] == "Resolved"].shape[0] / max(len(inc_f), 1) * 100, 2
) if not inc_f.empty and "status" in inc_f.columns else 0
unauthorized = int(f["unauthorized_entry_attempts"].sum())
counterfeit  = int(f["counterfeit_ticket_cases"].sum())
pitch_inv    = int(f["pitch_invasion_attempt"].sum())
fan_ej       = int(f["fan_ejections"].sum())
req_staff    = int(f["required_staff"].sum())
req_barr     = int(f["required_barricades"].sum())
med_teams    = int(f["deployed_medical_teams"].sum())
staff_ratio  = round(f["staff_adequacy_ratio"].mean(), 2)
top_risk_text = risk_matrix.head(5).to_string(index=False)

summary_text = f"""
Selected Filters Summary:
Stadiums: {', '.join(map(str, sel_stadium))}
Phases: {', '.join(map(str, sel_phase))}
Years: {', '.join(map(str, sel_year))}
Zone Types: {', '.join(map(str, sel_zone))}
Match Categories: {', '.join(map(str, sel_cat))}

Dashboard KPIs:
Overall Risk Score: {overall_risk_score}
Safety Risk Score: {safety_risk}
Critical Records/Zones Count: {critical_zone_count}
Monitor Records/Zones Count: {monitor_zone_count}
Medical Incident Rate: {med_rate} per 1000 people
Capacity Breach Percentage: {cap_breach}%
Resolution Rate: {res_rate}%
Average Ambulance Response Time: {amb_resp} minutes
Average Queue Wait Time: {avg_queue} minutes
Average Crowd Pressure Index: {avg_pressure}
Average Bottleneck Risk Score: {avg_bottleneck}
Average Heat Risk Index: {avg_heat}
High Risk Zones: {high_risk_zones}
Delayed Medical Zones: {delayed_med}
Unauthorized Entries: {unauthorized}
Counterfeit Ticket Cases: {counterfeit}
Pitch Invasion Attempts: {pitch_inv}
Fan Ejections: {fan_ej}
Required Staff: {req_staff}
Required Barricades: {req_barr}
Medical Teams: {med_teams}
Staff Adequacy Ratio: {staff_ratio}

Top Risk Priority Matrix:
{top_risk_text}
"""


# ═══════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ═══════════════════════════════════════════════════════════
if page == "Overview":
    page_header("🏠",
                "IPL Stadium Operations Master Command Dashboard",
                "Unified oversight compiling live safety metric trends, resource staffing balances, ambulance coordination, and match risk priority alerts.")

    # KPI Layout centered!
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1: kpi_card("Overall Risk Score",    str(overall_risk_score),      "crit", "Aggregate live score")
    with k2: kpi_card("Medical Incident Rate", str(med_rate),                "warn", "Per 1K spectators")
    with k3: kpi_card("Capacity Breach Ratio", f"{cap_breach}%",             "info", "Zones near/above limit")
    with k4: kpi_card("Incident Resolution",   f"{res_rate}%",               "ok",   "Current resolution rate")
    with k5: kpi_card("Ambulance Response",    f"{amb_resp} min",            "warn", "Mean response delay")

    st.write("")

    # Visualizations
    c1, c2 = st.columns([1.6, 1])
    with c1:
        tr = (f.groupby(["phase_cat", "zone_type"], as_index=False)["bottleneck_risk_score"]
              .mean().sort_values("phase_cat"))
        tr["phase"] = tr["phase_cat"].astype(str)
        fig = px.line(tr, x="phase", y="bottleneck_risk_score", color="zone_type",
                      markers=True, color_discrete_sequence=t["palette"],
                      title="Bottleneck Congestion Trend Across Match Phases")
        st.plotly_chart(sfig(fig, t, 310), use_container_width=True)
    with c2:
        rbc = f["risk_band"].value_counts().reset_index()
        rbc.columns = ["Risk Band", "Count"]
        fig = px.pie(rbc, names="Risk Band", values="Count", hole=0.55,
                     color="Risk Band",
                     color_discrete_map={"Critical": t["crit_col"],
                                         "Monitor": t["warn_col"], "Safe": t["ok_col"]},
                     title="Zone Threat Distribution Pie")
        st.plotly_chart(sfig(fig, t, 310), use_container_width=True)

    c3, c4 = st.columns([1.6, 1])
    with c3:
        mc = f["match_category"].value_counts().reset_index()
        mc.columns = ["match_category", "count"]
        fig = px.bar(mc, y="match_category", x="count", orientation="h",
                     color="match_category", color_discrete_sequence=t["palette"],
                     title="Proportion of Monitored Matches")
        fig.update_layout(showlegend=False)
        st.plotly_chart(sfig(fig, t, 290), use_container_width=True)
    with c4:
        pres = f.groupby("zone_type", as_index=False)["risk_score"].mean()
        fig = px.bar(pres, x="zone_type", y="risk_score", color="zone_type",
                     color_discrete_sequence=t["palette"],
                     title="Advanced Combined Risk Score by Zone Category")
        fig.update_layout(showlegend=False)
        st.plotly_chart(sfig(fig, t, 290), use_container_width=True)

    # Risk matrices
    sec_label("Master Operational Risk Priority Matrix")
    st.dataframe(risk_matrix, use_container_width=True, height=340)

    dl1, dl2 = st.columns(2)
    with dl1:
        st.download_button("⬇️ Export Risk Priority Matrix (.CSV)",
                           data=dataframe_to_csv_bytes(risk_matrix),
                           file_name="risk_priority_matrix.csv", mime="text/csv",
                           use_container_width=True)
    with dl2:
        st.download_button("⬇️ Export Filtered Operational Telemetry (.CSV)",
                           data=dataframe_to_csv_bytes(f),
                           file_name="filtered_operational_data.csv", mime="text/csv",
                           use_container_width=True)

    sec_label("Live Anomaly Alerts (Upper 90th Percentile Outliers)")
    st.dataframe(anomaly_table, use_container_width=True, height=280)

    # Control Progress indicators
    st.write("")
    p1, p2 = st.columns(2)
    with p1:
        st.markdown("##### 🚦 Live Capacity Pressure Index")
        st.progress(min(cap_breach / 100, 1.0))
        st.caption(f"{cap_breach}% of mapped stadium zones have breached loading boundaries")
        st.markdown("##### 🌊 Crowd Dynamic Pressure Index")
        st.progress(min(avg_pressure / 100, 1.0))
        st.caption(f"Average crowd-pressure loading index: {avg_pressure}")
    with p2:
        st.markdown("##### ⏳ Access Gate Queue stress")
        st.progress(min(avg_queue / 30, 1.0))
        st.caption(f"Average gate waiting list time: {avg_queue} minutes")
        st.markdown("##### 🚑 Paramedic Emergency Readiness")
        st.progress(max(0, min(1, 1 - (amb_resp / 20))))
        st.caption(f"Ambulance response transit delay: {amb_resp} minutes")

    # ── AI Executive Panel placed cleanly at bottom! ──
    ai_section_header("🤖 AI Executive Operations Evaluation")

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="ai-mini-card"><div class="ai-label">Overall Risk Score</div>'
                    f'<div class="ai-metric">{overall_risk_score}</div>'
                    f'<div class="ai-status-warning">● Master Index</div></div>',
                    unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="ai-mini-card"><div class="ai-label">Critical Records</div>'
                    f'<div class="ai-metric">{critical_zone_count}</div>'
                    f'<div class="ai-status-critical">● Immediate Support</div></div>',
                    unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="ai-mini-card"><div class="ai-label">Medical Delay Zones</div>'
                    f'<div class="ai-metric">{delayed_med}</div>'
                    f'<div class="ai-status-critical">● Dispatch delays</div></div>',
                    unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="ai-mini-card"><div class="ai-label">Anomaly Warnings</div>'
                    f'<div class="ai-metric">{len(anomaly_table)}</div>'
                    f'<div class="ai-status-warning">● Outlier clusters</div></div>',
                    unsafe_allow_html=True)

    top1, top2 = st.columns([1, 2.4])
    with top1:
        # State-persistent AI generation button
        generate_ai = st.button("🤖 Generate Live AI Insights Report", use_container_width=True)
        st.caption(f"Temp: {ai_temperature} | Max Tokens: {ai_max_tokens}")
    with top2:
        st.markdown(f"""
        <div class="ai-card" style="padding: 14px 18px;">
          <div class="insight-pill" style="margin-bottom: 6px;">AI Intelligence Service</div>
          Takes live filtered KPI vectors, hazard levels, anomalies, and active risk priority logs to produce specialized stadium safety tasks.
        </div>""", unsafe_allow_html=True)

    # Persistent AI Report display
    if "overview_report" not in st.session_state:
        st.session_state.overview_report = ""

    if generate_ai:
        with st.spinner("Analyzing executive logs with Cohere AI..."):
            st.session_state.overview_report = generate_cohere_insights(summary_text, "Overview Dashboard", ai_temperature, ai_max_tokens)

    if st.session_state.overview_report:
        st.markdown(f'<div class="ai-card" style="border-left: 5px solid {t["accent"]};"><h3>📋 Executive Safety Report</h3>{st.session_state.overview_report.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PAGE 2 — CROWD FLOW
# ═══════════════════════════════════════════════════════════
elif page == "Crowd Flow":
    page_header("🌊", "Crowd Flow & Access Congestion Intelligence",
                "Advanced tracking of spectator entry volumes, queue turnstile waiting delays, and gate crowd bottlenecks across match phases.")

    k1, k2, k3, k4 = st.columns(4)
    with k1: kpi_card("Bottleneck Active Zones", str(high_risk_zones),    "crit", "Bottleneck Score ≥ 70")
    with k2: kpi_card("Avg Bottleneck Level",    str(avg_bottleneck),     "warn", "Mean calculated score")
    with k3: kpi_card("Avg Queue Wait Time",     f"{avg_queue} min",      "info", "Median turnstile delay")
    with k4: kpi_card("Avg Crowd Pressure",      str(avg_pressure),       "ok",   "Density gradient index")

    st.write("")

    # Visualizations
    c1, c2 = st.columns([1.5, 1])
    with c1:
        pc = (f.groupby(["phase_cat", "zone_type"], as_index=False)["people_count"]
              .sum().sort_values("phase_cat"))
        pc["phase"] = pc["phase_cat"].astype(str)
        fig = px.line(pc, x="phase", y="people_count", color="zone_type",
                      markers=True, color_discrete_sequence=t["palette"],
                      title="Spectator Core Loading Trends by Match Phase")
        st.plotly_chart(sfig(fig, t, 295), use_container_width=True)
    with c2:
        mat = (f.groupby(["phase", "zone_type"])["avg_queue_wait_time"]
               .mean().round(2).unstack("zone_type"))
        mat = mat.reindex([p for p in PHASE_ORDER if p in mat.index])
        sec_label("Phase Matrix: Turnstile Delay index (min)")
        st.dataframe(
            mat.style.format("{:.1f} minutes").background_gradient(axis=None),
            use_container_width=True, height=220)

    c3, c4 = st.columns([1, 1.1])
    with c3:
        bn = f.groupby("zone_type", as_index=False)["bottleneck_risk_score"].mean().round(1)
        fig = px.bar(bn, y="zone_type", x="bottleneck_risk_score", orientation="h",
                     color_discrete_sequence=[t["accent"]],
                     title="Mean Bottleneck Score by Zone Type",
                     text="bottleneck_risk_score")
        fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")
        fig.update_layout(showlegend=False)
        st.plotly_chart(sfig(fig, t, 275), use_container_width=True)
    with c4:
        qs = f["queue_stress"].value_counts().reset_index()
        qs.columns = ["queue_stress", "count"]
        fig = px.pie(qs, names="queue_stress", values="count", hole=0.56,
                     color_discrete_sequence=t["palette"], title="Turnstile Crowd Queue stress Index")
        st.plotly_chart(sfig(fig, t, 275), use_container_width=True)

    sec_label("Critical Crowd Flow Bottleneck Risk Zones")
    crowd_flow_risk = risk_matrix[
        risk_matrix["Main Risk Reason"].isin(["High bottleneck risk", "Long queue wait time"])
    ].head(10)
    st.dataframe(crowd_flow_risk, use_container_width=True, height=280)

    dual = (f.groupby("zone_name", as_index=False)
            .agg(crowd_pressure=("crowd_pressure_index", "mean"),
                 bottleneck=("bottleneck_risk_score", "mean"),
                 risk_score=("risk_score", "mean"))
            .sort_values("risk_score", ascending=False).head(15))
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Avg Crowd Pressure Index", y=dual["zone_name"],
                         x=dual["crowd_pressure"], orientation="h", marker_color=t["accent"]))
    fig.add_trace(go.Bar(name="Avg Bottleneck Risk Score", y=dual["zone_name"],
                         x=dual["bottleneck"], orientation="h", marker_color=t["warn_col"]))
    fig.update_layout(barmode="group", title="Dynamic Density Pressure vs Bottleneck Risk",
                      yaxis=dict(categoryorder="total ascending"))
    st.plotly_chart(sfig(fig, t, 440), use_container_width=True)

    # ── AI Executive Panel placed cleanly at bottom! ──
    ai_section_header("🤖 Crowd Flow AI Controller")
    
    if "cf_report" not in st.session_state:
        st.session_state.cf_report = ""

    generate_ai_cf = st.button("🤖 Generate Crowd Flow AI Evaluation", use_container_width=True, key="ai_cf")
    if generate_ai_cf:
        with st.spinner("Analyzing entry queue vectors..."):
            high_risk_cf = f[f["bottleneck_risk_score"] >= 50][["zone_name", "phase", "people_count", "avg_queue_wait_time", "bottleneck_risk_score"]].sort_values("bottleneck_risk_score", ascending=False).head(10)
            high_risk_cf_text = high_risk_cf.to_string(index=False) if not high_risk_cf.empty else "No high bottleneck sectors detected under active filters."
            
            cf_context = f"""
Focus on spectator entry queue bottlenecks, gate queues, and zone flows:
- Mean Bottleneck Level: {avg_bottleneck}/100
- Mean Turnstile Queue Wait Time: {avg_queue} minutes
- Active Congested Sectors Count: {high_risk_zones} standings
- Mean Spectator Dynamic Pressure Index: {avg_pressure}/100

WORST CROWD CONGESTION SECTOR RECORDS DETECTED:
{high_risk_cf_text}

TOP RISK OPERATION LOGS:
{top_risk_text}
"""
            st.session_state.cf_report = generate_cohere_insights(cf_context, "Crowd Flow & Gate Wait Dashboard", ai_temperature, ai_max_tokens)
        
    if st.session_state.cf_report:
        st.markdown(f'<div class="ai-card" style="border-left: 5px solid {t["accent"]};"><h3>📋 Crowd Flow AI Insights</h3>{st.session_state.cf_report.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PAGE 3 — MEDICAL & HEAT
# ═══════════════════════════════════════════════════════════
elif page == "Medical & Heat":
    page_header("🏥", "Medical Response & Extreme Thermal Stress Tracker",
                "Assessing local weather heat index values, ambulance rescue dispatch tracks, dehydration vulnerability, and paramedic unit positions.")

    k1, k2, k3, k4 = st.columns(4)
    with k1: kpi_card("Medical Incident Rate",  str(med_rate),     "warn", "Per 1K spectators")
    with k2: kpi_card("Avg Ambulance Transit", f"{amb_resp} min", "crit", "Dispatch to scene lag")
    with k3: kpi_card("Avg Heat Risk Index",    str(avg_heat),     "warn", "Humidity & temp weight")
    with k4: kpi_card("Delayed Response Zones", str(delayed_med),  "crit", "Transit delay ≥ 10 min")

    st.write("")

    c1, c2 = st.columns([1.55, 1])
    with c1:
        heat = (f.groupby("phase_cat", as_index=False)["heat_risk_index"]
                .mean().sort_values("phase_cat"))
        heat["phase"] = heat["phase_cat"].astype(str)
        fig = px.line(heat, x="phase", y="heat_risk_index", markers=True,
                      color_discrete_sequence=[t["accent"]], title="Mean Heat Risk Vector by Match Phase")
        st.plotly_chart(sfig(fig, t, 300), use_container_width=True)
    with c2:
        med_s = (f.groupby("stadium_name", as_index=False)["medical_incidents"]
                 .sum().sort_values("medical_incidents"))
        fig = px.bar(med_s, y="stadium_name", x="medical_incidents", orientation="h",
                     color="stadium_name", color_discrete_sequence=t["palette"],
                     title="Paramedic Cases Handled by Venue")
        fig.update_layout(showlegend=False)
        st.plotly_chart(sfig(fig, t, 300), use_container_width=True)

    sec_label("Critical Medical & Thermal Alert Priorities")
    medical_risk = risk_matrix[
        risk_matrix["Main Risk Reason"].isin(["Delayed medical response", "High heat exposure"])
    ].head(10)
    st.dataframe(medical_risk, use_container_width=True, height=280)

    c3, c4 = st.columns([1, 1.6])
    with c3:
        if not inc_f.empty and "severity" in inc_f.columns:
            sev = inc_f["severity"].value_counts().reset_index()
            sev.columns = ["severity", "count"]
            fig = px.pie(sev, names="severity", values="count", hole=0.55,
                         color_discrete_sequence=t["palette"], title="Active Emergency Case Severity")
            fig.update_traces(textinfo="percent+value", textfont_size=11)
            st.plotly_chart(sfig(fig, t, 285), use_container_width=True)
        else:
            st.info("No active medical event registers detected under current filter states.")
    with c4:
        hr_med = f.groupby("zone_name", as_index=False).agg(
            heat=("heat_risk_index", "mean"),
            med=("medical_incidents", "mean"),
            risk_score=("risk_score", "mean"))
        fig = px.scatter(hr_med, x="heat", y="med", size="risk_score", color="zone_name",
                         color_discrete_sequence=t["palette"],
                         title="Stand Heat Stress vs Paramedic Emergency Cases")
        fig.update_traces(marker_size=11)
        st.plotly_chart(sfig(fig, t, 285), use_container_width=True)

    amb = (f.groupby(["phase_cat", "zone_type"], as_index=False)["ambulance_response_time"]
           .mean().sort_values("phase_cat"))
    amb["phase"] = amb["phase_cat"].astype(str)
    fig = px.line(amb, x="phase", y="ambulance_response_time", color="zone_type",
                  markers=True, color_discrete_sequence=t["palette"],
                  title="Paramedic Dispatch Lag Trend by Phase & Zone Category")
    st.plotly_chart(sfig(fig, t, 310), use_container_width=True)

    # ── AI Executive Panel placed cleanly at bottom! ──
    ai_section_header("🤖 Paramedic Control & Thermal Risk AI Monitor")
    
    if "mh_report" not in st.session_state:
        st.session_state.mh_report = ""

    generate_ai_mh = st.button("🤖 Generate Paramedic Operations AI Report", use_container_width=True, key="ai_mh")
    if generate_ai_mh:
        with st.spinner("Evaluating ambulance paths with Cohere AI..."):
            high_heat_med = f[(f["ambulance_response_time"] >= 8) | (f["heat_risk_index"] >= 30)][["zone_name", "phase", "temperature_celsius", "humidity_percent", "heat_risk_index", "ambulance_response_time", "medical_incidents"]].sort_values("heat_risk_index", ascending=False).head(10)
            high_heat_med_text = high_heat_med.to_string(index=False) if not high_heat_med.empty else "No thermal risk or delayed ambulance zones detected."
            
            mh_context = f"""
Focus on stadium weather/thermal indices, ambulance path delay risks, and medical case counts:
- Medical Incident Occurrence Rate: {med_rate} per 1000 people
- Mean Ambulance Transit lag: {amb_resp} minutes
- Average Stand Heat Stress Indicator (Combined Temp & Humidity): {avg_heat}
- Count of Delayed Ambulance Dispatch Stand Coordinates: {delayed_med}

WORST THERMAL STRESS & DELAYED MEDICAL STANDS REGISTERED:
{high_heat_med_text}

TOP RISK OPERATION LOGS:
{top_risk_text}
"""
            st.session_state.mh_report = generate_cohere_insights(mh_context, "Paramedic & Heat Stress Dashboard", ai_temperature, ai_max_tokens)
        
    if st.session_state.mh_report:
        st.markdown(f'<div class="ai-card" style="border-left: 5px solid {t["accent"]};"><h3>📋 Medical Safety Insights</h3>{st.session_state.mh_report.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PAGE 4 — SECURITY
# ═══════════════════════════════════════════════════════════
elif page == "Security":
    page_header("🔒", "Security Access Control & Boundary Activity Console",
                "Audit logs detailing perimeter breach attempts, duplicative or fake ticket cases, spectator ejections, and overall stand safety.")

    k1, k2, k3, k4 = st.columns(4)
    with k1: kpi_card("Perimeter Breach Attempts", f"{unauthorized:,}", "crit", "Access point violations")
    with k2: kpi_card("Frauds & Fake Tickets",     f"{counterfeit:,}", "warn", "Detected duplicate barcodes")
    with k3: kpi_card("Core Pitch Invasions",      f"{pitch_inv:,}",   "crit", "Aisle barrier penetrations")
    with k4: kpi_card("Ejected Spectators",        f"{fan_ej:,}",      "warn", "Disciplinary removals")

    st.write("")

    c1, c2 = st.columns([1.4, 1])
    with c1:
        ua = (f.groupby(["phase_cat", "zone_type"], as_index=False)["unauthorized_entry_attempts"]
              .mean().sort_values("phase_cat"))
        ua["phase"] = ua["phase_cat"].astype(str)
        fig = px.line(ua, x="phase", y="unauthorized_entry_attempts", color="zone_type",
                      markers=True, color_discrete_sequence=t["palette"],
                      title="Gate Duplication and Force Ingress attempts by Phase")
        st.plotly_chart(sfig(fig, t, 295), use_container_width=True)
    with c2:
        sec_s = (f.groupby("stadium_name", as_index=False)["security_incidents"]
                 .sum().sort_values("security_incidents"))
        fig = px.bar(sec_s, y="stadium_name", x="security_incidents", orientation="h",
                     color_discrete_sequence=[t["accent"]], title="Disciplinary Security Incident Occurrences")
        fig.update_layout(showlegend=False)
        st.plotly_chart(sfig(fig, t, 295), use_container_width=True)

    c3, c4 = st.columns([1.2, 1])
    with c3:
        cs = f.groupby("zone_name", as_index=False).agg(
            pressure=("crowd_pressure_index", "mean"),
            security=("security_incidents", "sum"),
            people=("people_count", "sum"),
            risk_score=("risk_score", "mean"))
        fig = px.scatter(cs, x="people", y="pressure", color="zone_name", size="risk_score",
                         color_discrete_sequence=t["palette"],
                         title="Dynamic Spectator Loading vs Boundary Safety Risk State")
        st.plotly_chart(sfig(fig, t, 295), use_container_width=True)
    with c4:
        sp = (f.groupby(["phase_cat", "zone_type"], as_index=False)["security_incidents"]
              .mean().sort_values("phase_cat"))
        sp["phase"] = sp["phase_cat"].astype(str)
        fig = px.bar(sp, x="phase", y="security_incidents", color="zone_type",
                     barmode="group", color_discrete_sequence=t["palette"],
                     title="Access Violations Classified by Zone category")
        st.plotly_chart(sfig(fig, t, 295), use_container_width=True)

    # ── AI Executive Panel placed cleanly at bottom! ──
    ai_section_header("🤖 Access & Dispatch Security AI Analyst")
    
    if "sec_report" not in st.session_state:
        st.session_state.sec_report = ""

    generate_ai_sec = st.button("🤖 Generate Security Analytics AI Report", use_container_width=True, key="ai_sec")
    if generate_ai_sec:
        with st.spinner("Analyzing perimeter access vectors with Cohere AI..."):
            high_risk_sec = f[f["security_incidents"] > 0][["zone_name", "phase", "people_count", "security_incidents", "unauthorized_entry_attempts", "counterfeit_ticket_cases", "fan_ejections"]].sort_values("security_incidents", ascending=False).head(10)
            high_risk_sec_text = high_risk_sec.to_string(index=False) if not high_risk_sec.empty else "No security incidents flagged under active filters."
            
            sec_context = f"""
Focus on access boundary controls, security wardens coordination, and gate ticket frauds:
- Perimeter Forced Ingress Attempts Count: {unauthorized} incidents
- Barcode Duplications & Fake Ticket Issues: {counterfeit} cases
- Pitch Barrier Invasion Attempts: {pitch_inv} cases
- Disciplinary Spectator Ejections: {fan_ej} counts

WORST ACCESS POINT SECURITY INFRACTIONS LOGGED:
{high_risk_sec_text}

TOP RISK OPERATION LOGS:
{top_risk_text}
"""
            st.session_state.sec_report = generate_cohere_insights(sec_context, "Access Control & Gate Security Dashboard", ai_temperature, ai_max_tokens)
        
    if st.session_state.sec_report:
        st.markdown(f'<div class="ai-card" style="border-left: 5px solid {t["accent"]};"><h3>📋 Security Audit Insights</h3>{st.session_state.sec_report.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PAGE 5 — RESOURCE PLANNING
# ═══════════════════════════════════════════════════════════
elif page == "Resource Planning":
    page_header("📦", "Operational Resource Scheduling and Asset Readiness",
                "Coordinating on-site marshall staffing densities, steel boundary fence resources, paramedic team positions, and response ratios.")

    k1, k2, k3, k4 = st.columns(4)
    with k1: kpi_card("Staff Adequacy Ratio", str(staff_ratio),    "ok",   "Staff capacity index")
    with k2: kpi_card("Total Warden Staff",   f"{req_staff:,}",    "info", "Active deployed marshals")
    with k3: kpi_card("Wicket Line Fences",   f"{req_barr:,}",     "warn", "Required active barricades")
    with k4: kpi_card("Paramedic Units",      f"{med_teams:,}",    "ok",   "Active medical squads")

    st.write("")
    sec_label("Assigned Logistical Plan Based on Zone Threat Level")
    resource_plan = risk_matrix[
        ["Stadium", "Zone", "Zone Type", "Phase",
         "Risk Score", "Risk Band", "Main Risk Reason", "Recommended Action"]
    ].head(12)
    st.dataframe(resource_plan, use_container_width=True, height=320)

    c1, c2 = st.columns([1.55, 1])
    with c1:
        rd = (f.groupby(["phase_cat", "zone_type"], as_index=False)["staff_adequacy_ratio"]
              .mean().sort_values("phase_cat"))
        rd["phase"] = rd["phase_cat"].astype(str)
        fig = px.line(rd, x="phase", y="staff_adequacy_ratio", color="zone_type",
                      markers=True, color_discrete_sequence=t["palette"],
                      title="Marshall Warden Adequacy Trends across Match Phases")
        st.plotly_chart(sfig(fig, t, 295), use_container_width=True)
    with c2:
        md = f.groupby("zone_type", as_index=False).agg(
            people=("people_count", "sum"), med_t=("deployed_medical_teams", "sum"))
        fig = px.scatter(md, x="people", y="med_t", color="zone_type", size="med_t",
                         color_discrete_sequence=t["palette"],
                         title="Medical Team Distribution vs Attendance Load")
        st.plotly_chart(sfig(fig, t, 295), use_container_width=True)

    c3, c4 = st.columns([1, 1])
    with c3:
        res = f.groupby("zone_type", as_index=False).agg(
            staff=("required_staff", "sum"), med=("deployed_medical_teams", "sum"))
        fig = go.Figure()
        fig.add_bar(y=res["zone_type"], x=res["staff"], name="Required Staff",
                    orientation="h", marker_color=t["palette"][0])
        fig.add_bar(y=res["zone_type"], x=res["med"], name="Medical Teams",
                    orientation="h", marker_color=t["palette"][1])
        fig.update_layout(barmode="group", title="Warden Allocation vs Medical Squad counts")
        st.plotly_chart(sfig(fig, t, 275), use_container_width=True)
    with c4:
        br = (f.groupby("zone_type", as_index=False)["required_barricades"]
              .sum().sort_values("required_barricades"))
        fig = px.bar(br, y="zone_type", x="required_barricades", orientation="h",
                     color_discrete_sequence=[t["palette"][0]],
                     title="Target Barricade Resource Deployment by Stand Category")
        fig.update_layout(showlegend=False)
        st.plotly_chart(sfig(fig, t, 275), use_container_width=True)

    mat2 = f.pivot_table(values="staff_adequacy_ratio",
                         index="stadium_name", columns="phase", aggfunc="mean").round(2)
    ord_cols = [p for p in PHASE_ORDER if p in mat2.columns]
    mat2 = mat2[ord_cols]
    sec_label("Stadium Staffing Density Factor Heatmap Matrix")
    st.dataframe(
        mat2.style.format("{:.1f} per 1K").background_gradient(axis=None),
        use_container_width=True)

    # ── AI Executive Panel placed cleanly at bottom! ──
    ai_section_header("🤖 Logistical Resource Allocation AI Advisor")
    
    if "rp_report" not in st.session_state:
        st.session_state.rp_report = ""

    generate_ai_rp = st.button("🤖 Generate Resource Optimization AI Report", use_container_width=True, key="ai_rp")
    if generate_ai_rp:
        with st.spinner("Analyzing warden staff capacity..."):
            low_adequacy_res = f[f["staff_adequacy_ratio"] < f["staff_adequacy_ratio"].median()][["zone_name", "phase", "people_count", "required_staff", "required_barricades", "staff_adequacy_ratio"]].sort_values("staff_adequacy_ratio", ascending=True).head(10)
            low_adequacy_res_text = low_adequacy_res.to_string(index=False) if not low_adequacy_res.empty else "No understaffed zones detected."
            
            rp_context = f"""
Focus on warden staffing levels, crowd fences/barricades placement, and paramedic deployment schedules:
- Combined Marshall/Warden Adequacy Density Index: {staff_ratio} per thousand spectators
- Active Steel Barricades Deployed: {req_barr} fences
- Paramedic Response Squads Active on site: {med_teams} squads
- Total Assigned Marshall Warden Staff count: {req_staff} marshals

STADIUM SECTORS WITH CRITICAL UNDERSTAFFING / OUTLIER DEMANDS:
{low_adequacy_res_text}

TOP RISK OPERATION LOGS:
{top_risk_text}
"""
            st.session_state.rp_report = generate_cohere_insights(rp_context, "Resource & Scheduling Dashboard", ai_temperature, ai_max_tokens)
        
    if st.session_state.rp_report:
        st.markdown(f'<div class="ai-card" style="border-left: 5px solid {t["accent"]};"><h3>📋 Logistics Optimization Insights</h3>{st.session_state.rp_report.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PAGE 6 — RISK MATRIX
# ═══════════════════════════════════════════════════════════
elif page == "Risk Matrix":
    page_header("🚨", "AI Risk Decision Matrix & Anomaly Detection Center",
                "Advanced prioritized decision-support tool helping operations commanders isolate and secure critical zone threat coordinates.")

    k1, k2, k3, k4 = st.columns(4)
    with k1: kpi_card("Overall Operations Risk", str(overall_risk_score),  "crit", "Combined live threat score")
    with k2: kpi_card("Critical Alert Records",  str(critical_zone_count), "crit", "Immediate control deployment")
    with k3: kpi_card("Monitor Alert Records",   str(monitor_zone_count),  "warn", "Warden standby alert")
    with k4: kpi_card("Upper Outlier Alerts",    str(len(anomaly_table)),  "info", "Unusual telemetry clusters")

    st.write("")
    sec_label("Live Risk Priority Matrix (Top 15 Congested stadium sectors)")
    st.dataframe(risk_matrix, use_container_width=True, height=420)
    st.download_button("⬇️ Download Hazard Priority Matrix (.CSV)",
                       data=dataframe_to_csv_bytes(risk_matrix),
                       file_name="risk_priority_matrix.csv", mime="text/csv",
                       use_container_width=True)

    sec_label("Safety Threats Classified by Venue and Stand category")
    c1, c2 = st.columns([1.3, 1])
    with c1:
        stadium_risk = (f.groupby(["stadium_name", "zone_type"], as_index=False)["risk_score"]
                        .mean().sort_values("risk_score", ascending=False))
        fig = px.bar(stadium_risk, x="risk_score", y="stadium_name", color="zone_type",
                     orientation="h", color_discrete_sequence=t["palette"],
                     title="Mean Advanced Risk score by Stadium Category")
        st.plotly_chart(sfig(fig, t, 360), use_container_width=True)
    with c2:
        risk_dist = f["risk_band"].value_counts().reset_index()
        risk_dist.columns = ["Risk Band", "Count"]
        fig = px.pie(risk_dist, names="Risk Band", values="Count", hole=0.55,
                     color="Risk Band",
                     color_discrete_map={"Critical": t["crit_col"],
                                         "Monitor": t["warn_col"], "Safe": t["ok_col"]},
                     title="Audit Records Risk Weight Percentage")
        st.plotly_chart(sfig(fig, t, 360), use_container_width=True)

    sec_label("Live Outlier Anomaly Register")
    st.dataframe(anomaly_table, use_container_width=True, height=340)
    st.download_button("⬇️ Download Anomaly Outliers Dataset (.CSV)",
                       data=dataframe_to_csv_bytes(anomaly_table),
                       file_name="stadium_anomalies_log.csv", mime="text/csv",
                       use_container_width=True)

    # ── AI Executive Panel placed cleanly at bottom! ──
    ai_section_header("🤖 Risk Score Calculations & Weighted Equation AI Assessment")
    
    if "rm_report" not in st.session_state:
        st.session_state.rm_report = ""

    generate_ai_rm = st.button("🤖 Generate Advanced Multi-Metric AI Threat Report", use_container_width=True, key="ai_rm")
    if generate_ai_rm:
        with st.spinner("Calculating hazard vectors..."):
            anomaly_snapshot = anomaly_table.head(8).to_string(index=False) if not anomaly_table.empty else "No anomalies detected."
            
            rm_context = f"""
Focus on overall stadium safety, risk indexes weighted calculations, and outlier anomalies:
- Live Calculated Operations Risk: {overall_risk_score}/100
- Critical Alert Records: {critical_zone_count} stand states
- Monitor Alert Records: {monitor_zone_count} stand states
- Outlier Anomalies Handled by safety core: {len(anomaly_table)} outlier points

STADIUM EXTREME TELEMETRY ANOMALIES LOG SNAPSHOT:
{anomaly_snapshot}

TOP HAZARD PRIORITY DATABASE RECORDS:
{top_risk_text}
"""
            st.session_state.rm_report = generate_cohere_insights(rm_context, "Advanced Risk & Anomaly Matrix Dashboard", ai_temperature, ai_max_tokens)
        
    if st.session_state.rm_report:
        st.markdown(f'<div class="ai-card" style="border-left: 5px solid {t["accent"]};"><h3>📋 Command Matrix Insights</h3>{st.session_state.rm_report.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PAGE 7 — ASK AI
# ═══════════════════════════════════════════════════════════
elif page == "Ask AI":
    page_header("💬", "Conversational AI Command Control Assistant",
                "Directly query the live stadium database, ask safety questions, and generate instant crowd control task plans.")

    # State controller initialization
    if "ai_question" not in st.session_state:
        st.session_state.ai_question = ""
    if "ai_answer" not in st.session_state:
        st.session_state.ai_answer = ""

    k1, k2, k3, k4 = st.columns(4)
    with k1: kpi_card("Overall Operational Risk", str(overall_risk_score),  "crit", "Combined target level")
    with k2: kpi_card("Critical Points",   str(critical_zone_count), "crit", "Immediate control zones")
    with k3: kpi_card("Active Anomalies",   str(len(anomaly_table)),  "warn", "Outlier clusters flagged")
    with k4: kpi_card("Avg Queue Delay",    f"{avg_queue} min",       "info", "Turnstile queue target")

    # Live connection indicator
    api_key_present = bool(get_cohere_key())
    if not api_key_present:
        st.warning(
            "⚠️ **Cohere AI Service Offline (API key missing).**\n\n"
            "To enable live conversational Q&A capability:\n"
            "1. Go to your **Streamlit Cloud Dashboard** → find this App → click the context menu.\n"
            "2. Open **Settings → Secrets** and paste your API key exactly like this:\n"
            "```\nCOHERE_API_KEY = \"your_real_cohere_api_key\"\n```\n"
            "Get your key free at [dashboard.cohere.com](https://dashboard.cohere.com/api-keys)"
        )
    else:
        st.success("✅ **Cohere AI Command Service is connected.** Live operations advisors correspond beautifully.")

    st.write("")
    sec_label("Suggested Quick Operations Questions")

    # Center buttons gracefully
    q1, q2, q3 = st.columns(3)
    with q1:
        if st.button("Which sectors need immediate help?", use_container_width=True):
            st.session_state.ai_question = "Which stadium sectors need the most immediate crowd control help right now and why?"
            st.session_state.ai_answer = ""
            st.rerun()
    with q2:
        if st.button("Logistical first actions?", use_container_width=True):
            st.session_state.ai_question = "Identify the top 3 logistical tasks the operations team should execute first."
            st.session_state.ai_answer = ""
            st.rerun()
    with q3:
        if st.button("Explain dashboard results simply", use_container_width=True):
            st.session_state.ai_question = "Translate this dashboard's core metrics into an easy, executive presentation summary."
            st.session_state.ai_answer = ""
            st.rerun()

    q4, q5, q6 = st.columns(3)
    with q4:
        if st.button("Identify high heat vulnerabilities", use_container_width=True):
            st.session_state.ai_question = "Is heat risk a major threat here? What are the worst thermal coordinates and recommended actions?"
            st.session_state.ai_answer = ""
            st.rerun()
    with q5:
        if st.button("Which phase represents the most threat?", use_container_width=True):
            st.session_state.ai_question = "Which phase shows the most elevated safety and density threat? What are the corresponding control recommendations?"
            st.session_state.ai_answer = ""
            st.rerun()
    with q6:
        if st.button("Give 5 project briefing points", use_container_width=True):
            st.session_state.ai_question = "Compose 5 clear briefing points explanatory of this stadium crowd-safety dashboard project."
            st.session_state.ai_answer = ""
            st.rerun()

    # Manual question entrance
    user_question = st.text_area(
        "Enter Your Custom operations Command Question",
        value=st.session_state.ai_question,
        placeholder="Example: Which stadium stands suffer from the highest bottleneck risk? What are the priority warden allocation tasks there?",
        height=120, key="qa_text_area"
    )

    ask_btn = st.button("💬 Query Advisor Assistant", use_container_width=True)

    if ask_btn:
        if not user_question.strip():
            st.warning("Please input or pick a card questions above first.")
        else:
            qa_context = f"""
Live telemetry logs vectors passed:
Overall stadium risk level: {overall_risk_score}
Integrated crowd safety score: {safety_risk}
Critical stands flagged counts: {critical_zone_count}
Monitor alert stand counts: {monitor_zone_count}
Paramedic medical incidents: {med_rate} cases
Exceeded loading boundaries: {cap_breach}%
Incidents solved index: {res_rate}%
Ambulance Response transport lag: {amb_resp} mins
Median waiting turnstile queue: {avg_queue} mins
Dynamic density crowd pressure: {avg_pressure}
Bottleneck alert scores mean: {avg_bottleneck}
Local heat hazard indices average: {avg_heat}
Worst bottlenecks counts: {high_risk_zones} standings
Delayed dispatch paramedics counted: {delayed_med} Stand coordinates
Unauthorized intrusions: {unauthorized}
Counterfeits & fake ticket fraud events: {counterfeit}
Gate pitch breach warnings: {pitch_inv}
Removal of spectators ejected: {fan_ej}
Total active deployed warden staff: {req_staff}
Fences & barricade allocation reserves: {req_barr}
Paramedic deploy teams on location: {med_teams}
Warden staffing density index: {staff_ratio}

Worse risk priority matrix points logged:
{risk_matrix.head(10).to_string(index=False)}

Upper percent alert anomaly listings:
{anomaly_table.head(10).to_string(index=False)}
"""
            with st.spinner("AI Operations Consultant is calculating response..."):
                st.session_state.ai_answer = ask_ai_question(
                    user_question, qa_context, temperature_value=0.3, token_value=750)
                st.session_state.ai_question = user_question
                st.rerun()

    # Render Q&A outcome card
    if st.session_state.ai_answer:
        st.markdown(f"""
        <div class="ai-card" style="border-left: 5px solid {t["accent"]};">
        <h3>💬 AI Advisor Response</h3>
        {st.session_state.ai_answer.replace(chr(10), "<br>")}
        </div>""", unsafe_allow_html=True)

    sec_label("Warden Database Matrices referenced by live AI Models")
    c1, c2 = st.columns(2)
    with c1:
        st.caption("Active threat hotspots fed to Cohere chat prompt:")
        st.dataframe(risk_matrix.head(8), use_container_width=True, height=260)
    with c2:
        st.caption("Extreme outlier anomalies monitored by safety core:")
        st.dataframe(anomaly_table.head(8), use_container_width=True, height=260)


# ─────────────────────────────────────────────────────────
# FOOTER Layout
# ─────────────────────────────────────────────────────────
st.markdown("<hr style='margin-top:40px; margin-bottom:12px; opacity:0.3;'>", unsafe_allow_html=True)
st.markdown(
    f'<p style="text-align:center;font-size:11px;color:{t["text2"]};padding:4px 0; margin-bottom: 0;">'
    "🏏 IPL Stadium Crowd Safety Management Suite &nbsp;|&nbsp; Certified Operations Dashboard &nbsp;|&nbsp; Powered by Cohere AI Command Service"
    "</p>", unsafe_allow_html=True)
