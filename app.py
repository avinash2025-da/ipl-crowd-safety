"""
IPL Crowd Safety Management Dashboard — Streamlit + Claude AI
Run: streamlit run app.py
Install: pip install streamlit pandas numpy plotly openpyxl anthropic matplotlib
"""

import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components
import anthropic

# ─────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IPL Crowd Safety Management",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

PHASE_ORDER = ["Pre-match", "First innings", "Break", "Second innings", "Exit phase"]

# ─────────────────────────────────────────────────────────
# THEMES
# ─────────────────────────────────────────────────────────
THEMES = {
    "Home": {
        "bg": "#0D0B1E", "sidebar": "#161230", "card": "#1E1A35",
        "accent": "#7C3AED", "accent_lt": "#2D1B69", "accent2": "#A78BFA",
        "text": "#F8F8FF", "text2": "#A78BFA", "border": "#3D2B7A",
        "plot_bg": "#1E1A35", "paper_bg": "#0D0B1E", "grid": "#2D1B69",
        "legend_rgba": "rgba(13,11,30,0.92)",
        "palette": ["#7C3AED","#A78BFA","#F59E0B","#10B981","#EF4444","#3B82F6"],
        "crit_col": "#EF4444", "warn_col": "#F59E0B", "ok_col": "#10B981", "info_col": "#7C3AED",
    },
    "Intro": {
        "bg": "#0A0818", "sidebar": "#120F26", "card": "#181530",
        "accent": "#6D28D9", "accent_lt": "#2D1B69", "accent2": "#8B5CF6",
        "text": "#F0EEFF", "text2": "#8B5CF6", "border": "#3D2B7A",
        "plot_bg": "#181530", "paper_bg": "#0A0818", "grid": "#2D1B69",
        "legend_rgba": "rgba(10,8,24,0.92)",
        "palette": ["#6D28D9","#8B5CF6","#F59E0B","#10B981","#EF4444","#3B82F6"],
        "crit_col": "#EF4444", "warn_col": "#F59E0B", "ok_col": "#10B981", "info_col": "#6D28D9",
    },
    "Overview": {
        "bg": "#F6F4FF", "sidebar": "#EDE9FE", "card": "#FFFFFF",
        "accent": "#7C3AED", "accent_lt": "#EDE9FE", "accent2": "#5B21B6",
        "text": "#1E1B4B", "text2": "#6B7280", "border": "#C4B5FD",
        "plot_bg": "#FFFFFF", "paper_bg": "#F6F4FF", "grid": "#F0EBFF",
        "legend_rgba": "rgba(246,244,255,0.92)",
        "palette": ["#7C3AED","#A78BFA","#F59E0B","#10B981","#EF4444","#3B82F6"],
        "crit_col": "#EF4444", "warn_col": "#F59E0B", "ok_col": "#10B981", "info_col": "#7C3AED",
    },
    "Crowd Flow": {
        "bg": "#EFF6FF", "sidebar": "#DBEAFE", "card": "#FFFFFF",
        "accent": "#1D4ED8", "accent_lt": "#DBEAFE", "accent2": "#1E40AF",
        "text": "#1E2A4A", "text2": "#6B7280", "border": "#93C5FD",
        "plot_bg": "#FFFFFF", "paper_bg": "#EFF6FF", "grid": "#E8F2FF",
        "legend_rgba": "rgba(239,246,255,0.92)",
        "palette": ["#1D4ED8","#60A5FA","#F59E0B","#10B981","#8B5CF6","#EF4444"],
        "crit_col": "#EF4444", "warn_col": "#F59E0B", "ok_col": "#10B981", "info_col": "#1D4ED8",
    },
    "Medical & Heat": {
        "bg": "#FFF1F2", "sidebar": "#FFE4E6", "card": "#FFFFFF",
        "accent": "#E11D48", "accent_lt": "#FFE4E6", "accent2": "#BE123C",
        "text": "#3B0A14", "text2": "#6B7280", "border": "#FDA4AF",
        "plot_bg": "#FFFFFF", "paper_bg": "#FFF1F2", "grid": "#FFF0F1",
        "legend_rgba": "rgba(255,241,242,0.92)",
        "palette": ["#E11D48","#FB7185","#F97316","#8B5CF6","#3B82F6","#10B981"],
        "crit_col": "#E11D48", "warn_col": "#F97316", "ok_col": "#10B981", "info_col": "#8B5CF6",
    },
    "Security": {
        "bg": "#FFFBEB", "sidebar": "#FEF3C7", "card": "#FFFFFF",
        "accent": "#D97706", "accent_lt": "#FEF3C7", "accent2": "#B45309",
        "text": "#1C1007", "text2": "#6B7280", "border": "#FCD34D",
        "plot_bg": "#FFFFFF", "paper_bg": "#FFFBEB", "grid": "#FFFCF0",
        "legend_rgba": "rgba(255,251,235,0.92)",
        "palette": ["#D97706","#F59E0B","#3B82F6","#10B981","#8B5CF6","#EF4444"],
        "crit_col": "#EF4444", "warn_col": "#D97706", "ok_col": "#10B981", "info_col": "#3B82F6",
    },
    "Resource Planning": {
        "bg": "#F0FDFA", "sidebar": "#CCFBF1", "card": "#FFFFFF",
        "accent": "#0D9488", "accent_lt": "#CCFBF1", "accent2": "#0F766E",
        "text": "#042F2E", "text2": "#6B7280", "border": "#5EEAD4",
        "plot_bg": "#FFFFFF", "paper_bg": "#F0FDFA", "grid": "#EDFDF8",
        "legend_rgba": "rgba(240,253,250,0.92)",
        "palette": ["#0D9488","#34D399","#3B82F6","#8B5CF6","#F59E0B","#EF4444"],
        "crit_col": "#EF4444", "warn_col": "#F59E0B", "ok_col": "#0D9488", "info_col": "#3B82F6",
    },
    "Risk Matrix": {
        "bg": "#F8FAFC", "sidebar": "#E2E8F0", "card": "#FFFFFF",
        "accent": "#DC2626", "accent_lt": "#FEE2E2", "accent2": "#991B1B",
        "text": "#111827", "text2": "#6B7280", "border": "#CBD5E1",
        "plot_bg": "#FFFFFF", "paper_bg": "#F8FAFC", "grid": "#E5E7EB",
        "legend_rgba": "rgba(248,250,252,0.92)",
        "palette": ["#DC2626","#F97316","#F59E0B","#10B981","#3B82F6","#8B5CF6"],
        "crit_col": "#DC2626", "warn_col": "#F59E0B", "ok_col": "#10B981", "info_col": "#3B82F6",
    },
    "Ask AI": {
        "bg": "#F5F3FF", "sidebar": "#EDE9FE", "card": "#FFFFFF",
        "accent": "#8B5CF6", "accent_lt": "#EDE9FE", "accent2": "#6D28D9",
        "text": "#1E1B4B", "text2": "#6B7280", "border": "#C4B5FD",
        "plot_bg": "#FFFFFF", "paper_bg": "#F5F3FF", "grid": "#EDE9FE",
        "legend_rgba": "rgba(245,243,255,0.92)",
        "palette": ["#8B5CF6","#A78BFA","#F59E0B","#10B981","#EF4444","#3B82F6"],
        "crit_col": "#EF4444", "warn_col": "#F59E0B", "ok_col": "#10B981", "info_col": "#8B5CF6",
    },
}

PAGES = [
    ("🎬", "Intro"),
    ("🏠", "Home"),
    ("📊", "Overview"),
    ("🌊", "Crowd Flow"),
    ("🏥", "Medical & Heat"),
    ("🔒", "Security"),
    ("📦", "Resource Planning"),
    ("🚨", "Risk Matrix"),
    ("💬", "Ask AI"),
]

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
            st.error(f"Missing file: data/{fname}")
            st.stop()
        return pd.read_excel(path)

    ops     = _read("fact_operations_main.xlsx")
    inc     = _read("fact_incidents.xlsx")
    evt     = _read("fact_events.xlsx")
    zone    = _read("dim_zone.xlsx")
    stadium = _read("dim_stadium.xlsx")

    for df in [ops, inc, evt, zone, stadium]:
        df.columns = df.columns.str.strip().str.lower()

    ops = ops.merge(zone[["zone_id","zone_name","zone_type"]], on="zone_id", how="left")
    zone_s = zone[["zone_id","stadium_id"]].merge(
        stadium[["stadium_id","stadium_name"]], on="stadium_id", how="left")
    ops = ops.merge(zone_s[["zone_id","stadium_name"]], on="zone_id", how="left")

    evt_cols = ["event_id","season_year","is_final_match","total_attendance"]
    ops = ops.merge(evt[evt_cols], on="event_id", how="left")

    ops["heat_risk_index"]      = ops["temperature_celsius"]*0.7 + ops["humidity_percent"]*0.3
    ops["occupancy_pct"]        = ops["occupancy_rate"]*100
    ops["capacity_breach"]      = (ops["occupancy_rate"]>=0.55).astype(int)
    ops["staff_adequacy_ratio"] = np.where(
        ops["people_count"]>0, ops["required_staff"]/ops["people_count"]*1000, 0)

    ops["occupancy_risk_band"] = pd.cut(ops["occupancy_rate"],
        bins=[-np.inf,0.45,0.60,0.70,np.inf],
        labels=["Low","Moderate","High","Critical"])

    ops["queue_stress"] = pd.cut(ops["avg_queue_wait_time"],
        bins=[-np.inf,10,20,25,np.inf],
        labels=["Acceptable under 10 min","Moderate 10-20 min",
                "High 20-25 min","Extreme 25+ min"])

    q75 = evt["total_attendance"].quantile(0.75)
    q40 = evt["total_attendance"].quantile(0.40)
    evt["match_category"] = np.select(
        [evt["is_final_match"]==1, evt["total_attendance"]>=q75, evt["total_attendance"]>=q40],
        ["Final Match","High Attendance Match","Moderate Attendance Match"],
        default="Regular Match")
    ops = ops.merge(evt[["event_id","match_category"]], on="event_id", how="left")
    ops["match_category"] = ops["match_category"].fillna("Regular Match")

    inc = inc.merge(evt[["event_id","season_year"]], on="event_id", how="left")
    inc = inc.merge(zone_s[["zone_id","stadium_name"]], on="zone_id", how="left")
    return ops, inc


try:
    ops, inc = load_all()
except Exception as e:
    st.error(f"Data load error: {e}")
    st.stop()


# ─────────────────────────────────────────────────────────
# DRAGGABLE SIDEBAR  — injected once, works on all pages
# ─────────────────────────────────────────────────────────
def inject_draggable_sidebar():
    components.html("""
<script>
(function(){
  function setup(){
    var sb = window.parent.document.querySelector('[data-testid="stSidebar"]');
    if(!sb){ setTimeout(setup,800); return; }
    if(sb.querySelector('#ipl-sb-drag')) return;

    var handle = window.parent.document.createElement('div');
    handle.id  = 'ipl-sb-drag';
    handle.title = 'Drag to resize sidebar';
    handle.style.cssText = [
      'position:absolute','right:-5px','top:0','width:10px','height:100%',
      'cursor:col-resize','z-index:9999','background:transparent',
      'border-radius:5px','transition:background .2s',
      'display:flex','align-items:center','justify-content:center'
    ].join(';');

    /* visual pill indicator */
    var pill = window.parent.document.createElement('div');
    pill.style.cssText = [
      'width:4px','height:40px','border-radius:4px',
      'background:rgba(124,58,237,.28)','transition:all .2s',
      'pointer-events:none'
    ].join(';');
    handle.appendChild(pill);

    var dragging=false, sx=0, sw=0;

    handle.addEventListener('mouseenter',function(){
      pill.style.background='rgba(124,58,237,.65)';
      pill.style.height='60px';
    });
    handle.addEventListener('mouseleave',function(){
      if(!dragging){
        pill.style.background='rgba(124,58,237,.28)';
        pill.style.height='40px';
      }
    });

    handle.addEventListener('mousedown',function(e){
      dragging=true; sx=e.clientX; sw=sb.getBoundingClientRect().width;
      window.parent.document.body.style.userSelect='none';
      pill.style.background='rgba(124,58,237,.85)';
      pill.style.height='80px';
      e.preventDefault();
    });

    window.parent.document.addEventListener('mousemove',function(e){
      if(!dragging) return;
      var w=sw+(e.clientX-sx);
      if(w>=160 && w<=560){
        sb.style.setProperty('min-width',w+'px','important');
        sb.style.setProperty('max-width',w+'px','important');
        sb.style.setProperty('width',    w+'px','important');
      }
    });

    window.parent.document.addEventListener('mouseup',function(){
      if(dragging){
        dragging=false;
        pill.style.background='rgba(124,58,237,.28)';
        pill.style.height='40px';
        window.parent.document.body.style.userSelect='';
      }
    });

    sb.style.position='relative';
    sb.appendChild(handle);
  }
  setTimeout(setup,900);
})();
</script>
""", height=0)


# ─────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────
def inject_css(t):
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Sora:wght@600;700;800&display=swap');

html,body,[class*="css"]{{ font-family:'Plus Jakarta Sans',sans-serif; }}
.stApp{{ background-color:{t['bg']}; color:{t['text']}; }}
.block-container{{ padding-top:3.8rem; padding-bottom:1rem; max-width:1580px; }}

/* ── Sidebar ── */
section[data-testid="stSidebar"]{{
    background-color:{t['sidebar']};
    border-right:2px solid {t['border']};
    min-width:235px !important; max-width:235px !important;
}}
section[data-testid="stSidebar"] *{{ color:{t['text']} !important; }}
section[data-testid="stSidebar"] .stButton>button{{
    width:100% !important; text-align:left !important;
    background:{t['card']} !important; border:1px solid {t['border']} !important;
    border-radius:12px !important; padding:10px 14px !important;
    font-size:13px !important; font-weight:700 !important;
    color:{t['text']} !important; margin-bottom:5px !important;
    box-shadow:0 1px 3px rgba(0,0,0,.06) !important; transition:all .15s !important;
}}
section[data-testid="stSidebar"] .stButton>button:hover{{
    background:{t['accent_lt']} !important;
    border-color:{t['accent']} !important;
    color:{t['accent2']} !important;
}}

/* ── Page header — fully centred ── */
.dash-header{{
    background:linear-gradient(120deg,{t['card']} 55%,{t['accent_lt']});
    border:1px solid {t['border']}; border-left:6px solid {t['accent']};
    border-radius:18px; padding:26px 28px 20px;
    margin-bottom:24px;
    box-shadow:0 2px 14px rgba(0,0,0,.07);
    display:flex; flex-direction:column;
    align-items:center; justify-content:center;
    text-align:center; gap:8px;
    width:100%;
}}
.dash-header-icon{{ font-size:42px; line-height:1; margin-bottom:6px; }}
.dash-title{{
    font-family:'Sora',sans-serif; font-size:26px; font-weight:800;
    color:{t['text']}; margin:0; text-align:center; width:100%;
}}
.dash-sub{{
    font-size:13px; color:{t['text2']}; margin:0; font-weight:500;
    text-align:center; width:100%; max-width:720px;
}}

/* ── KPI cards — fully centred values ── */
.kpi-card{{
    background:{t['card']}; border:1px solid {t['border']};
    border-radius:16px; padding:20px 14px 16px;
    min-height:112px; box-shadow:0 2px 10px rgba(0,0,0,.055);
    position:relative; overflow:hidden;
    display:flex; flex-direction:column;
    align-items:center; justify-content:center;
    text-align:center; margin-bottom:18px;
    width:100%;
}}
.kpi-card::before{{
    content:''; position:absolute; top:0; left:0;
    width:100%; height:4px; border-radius:16px 16px 0 0;
}}
.kpi-info::before  {{ background:{t['info_col']}; }}
.kpi-warn::before  {{ background:{t['warn_col']}; }}
.kpi-crit::before  {{ background:{t['crit_col']}; }}
.kpi-ok::before    {{ background:{t['ok_col']}; }}
.kpi-label{{
    font-size:10px; font-weight:700; text-transform:uppercase;
    letter-spacing:.9px; color:{t['text2']};
    margin-bottom:10px;
    text-align:center; width:100%;
}}
.kpi-val{{
    font-family:'Sora',sans-serif; font-size:30px; font-weight:800;
    color:{t['text']}; line-height:1;
    text-align:center; width:100%; display:block;
}}
.kpi-sub{{
    font-size:10px; color:{t['text2']};
    margin-top:6px; text-align:center; width:100%;
}}

/* ── Section label ── */
.sec-lbl{{
    font-family:'Sora',sans-serif; font-size:12px; font-weight:700;
    color:{t['accent2']}; text-transform:uppercase; letter-spacing:.9px;
    margin:18px 0 8px 0; padding-bottom:5px; border-bottom:2px solid {t['accent_lt']};
}}

/* ── AI cards ── */
.ai-card{{
    background:{t["card"]}; border:1px solid {t["border"]}; border-radius:18px;
    padding:20px; box-shadow:0 2px 12px rgba(0,0,0,.05);
    margin-bottom:14px; color:{t["text"]};
}}
.ai-mini-card{{
    background:{t["card"]}; border:1px solid {t["border"]};
    border-left:5px solid {t["accent"]}; border-radius:14px;
    padding:14px; margin-bottom:10px; box-shadow:0 2px 8px rgba(0,0,0,.045);
    display:flex; flex-direction:column; align-items:center; text-align:center;
}}
.ai-metric{{
    font-size:28px; font-weight:800; color:{t["text"]};
    font-family:'Sora',sans-serif; text-align:center; width:100%; display:block;
}}
.ai-label{{
    font-size:11px; text-transform:uppercase; font-weight:700;
    letter-spacing:.7px; color:{t["text2"]}; text-align:center; width:100%;
}}
.ai-status-critical{{ color:#DC2626; font-weight:700; font-size:12px; text-align:center; }}
.ai-status-warning {{ color:#F59E0B; font-weight:700; font-size:12px; text-align:center; }}
.ai-status-good    {{ color:#10B981; font-weight:700; font-size:12px; text-align:center; }}

.insight-pill{{
    display:inline-block; padding:6px 14px; border-radius:999px;
    font-size:11px; font-weight:700; margin-bottom:8px;
    background:{t["accent_lt"]}; color:{t["accent2"]};
}}

/* ── Charts + dataframes ── */
div[data-testid="stPlotlyChart"]>div{{
    border-radius:14px !important; border:1px solid {t['border']} !important;
    box-shadow:0 2px 8px rgba(0,0,0,.045) !important;
}}
[data-testid="stDataFrame"]{{
    border-radius:12px; border:1px solid {t['border']}; overflow:hidden;
}}

/* ── Streamlit metric override for centering ── */
[data-testid="stMetric"]{{
    text-align:center !important;
}}
[data-testid="stMetricValue"]{{
    justify-content:center !important;
}}

/* ── Scrollbar ── */
::-webkit-scrollbar{{ width:5px; height:5px; }}
::-webkit-scrollbar-track{{ background:{t['bg']}; }}
::-webkit-scrollbar-thumb{{ background:{t['border']}; border-radius:3px; }}
hr{{ border-color:{t['border']} !important; opacity:.6; }}
</style>
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
  <div class="dash-header-icon">{icon}</div>
  <div class="dash-title">{title}</div>
  <div class="dash-sub">{subtitle}</div>
</div>""", unsafe_allow_html=True)


def sec_label(text):
    st.markdown(f'<div class="sec-lbl">{text}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
# CLAUDE AI HELPERS
# ─────────────────────────────────────────────────────────
def get_anthropic_key():
    """Read Anthropic API key from Streamlit secrets — multiple fallbacks."""
    try:
        key = st.secrets["ANTHROPIC_API_KEY"]
        if key:
            return str(key).strip()
    except Exception:
        pass
    try:
        key = st.secrets.get("ANTHROPIC_API_KEY", "")
        if key:
            return str(key).strip()
    except Exception:
        pass
    return ""


def generate_ai_insights(summary_text, temperature_value=0.4, token_value=700):
    api_key = get_anthropic_key()
    if not api_key:
        return (
            "⚠️ **Claude AI API key not configured.**\n\n"
            "To fix this:\n"
            "1. Go to **share.streamlit.io** → your app\n"
            "2. Click **⋮ menu** → **Settings** → **Secrets**\n"
            "3. Add:  `ANTHROPIC_API_KEY = \"your_key_here\"`\n"
            "4. Save and the app will reload automatically."
        )
    try:
        client = anthropic.Anthropic(api_key=api_key)
        prompt = f"""You are a professional data analyst for an IPL Crowd Safety Management Dashboard.

Based on the dashboard metrics below, generate:
1. Key insights (2-3 bullet points)
2. Risk observations (2-3 bullet points)
3. Practical recommendations (2-3 bullet points)
4. A short presentation-friendly summary paragraph

Rules:
- Use simple professional language.
- Focus on crowd safety, bottlenecks, medical readiness, heat exposure, security, and resource planning.
- Give clear actions for stadium operations teams.
- Keep it concise and dashboard-friendly.

Dashboard Summary:
{summary_text}
"""
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=token_value,
            temperature=min(temperature_value, 1.0),
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    except Exception as e:
        return f"❌ Claude AI error: {e}\n\nPlease verify your API key in Streamlit Cloud Secrets."


def ask_ai_question(question, context_text, temperature_value=0.3, token_value=600):
    api_key = get_anthropic_key()
    if not api_key:
        return (
            "⚠️ **Claude AI API key not configured.**\n\n"
            "Go to Streamlit Cloud → App Settings → Secrets → add:  "
            "`ANTHROPIC_API_KEY = \"your_key_here\"`"
        )
    try:
        client = anthropic.Anthropic(api_key=api_key)
        prompt = f"""You are an AI assistant inside an IPL Crowd Safety Management Dashboard.
Answer the user's question using only the dashboard context below.
Be concise, professional and action-oriented.

Dashboard Context:
{context_text}

User Question: {question}
"""
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=token_value,
            temperature=min(temperature_value, 1.0),
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    except Exception as e:
        return f"❌ Claude AI error: {e}"


def sfig(fig, t, h=320):
    fig.update_layout(
        height=h, paper_bgcolor=t["paper_bg"], plot_bgcolor=t["plot_bg"],
        font=dict(color=t["text"], family="Plus Jakarta Sans", size=12),
        title_font=dict(color=t["text"], size=14, family="Sora"), title_x=0.03,
        legend=dict(bgcolor=t["legend_rgba"], bordercolor=t["border"], borderwidth=1,
                    font=dict(color=t["text2"], size=11)),
        margin=dict(l=30, r=20, t=50, b=30), colorway=t["palette"],
    )
    fig.update_xaxes(gridcolor=t["grid"], zerolinecolor=t["grid"], linecolor=t["border"],
                     tickfont=dict(color=t["text2"]), title_font=dict(color=t["text2"]))
    fig.update_yaxes(gridcolor=t["grid"], zerolinecolor=t["grid"], linecolor=t["border"],
                     tickfont=dict(color=t["text2"]), title_font=dict(color=t["text2"]))
    return fig


def safe_norm(series):
    mn, mx = series.min(), series.max()
    if pd.isna(mn) or pd.isna(mx) or mx == mn:
        return pd.Series(0, index=series.index)
    return ((series - mn) / (mx - mn)) * 100


def add_advanced_risk_features(df):
    df = df.copy()
    df["security_total"] = (
        df["security_incidents"].fillna(0)
        + df["unauthorized_entry_attempts"].fillna(0)
        + df["counterfeit_ticket_cases"].fillna(0)
        + df["fan_ejections"].fillna(0))
    df["risk_score"] = (
        safe_norm(df["crowd_pressure_index"].fillna(0)) * 0.25
        + safe_norm(df["bottleneck_risk_score"].fillna(0)) * 0.25
        + safe_norm(df["avg_queue_wait_time"].fillna(0)) * 0.15
        + safe_norm(df["ambulance_response_time"].fillna(0)) * 0.15
        + safe_norm(df["heat_risk_index"].fillna(0)) * 0.10
        + safe_norm(df["security_total"].fillna(0)) * 0.10).round(2)
    df["risk_band"] = pd.cut(df["risk_score"], bins=[-1,40,70,101],
                             labels=["Safe","Monitor","Critical"])
    df["risk_reason"] = np.select(
        [df["bottleneck_risk_score"]>=70, df["ambulance_response_time"]>=10,
         df["avg_queue_wait_time"]>=20,
         df["heat_risk_index"]>=df["heat_risk_index"].quantile(0.75),
         df["security_total"]>=df["security_total"].quantile(0.75)],
        ["High bottleneck risk","Delayed medical response","Long queue wait time",
         "High heat exposure","High security activity"],
        default="Normal operating condition")
    df["recommended_action"] = np.select(
        [df["risk_reason"]=="High bottleneck risk",
         df["risk_reason"]=="Delayed medical response",
         df["risk_reason"]=="Long queue wait time",
         df["risk_reason"]=="High heat exposure",
         df["risk_reason"]=="High security activity"],
        ["Add barricades and redirect crowd flow",
         "Deploy extra medical team and ambulance support",
         "Open additional gates and improve queue control",
         "Provide water points and cooling zones",
         "Increase security staff and access checks"],
        default="Continue monitoring")
    return df


def create_risk_priority_matrix(df):
    cols = ["stadium_name","zone_name","zone_type","phase","risk_score","risk_band",
            "risk_reason","recommended_action","people_count","avg_queue_wait_time",
            "ambulance_response_time","bottleneck_risk_score","heat_risk_index"]
    avail = [c for c in cols if c in df.columns]
    m = df[avail].sort_values("risk_score", ascending=False).head(15).copy()
    m.rename(columns={
        "stadium_name":"Stadium","zone_name":"Zone","zone_type":"Zone Type","phase":"Phase",
        "risk_score":"Risk Score","risk_band":"Risk Band","risk_reason":"Main Risk Reason",
        "recommended_action":"Recommended Action","people_count":"People Count",
        "avg_queue_wait_time":"Queue Wait","ambulance_response_time":"Ambulance Response",
        "bottleneck_risk_score":"Bottleneck Score","heat_risk_index":"Heat Risk",
    }, inplace=True)
    return m


def create_anomaly_table(df):
    metrics = ["avg_queue_wait_time","ambulance_response_time","bottleneck_risk_score",
               "crowd_pressure_index","heat_risk_index","security_total","medical_incidents"]
    tmp = df.copy()
    exist = [m for m in metrics if m in tmp.columns]
    flags = []
    for m in exist:
        col = f"{m}_anomaly"
        tmp[col] = tmp[m] >= tmp[m].quantile(0.90)
        flags.append(col)
    tmp["anomaly_count"]  = tmp[flags].sum(axis=1)
    tmp["anomaly_reason"] = tmp.apply(
        lambda r: ", ".join([m.replace("_"," ").title() for m in exist
                             if r.get(f"{m}_anomaly", False)]), axis=1)
    anoms = tmp[tmp["anomaly_count"]>0].copy()
    cols = ["stadium_name","zone_name","zone_type","phase","anomaly_count","anomaly_reason",
            "risk_score","avg_queue_wait_time","ambulance_response_time",
            "bottleneck_risk_score","heat_risk_index"]
    avail = [c for c in cols if c in anoms.columns]
    anoms = anoms[avail].sort_values(["anomaly_count","risk_score"],ascending=False).head(15)
    anoms.rename(columns={
        "stadium_name":"Stadium","zone_name":"Zone","zone_type":"Zone Type","phase":"Phase",
        "anomaly_count":"Anomaly Count","anomaly_reason":"Anomaly Reason",
        "risk_score":"Risk Score","avg_queue_wait_time":"Queue Wait",
        "ambulance_response_time":"Ambulance Response","bottleneck_risk_score":"Bottleneck Score",
        "heat_risk_index":"Heat Risk",
    }, inplace=True)
    return anoms


def csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8")


# ─────────────────────────────────────────────────────────
# REUSABLE AI INSIGHTS PANEL  — placed at bottom of each page
# ─────────────────────────────────────────────────────────
def render_ai_insights_panel(page_key, summary, t, ai_temp, ai_tokens,
                              crit_count, mon_count, anom_count,
                              cap_breach_val, avg_pressure_val,
                              avg_queue_val, amb_resp_val):
    """Render a consistent Claude AI insights block at the bottom of a dashboard page."""
    st.markdown("<hr>", unsafe_allow_html=True)
    sec_label("🤖 Claude AI Intelligence — Operational Insights")

    ai_top1, ai_top2 = st.columns([1, 2.6])
    with ai_top1:
        generate_ai = st.button(
            "🤖 Generate AI Insights",
            key=f"ai_gen_{page_key}",
            use_container_width=True
        )
        st.caption(f"Temperature: {ai_temp} | Max Tokens: {ai_tokens}")
    with ai_top2:
        st.markdown(f"""
<div class="ai-card">
  <div class="insight-pill">Claude AI Executive Summary</div>
  Powered by Claude AI — uses filtered KPIs, advanced risk scores, anomaly
  detection and priority matrix to generate actionable operational recommendations
  for stadium safety teams.
</div>""", unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="ai-mini-card"><div class="ai-label">Critical Records</div>'
                    f'<div class="ai-metric">{crit_count}</div>'
                    f'<div class="ai-status-critical">● Immediate Attention</div></div>',
                    unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="ai-mini-card"><div class="ai-label">Monitor Records</div>'
                    f'<div class="ai-metric">{mon_count}</div>'
                    f'<div class="ai-status-warning">● Under Watch</div></div>',
                    unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="ai-mini-card"><div class="ai-label">Anomaly Alerts</div>'
                    f'<div class="ai-metric">{anom_count}</div>'
                    f'<div class="ai-status-warning">● Unusual Patterns</div></div>',
                    unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="ai-mini-card"><div class="ai-label">Capacity Breach %</div>'
                    f'<div class="ai-metric">{cap_breach_val}%</div>'
                    f'<div class="ai-status-critical">● Zone Threshold</div></div>',
                    unsafe_allow_html=True)

    p1, p2 = st.columns(2)
    with p1:
        st.markdown("##### 🌊 Crowd Pressure")
        st.progress(min(avg_pressure_val/100, 1.0))
        st.caption(f"Average Pressure Index: {avg_pressure_val}")
    with p2:
        st.markdown("##### ⏳ Queue Congestion")
        st.progress(min(avg_queue_val/30, 1.0))
        st.caption(f"Average Wait: {avg_queue_val} min")

    p3, p4 = st.columns(2)
    with p3:
        st.markdown("##### 🚑 Emergency Readiness")
        st.progress(max(0, min(1, 1-(amb_resp_val/20))))
        st.caption(f"Ambulance Response: {amb_resp_val} min")
    with p4:
        st.markdown("##### 🚦 Capacity Status")
        st.progress(min(cap_breach_val/100, 1.0))
        st.caption(f"{cap_breach_val}% zones near/exceeding threshold")

    result_key = f"ai_result_{page_key}"
    if result_key not in st.session_state:
        st.session_state[result_key] = ""

    if generate_ai:
        with st.spinner("Claude AI is analyzing dashboard data..."):
            st.session_state[result_key] = generate_ai_insights(summary, ai_temp, ai_tokens)

    if st.session_state.get(result_key):
        tab1, tab2, tab3, tab4 = st.tabs(
            ["📌 Key Insights", "⚠️ Risks", "✅ Recommendations", "📖 Full AI Output"])
        with tab1:
            st.markdown(f"""
<div class="ai-card"><h3>📌 Key Operational Insights</h3><ul>
<li>Critical risk records flagged: <b>{crit_count}</b> require immediate operational response.</li>
<li>Monitor records: <b>{mon_count}</b> zones under active observation.</li>
<li>Anomaly detection identified <b>{anom_count}</b> unusual operating patterns in filtered data.</li>
</ul></div>""", unsafe_allow_html=True)
        with tab2:
            st.markdown("""
<div class="ai-card"><h3>⚠️ Critical Risk Observations</h3><ul>
<li>🔴 High bottleneck risk zones need immediate crowd-control support.</li>
<li>🔴 Delayed ambulance response impacts emergency readiness in critical zones.</li>
<li>🟠 Long queue wait times increase congestion during entry and exit phases.</li>
<li>🟠 Heat exposure elevates medical vulnerability in open and entry zones.</li>
</ul></div>""", unsafe_allow_html=True)
        with tab3:
            st.markdown("""
<div class="ai-card"><h3>✅ Priority Action Plan</h3><ul>
<li>Deploy extra staff immediately to top-ranked risk zones.</li>
<li>Open additional gates during queue spikes (Pre-match / Exit phase).</li>
<li>Reposition medical teams closer to delayed-response zones.</li>
<li>Add barricades for high bottleneck zones before match start.</li>
</ul></div>""", unsafe_allow_html=True)
        with tab4:
            result_text = st.session_state[result_key].replace(chr(10), "<br>")
            st.markdown(
                f'<div class="ai-card"><h3>📖 Claude AI Full Analysis</h3>{result_text}</div>',
                unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
# SIDEBAR  — navigation + filters
# ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div style="text-align:center;padding:6px 0 14px 0;">
  <div style="font-size:32px;">🏏</div>
  <div style="font-family:'Sora',sans-serif;font-size:15px;font-weight:800;margin-top:4px;">
    IPL Crowd Safety
  </div>
  <div style="font-size:9.5px;letter-spacing:.8px;font-weight:600;opacity:.5;margin-top:2px;">
    MANAGEMENT DASHBOARD
  </div>
</div>""", unsafe_allow_html=True)

    for icon, name in PAGES:
        if st.button(f"{icon}  {name}", key=f"nav_{name}"):
            st.session_state.active_page = name
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<p style="font-size:10px;font-weight:700;letter-spacing:.8px;'
                'margin:0 0 8px 0;opacity:.6;">FILTERS</p>', unsafe_allow_html=True)

    all_stadiums = sorted(ops["stadium_name"].dropna().unique())
    sel_stadium  = st.multiselect("Stadium",        all_stadiums, default=all_stadiums, key="f_stad")
    sel_phase    = st.multiselect("Phase",          PHASE_ORDER,  default=PHASE_ORDER,  key="f_ph")
    all_years    = sorted(ops["season_year"].dropna().astype(int).unique())
    sel_year     = st.multiselect("Year",           all_years,    default=all_years,    key="f_yr")
    all_zones    = sorted(ops["zone_type"].dropna().unique())
    sel_zone     = st.multiselect("Zone Type",      all_zones,    default=all_zones,    key="f_zt")
    all_cats     = sorted(ops["match_category"].dropna().unique())
    sel_cat      = st.multiselect("Match Category", all_cats,     default=all_cats,     key="f_mc")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<p style="font-size:10px;font-weight:700;letter-spacing:.8px;'
                'margin:0 0 8px 0;opacity:.6;">CLAUDE AI SETTINGS</p>', unsafe_allow_html=True)
    ai_temperature = st.slider("Temperature", 0.0, 1.0, 0.4, 0.1)
    ai_max_tokens  = st.slider("Max Tokens",  100, 2000, 700, 100)


# ─────────────────────────────────────────────────────────
# FILTER DATA
# ─────────────────────────────────────────────────────────
f = ops[
    ops["stadium_name"].isin(sel_stadium) &
    ops["phase"].isin(sel_phase) &
    ops["season_year"].astype(int).isin(sel_year) &
    ops["zone_type"].isin(sel_zone) &
    ops["match_category"].isin(sel_cat)
].copy()

page = st.session_state.active_page
t    = THEMES.get(page, THEMES["Home"])
inject_css(t)
inject_draggable_sidebar()

if f.empty and page not in ("Home", "Intro"):
    st.warning("⚠️ No data for the selected filters. Please widen your selection.")
    st.stop()

if page not in ("Home", "Intro"):
    f["phase_cat"] = pd.Categorical(f["phase"], categories=PHASE_ORDER, ordered=True)
    inc_f = inc[
        inc["stadium_name"].isin(sel_stadium) &
        inc["season_year"].astype(int).isin(sel_year)
    ].copy() if "stadium_name" in inc.columns and "season_year" in inc.columns else inc.copy()

    f             = add_advanced_risk_features(f)
    risk_matrix   = create_risk_priority_matrix(f)
    anomaly_table = create_anomaly_table(f)

    # ── KPI calculations ──
    safety_risk         = round(f["crowd_pressure_index"].mean()*0.40
                                + f["bottleneck_risk_score"].mean()*0.35
                                + f["avg_queue_wait_time"].mean()*0.25, 2)
    overall_risk_score  = round(f["risk_score"].mean(), 2)
    critical_zone_count = int((f["risk_band"]=="Critical").sum())
    monitor_zone_count  = int((f["risk_band"]=="Monitor").sum())
    med_rate            = round(f["medical_incidents"].sum()/max(f["people_count"].sum(),1)*1000, 2)
    cap_breach          = round(f["capacity_breach"].mean()*100, 2)
    amb_resp            = round(f["ambulance_response_time"].mean(), 2)
    avg_queue           = round(f["avg_queue_wait_time"].mean(), 2)
    avg_pressure        = round(f["crowd_pressure_index"].mean(), 2)
    avg_bottleneck      = round(f["bottleneck_risk_score"].mean(), 2)
    avg_heat            = round(f["heat_risk_index"].mean(), 2)
    high_risk_zones     = int(f[f["bottleneck_risk_score"]>=70]["zone_id"].nunique())
    delayed_med         = int(f[f["ambulance_response_time"]>=10]["zone_id"].nunique())
    res_rate = round(
        inc_f[inc_f["status"]=="Resolved"].shape[0]/max(len(inc_f),1)*100, 2
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
Filters — Stadiums: {', '.join(map(str,sel_stadium))} | Phases: {', '.join(map(str,sel_phase))}
Years: {', '.join(map(str,sel_year))} | Zone Types: {', '.join(map(str,sel_zone))}
Match Categories: {', '.join(map(str,sel_cat))}

KPIs:
Overall Risk Score: {overall_risk_score} | Safety Risk Score: {safety_risk}
Critical Records: {critical_zone_count} | Monitor Records: {monitor_zone_count}
Medical Incident Rate: {med_rate} per 1000 people | Capacity Breach: {cap_breach}%
Resolution Rate: {res_rate}% | Ambulance Response: {amb_resp} min
Queue Wait: {avg_queue} min | Crowd Pressure: {avg_pressure} | Bottleneck Risk: {avg_bottleneck}
Heat Risk: {avg_heat} | High Risk Zones: {high_risk_zones} | Delayed Medical Zones: {delayed_med}
Unauthorized Entries: {unauthorized} | Counterfeit Cases: {counterfeit}
Pitch Invasions: {pitch_inv} | Fan Ejections: {fan_ej}
Required Staff: {req_staff} | Barricades: {req_barr} | Medical Teams: {med_teams}
Staff Adequacy Ratio: {staff_ratio}

Top Risk Priority Matrix:
{top_risk_text}
"""


# ══════════════════════════════════════════════════════════
# PAGE 0 — INTRO  (New dedicated intro/splash page)
# ══════════════════════════════════════════════════════════
if page == "Intro":
    st.markdown("""
<style>
.intro-hero {
    background: linear-gradient(135deg, #0A0818 0%, #1A0A3C 40%, #0C1E3A 100%);
    border-radius: 28px;
    padding: 70px 48px 56px;
    text-align: center;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 24px 80px rgba(109,40,217,.40);
    border: 1px solid #2D1B69;
}
.intro-hero::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse at 50% 0%, rgba(124,58,237,.25) 0%, transparent 65%),
                radial-gradient(ellipse at 80% 80%, rgba(59,130,246,.12) 0%, transparent 55%);
    pointer-events: none;
}
.intro-badge {
    display: inline-block;
    background: rgba(124,58,237,.18);
    border: 1px solid rgba(124,58,237,.45);
    border-radius: 999px;
    padding: 5px 18px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #A78BFA;
    text-transform: uppercase;
    margin-bottom: 20px;
}
.intro-title {
    font-family: 'Sora', sans-serif;
    font-size: clamp(32px, 5vw, 52px);
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1.18;
    margin: 0 0 16px;
    text-shadow: 0 2px 30px rgba(167,139,250,.4);
    letter-spacing: -0.5px;
}
.intro-accent { color: #A78BFA; }
.intro-sub {
    font-size: 16px;
    color: #CBD5E1;
    max-width: 680px;
    margin: 0 auto 36px;
    line-height: 1.75;
    font-weight: 400;
}
.intro-stat-row {
    display: flex;
    justify-content: center;
    gap: 18px;
    flex-wrap: wrap;
    margin-top: 36px;
}
.intro-stat {
    background: rgba(255,255,255,.06);
    border: 1px solid rgba(255,255,255,.12);
    border-radius: 14px;
    padding: 16px 28px;
    min-width: 130px;
    text-align: center;
}
.intro-stat-val {
    font-family: 'Sora', sans-serif;
    font-size: 30px;
    font-weight: 800;
    color: #A78BFA;
    display: block;
}
.intro-stat-lbl {
    font-size: 10px;
    font-weight: 600;
    color: #94A3B8;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-top: 4px;
    display: block;
}
.module-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 14px;
    margin-bottom: 28px;
}
.module-card {
    background: linear-gradient(135deg, #1A1535 0%, #130F2A 100%);
    border: 1px solid #2D1B69;
    border-radius: 16px;
    padding: 22px 20px;
    transition: transform .18s, border-color .18s, box-shadow .18s;
    position: relative;
    overflow: hidden;
}
.module-card:hover {
    transform: translateY(-3px);
    border-color: #7C3AED;
    box-shadow: 0 8px 32px rgba(124,58,237,.22);
}
.module-card-accent {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 3px;
    border-radius: 16px 16px 0 0;
}
.module-icon { font-size: 30px; margin-bottom: 10px; }
.module-name {
    font-family: 'Sora', sans-serif;
    font-size: 15px; font-weight: 800;
    color: #F0EEFF; margin-bottom: 6px;
}
.module-desc { font-size: 12px; color: #94A3B8; line-height: 1.55; }
.tech-chip {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(255,255,255,.05);
    border: 1px solid rgba(255,255,255,.10);
    border-radius: 999px;
    padding: 6px 16px;
    font-size: 12px; font-weight: 600;
    color: #94A3B8;
    margin: 4px;
}
.how-step {
    background: linear-gradient(135deg, #1A1535 0%, #130F2A 100%);
    border: 1px solid #2D1B69;
    border-radius: 14px;
    padding: 20px;
    text-align: center;
}
.how-step-num {
    font-family: 'Sora', sans-serif;
    font-size: 28px; font-weight: 800;
    color: #7C3AED; display: block; margin-bottom: 8px;
}
.how-step-title {
    font-size: 13px; font-weight: 700;
    color: #F0EEFF; display: block; margin-bottom: 6px;
}
.how-step-desc { font-size: 12px; color: #94A3B8; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)

    ops_all = ops.copy()
    total_matches  = ops_all["event_id"].nunique() if "event_id" in ops_all.columns else 0
    total_stadiums = ops_all["stadium_name"].nunique() if "stadium_name" in ops_all.columns else 0
    total_zones    = ops_all["zone_name"].nunique()    if "zone_name"    in ops_all.columns else 0
    total_records  = len(ops_all)

    # Hero banner
    st.markdown(f"""
<div class="intro-hero">
  <div class="intro-badge">🏏 IPL Season Crowd Intelligence Platform</div>
  <h1 class="intro-title">
    Real-Time Safety<br>
    <span class="intro-accent">Command Centre</span>
  </h1>
  <p class="intro-sub">
    A unified intelligence dashboard for IPL stadium operations teams — monitoring
    crowd flow, medical readiness, security threats, and resource allocation
    across every zone and match phase, powered by advanced risk analytics and
    <strong style="color:#A78BFA;">Claude AI</strong>.
  </p>
  <div class="intro-stat-row">
    <div class="intro-stat">
      <span class="intro-stat-val">{total_records:,}</span>
      <span class="intro-stat-lbl">Data Records</span>
    </div>
    <div class="intro-stat">
      <span class="intro-stat-val" style="color:#34D399;">{total_stadiums}</span>
      <span class="intro-stat-lbl">Stadiums</span>
    </div>
    <div class="intro-stat">
      <span class="intro-stat-val" style="color:#F59E0B;">{total_zones}</span>
      <span class="intro-stat-lbl">Zones Monitored</span>
    </div>
    <div class="intro-stat">
      <span class="intro-stat-val" style="color:#EF4444;">{total_matches}</span>
      <span class="intro-stat-lbl">Events Tracked</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    # CTA button
    cta_l, cta_c, cta_r = st.columns([1.5, 1, 1.5])
    with cta_c:
        if st.button("🚀  Enter Dashboard", key="intro_cta", use_container_width=True):
            st.session_state.active_page = "Overview"
            st.rerun()

    st.write("")

    # What this dashboard does
    st.markdown("""
<h2 style="font-family:'Sora',sans-serif;font-size:20px;font-weight:800;
           color:#F0EEFF;text-align:center;margin:8px 0 6px;">
  What This Dashboard Does
</h2>
<p style="text-align:center;font-size:13px;color:#94A3B8;margin-bottom:24px;">
  Seven specialised modules — each designed for a core operational responsibility
</p>
""", unsafe_allow_html=True)

    modules = [
        ("📊","Overview","#7C3AED",
         "Executive command view with overall risk score, KPI summary, risk band distribution, "
         "match category analysis and anomaly detection alerts."),
        ("🌊","Crowd Flow","#1D4ED8",
         "Zone congestion mapping, bottleneck risk scores, queue stress categories and "
         "crowd pressure trends across all five match phases."),
        ("🏥","Medical & Heat","#E11D48",
         "Heat risk index monitoring, medical incident rates, ambulance response time "
         "analysis and emergency readiness scoring by stadium and phase."),
        ("🔒","Security","#D97706",
         "Unauthorized entry attempts, counterfeit ticket detection, pitch invasion tracking "
         "and fan ejection analysis segmented by zone and phase."),
        ("📦","Resource Planning","#0D9488",
         "Staff adequacy ratios, barricade deployment requirements, medical team allocation "
         "and operational readiness across all match phases."),
        ("🚨","Risk Matrix","#DC2626",
         "AI-powered top-15 risk priority matrix with composite risk scores, primary risk "
         "reasons and recommended actions for immediate deployment."),
        ("💬","Ask AI","#8B5CF6",
         "Natural language Q&A powered by Claude AI — ask operational questions and "
         "receive data-grounded, action-oriented answers in seconds."),
    ]

    st.markdown('<div class="module-grid">', unsafe_allow_html=True)
    for icon, name, color, desc in modules:
        st.markdown(f"""
<div class="module-card">
  <div class="module-card-accent" style="background:{color};"></div>
  <div class="module-icon">{icon}</div>
  <div class="module-name">{name}</div>
  <div class="module-desc">{desc}</div>
</div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")

    # How to use
    st.markdown("""
<h2 style="font-family:'Sora',sans-serif;font-size:20px;font-weight:800;
           color:#F0EEFF;text-align:center;margin:8px 0 6px;">
  How to Use This Dashboard
</h2>
<p style="text-align:center;font-size:13px;color:#94A3B8;margin-bottom:20px;">
  Three simple steps to get operational insights
</p>
""", unsafe_allow_html=True)

    h1, h2, h3 = st.columns(3)
    steps = [
        ("01","Apply Filters","Use the sidebar to narrow down by stadium, phase, year, zone type or match category to focus your analysis."),
        ("02","Explore Modules","Navigate through the seven dashboard modules using the sidebar. Each page shows contextual KPIs, charts and risk tables."),
        ("03","Ask AI","Hit 'Generate AI Insights' at the bottom of any page, or visit the Ask AI page to ask natural language operational questions."),
    ]
    for col, (num, title, desc) in zip([h1, h2, h3], steps):
        with col:
            st.markdown(f"""
<div class="how-step">
  <span class="how-step-num">{num}</span>
  <span class="how-step-title">{title}</span>
  <span class="how-step-desc">{desc}</span>
</div>""", unsafe_allow_html=True)

    st.write("")

    # Tech stack
    st.markdown("""
<div style="background:linear-gradient(135deg,#1A1535,#130F2A);
            border:1px solid #2D1B69;border-radius:18px;padding:22px 28px;
            text-align:center;margin-top:10px;">
  <p style="font-size:11px;color:#6B7280;text-transform:uppercase;
            letter-spacing:1.5px;margin-bottom:14px;font-weight:700;">BUILT WITH</p>
  <div style="display:flex;justify-content:center;flex-wrap:wrap;">
    <span class="tech-chip">🐍 Python</span>
    <span class="tech-chip" style="color:#FF4B4B;">⚡ Streamlit</span>
    <span class="tech-chip" style="color:#A78BFA;">📊 Plotly</span>
    <span class="tech-chip" style="color:#34D399;">🤖 Claude AI</span>
    <span class="tech-chip" style="color:#F59E0B;">🐼 Pandas &amp; NumPy</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# PAGE 1 — HOME  (Quick stats + feature summary)
# ══════════════════════════════════════════════════════════
elif page == "Home":
    ops_all = ops.copy()
    total_matches  = ops_all["event_id"].nunique() if "event_id" in ops_all.columns else "N/A"
    total_stadiums = ops_all["stadium_name"].nunique() if "stadium_name" in ops_all.columns else "N/A"
    total_zones    = ops_all["zone_name"].nunique()    if "zone_name"    in ops_all.columns else "N/A"
    total_records  = len(ops_all)

    st.markdown(f"""
<div style="background:linear-gradient(135deg,#1E0A3C 0%,#3D1A78 45%,#0F2A50 100%);
            border-radius:24px;padding:60px 40px 50px;text-align:center;margin-bottom:30px;
            box-shadow:0 20px 60px rgba(124,58,237,.35);">
  <div style="font-size:80px;margin-bottom:12px;filter:drop-shadow(0 4px 20px rgba(167,139,250,.6));">🏏</div>
  <h1 style="font-family:'Sora',sans-serif;font-size:40px;font-weight:800;color:#FFFFFF;
             margin:0 0 12px;text-shadow:0 2px 20px rgba(167,139,250,.5);">
    IPL Crowd Safety Management
  </h1>
  <p style="font-size:17px;font-weight:700;color:#A78BFA;margin:0 0 16px;
            letter-spacing:2px;text-transform:uppercase;">
    Management Dashboard
  </p>
  <p style="font-size:15.5px;color:#CBD5E1;max-width:680px;margin:0 auto 10px;
            line-height:1.7;font-weight:400;">
    An intelligent platform for real-time crowd safety monitoring, risk detection,
    and operational decision support across IPL stadiums — powered by advanced
    analytics and Claude AI.
  </p>
</div>
""", unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1.5, 1, 1.5])
    with col_c:
        if st.button("🚀  Enter Dashboard", key="cta_enter", use_container_width=True):
            st.session_state.active_page = "Overview"
            st.rerun()

    st.write("")

    s1, s2, s3, s4 = st.columns(4)
    stat_style = ("background:linear-gradient(135deg,#1E1A35,#2D1B69);"
                  "border:1px solid #3D2B7A;border-radius:16px;padding:22px 14px;"
                  "text-align:center;box-shadow:0 4px 20px rgba(124,58,237,.2);margin-bottom:16px;")
    with s1:
        st.markdown(f'<div style="{stat_style}"><div style="font-size:36px;font-weight:800;color:#A78BFA;font-family:Sora,sans-serif;">{total_records:,}</div><div style="font-size:11px;color:#94A3B8;text-transform:uppercase;letter-spacing:1px;margin-top:6px;">Total Records</div></div>', unsafe_allow_html=True)
    with s2:
        st.markdown(f'<div style="{stat_style}"><div style="font-size:36px;font-weight:800;color:#34D399;font-family:Sora,sans-serif;">{total_stadiums}</div><div style="font-size:11px;color:#94A3B8;text-transform:uppercase;letter-spacing:1px;margin-top:6px;">Stadiums</div></div>', unsafe_allow_html=True)
    with s3:
        st.markdown(f'<div style="{stat_style}"><div style="font-size:36px;font-weight:800;color:#F59E0B;font-family:Sora,sans-serif;">{total_zones}</div><div style="font-size:11px;color:#94A3B8;text-transform:uppercase;letter-spacing:1px;margin-top:6px;">Zones Monitored</div></div>', unsafe_allow_html=True)
    with s4:
        st.markdown(f'<div style="{stat_style}"><div style="font-size:36px;font-weight:800;color:#EF4444;font-family:Sora,sans-serif;">{total_matches}</div><div style="font-size:11px;color:#94A3B8;text-transform:uppercase;letter-spacing:1px;margin-top:6px;">Events Tracked</div></div>', unsafe_allow_html=True)

    st.write("")
    st.markdown('<p style="text-align:center;font-size:11px;font-weight:700;letter-spacing:2px;'
                'color:#6B7280;text-transform:uppercase;margin-bottom:16px;">DASHBOARD MODULES</p>',
                unsafe_allow_html=True)

    features = [
        ("📊","Overview","Executive KPIs, risk trends, match distribution and crowd pressure analysis.","#7C3AED"),
        ("🌊","Crowd Flow","Queue stress, bottleneck risk, people count by phase and zone congestion.","#1D4ED8"),
        ("🏥","Medical & Heat","Heat risk index, medical incidents, ambulance response and severity analysis.","#E11D48"),
        ("🔒","Security","Unauthorized entries, counterfeit tickets, pitch invasions and fan ejections.","#D97706"),
        ("📦","Resource Planning","Staff adequacy, barricade requirements and medical team deployment.","#0D9488"),
        ("🚨","Risk Matrix","AI-powered risk priority matrix, anomaly detection and recommended actions.","#DC2626"),
        ("💬","Ask AI","Ask natural language questions and get Claude AI answers about dashboard data.","#8B5CF6"),
    ]

    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]
    for i, (icon, name, desc, color) in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
<div style="background:linear-gradient(135deg,#1E1A35,#161230);border:1px solid #3D2B7A;
            border-left:5px solid {color};border-radius:14px;padding:18px 16px;
            margin-bottom:14px;box-shadow:0 4px 16px rgba(0,0,0,.3);">
  <div style="font-size:28px;margin-bottom:8px;">{icon}</div>
  <div style="font-family:'Sora',sans-serif;font-size:14px;font-weight:800;color:#F8F8FF;
              margin-bottom:6px;">{name}</div>
  <div style="font-size:12px;color:#94A3B8;line-height:1.5;">{desc}</div>
</div>""", unsafe_allow_html=True)

    st.write("")
    st.markdown("""
<div style="background:linear-gradient(135deg,#1E1A35,#161230);border:1px solid #3D2B7A;
            border-radius:16px;padding:20px 28px;text-align:center;margin-top:10px;">
  <p style="font-size:11px;color:#6B7280;text-transform:uppercase;letter-spacing:1.5px;
            margin-bottom:12px;">BUILT WITH</p>
  <div style="display:flex;justify-content:center;gap:12px;flex-wrap:wrap;">
    <span style="background:#1E293B;border:1px solid #334155;border-radius:999px;
                 padding:6px 16px;font-size:12px;font-weight:700;color:#94A3B8;">🐍 Python</span>
    <span style="background:#FF4B4B20;border:1px solid #FF4B4B40;border-radius:999px;
                 padding:6px 16px;font-size:12px;font-weight:700;color:#FF4B4B;">⚡ Streamlit</span>
    <span style="background:#636EFA20;border:1px solid #636EFA40;border-radius:999px;
                 padding:6px 16px;font-size:12px;font-weight:700;color:#A78BFA;">📊 Plotly</span>
    <span style="background:#10B98120;border:1px solid #10B98140;border-radius:999px;
                 padding:6px 16px;font-size:12px;font-weight:700;color:#34D399;">🤖 Claude AI</span>
    <span style="background:#F59E0B20;border:1px solid #F59E0B40;border-radius:999px;
                 padding:6px 16px;font-size:12px;font-weight:700;color:#F59E0B;">🐼 Pandas</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# PAGE 2 — OVERVIEW
# ══════════════════════════════════════════════════════════
elif page == "Overview":
    page_header("📊","IPL Stadium Crowd Management & Public Safety Dashboard",
                "Executive overview — crowd movement, stadium risk, medical response and match safety performance")

    k1, k2, k3, k4, k5 = st.columns(5)
    with k1: kpi_card("Overall Risk Score",    overall_risk_score,      "crit","Advanced combined score")
    with k2: kpi_card("Medical Incident Rate", med_rate,                "warn","Per 1K people")
    with k3: kpi_card("Capacity Breach",       f"{cap_breach}%",        "info")
    with k4: kpi_card("Resolution Rate",       f"{res_rate}%",          "ok")
    with k5: kpi_card("Ambulance Response",    f"{amb_resp} min",       "warn")

    st.write("")

    # ── Risk Priority Matrix ──
    sec_label("AI Risk Priority Matrix — Top Risk Zones")
    st.dataframe(risk_matrix, use_container_width=True, height=360)
    dl1, dl2 = st.columns(2)
    with dl1:
        st.download_button("⬇️ Download Risk Priority Matrix CSV",
                           data=csv_bytes(risk_matrix), file_name="risk_priority_matrix.csv",
                           mime="text/csv", use_container_width=True)
    with dl2:
        st.download_button("⬇️ Download Filtered Dashboard Data CSV",
                           data=csv_bytes(f), file_name="filtered_dashboard_data.csv",
                           mime="text/csv", use_container_width=True)

    # ── Anomaly table ──
    sec_label("Anomaly Detection — Unusual Safety Patterns")
    st.dataframe(anomaly_table, use_container_width=True, height=290)

    st.write("")

    # ── Charts ──
    c1, c2 = st.columns([1.6, 1])
    with c1:
        tr = (f.groupby(["phase_cat","zone_type"], as_index=False)["bottleneck_risk_score"]
              .mean().sort_values("phase_cat"))
        tr["phase"] = tr["phase_cat"].astype(str)
        fig = px.line(tr, x="phase", y="bottleneck_risk_score", color="zone_type",
                      markers=True, color_discrete_sequence=t["palette"],
                      title="Operational Risk Trend by Phase")
        st.plotly_chart(sfig(fig,t,310), use_container_width=True)
    with c2:
        rbc = f["risk_band"].value_counts().reset_index()
        rbc.columns = ["Risk Band","Count"]
        fig = px.pie(rbc, names="Risk Band", values="Count", hole=0.55,
                     color="Risk Band",
                     color_discrete_map={"Critical":t["crit_col"],"Monitor":t["warn_col"],"Safe":t["ok_col"]},
                     title="Risk Band Distribution")
        st.plotly_chart(sfig(fig,t,310), use_container_width=True)

    c3, c4 = st.columns([1.6, 1])
    with c3:
        mc = f["match_category"].value_counts().reset_index()
        mc.columns = ["match_category","count"]
        fig = px.bar(mc, y="match_category", x="count", orientation="h",
                     color="match_category", color_discrete_sequence=t["palette"],
                     title="Match Distribution")
        fig.update_layout(showlegend=False)
        st.plotly_chart(sfig(fig,t,290), use_container_width=True)
    with c4:
        pres = f.groupby("zone_type", as_index=False)["risk_score"].mean()
        fig = px.bar(pres, x="zone_type", y="risk_score", color="zone_type",
                     color_discrete_sequence=t["palette"],
                     title="Average Advanced Risk Score by Zone Type")
        fig.update_layout(showlegend=False)
        st.plotly_chart(sfig(fig,t,290), use_container_width=True)

    # ── AI INTELLIGENCE PANEL — at bottom ──
    render_ai_insights_panel(
        "overview", summary_text, t, ai_temperature, ai_max_tokens,
        critical_zone_count, monitor_zone_count, len(anomaly_table),
        cap_breach, avg_pressure, avg_queue, amb_resp
    )


# ══════════════════════════════════════════════════════════
# PAGE 3 — CROWD FLOW
# ══════════════════════════════════════════════════════════
elif page == "Crowd Flow":
    page_header("🌊","Crowd Flow and Congestion Intelligence",
                "Zone congestion, crowd pressure trends, and high-risk areas across match phases")

    k1, k2, k3, k4 = st.columns(4)
    with k1: kpi_card("High Risk Zones",     high_risk_zones,    "crit","bottleneck >= 70")
    with k2: kpi_card("Avg Bottleneck Risk", avg_bottleneck,     "warn")
    with k3: kpi_card("Avg Queue Wait",      f"{avg_queue} min", "info")
    with k4: kpi_card("Avg Crowd Pressure",  avg_pressure,       "ok")

    st.write("")
    c1, c2 = st.columns([1.5, 1])
    with c1:
        pc = (f.groupby(["phase_cat","zone_type"], as_index=False)["people_count"]
              .sum().sort_values("phase_cat"))
        pc["phase"] = pc["phase_cat"].astype(str)
        fig = px.line(pc, x="phase", y="people_count", color="zone_type",
                      markers=True, color_discrete_sequence=t["palette"],
                      title="People Count by Phase Order and Zone Type")
        st.plotly_chart(sfig(fig,t,295), use_container_width=True)
    with c2:
        mat = (f.groupby(["phase","zone_type"])["avg_queue_wait_time"]
               .mean().round(2).unstack("zone_type"))
        mat = mat.reindex([p for p in PHASE_ORDER if p in mat.index])
        sec_label("Avg Queue Wait Time Matrix")
        st.dataframe(mat.style.format("{:.2f}").background_gradient(axis=None),
                     use_container_width=True, height=220)

    c3, c4 = st.columns([1, 1.1])
    with c3:
        bn = f.groupby("zone_type", as_index=False)["bottleneck_risk_score"].mean().round(1)
        fig = px.bar(bn, y="zone_type", x="bottleneck_risk_score", orientation="h",
                     color_discrete_sequence=[t["crit_col"]],
                     title="Avg Bottleneck Risk Score by Zone Type",
                     text="bottleneck_risk_score")
        fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")
        fig.update_layout(showlegend=False)
        st.plotly_chart(sfig(fig,t,275), use_container_width=True)
    with c4:
        qs = f["queue_stress"].value_counts().reset_index()
        qs.columns = ["queue_stress","count"]
        fig = px.pie(qs, names="queue_stress", values="count", hole=0.56,
                     color_discrete_sequence=t["palette"], title="Queue Stress Category")
        st.plotly_chart(sfig(fig,t,275), use_container_width=True)

    sec_label("Top Crowd Flow Risk Zones")
    cf_risk = risk_matrix[
        risk_matrix["Main Risk Reason"].isin(["High bottleneck risk","Long queue wait time"])
    ].head(10)
    st.dataframe(cf_risk, use_container_width=True, height=300)

    dual = (f.groupby("zone_name", as_index=False)
            .agg(crowd_pressure=("crowd_pressure_index","mean"),
                 bottleneck=("bottleneck_risk_score","mean"),
                 risk_score=("risk_score","mean"))
            .sort_values("risk_score", ascending=False).head(15))
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Avg Crowd Pressure Index", y=dual["zone_name"],
                         x=dual["crowd_pressure"], orientation="h", marker_color=t["accent"]))
    fig.add_trace(go.Bar(name="Avg Bottleneck Risk Score", y=dual["zone_name"],
                         x=dual["bottleneck"], orientation="h", marker_color=t["warn_col"]))
    fig.update_layout(barmode="group", title="Crowd Pressure vs Bottleneck Risk by Zone",
                      yaxis=dict(categoryorder="total ascending"))
    st.plotly_chart(sfig(fig,t,440), use_container_width=True)

    # ── AI INTELLIGENCE PANEL — at bottom ──
    render_ai_insights_panel(
        "crowdflow", summary_text, t, ai_temperature, ai_max_tokens,
        critical_zone_count, monitor_zone_count, len(anomaly_table),
        cap_breach, avg_pressure, avg_queue, amb_resp
    )


# ══════════════════════════════════════════════════════════
# PAGE 4 — MEDICAL & HEAT
# ══════════════════════════════════════════════════════════
elif page == "Medical & Heat":
    page_header("🏥","Medical and Heat Intelligence",
                "Heat stress, medical incidents, ambulance response and emergency readiness")

    k1, k2, k3, k4 = st.columns(4)
    with k1: kpi_card("Medical Incident Rate",  med_rate,          "warn","per 1K people")
    with k2: kpi_card("Avg Ambulance Response", f"{amb_resp} min", "crit")
    with k3: kpi_card("Avg Heat Risk Index",    avg_heat,          "warn")
    with k4: kpi_card("Delayed Medical Zones",  delayed_med,       "crit","response >= 10 min")

    st.write("")
    c1, c2 = st.columns([1.55, 1])
    with c1:
        heat = (f.groupby("phase_cat", as_index=False)["heat_risk_index"]
                .mean().sort_values("phase_cat"))
        heat["phase"] = heat["phase_cat"].astype(str)
        fig = px.line(heat, x="phase", y="heat_risk_index", markers=True,
                      color_discrete_sequence=[t["accent"]], title="Heat Risk Index by Phase")
        fig.update_traces(line_width=3, marker_size=10)
        st.plotly_chart(sfig(fig,t,300), use_container_width=True)
    with c2:
        med_s = (f.groupby("stadium_name", as_index=False)["medical_incidents"]
                 .sum().sort_values("medical_incidents"))
        fig = px.bar(med_s, y="stadium_name", x="medical_incidents", orientation="h",
                     color="stadium_name", color_discrete_sequence=t["palette"],
                     title="Medical Incidents by Stadium")
        fig.update_layout(showlegend=False)
        st.plotly_chart(sfig(fig,t,300), use_container_width=True)

    sec_label("Medical & Heat Priority Zones")
    med_risk = risk_matrix[
        risk_matrix["Main Risk Reason"].isin(["Delayed medical response","High heat exposure"])
    ].head(10)
    st.dataframe(med_risk, use_container_width=True, height=280)

    c3, c4 = st.columns([1, 1.6])
    with c3:
        if not inc_f.empty and "severity" in inc_f.columns:
            sev = inc_f["severity"].value_counts().reset_index()
            sev.columns = ["severity","count"]
            fig = px.pie(sev, names="severity", values="count", hole=0.55,
                         color_discrete_sequence=t["palette"], title="Incident by Severity")
            fig.update_traces(textinfo="percent+value", textfont_size=11)
            st.plotly_chart(sfig(fig,t,285), use_container_width=True)
        else:
            st.info("No incident severity data for current filters.")
    with c4:
        hr_med = f.groupby("zone_name", as_index=False).agg(
            heat=("heat_risk_index","mean"), med=("medical_incidents","mean"),
            risk_score=("risk_score","mean"))
        fig = px.scatter(hr_med, x="heat", y="med", size="risk_score", color="zone_name",
                         color_discrete_sequence=t["palette"],
                         title="Heat Risk vs Medical Incidents by Zone")
        st.plotly_chart(sfig(fig,t,285), use_container_width=True)

    amb = (f.groupby(["phase_cat","zone_type"], as_index=False)["ambulance_response_time"]
           .mean().sort_values("phase_cat"))
    amb["phase"] = amb["phase_cat"].astype(str)
    fig = px.line(amb, x="phase", y="ambulance_response_time", color="zone_type",
                  markers=True, color_discrete_sequence=t["palette"],
                  title="Ambulance Response Time by Phase and Zone Type")
    st.plotly_chart(sfig(fig,t,310), use_container_width=True)

    # ── AI INTELLIGENCE PANEL — at bottom ──
    render_ai_insights_panel(
        "medical", summary_text, t, ai_temperature, ai_max_tokens,
        critical_zone_count, monitor_zone_count, len(anomaly_table),
        cap_breach, avg_pressure, avg_queue, amb_resp
    )


# ══════════════════════════════════════════════════════════
# PAGE 5 — SECURITY
# ══════════════════════════════════════════════════════════
elif page == "Security":
    page_header("🔒","Security & Unauthorized Activity Monitoring",
                "Unauthorized entries, security incidents, ticket fraud, fan ejections and stadium safety")

    k1, k2, k3, k4 = st.columns(4)
    with k1: kpi_card("Unauthorized Entries", f"{unauthorized:,}", "crit")
    with k2: kpi_card("Counterfeit Cases",    f"{counterfeit:,}", "warn")
    with k3: kpi_card("Pitch Invasions",      f"{pitch_inv:,}",   "crit")
    with k4: kpi_card("Fan Ejections",        f"{fan_ej:,}",      "warn")

    st.write("")
    c1, c2 = st.columns([1.4, 1])
    with c1:
        ua = (f.groupby(["phase_cat","zone_type"], as_index=False)["unauthorized_entry_attempts"]
              .mean().sort_values("phase_cat"))
        ua["phase"] = ua["phase_cat"].astype(str)
        fig = px.line(ua, x="phase", y="unauthorized_entry_attempts", color="zone_type",
                      markers=True, color_discrete_sequence=t["palette"],
                      title="Unauthorized Entry by Phase and Zone Type")
        st.plotly_chart(sfig(fig,t,295), use_container_width=True)
    with c2:
        sec_s = (f.groupby("stadium_name", as_index=False)["security_incidents"]
                 .sum().sort_values("security_incidents"))
        fig = px.bar(sec_s, y="stadium_name", x="security_incidents", orientation="h",
                     color_discrete_sequence=[t["accent"]], title="Security Incidents by Stadium")
        fig.update_layout(showlegend=False)
        st.plotly_chart(sfig(fig,t,295), use_container_width=True)

    c3, c4 = st.columns([1.2, 1])
    with c3:
        cs = f.groupby("zone_name", as_index=False).agg(
            pressure=("crowd_pressure_index","mean"),
            security=("security_incidents","sum"),
            people=("people_count","sum"),
            risk_score=("risk_score","mean"))
        fig = px.scatter(cs, x="people", y="pressure", color="zone_name", size="risk_score",
                         color_discrete_sequence=t["palette"],
                         title="Crowd Pressure vs Security Risk")
        st.plotly_chart(sfig(fig,t,295), use_container_width=True)
    with c4:
        sp = (f.groupby(["phase_cat","zone_type"], as_index=False)["security_incidents"]
              .mean().sort_values("phase_cat"))
        sp["phase"] = sp["phase_cat"].astype(str)
        fig = px.bar(sp, x="phase", y="security_incidents", color="zone_type",
                     barmode="group", color_discrete_sequence=t["palette"],
                     title="Security Incidents by Phase and Zone Type")
        st.plotly_chart(sfig(fig,t,295), use_container_width=True)

    # ── AI INTELLIGENCE PANEL — at bottom ──
    render_ai_insights_panel(
        "security", summary_text, t, ai_temperature, ai_max_tokens,
        critical_zone_count, monitor_zone_count, len(anomaly_table),
        cap_breach, avg_pressure, avg_queue, amb_resp
    )


# ══════════════════════════════════════════════════════════
# PAGE 6 — RESOURCE PLANNING
# ══════════════════════════════════════════════════════════
elif page == "Resource Planning":
    page_header("📦","Resource Planning & Operational Readiness",
                "Staff requirements, barricade deployment, medical teams and readiness across phases")

    k1, k2, k3, k4 = st.columns(4)
    with k1: kpi_card("Staff Adequacy Ratio", staff_ratio,      "ok")
    with k2: kpi_card("Total Required Staff", f"{req_staff:,}", "info")
    with k3: kpi_card("Total Barricades",     f"{req_barr:,}",  "warn")
    with k4: kpi_card("Total Medical Teams",  f"{med_teams:,}", "ok")

    st.write("")
    sec_label("Resource Action Plan Based on Risk Matrix")
    resource_plan = risk_matrix[
        ["Stadium","Zone","Zone Type","Phase","Risk Score","Risk Band",
         "Main Risk Reason","Recommended Action"]
    ].head(12)
    st.dataframe(resource_plan, use_container_width=True, height=320)

    c1, c2 = st.columns([1.55, 1])
    with c1:
        rd = (f.groupby(["phase_cat","zone_type"], as_index=False)["staff_adequacy_ratio"]
              .mean().sort_values("phase_cat"))
        rd["phase"] = rd["phase_cat"].astype(str)
        fig = px.line(rd, x="phase", y="staff_adequacy_ratio", color="zone_type",
                      markers=True, color_discrete_sequence=t["palette"],
                      title="Operational Readiness Across Match Phases")
        st.plotly_chart(sfig(fig,t,295), use_container_width=True)
    with c2:
        md = f.groupby("zone_type", as_index=False).agg(
            people=("people_count","sum"), med_t=("deployed_medical_teams","sum"))
        fig = px.scatter(md, x="people", y="med_t", color="zone_type", size="med_t",
                         color_discrete_sequence=t["palette"],
                         title="Medical Team Deployment vs Crowd Size")
        st.plotly_chart(sfig(fig,t,295), use_container_width=True)

    c3, c4 = st.columns([1, 1])
    with c3:
        res = f.groupby("zone_type", as_index=False).agg(
            staff=("required_staff","sum"), med=("deployed_medical_teams","sum"))
        fig = go.Figure()
        fig.add_bar(y=res["zone_type"], x=res["staff"], name="Required Staff",
                    orientation="h", marker_color=t["palette"][0])
        fig.add_bar(y=res["zone_type"], x=res["med"], name="Medical Teams",
                    orientation="h", marker_color=t["palette"][1])
        fig.update_layout(barmode="group", title="Required Staff vs Medical Deployment")
        st.plotly_chart(sfig(fig,t,275), use_container_width=True)
    with c4:
        br = (f.groupby("zone_type", as_index=False)["required_barricades"]
              .sum().sort_values("required_barricades"))
        fig = px.bar(br, y="zone_type", x="required_barricades", orientation="h",
                     color_discrete_sequence=[t["palette"][0]],
                     title="Barricade Requirements by Zone")
        fig.update_layout(showlegend=False)
        st.plotly_chart(sfig(fig,t,275), use_container_width=True)

    mat2 = f.pivot_table(values="staff_adequacy_ratio",
                         index="stadium_name", columns="phase", aggfunc="mean").round(2)
    ord_cols = [p for p in PHASE_ORDER if p in mat2.columns]
    mat2 = mat2[ord_cols]
    sec_label("Staff Adequacy Ratio — Stadium x Phase")
    st.dataframe(mat2.style.format("{:.2f}").background_gradient(axis=None),
                 use_container_width=True)

    # ── AI INTELLIGENCE PANEL — at bottom ──
    render_ai_insights_panel(
        "resource", summary_text, t, ai_temperature, ai_max_tokens,
        critical_zone_count, monitor_zone_count, len(anomaly_table),
        cap_breach, avg_pressure, avg_queue, amb_resp
    )


# ══════════════════════════════════════════════════════════
# PAGE 7 — RISK MATRIX
# ══════════════════════════════════════════════════════════
elif page == "Risk Matrix":
    page_header("🚨","AI Risk Priority Matrix & Anomaly Intelligence",
                "Advanced decision-support: critical zones, risk reasons and recommended actions")

    k1, k2, k3, k4 = st.columns(4)
    with k1: kpi_card("Overall Risk Score", overall_risk_score,  "crit")
    with k2: kpi_card("Critical Records",   critical_zone_count, "crit")
    with k3: kpi_card("Monitor Records",    monitor_zone_count,  "warn")
    with k4: kpi_card("Anomaly Alerts",     len(anomaly_table),  "info")

    st.write("")
    sec_label("Top 15 Risk Priority Matrix")
    st.dataframe(risk_matrix, use_container_width=True, height=420)
    st.download_button("⬇️ Download Full Risk Priority Matrix",
                       data=csv_bytes(risk_matrix), file_name="risk_priority_matrix.csv",
                       mime="text/csv", use_container_width=True)

    sec_label("Risk Score by Stadium and Zone Type")
    c1, c2 = st.columns([1.3, 1])
    with c1:
        sr = (f.groupby(["stadium_name","zone_type"], as_index=False)["risk_score"]
              .mean().sort_values("risk_score", ascending=False))
        fig = px.bar(sr, x="risk_score", y="stadium_name", color="zone_type",
                     orientation="h", color_discrete_sequence=t["palette"],
                     title="Average Risk Score by Stadium and Zone Type")
        st.plotly_chart(sfig(fig,t,360), use_container_width=True)
    with c2:
        rd = f["risk_band"].value_counts().reset_index()
        rd.columns = ["Risk Band","Count"]
        fig = px.pie(rd, names="Risk Band", values="Count", hole=0.55,
                     color="Risk Band",
                     color_discrete_map={"Critical":t["crit_col"],"Monitor":t["warn_col"],"Safe":t["ok_col"]},
                     title="Risk Band Distribution")
        st.plotly_chart(sfig(fig,t,360), use_container_width=True)

    sec_label("Anomaly Detection Table")
    st.dataframe(anomaly_table, use_container_width=True, height=360)
    st.download_button("⬇️ Download Anomaly Detection CSV",
                       data=csv_bytes(anomaly_table), file_name="anomaly_detection.csv",
                       mime="text/csv", use_container_width=True)

    # ── AI INTELLIGENCE PANEL — at bottom ──
    render_ai_insights_panel(
        "riskmatrix", summary_text, t, ai_temperature, ai_max_tokens,
        critical_zone_count, monitor_zone_count, len(anomaly_table),
        cap_breach, avg_pressure, avg_queue, amb_resp
    )


# ══════════════════════════════════════════════════════════
# PAGE 8 — ASK AI
# ══════════════════════════════════════════════════════════
elif page == "Ask AI":
    page_header("💬","Ask AI — Claude-Powered Dashboard Q&A Assistant",
                "Ask questions about crowd risk, medical readiness, security, staffing and priority zones")

    if "ai_question" not in st.session_state:
        st.session_state.ai_question = ""
    if "ai_answer" not in st.session_state:
        st.session_state.ai_answer = ""

    k1, k2, k3, k4 = st.columns(4)
    with k1: kpi_card("Overall Risk Score", overall_risk_score,  "crit")
    with k2: kpi_card("Critical Records",   critical_zone_count, "crit")
    with k3: kpi_card("Anomaly Alerts",     len(anomaly_table),  "warn")
    with k4: kpi_card("Avg Queue Wait",     f"{avg_queue} min",  "info")

    st.write("")

    # ── API key status ──
    key_ok = bool(get_anthropic_key())
    if key_ok:
        st.success("✅ Claude AI is connected and ready.", icon="🤖")
    else:
        st.error(
            "⚠️ **Claude AI API key not configured.**  \n"
            "Go to **Streamlit Cloud → App menu (⋮) → Settings → Secrets** and add:  \n"
            "`ANTHROPIC_API_KEY = \"your_key_here\"`  \n"
            "Then click **Save** — the app will reload automatically.",
            icon="🔑")

    sec_label("Suggested Questions")
    q1, q2, q3 = st.columns(3)
    with q1:
        if st.button("Which zones need urgent attention?", use_container_width=True):
            st.session_state.ai_question = "Which zones need urgent attention and why?"
            st.session_state.ai_answer = ""
    with q2:
        if st.button("What should operations team do first?", use_container_width=True):
            st.session_state.ai_question = "What should the stadium operations team do first?"
            st.session_state.ai_answer = ""
    with q3:
        if st.button("Explain this dashboard simply", use_container_width=True):
            st.session_state.ai_question = "Explain this dashboard in simple presentation-friendly language."
            st.session_state.ai_answer = ""

    q4, q5, q6 = st.columns(3)
    with q4:
        if st.button("Why is medical risk important?", use_container_width=True):
            st.session_state.ai_question = "Why is medical risk important for IPL crowd safety?"
            st.session_state.ai_answer = ""
    with q5:
        if st.button("Which phase is most risky?", use_container_width=True):
            st.session_state.ai_question = "Which match phase is most risky and what action is needed?"
            st.session_state.ai_answer = ""
    with q6:
        if st.button("Give 5 interview talking points", use_container_width=True):
            st.session_state.ai_question = "Give me 5 interview talking points for explaining this project."
            st.session_state.ai_answer = ""

    user_question = st.text_area(
        "Ask your own dashboard question",
        value=st.session_state.ai_question,
        placeholder="Example: Which stadium has the highest crowd risk and why?",
        height=120, key="qa_text_area")

    ask_btn = st.button("💬 Ask AI", use_container_width=True)

    if ask_btn:
        if not user_question.strip():
            st.warning("Please type or select a question first.")
        else:
            qa_context = f"""
Dashboard KPIs:
Overall Risk Score: {overall_risk_score} | Safety Risk: {safety_risk}
Critical Records: {critical_zone_count} | Monitor Records: {monitor_zone_count}
Medical Rate: {med_rate}/1000 | Capacity Breach: {cap_breach}% | Resolution Rate: {res_rate}%
Ambulance Response: {amb_resp} min | Queue Wait: {avg_queue} min
Crowd Pressure: {avg_pressure} | Bottleneck Risk: {avg_bottleneck} | Heat Risk: {avg_heat}
High Risk Zones: {high_risk_zones} | Delayed Medical Zones: {delayed_med}
Unauthorized: {unauthorized} | Counterfeit: {counterfeit} | Pitch Invasions: {pitch_inv}
Fan Ejections: {fan_ej} | Staff Required: {req_staff} | Barricades: {req_barr}
Medical Teams: {med_teams} | Staff Ratio: {staff_ratio}

Top Risk Matrix:
{risk_matrix.head(10).to_string(index=False)}

Anomaly Table:
{anomaly_table.head(10).to_string(index=False)}
"""
            with st.spinner("Claude AI is analyzing your question..."):
                st.session_state.ai_answer = ask_ai_question(
                    user_question, qa_context, temperature_value=0.3, token_value=700)

    if st.session_state.ai_answer:
        st.markdown(f"""
<div class="ai-card">
  <h3>💬 Claude AI Answer</h3>
  {st.session_state.ai_answer.replace(chr(10),"<br>")}
</div>""", unsafe_allow_html=True)

    sec_label("Q&A Context Tables")
    c1, c2 = st.columns(2)
    with c1:
        st.caption("Top risk records used by AI")
        st.dataframe(risk_matrix.head(8), use_container_width=True, height=260)
    with c2:
        st.caption("Top anomaly records used by AI")
        st.dataframe(anomaly_table.head(8), use_container_width=True, height=260)


# ─────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    f'<p style="text-align:center;font-size:11px;color:{t["text2"]};padding:4px 0;">'
    "🏏 IPL Crowd Safety Management Dashboard &nbsp;|&nbsp;"
    " Streamlit + Plotly + Claude AI &nbsp;|&nbsp; Advanced Risk Matrix Enabled"
    "</p>", unsafe_allow_html=True)
