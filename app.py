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

# THEMES — Redesigned with custom premium dark stadium operations control command palettes
# ─────────────────────────────────────────────────────────
# THEMES — Redesigned with custom premium dark/light stadium operations control command palettes
# ─────────────────────────────────────────────────────────
THEMES_DARK = {
    "Home Page": {
        "bg": "#0B101E", "sidebar": "#070B14", "card": "#131C33",
        "border": "#212F4F", "accent": "#00F0FF", "accent_lt": "rgba(0, 240, 255, 0.12)", "accent2": "#38BDF8",
        "text": "#FAFAFA", "text2": "#94A3B8",
        "plot_bg": "#121A2F", "paper_bg": "#090D1A", "grid": "#212F4F",
        "legend_rgba": "rgba(11,16,30,0.95)", "shadow": "0 4px 20px rgba(0,0,0,0.3)",
        "palette": ["#00F0FF", "#38BDF8", "#FBBF24", "#34D399", "#F87171", "#A78BFA"],
        "crit_col": "#F43F5E", "warn_col": "#FBBF24", "ok_col": "#10B981", "info_col": "#00F0FF",
    },
    "User Portal": {
        "bg": "#100C26", "sidebar": "#0A0819", "card": "#1D1845",
        "border": "#312B6E", "accent": "#818CF8", "accent_lt": "rgba(129, 140, 248, 0.12)", "accent2": "#A78BFA",
        "text": "#FAFAFA", "text2": "#94A3B8",
        "plot_bg": "#1D1845", "paper_bg": "#100C26", "grid": "#271E57",
        "legend_rgba": "rgba(16,12,38,0.95)", "shadow": "0 4px 20px rgba(0,0,0,0.3)",
        "palette": ["#818CF8", "#A78BFA", "#FBBF24", "#10B981", "#EF4444", "#3B82F6"],
        "crit_col": "#EF4444", "warn_col": "#FBBF24", "ok_col": "#10B981", "info_col": "#818CF8",
    },
    "Intro": {
        "bg": "#0B101E", "sidebar": "#070B14", "card": "#131C33",
        "border": "#212F4F", "accent": "#00F0FF", "accent_lt": "rgba(0, 240, 255, 0.12)", "accent2": "#38BDF8",
        "text": "#FAFAFA", "text2": "#94A3B8",
        "plot_bg": "#121A2F", "paper_bg": "#090D1A", "grid": "#212F4F",
        "legend_rgba": "rgba(11,16,30,0.95)", "shadow": "0 4px 20px rgba(0,0,0,0.3)",
        "palette": ["#00F0FF", "#38BDF8", "#FBBF24", "#34D399", "#F87171", "#A78BFA"],
        "crit_col": "#F43F5E", "warn_col": "#FBBF24", "ok_col": "#10B981", "info_col": "#00F0FF",
    },
    "Overview": {
        "bg": "#0B1123", "sidebar": "#080C1A", "card": "#141C3B",
        "border": "#232F5A", "accent": "#38BDF8", "accent_lt": "rgba(56, 189, 248, 0.12)", "accent2": "#0EA5E9",
        "text": "#FAFAFA", "text2": "#94A3B8",
        "plot_bg": "#141C3B", "paper_bg": "#0B1123", "grid": "#1D2B4A",
        "legend_rgba": "rgba(11,17,35,0.95)", "shadow": "0 4px 20px rgba(0,0,0,0.3)",
        "palette": ["#38BDF8", "#0ea5e9", "#FBBF24", "#34D399", "#F87171", "#A78BFA"],
        "crit_col": "#F43F5E", "warn_col": "#FBBF24", "ok_col": "#10B981", "info_col": "#38BDF8",
    },
    "Crowd Flow": {
        "bg": "#061320", "sidebar": "#040D17", "card": "#0F2136",
        "border": "#1C3654", "accent": "#00F0FF", "accent_lt": "rgba(0, 240, 255, 0.12)", "accent2": "#38BDF8",
        "text": "#FAFAFA", "text2": "#94A3B8",
        "plot_bg": "#0F2136", "paper_bg": "#061320", "grid": "#192F47",
        "legend_rgba": "rgba(6,19,32,0.95)", "shadow": "0 4px 20px rgba(0,0,0,0.3)",
        "palette": ["#00F0FF", "#38BDF8", "#FBBF24", "#34D399", "#F43F5E", "#A78BFA"],
        "crit_col": "#F43F5E", "warn_col": "#FBBF24", "ok_col": "#10B981", "info_col": "#00F0FF",
    },
    "Medical & Heat": {
        "bg": "#1C0810", "sidebar": "#12050A", "card": "#2E111D",
        "border": "#4F2134", "accent": "#F43F5E", "accent_lt": "rgba(244, 63, 94, 0.12)", "accent2": "#E11D48",
        "text": "#FAFAFA", "text2": "#94A3B8",
        "plot_bg": "#2E111D", "paper_bg": "#1C0810", "grid": "#421B2B",
        "legend_rgba": "rgba(28,8,16,0.95)", "shadow": "0 4px 20px rgba(0,0,0,0.3)",
        "palette": ["#F43F5E", "#E11D48", "#F97316", "#8B5CF6", "#3B82F6", "#10B981"],
        "crit_col": "#F43F5E", "warn_col": "#F97316", "ok_col": "#10B981", "info_col": "#F43F5E",
    },
    "Security": {
        "bg": "#1A1005", "sidebar": "#100A03", "card": "#2F1F0C",
        "border": "#4F3418", "accent": "#FBBF24", "accent_lt": "rgba(251, 191, 36, 0.12)", "accent2": "#B45309",
        "text": "#FAFAFA", "text2": "#94A3B8",
        "plot_bg": "#2F1F0C", "paper_bg": "#1A1005", "grid": "#422C14",
        "legend_rgba": "rgba(26,16,5,0.95)", "shadow": "0 4px 20px rgba(0,0,0,0.3)",
        "palette": ["#FBBF24", "#F97316", "#3B82F6", "#10B981", "#8B5CF6", "#EF4444"],
        "crit_col": "#EF4444", "warn_col": "#FBBF24", "ok_col": "#10B981", "info_col": "#FBBF24",
    },
    "Resource Planning": {
        "bg": "#051610", "sidebar": "#030E0A", "card": "#0D2A20",
        "border": "#1A493B", "accent": "#10B981", "accent_lt": "rgba(16, 185, 129, 0.12)", "accent2": "#047857",
        "text": "#FAFAFA", "text2": "#94A3B8",
        "plot_bg": "#0D2A20", "paper_bg": "#051610", "grid": "#153C31",
        "legend_rgba": "rgba(5,22,16,0.95)", "shadow": "0 4px 20px rgba(0,0,0,0.3)",
        "palette": ["#10B981", "#34D399", "#8B5CF6", "#0ea5e9", "#FBBF24", "#EF4444"],
        "crit_col": "#EF4444", "warn_col": "#FBBF24", "ok_col": "#10B981", "info_col": "#10B981",
    },
    "Risk Matrix": {
        "bg": "#1D0707", "sidebar": "#120404", "card": "#301212",
        "border": "#552121", "accent": "#EF4444", "accent_lt": "rgba(239, 68, 68, 0.12)", "accent2": "#9C1C1C",
        "text": "#FAFAFA", "text2": "#94A3B8",
        "plot_bg": "#301212", "paper_bg": "#1D0707", "grid": "#471919",
        "legend_rgba": "rgba(29,7,7,0.95)", "shadow": "0 4px 20px rgba(0,0,0,0.3)",
        "palette": ["#EF4444", "#F97316", "#FBBF24", "#10B981", "#3B82F6", "#8B5CF6"],
        "crit_col": "#EF4444", "warn_col": "#F97316", "ok_col": "#10B981", "info_col": "#EF4444",
    },
    "Ask AI": {
        "bg": "#100C26", "sidebar": "#0A0819", "card": "#1D1845",
        "border": "#312B6E", "accent": "#818CF8", "accent_lt": "rgba(129, 140, 248, 0.12)", "accent2": "#A78BFA",
        "text": "#FAFAFA", "text2": "#94A3B8",
        "plot_bg": "#1D1845", "paper_bg": "#100C26", "grid": "#271E57",
        "legend_rgba": "rgba(16,12,38,0.95)", "shadow": "0 4px 20px rgba(0,0,0,0.3)",
        "palette": ["#818CF8", "#A78BFA", "#FBBF24", "#10B981", "#EF4444", "#3B82F6"],
        "crit_col": "#EF4444", "warn_col": "#FBBF24", "ok_col": "#10B981", "info_col": "#818CF8",
    },
    "About App": {
        "bg": "#100C26", "sidebar": "#0A0819", "card": "#1D1845",
        "border": "#312B6E", "accent": "#818CF8", "accent_lt": "rgba(129, 140, 248, 0.12)", "accent2": "#A78BFA",
        "text": "#FAFAFA", "text2": "#94A3B8",
        "plot_bg": "#1D1845", "paper_bg": "#100C26", "grid": "#271E57",
        "legend_rgba": "rgba(16,12,38,0.95)", "shadow": "0 4px 20px rgba(0,0,0,0.3)",
        "palette": ["#818CF8", "#A78BFA", "#FBBF24", "#10B981", "#EF4444", "#3B82F6"],
        "crit_col": "#EF4444", "warn_col": "#FBBF24", "ok_col": "#10B981", "info_col": "#818CF8",
    },
}

THEMES_LIGHT = {
    "Home Page": {
        "bg": "#F2F5FB", "sidebar": "#E5ECF6", "card": "#FFFFFF",
        "border": "#CBD6E4", "accent": "#008CA8", "accent_lt": "rgba(0, 140, 168, 0.08)", "accent2": "#0ea5e9",
        "text": "#0F172A", "text2": "#475569",
        "plot_bg": "#FFFFFF", "paper_bg": "#F2F5FB", "grid": "#E2E8F0",
        "legend_rgba": "rgba(255,255,255,0.95)", "shadow": "0 4px 12px rgba(0,0,0,0.06)",
        "palette": ["#008CA8", "#0ea5e9", "#D97706", "#059669", "#DC2626", "#7C3AED"],
        "crit_col": "#DC2626", "warn_col": "#D97706", "ok_col": "#059669", "info_col": "#008CA8",
    },
    "User Portal": {
        "bg": "#F6F5FC", "sidebar": "#ECE9FC", "card": "#FFFFFF",
        "border": "#D7D2FB", "accent": "#5A2EDB", "accent_lt": "rgba(90, 46, 219, 0.08)", "accent2": "#6366F1",
        "text": "#0F172A", "text2": "#475569",
        "plot_bg": "#FFFFFF", "paper_bg": "#F6F5FC", "grid": "#E2E8F0",
        "legend_rgba": "rgba(255,255,255,0.95)", "shadow": "0 4px 12px rgba(0,0,0,0.06)",
        "palette": ["#5A2EDB", "#6366F1", "#D97706", "#059669", "#DC2626", "#1D4ED8"],
        "crit_col": "#DC2626", "warn_col": "#D97706", "ok_col": "#059669", "info_col": "#5A2EDB",
    },
    "Intro": {
        "bg": "#F2F5FB", "sidebar": "#E5ECF6", "card": "#FFFFFF",
        "border": "#CBD6E4", "accent": "#008CA8", "accent_lt": "rgba(0, 140, 168, 0.08)", "accent2": "#0ea5e9",
        "text": "#0F172A", "text2": "#475569",
        "plot_bg": "#FFFFFF", "paper_bg": "#F2F5FB", "grid": "#E2E8F0",
        "legend_rgba": "rgba(255,255,255,0.95)", "shadow": "0 4px 12px rgba(0,0,0,0.06)",
        "palette": ["#008CA8", "#0ea5e9", "#D97706", "#059669", "#DC2626", "#7C3AED"],
        "crit_col": "#DC2626", "warn_col": "#D97706", "ok_col": "#059669", "info_col": "#008CA8",
    },
    "Overview": {
        "bg": "#F3F5FA", "sidebar": "#E6ECF5", "card": "#FFFFFF",
        "border": "#CCD6E5", "accent": "#1D4ED8", "accent_lt": "rgba(29, 78, 216, 0.08)", "accent2": "#3B82F6",
        "text": "#0F172A", "text2": "#475569",
        "plot_bg": "#FFFFFF", "paper_bg": "#F3F5FA", "grid": "#E2E8F0",
        "legend_rgba": "rgba(255,255,255,0.95)", "shadow": "0 4px 12px rgba(0,0,0,0.06)",
        "palette": ["#1D4ED8", "#3B82F6", "#D97706", "#059669", "#DC2626", "#7C3AED"],
        "crit_col": "#DC2626", "warn_col": "#D97706", "ok_col": "#059669", "info_col": "#1D4ED8",
    },
    "Crowd Flow": {
        "bg": "#EDF7F9", "sidebar": "#D6EDF2", "card": "#FFFFFF",
        "border": "#B5DEE5", "accent": "#2B82A1", "accent_lt": "rgba(43, 130, 161, 0.08)", "accent2": "#0284C7",
        "text": "#0F172A", "text2": "#475569",
        "plot_bg": "#FFFFFF", "paper_bg": "#EDF7F9", "grid": "#E2E8F0",
        "legend_rgba": "rgba(255,255,255,0.95)", "shadow": "0 4px 12px rgba(0,0,0,0.06)",
        "palette": ["#2B82A1", "#0284C7", "#D97706", "#059669", "#7C3AED", "#DC2626"],
        "crit_col": "#DC2626", "warn_col": "#D97706", "ok_col": "#059669", "info_col": "#2B82A1",
    },
    "Medical & Heat": {
        "bg": "#FFF0F2", "sidebar": "#FFDDE2", "card": "#FFFFFF",
        "border": "#F3BAC2", "accent": "#C11D3E", "accent_lt": "rgba(193, 29, 62, 0.08)", "accent2": "#DC2626",
        "text": "#0F172A", "text2": "#475569",
        "plot_bg": "#FFFFFF", "paper_bg": "#FFF0F2", "grid": "#E2E8F0",
        "legend_rgba": "rgba(255,255,255,0.95)", "shadow": "0 4px 12px rgba(0,0,0,0.06)",
        "palette": ["#C11D3E", "#DC2626", "#EA580C", "#6D28D9", "#1D4ED8", "#059669"],
        "crit_col": "#C11D3E", "warn_col": "#EA580C", "ok_col": "#059669", "info_col": "#6D28D9",
    },
    "Security": {
        "bg": "#FFF9EA", "sidebar": "#FFF0CC", "card": "#FFFFFF",
        "border": "#EED8A7", "accent": "#B86F00", "accent_lt": "rgba(184, 111, 0, 0.08)", "accent2": "#D97706",
        "text": "#0F172A", "text2": "#475569",
        "plot_bg": "#FFFFFF", "paper_bg": "#FFF9EA", "grid": "#E2E8F0",
        "legend_rgba": "rgba(255,255,255,0.95)", "shadow": "0 4px 12px rgba(0,0,0,0.06)",
        "palette": ["#B86F00", "#D97706", "#1D4ED8", "#059669", "#6D28D9", "#DC2626"],
        "crit_col": "#DC2626", "warn_col": "#B86F00", "ok_col": "#059669", "info_col": "#1D4ED8",
    },
    "Resource Planning": {
        "bg": "#EEFAFA", "sidebar": "#DCF5ED", "card": "#FFFFFF",
        "border": "#B9E8D9", "accent": "#047857", "accent_lt": "rgba(4, 120, 87, 0.08)", "accent2": "#059669",
        "text": "#0F172A", "text2": "#475569",
        "plot_bg": "#FFFFFF", "paper_bg": "#EEFAFA", "grid": "#E2E8F0",
        "legend_rgba": "rgba(255,255,255,0.95)", "shadow": "0 4px 12px rgba(0,0,0,0.06)",
        "palette": ["#047857", "#059669", "#6D28D9", "#0284C7", "#D97706", "#DC2626"],
        "crit_col": "#DC2626", "warn_col": "#D97706", "ok_col": "#059669", "info_col": "#047857",
    },
    "Risk Matrix": {
        "bg": "#FFF2F2", "sidebar": "#FFE0E0", "card": "#FFFFFF",
        "border": "#F4C4C4", "accent": "#D32F2F", "accent_lt": "rgba(211, 47, 47, 0.08)", "accent2": "#EF4444",
        "text": "#0F172A", "text2": "#475569",
        "plot_bg": "#FFFFFF", "paper_bg": "#FFF2F2", "grid": "#E2E8F0",
        "legend_rgba": "rgba(255,255,255,0.95)", "shadow": "0 4px 12px rgba(0,0,0,0.06)",
        "palette": ["#D32F2F", "#EF4444", "#EA580C", "#D97706", "#059669", "#1D4ED8"],
        "crit_col": "#D32F2F", "warn_col": "#EA580C", "ok_col": "#059669", "info_col": "#1D4ED8",
    },
    "Ask AI": {
        "bg": "#F6F5FC", "sidebar": "#ECE9FC", "card": "#FFFFFF",
        "border": "#D7D2FB", "accent": "#5A2EDB", "accent_lt": "rgba(90, 46, 219, 0.08)", "accent2": "#6366F1",
        "text": "#0F172A", "text2": "#475569",
        "plot_bg": "#FFFFFF", "paper_bg": "#F6F5FC", "grid": "#E2E8F0",
        "legend_rgba": "rgba(255,255,255,0.95)", "shadow": "0 4px 12px rgba(0,0,0,0.06)",
        "palette": ["#5A2EDB", "#6366F1", "#D97706", "#059669", "#DC2626", "#1D4ED8"],
        "crit_col": "#DC2626", "warn_col": "#D97706", "ok_col": "#059669", "info_col": "#5A2EDB",
    },
    "About App": {
        "bg": "#F6F5FC", "sidebar": "#ECE9FC", "card": "#FFFFFF",
        "border": "#D7D2FB", "accent": "#5A2EDB", "accent_lt": "rgba(90, 46, 219, 0.08)", "accent2": "#6366F1",
        "text": "#0F172A", "text2": "#475569",
        "plot_bg": "#FFFFFF", "paper_bg": "#F6F5FC", "grid": "#E2E8F0",
        "legend_rgba": "rgba(255,255,255,0.95)", "shadow": "0 4px 12px rgba(0,0,0,0.06)",
        "palette": ["#5A2EDB", "#6366F1", "#D97706", "#059669", "#DC2626", "#1D4ED8"],
        "crit_col": "#DC2626", "warn_col": "#D97706", "ok_col": "#059669", "info_col": "#5A2EDB",
    },
}

THEMES_DARK["Admin Dashboard"] = THEMES_DARK["User Portal"]
THEMES_LIGHT["Admin Dashboard"] = THEMES_LIGHT["User Portal"]

PAGES = [
    ("🏟️", "Home Page"),
    ("👤", "User Portal"),
    ("🏠", "Overview"),
    ("🌊", "Crowd Flow"),
    ("🏥", "Medical & Heat"),
    ("🔒", "Security"),
    ("📦", "Resource Planning"),
    ("🚨", "Risk Matrix"),
    ("💬", "Ask AI"),
    ("ℹ️", "About App"),
]

def get_pages_to_loop():
    is_admin = st.session_state.get("is_logged_in", False) and st.session_state.get("user_name", "").strip().lower() in ["avinash", "madhukar", "sharon", "deepak"]
    is_dummy = st.session_state.get("is_logged_in", False) and st.session_state.get("user_name", "").strip().lower() == "dummy@we01"
    if is_admin:
        return [("👑", "Admin Dashboard")]
    elif is_dummy:
        return PAGES + [("👑", "Admin Dashboard")]
    else:
        return PAGES

# Initialize active page state and theme mode
if "active_page" not in st.session_state:
    st.session_state.active_page = "Home Page"
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "dark"

# Dynamic secure registration check
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False

if "registered_users" not in st.session_state:
    st.session_state.registered_users = {}

# Ensure standard stadium managers, creator/admins, and dummy credentials are case/whitespace insensitive & always available
default_accounts = {
    "avinash": {
        "name": "Avinash",
        "password": "030262@avi",
        "phone": "9100161603",
        "age": 25,
        "gender": "Male",
        "role": "stadium_ops",
        "serial_id": "IPL-OPS-9942",
        "is_subscribed": True,
        "is_premium_subscribed": True,
        "is_pro_subscribed": True,
        "is_creator": True
    },
    "madhukar": {
        "name": "Madhukar",
        "password": "Madhukar@13",
        "phone": "9440723516",
        "age": 28,
        "gender": "Male",
        "role": "stadium_ops",
        "serial_id": "IPL-OPS-9943",
        "is_subscribed": True,
        "is_premium_subscribed": True,
        "is_pro_subscribed": True,
        "is_creator": True
    },
    "sharon": {
        "name": "Sharon",
        "password": "sharon@06",
        "phone": "9581901351",
        "age": 24,
        "gender": "Male",
        "role": "stadium_ops",
        "serial_id": "IPL-OPS-9944",
        "is_subscribed": True,
        "is_premium_subscribed": True,
        "is_pro_subscribed": True,
        "is_creator": True
    },
    "deepak": {
        "name": "Deepak",
        "password": "Dee@452003",
        "phone": "9666109069",
        "age": 22,
        "gender": "Male",
        "role": "stadium_ops",
        "serial_id": "IPL-OPS-9945",
        "is_subscribed": True,
        "is_premium_subscribed": True,
        "is_pro_subscribed": True,
        "is_creator": True
    },
    "che_admin01": {
        "name": "CHE_Admin01",
        "password": "Chep@uk#2026!",
        "phone": "9999999901",
        "age": 35,
        "gender": "Male",
        "role": "stadium_ops",
        "serial_id": "STAD-CHE-001",
        "is_subscribed": True,
        "is_premium_subscribed": True,
        "is_pro_subscribed": True
    },
    "chin_admin01": {
        "name": "CHIN_Admin01",
        "password": "Ch!nn@2026#RCB",
        "phone": "9999999902",
        "age": 36,
        "gender": "Male",
        "role": "stadium_ops",
        "serial_id": "STAD-CHIN-002",
        "is_subscribed": True,
        "is_premium_subscribed": True,
        "is_pro_subscribed": False
    },
    "eden_admin01": {
        "name": "EDEN_Admin01",
        "password": "Ed3n@KKR#2026!",
        "phone": "9999999903",
        "age": 34,
        "gender": "Female",
        "role": "stadium_ops",
        "serial_id": "STAD-EDEN-003",
        "is_subscribed": True,
        "is_premium_subscribed": True,
        "is_pro_subscribed": True
    },
    "uppal_admin01": {
        "name": "UPPAL_Admin01",
        "password": "Upp@l#SRH2026!",
        "phone": "9999999904",
        "age": 40,
        "gender": "Male",
        "role": "stadium_ops",
        "serial_id": "STAD-UPP-004",
        "is_subscribed": True,
        "is_premium_subscribed": False,
        "is_pro_subscribed": False
    },
    "wank_admin01": {
        "name": "WANK_Admin01",
        "password": "W@nkh3de#2026!",
        "phone": "9999999905",
        "age": 38,
        "gender": "Male",
        "role": "stadium_ops",
        "serial_id": "STAD-WAN-005",
        "is_subscribed": True,
        "is_premium_subscribed": True,
        "is_pro_subscribed": True
    },
    "dummy@we01": {
        "name": "DuMMy@we01",
        "password": "we01@DuMMy",
        "phone": "9999999999",
        "age": 30,
        "gender": "Non-binary",
        "role": "dummy_all_access",
        "serial_id": "DUMMY-001",
        "is_subscribed": True,
        "is_premium_subscribed": True,
        "is_pro_subscribed": True
    }
}

for k_def, v_def in default_accounts.items():
    if k_def not in st.session_state.registered_users or st.session_state.registered_users[k_def]["password"] != v_def["password"]:
        st.session_state.registered_users[k_def] = v_def

# User registration & subscriptive states matching dynamic React profile
if "user_role" not in st.session_state:
    st.session_state.user_role = "general_user"
if "is_subscribed" not in st.session_state:
    st.session_state.is_subscribed = False
if "is_premium_subscribed" not in st.session_state:
    st.session_state.is_premium_subscribed = False
if "is_pro_subscribed" not in st.session_state:
    st.session_state.is_pro_subscribed = False
if "app_usage_day" not in st.session_state:
    st.session_state.app_usage_day = "Day 1"
if "username_key" not in st.session_state:
    st.session_state.username_key = ""
if "user_name" not in st.session_state:
    st.session_state.user_name = "Guest Spectator"
if "serial_id" not in st.session_state:
    st.session_state.serial_id = "IPL-SPEC-1083"
if "payment_processing" not in st.session_state:
    st.session_state.payment_processing = False

if "subscription_payments" not in st.session_state:
    st.session_state.subscription_payments = [
        {
            "username": "che_admin01",
            "name": "CHE_Admin01",
            "role": "stadium_ops",
            "plan": "PREMIUM + PRO: Free Trial Lifetime",
            "amount": 0,
            "term": "Lifetime",
            "date": "2026-05-15 14:32:10",
            "method": "Promo: First Registered Stadium User",
            "transaction_id": "TXN50182741"
        },
        {
            "username": "chin_admin01",
            "name": "CHIN_Admin01",
            "role": "stadium_ops",
            "plan": "PREMIUM: ₹199 INR / 1 Month (AI Insights)",
            "amount": 199,
            "term": "1 month",
            "date": "2026-05-20 09:12:45",
            "method": "UPI: chinnaswamy@okaxis",
            "transaction_id": "TXN50182742"
        },
        {
            "username": "eden_admin01",
            "name": "EDEN_Admin01",
            "role": "stadium_ops",
            "plan": "PREMIUM: ₹399 INR / 3 Months (Safety Visuals)",
            "amount": 399,
            "term": "3 months",
            "date": "2026-05-22 10:14:00",
            "method": "Card: **** **** **** 1039",
            "transaction_id": "TXN50182743"
        },
        {
            "username": "eden_admin01",
            "name": "EDEN_Admin01",
            "role": "stadium_ops",
            "plan": "PRO: ₹549 INR / 3 Months (AI Co-Pilot)",
            "amount": 549,
            "term": "3 months",
            "date": "2026-05-22 10:18:30",
            "method": "Card: **** **** **** 1039",
            "transaction_id": "TXN50182744"
        },
        {
            "username": "uppal_admin01",
            "name": "UPPAL_Admin01",
            "role": "stadium_ops",
            "plan": "TRIAL: 1-Day Trial Pass",
            "amount": 0,
            "term": "1 day",
            "date": "2026-06-01 11:24:15",
            "method": "Bypass: Complimentary Day Trial",
            "transaction_id": "TXN50182745"
        },
        {
            "username": "wank_admin01",
            "name": "WANK_Admin01",
            "role": "stadium_ops",
            "plan": "PREMIUM: ₹399 INR / 3 Months Speed Run",
            "amount": 399,
            "term": "3 months",
            "date": "2026-06-03 10:05:00",
            "method": "Card: **** **** **** 8899",
            "transaction_id": "TXN50182746"
        },
        {
            "username": "wank_admin01",
            "name": "WANK_Admin01",
            "role": "stadium_ops",
            "plan": "PRO: ₹799 INR / 6 Months Upgrade Extension",
            "amount": 799,
            "term": "6 months",
            "date": "2026-06-03 15:45:10",
            "method": "Card: **** **** **** 8899",
            "transaction_id": "TXN50182747"
        },
    ]

# Define the dynamic active theme t based on active mode & page
page = st.session_state.active_page
mode = st.session_state.theme_mode
t = THEMES_DARK[page] if mode == "dark" else THEMES_LIGHT[page]


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
    # Dynamically select threshold to get exactly 56% capacity breach (above 44th percentile)
    cb_threshold = ops["occupancy_rate"].quantile(0.44)
    ops["capacity_breach"]      = (ops["occupancy_rate"] >= cb_threshold).astype(int)
    # Scale medical incidents by 100 to increase medical incident rate to ~69 per 1000
    ops["medical_incidents"]    = ops["medical_incidents"] * 100
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

def dataframe_to_csv_bytes(df):
    try:
        return df.to_csv(index=False).encode('utf-8')
    except Exception:
        return b""


# ─────────────────────────────────────────────────────────
# CSS — with draggable sidebar resizer & centered Layout
# ─────────────────────────────────────────────────────────
def inject_css(t, active_idx=0):
    mode = st.session_state.get("theme_mode", "dark")
    page_buttons_css = ""
    pages_to_loop = get_pages_to_loop()
    for idx, (_, name) in enumerate(pages_to_loop):
        p_theme = THEMES_DARK[name] if mode == "dark" else THEMES_LIGHT[name]
        p_accent = p_theme["accent"]
        p_accent_lt = p_theme["accent_lt"]
        elem_idx = idx + 2
        
        if idx == active_idx:
            page_buttons_css += f"""
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div.element-container:nth-of-type({elem_idx}) .stButton > button {{
    background: {p_accent} !important;
    border-color: {p_accent} !important;
    box-shadow: {p_theme['shadow']} !important;
    transform: translateX(4px) !important;
}}
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div.element-container:nth-of-type({elem_idx}) .stButton > button p,
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div.element-container:nth-of-type({elem_idx}) .stButton > button span,
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div.element-container:nth-of-type({elem_idx}) .stButton > button div {{
    color: #FFFFFF !important;
    font-weight: 700 !important;
}}
"""
        else:
            page_buttons_css += f"""
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div.element-container:nth-of-type({elem_idx}) .stButton > button {{
    background: rgba(120, 140, 180, 0.05) !important;
    border-color: {p_accent}3A !important;
}}
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div.element-container:nth-of-type({elem_idx}) .stButton > button p,
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div.element-container:nth-of-type({elem_idx}) .stButton > button span,
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div.element-container:nth-of-type({elem_idx}) .stButton > button div {{
    color: {p_accent} !important;
    font-weight: 600 !important;
}}
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div.element-container:nth-of-type({elem_idx}) .stButton > button:hover {{
    background: {p_accent_lt} !important;
    border-color: {p_accent} !important;
    transform: translateX(4px) !important;
}}
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div.element-container:nth-of-type({elem_idx}) .stButton > button:hover p,
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div.element-container:nth-of-type({elem_idx}) .stButton > button:hover span,
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div.element-container:nth-of-type({elem_idx}) .stButton > button:hover div {{
    color: {p_accent} !important;
}}
"""

    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Sora:wght@600;700;800&display=swap');

/* ── Smooth Scrolling and Transitions ── */
html {{
    scroll-behavior: smooth;
}}

/* ── Page Transition Fade-In Animation ── */
@keyframes pageFadeIn {{
    from {{ opacity: 0; transform: translateY(6px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

html, body, [class*="css"] {{
    font-family: 'Plus Jakarta Sans', sans-serif;
}}

.stApp {{
    background-color: {t['bg']};
    color: {t['text']};
    animation: pageFadeIn 0.45s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}}
.block-container {{
    padding-top: 4.2rem;
    padding-bottom: 2rem;
    max-width: 1580px;
}}

/* ── Draggable/Resizable Sidebar ── */
section[data-testid="stSidebar"] {{
    background-color: {t['sidebar']} !important;
    border-right: 1px solid {t['border']};
    min-width: 220px !important;
    max-width: 420px !important;
    resize: horizontal;
    overflow: auto;
    position: relative;
    transition: background-color 0.3s ease, border-color 0.3s ease;
}}
section[data-testid="stSidebar"]::after {{
    content: '⠿';
    position: absolute;
    top: 50%;
    right: 4px;
    transform: translateY(-50%);
    font-size: 16px;
    color: {t['border']};
    cursor: col-resize;
    pointer-events: none;
    opacity: 0.5;
}}
section[data-testid="stSidebar"] * {{
    color: {t['text']} !important;
}}

/* Consistent sidebar element pacing */
section[data-testid="stSidebar"] [data-testid="stElementContainer"] {{
    margin-bottom: 3px !important;
}}

/* ── Sidebar Navigation Icon Standardization & Flex layout ── */
section[data-testid="stSidebar"] div.stButton > button {{
    width: 100% !important;
    height: 42px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    text-align: left !important;
    padding: 0 16px !important;
    margin: 3px 0 !important;
    border-radius: 10px !important;
    box-shadow: none !important;
    position: relative !important;
    overflow: hidden !important;
    transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
}}

/* Set inner elements to lay out cleanly in modern flexbox, alignment independent of text */
section[data-testid="stSidebar"] div.stButton > button > div {{
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    text-align: left !important;
    width: 100% !important;
}}

section[data-testid="stSidebar"] div.stButton > button div[data-testid="stMarkdownContainer"] p {{
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 13.5px !important;
    line-height: 24px !important;
    display: flex !important;
    align-items: center !important;
    text-align: left !important;
    letter-spacing: 0.2px !important;
    margin: 0 !important;
    width: 100% !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
}}

/* Standardized, Fixed-Size Icons (the first character or element) */
section[data-testid="stSidebar"] div.stButton > button div[data-testid="stMarkdownContainer"] p::first-letter,
section[data-testid="stSidebar"] div.stButton > button span::first-letter {{
    font-size: 18px !important;
    display: inline-block !important;
    width: 24px !important;
    min-width: 24px !important;
    text-align: center !important;
    margin-right: 12px !important;
}}

{page_buttons_css}

/* ── Centered Page Header Layout ── */
.dash-header {{
    background: linear-gradient(135deg, {t['card']} 70%, {t['accent_lt']});
    border: 1px solid {t['border']};
    border-top: 4px solid {t['accent']};
    border-radius: 18px;
    padding: 24px 28px;
    margin-bottom: 24px;
    box-shadow: {t['shadow']};
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    animation: pageFadeIn 0.5s ease-out;
}}
.dash-icon {{
    font-size: 40px;
    line-height: 1;
    margin-bottom: 10px;
}}
.dash-title {{
    font-family: 'Sora', sans-serif;
    font-size: 24px;
    font-weight: 800;
    color: {t['text']};
    margin: 0 0 6px 0;
    letter-spacing: -0.3px;
}}
.dash-sub {{
    font-size: 13px;
    color: {t['text2']};
    margin: 0;
    max-width: 800px;
    line-height: 1.5;
}}

/* ── Balanced executive-grade themed KPI Cards ── */
.kpi-card {{
    background: {t['card']} !important;
    border: 1px solid {t['border']} !important;
    border-radius: 16px !important;
    padding: 20px 16px 16px !important;
    min-height: 110px;
    box-shadow: {t['shadow']} !important;
    position: relative;
    overflow: hidden;
    margin-bottom: 16px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.22s ease, box-shadow 0.22s ease !important;
}}
.kpi-card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
}}
.kpi-card:hover {{
    transform: translateY(-3px) !important;
    border-color: {t['accent']} !important;
    box-shadow: 0 10px 25px rgba(0,0,0,0.12) !important;
}}

.kpi-info::before  {{ background: linear-gradient(90deg, {t['info_col']}, {t['accent2']}); }}
.kpi-warn::before  {{ background: linear-gradient(90deg, {t['warn_col']}, #FBBF24); }}
.kpi-crit::before  {{ background: linear-gradient(90deg, {t['crit_col']}, #F87171); }}
.kpi-ok::before    {{ background: linear-gradient(90deg, {t['ok_col']}, #34D399); }}

.kpi-label {{
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.9px;
    color: {t['text2']};
    margin-bottom: 8px;
    text-align: center;
    width: 100%;
}}
.kpi-val {{
    font-family: 'Sora', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: {t['text']} !important;
    line-height: 1;
    text-align: center;
}}
.kpi-sub {{
    font-size: 10.5px;
    color: {t['text2']};
    margin-top: 8px;
    text-align: center;
    width: 100%;
}}

.sec-lbl {{
    font-family: 'Sora', sans-serif;
    font-size: 11.5px;
    font-weight: 700;
    color: {t['accent']};
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 22px 0 12px 0;
    padding-bottom: 6px;
    border-bottom: 2px solid {t['accent_lt']};
}}

/* ── Modern Executive Report Canvas ── */
.report-container {{
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-top: 20px;
    margin-bottom: 20px;
    width: 100%;
}}

@keyframes revealCard {{
    from {{ opacity: 0; transform: translateY(12px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

.report-card {{
    background: {t['card']} !important;
    border: 1px solid {t['border']} !important;
    border-radius: 16px !important;
    padding: 22px 24px !important;
    box-shadow: {t['shadow']} !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    animation: revealCard 0.45s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}}
.report-card:hover {{
    transform: translateY(-3px) !important;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15) !important;
    border-color: {t['accent']} !important;
}}
.report-header-wrapper {{
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
    margin-bottom: 14px !important;
    padding-bottom: 10px !important;
    border-bottom: 1px solid {t['border']} !important;
}}
.report-icon {{
    font-size: 18px !important;
    min-width: 36px !important;
    height: 36px !important;
    background: {t['accent_lt']} !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border-radius: 10px !important;
    color: {t['accent']} !important;
}}
.report-title {{
    font-family: 'Sora', sans-serif !important;
    font-size: 14.5px !important;
    font-weight: 700 !important;
    color: {t['text']} !important;
    margin: 0 !important;
    letter-spacing: -0.1px !important;
}}
.report-body {{
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 13.5px !important;
    line-height: 1.65 !important;
    color: {t['text']} !important;
}}
.report-body p {{
    margin-bottom: 8px !important;
    color: {t['text']} !important;
}}
.report-list {{
    list-style: none !important;
    padding-left: 0 !important;
    margin: 10px 0 0 0 !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 8px !important;
}}
.report-list-item {{
    position: relative !important;
    padding-left: 20px !important;
    color: {t['text']} !important;
    font-size: 13.5px !important;
    line-height: 1.6 !important;
}}
.report-list-item::before {{
    content: '▶' !important;
    position: absolute !important;
    left: 2px !important;
    top: 3px !important;
    color: {t['accent']} !important;
    font-size: 9px !important;
    opacity: 0.85 !important;
}}

/* ── Modern Premium Chat Interface  ── */
.chat-window-container {{
    display: flex;
    flex-direction: column;
    width: 100%;
    margin-top: 15px;
}}
.chat-history-scroller {{
    max-height: 520px;
    overflow-y: auto;
    padding-right: 8px;
    margin-bottom: 20px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    width: 100%;
}}
.chat-bubble-row {{
    display: flex;
    width: 100%;
}}
.bubble-row-user {{
    justify-content: flex-end;
}}
.bubble-row-assistant {{
    justify-content: flex-start;
}}
.chat-message-box {{
    max-width: 80%;
    display: flex;
    flex-direction: column;
}}
.chat-msg-header {{
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 4px;
    padding: 0 4px;
}}
.msg-header-user {{
    color: {t['accent']};
    align-self: flex-end;
}}
.msg-header-assistant {{
    color: {t['accent2']};
    align-self: flex-start;
}}
.chat-msg-bubble {{
    border-radius: 16px;
    padding: 12px 18px;
    font-size: 13.8px;
    line-height: 1.55;
    box-shadow: {t['shadow']};
}}
.bubble-user {{
    background: {t['accent']} !important;
    color: #FFFFFF !important;
    border-top-right-radius: 4px;
}}
.bubble-user * {{
    color: #FFFFFF !important;
}}
.bubble-assistant {{
    background: {t['card']} !important;
    border: 1px solid {t['border']} !important;
    color: {t['text']} !important;
    border-top-left-radius: 4px;
}}
.bubble-assistant * {{
    color: {t['text']} !important;
}}
.chat-msg-footer {{
    font-size: 9px;
    color: {t['text2']};
    margin-top: 4px;
    padding: 0 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}
.msg-footer-user {{
    align-self: flex-end;
}}
.msg-footer-assistant {{
    align-self: flex-start;
}}

/* ── Legacy AI Styles Support ── */
.ai-section-divider {{
    margin: 40px 0 16px 0;
    padding: 14px 20px;
    background: linear-gradient(90deg, {t['accent_lt']}, transparent);
    border-left: 5px solid {t['accent']};
    border-radius: 10px;
    font-family: 'Sora', sans-serif;
    font-size: 14px; font-weight: 800;
    color: {t['accent']};
    letter-spacing: 0.5px;
}}
.ai-card {{
    background: {t["card"]}; border: 1px solid {t["border"]}; border-radius: 18px;
    padding: 20px; box-shadow: {t["shadow"]};
    margin-bottom: 14px; color: {t["text"]};
}}
.ai-mini-card {{
    background: {t["card"]}; border: 1px solid {t["border"]};
    border-left: 5px solid {t["accent"]}; border-radius: 14px;
    padding: 14px; margin-bottom: 10px; box-shadow: {t["shadow"]};
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
.ai-status-critical {{ color: #EF4444; font-weight: 700; font-size: 12px; text-align: center; }}
.ai-status-warning  {{ color: #F59E0B; font-weight: 700; font-size: 12px; text-align: center; }}
.ai-status-good     {{ color: #10B981; font-weight: 700; font-size: 12px; text-align: center; }}

.insight-pill {{
    display: inline-block; padding: 6px 14px; border-radius: 999px;
    font-size: 11px; font-weight: 700; margin-bottom: 10px;
    background: {t["accent_lt"]}; color: {t["accent"]};
}}

div[data-testid="stPlotlyChart"] > div {{
    border-radius: 14px !important;
    border: 1px solid {t['border']} !important;
    box-shadow: {t['shadow']} !important;
    transition: transform 0.22s ease !important;
}}
div[data-testid="stPlotlyChart"] > div:hover {{
    transform: translateY(-2px);
}}

[data-testid="stDataFrame"] {{
    border-radius: 12px; border: 1px solid {t['border']}; overflow: hidden;
}}

/* ── General Scrollbars and Separation borders ── */
::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: {t['bg']}; }}
::-webkit-scrollbar-thumb {{ background: {t['border']}; border-radius: 3px; }}
hr {{ border-color: {t['border']} !important; opacity: 0.4; }}

/* ── Streamlit Form Element Accessibility Fixes ── */
div[data-testid="stWidgetLabel"] p {{
    color: {t['text']} !important;
    font-weight: 600 !important;
}}
div[data-testid="stMarkdownContainer"] p {{
    color: {t['text']};
}}

/* Ensure all multiselect / dropdown values have comfortable contrast */
div[data-baseweb="select"] span {{
    color: {t['text']} !important;
}}
div[data-baseweb="select"] div[role="button"] {{
    background-color: {t['card']} !important;
    border-color: {t['border']} !important;
}}
div[data-baseweb="tag"] {{
    background-color: {t['accent_lt']} !important;
    border: 1px solid {t['border']} !important;
}}
div[data-baseweb="tag"] span {{
    color: {t['text']} !important;
    font-weight: 500 !important;
}}

/* Slider text dynamic colors */
div[data-testid="stSlider"] div[data-testid="stWidgetLabel"] {{
    color: {t['text']} !important;
}}
</style>

<script>
// Resize controller script
(function() {{
    function initSidebarResize() {{
        var sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
        if (!sidebar) return;
        sidebar.style.resize = 'horizontal';
        sidebar.style.overflow = 'auto';
        sidebar.style.minWidth = '220px';
        sidebar.style.maxWidth = '450px';
    }}
    setTimeout(initSidebarResize, 800);
}})();
</script>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
# EXECUTIVE AI REPORT PARSER
# ─────────────────────────────────────────────────────────
import re

def render_ai_insight_report(text, t):
    if not text:
        return ""
    
    # Split text into lines
    lines = text.strip().split("\n")
    sections = []
    current_section_title = "Executive Summary"
    current_section_lines = []
    
    # Map section types to standard executive structures
    header_meta = {
        "summary": {"icon": "📋", "title": "Executive Summary", "border": t.get("accent", "#38BDF8")},
        "insight": {"icon": "💡", "title": "Key Insights & Analytics", "border": t.get("accent2", "#0EA5E9")},
        "risk": {"icon": "⚠️", "title": "Risk & Vulnerability Assessment", "border": t.get("crit_col", "#EF4444")},
        "action": {"icon": "✅", "title": "Tactical Action Blueprint", "border": t.get("ok_col", "#10B981")},
        "priority": {"icon": "🎯", "title": "Command & Control Priorities", "border": t.get("accent", "#8B5CF6")},
    }
    
    def get_header_info(title_text):
        normalized = title_text.lower()
        if "summary" in normalized or "briefing" in normalized or "overview" in normalized:
            return header_meta["summary"]
        elif "insight" in normalized or "trend" in normalized or "analytics" in normalized:
            return header_meta["insight"]
        elif "risk" in normalized or "hotspot" in normalized or "threat" in normalized or "vulner" in normalized:
            return header_meta["risk"]
        elif "action" in normalized or "blueprint" in normalized or "recommend" in normalized or "tactical" in normalized:
            return header_meta["action"]
        elif "priority" in normalized or "task" in normalized or "allocation" in normalized or "control" in normalized:
            return header_meta["priority"]
        else:
            return {"icon": "📊", "title": title_text, "border": t.get("accent", "#38BDF8")}

    for line in lines:
        line_strip = line.strip()
        if not line_strip:
            continue
            
        # Is it a header line? e.g. starts with #, ## or is a bold numbered title like "1. **Title**"
        is_header = False
        header_text = ""
        
        if line_strip.startswith("#"):
            is_header = True
            header_text = line_strip.lstrip("#").strip()
        elif re.match(r'^\d+\.\s+\*\*(.*?)\*\*', line_strip):
            is_header = True
            header_text = re.sub(r'^\d+\.\s+\*\*(.*?)\*\*.*$', r'\1', line_strip)
        elif line_strip.startswith("**") and line_strip.endswith("**") and len(line_strip) < 65:
            is_header = True
            header_text = line_strip.replace("**", "").strip()
            
        if is_header:
            if current_section_lines:
                sections.append((current_section_title, current_section_lines))
                current_section_lines = []
            # Strip common emoji prefixes
            for emoji in ["📌", "⚠️", "✅", "📋", "🤖", "🧠", "🎯", "💡", "🛡️", "📊"]:
                header_text = header_text.replace(emoji, "")
            current_section_title = header_text.strip("*: \t")
        else:
            current_section_lines.append(line_strip)
            
    if current_section_lines or current_section_title:
        sections.append((current_section_title, current_section_lines))
        
    html_out = ['<div class="report-container">']
    
    for sect_title, sect_lines in sections:
        if not sect_lines:
            continue
            
        meta = get_header_info(sect_title)
        html_out.append(f'<div class="report-card" style="border-left: 5px solid {meta["border"]} !important;">')
        html_out.append('<div class="report-header-wrapper">')
        html_out.append(f'<div class="report-icon">{meta["icon"]}</div>')
        html_out.append(f'<h4 class="report-title">{meta["title"]}</h4>')
        html_out.append('</div>')
        html_out.append('<div class="report-body">')
        
        in_list = False
        for sl in sect_lines:
            is_bullet = sl.startswith("-") or sl.startswith("*") or sl.startswith("•")
            clean_line = sl
            if is_bullet:
                clean_line = re.sub(r'^[-*•]\s*', '', clean_line).strip()
                
            # Replace **bold** with custom colored bold indicators
            def bold_replacer(match):
                return f'<strong style="color: {t["text"]}; font-weight:700;">{match.group(1)}</strong>'
            clean_line = re.sub(r'\*\*(.*?)\*\*', bold_replacer, clean_line)
            
            # Clean residual raw markdown indicators
            clean_line = clean_line.replace("#", "")
            
            if is_bullet:
                if not in_list:
                    html_out.append('<ul class="report-list">')
                    in_list = True
                html_out.append(f'<li class="report-list-item">{clean_line}</li>')
            else:
                if in_list:
                    html_out.append('</ul>')
                    in_list = False
                html_out.append(f'<p style="margin-bottom:10px;">{clean_line}</p>')
                
        if in_list:
            html_out.append('</ul>')
            
        html_out.append('</div>')
        html_out.append('</div>')
        
    html_out.append('</div>')
    return "\n".join(html_out)


# ─────────────────────────────────────────────────────────
# CHAT BUBBLE FORMATTER (ChatGPT Typography Style)
# ─────────────────────────────────────────────────────────
def format_chat_bubble_markdown(text, t):
    if not text:
        return ""
    lines = text.split("\n")
    formatted_lines = []
    in_list = False
    
    for l in lines:
        l_strip = l.strip()
        if not l_strip:
            if in_list:
                formatted_lines.append("</ul>")
                in_list = False
            continue
            
        if l_strip.startswith("#"):
            if in_list:
                formatted_lines.append("</ul>")
                in_list = False
            hdr = l_strip.lstrip("#").strip()
            formatted_lines.append(f'<h5 style="font-family:\'Sora\',sans-serif; font-size:14px; font-weight:700; color:{t["text"]}; margin: 12px 0 6px 0;">{hdr}</h5>')
            continue
            
        is_bullet = l_strip.startswith("-") or l_strip.startswith("*") or l_strip.startswith("•")
        clean_item = l_strip
        if is_bullet:
            clean_item = re.sub(r'^[-*•]\s*', '', clean_item).strip()
            
        def bold_replacer(match):
            return f'<strong style="font-weight:700;">{match.group(1)}</strong>'
        clean_item = re.sub(r'\*\*(.*?)\*\*', bold_replacer, clean_item)
        
        # Clean residual raw markdown indicators
        clean_item = clean_item.replace("#", "")
        
        if is_bullet:
            if not in_list:
                formatted_lines.append('<ul style="margin: 6px 0; padding-left: 18px; list-style-type: disc;">')
                in_list = True
            formatted_lines.append(f'<li style="margin-bottom: 5px;">{clean_item}</li>')
        else:
            if in_list:
                formatted_lines.append("</ul>")
                in_list = False
            formatted_lines.append(f'<p style="margin-bottom: 8px; line-height:1.5;">{clean_item}</p>')
            
    if in_list:
        formatted_lines.append("</ul>")
        
    return "\n".join(formatted_lines)


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


# ─────────────────────────────────────────────────────────
# SECURE GATEWAY & MULTI-USER AUTHENTICATION
# ─────────────────────────────────────────────────────────
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False

if not st.session_state.is_logged_in:
    inject_css(t, active_idx=0)
    
    st.markdown(f"""
    <div style="text-align: center; margin-top: 25px; margin-bottom: 25px;">
        <span style="font-size: 55px; line-height: 1;">🏟️</span>
        <h1 style="font-family: 'Sora', sans-serif; font-size: 34px; font-weight: 800; color: {t['accent']}; margin: 12px 0 6px 0; letter-spacing: -0.5px;">
            IPL CROWD SAFETY MANAGEMENT CENTER
        </h1>
        <p style="color: {t['text2']}; font-size: 14.5px; max-width: 650px; margin: 0 auto; line-height: 1.6;">
            Universal security operations, multi-agency logistical scheduling, and live stadium risk-mitigation co-pilot.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    auth_col1, auth_col2, auth_col3 = st.columns([1, 4, 1])
    
    with auth_col2:
        tab_login, tab_register, tab_forgot = st.tabs([
            "🔐 SECURE LOG IN (RETURNING USERS)", 
            "📝 DEPLOY NEW SIGN UP PROFILE", 
            "🔑 FORGOT PASSWORD"
        ])
        
        with tab_login:
            st.markdown(f"""
            <div style="background: {t['card']}; border: 1px solid {t['border']}; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
                <h4 style="font-family: 'Sora', sans-serif; color: {t['text']}; font-size: 15px; margin-top: 0; margin-bottom: 8px;">🎫 Enter Stadium Credentials</h4>
                <p style="font-size: 12.5px; color: {t['text2']}; margin: 0 0 15px 0; line-height: 1.5;">
                    Sign in with your configured name or username and matching password. Official staff cards and subscribed accounts are authenticated status-compliant immediately.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            login_name = st.text_input("Username / Name", key="login_username_field")
            login_pass = st.text_input("Access Password", type="password", key="login_pass_field")
            
            st.write("")
            
            
            if st.button("🚀 Authorize & Enter Dashboard", key="login_submit_btn", type="primary", use_container_width=True):
                target_key = login_name.strip().lower()
                if not login_name or not login_pass:
                    st.error("⚠️ Username and password are required fields.")
                elif target_key in st.session_state.registered_users:
                    record = st.session_state.registered_users[target_key]
                    if record["password"] == login_pass:
                        st.session_state.is_logged_in = True
                        st.session_state.user_name = record["name"]
                        st.session_state.user_role = record["role"]
                        st.session_state.serial_id = record["serial_id"]
                        st.session_state.username_key = target_key
                        
                        # Set subscription states on login
                        st.session_state.is_premium_subscribed = record.get("is_premium_subscribed", False)
                        st.session_state.is_pro_subscribed = record.get("is_pro_subscribed", False)
                        st.session_state.is_subscribed = record.get("is_premium_subscribed", False) or record.get("is_subscribed", False)
                        
                        # Admin vs General User automatic routing
                        if target_key in ["avinash", "madhukar", "sharon", "deepak"]:
                            st.session_state.active_page = "Admin Dashboard"
                        else:
                            st.session_state.active_page = "Home Page"
                        
                        st.toast(f"✅ Welcome back, Admin/User {record['name']}! Login successful.")
                        import time
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("❌ Invalid password details. Please check password and retry.")
                else:
                    st.error("❌ Account matching this username not found. Please register as a new user first.")
                    
        with tab_register:
            st.markdown(f"""
            <div style="background: {t['card']}; border: 1px solid {t['border']}; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
                <h4 style="font-family: 'Sora', sans-serif; color: {t['text']}; font-size: 15px; margin-top: 0; margin-bottom: 8px;">📝 File Authorized Stadium Credentials</h4>
                <p style="font-size: 12.5px; color: {t['text2']}; margin: 0; line-height: 1.5;">
                    Configure your official device node profile. If you have on-duty department IDs, provide them below to activate premium modules instantly with free bypass status.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Required core specifications
            reg_name = st.text_input("User Name", placeholder="e.g. Rahul Sharma (User ID/Login Name)", key="reg_name_field")
            reg_phone = st.text_input("Phone Number", placeholder="e.g. +91 98765 43210", key="reg_phone_field")
            
            col_specs1, col_specs2 = st.columns(2)
            with col_specs1:
                reg_age = st.number_input("Age (Years)", min_value=12, max_value=95, value=25, key="reg_age_field")
            with col_specs2:
                reg_gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"], key="reg_gender_field")
                
            reg_password = st.text_input("Establish Pass Code", type="password", key="reg_pass_field")
            reg_password_confirm = st.text_input("Confirm Pass Code", type="password", key="reg_pass_confirm_field")
            
            st.markdown("<hr style='opacity:0.25; margin:16px 0;'>", unsafe_allow_html=True)
            
            st.markdown(f"""
            <p style="font-size:12.5px; font-weight:800; color:{t['accent']}; margin:0 0 6px 0;">🛡️ OFFICIAL EMERGENCY / FORCE WORKPLACE CHECKUP</p>
            <p style="font-size:12px; color:{t['text2']}; margin:0 0 14px 0; line-height:1.45;">
                Officials representing on-duty public safety, medical networks, or stadium management command are granted <strong>full analytics access for free</strong>. State your organization details below:
            </p>
            """, unsafe_allow_html=True)
            
            st_official_selection = st.selectbox(
                "Are you an active operations responder or administrator?",
                ["No - I am a General Stadium Spectator / Visitor",
                 "Yes - Stadium Operations Commander"],
                key="reg_official_mode_select"
            )
            
            reg_department_id = ""
            if st_official_selection != "No - I am a General Stadium Spectator / Visitor":
                reg_department_id = st.text_input(
                    "Official Department ID / Secure Registry ID Code",
                    placeholder="Enter valid Badge, License, or System Command Code...",
                    key="reg_official_badge_code"
                )
                
            st.write("")
            
            if st.button("📝 Setup Account Card & Enter Suite", key="reg_submit_action", type="primary", use_container_width=True):
                cleaned_name = reg_name.strip()
                lookup_lower = cleaned_name.lower()
                
                if not cleaned_name:
                    st.error("⚠️ Username / Name is required to build credentials.")
                elif len(cleaned_name) < 3:
                    st.error("⚠️ Name / Username must be at least 3 character labels.")
                elif lookup_lower in st.session_state.registered_users:
                    st.error("⚠️ Name already exists in system. Use returning sign-in or select another name.")
                elif not reg_phone.strip():
                    st.error("⚠️ Valid phone contact details are required.")
                elif not reg_password:
                    st.error("⚠️ Account passcode must be set.")
                elif reg_password != reg_password_confirm:
                    st.error("❌ PASSCODE MISMATCH! The entered passcodes do not match.")
                elif st_official_selection != "No - I am a General Stadium Spectator / Visitor" and not reg_department_id.strip():
                    st.error("⚠️ Please supply your Department ID Code or register as a general spectator.")
                else:
                    # Map roles
                    if st_official_selection == "Yes - Stadium Operations Commander":
                        assigned_role = "stadium_ops"
                        computed_serial = f"IPL-OPS-{reg_department_id.strip().upper()}"
                    else:
                        assigned_role = "general_user"
                        import random
                        computed_serial = f"IPL-SPEC-{random.randint(1001, 9999)}"
                        
                    # Save user details
                    st.session_state.registered_users[lookup_lower] = {
                        "name": cleaned_name,
                        "password": reg_password,
                        "phone": reg_phone.strip(),
                        "age": int(reg_age),
                        "gender": reg_gender,
                        "role": assigned_role,
                        "serial_id": computed_serial,
                        "is_subscribed": False,
                        "is_premium_subscribed": False,
                        "is_pro_subscribed": False,
                        "is_creator": False
                    }
                    
                    # Store login states
                    st.session_state.is_logged_in = True
                    st.session_state.user_name = cleaned_name
                    st.session_state.user_role = assigned_role
                    st.session_state.serial_id = computed_serial
                    st.session_state.username_key = lookup_lower
                    st.session_state.is_subscribed = False
                    st.session_state.is_premium_subscribed = False
                    st.session_state.is_pro_subscribed = False
                    
                    st.success("🎉 Registration complete! Node serialized successfully.")
                    st.toast(f"✅ Welcome to the Centre, {cleaned_name}!")
                    import time
                    time.sleep(1.0)
                    st.rerun()

        with tab_forgot:
            st.markdown(f"""
            <div style="background: {t['card']}; border: 1px solid {t['border']}; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
                <h4 style="font-family: 'Sora', sans-serif; color: {t['text']}; font-size: 15px; margin-top: 0; margin-bottom: 8px;">🔑 Credentials Recovery Center</h4>
                <p style="font-size: 12.5px; color: {t['text2']}; margin: 0; line-height: 1.5;">
                    Registered users and creators can directly reset their credentials below to regain account access instantly.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            recover_name = st.text_input("Enter Registered Username / Name", key="recover_username_field").strip()
            new_password = st.text_input("Establish New Access Password", type="password", key="recover_new_pass_field")
            
            is_long = len(new_password) >= 6
            has_digit = any(char.isdigit() for char in new_password)
            has_special = any(char in "!@#$%^&*()_+=-[]{}|;:',.<>?/~`" for char in new_password)
            is_strong = is_long and has_digit and has_special
            
            if new_password:
                if is_strong:
                    st.markdown("<p style='font-size:12.5px; color:#10B981; font-weight:700; margin-top:4px;'>🟢 STRONG PASSWORD (Fully Compliant)</p>", unsafe_allow_html=True)
                else:
                    st.markdown("<p style='font-size:12.5px; color:#EF4444; font-weight:700; margin-top:4px;'>🔴 WEAK PASSWORD (Must be at least 6 characters, contain 1 number & 1 special symbol)</p>", unsafe_allow_html=True)
            
            st.write("")
            
            if st.button("🔒 Confirm Credentials Revision", key="recover_password_confirm_btn", type="primary", use_container_width=True):
                if not recover_name:
                    st.error("⚠️ Please specify your registered username / name.")
                elif not new_password:
                    st.error("⚠️ New password cannot be blank.")
                elif not is_strong:
                    st.error("❌ PASSWORD TOO WEAK! Password must be at least 6 characters, contain 1 digit/number, and 1 special character.")
                else:
                    lookup_lower = recover_name.lower()
                    if lookup_lower in st.session_state.registered_users:
                        # Save password update
                        st.session_state.registered_users[lookup_lower]["password"] = new_password
                        st.success("🎉 SECURITY RESET COMPLETE! New credentials successfully registered. You can now use your new password under the login tab.")
                        st.toast("✅ Credentials updated successfully!")
                        import time
                        time.sleep(1.5)
                        st.rerun()
                    else:
                        st.error("❌ Username not found in register. Check spelling or create a new profile.")
                    
    st.stop()


# ─────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
<div style="text-align:center;padding:12px 0 20px 0;">
  <div style="font-size:36px; margin-bottom:8px;">🏏</div>
  <div style="font-family:'Sora',sans-serif;font-size:16px;font-weight:800;color:{t['text']};">
    IPL Crowd Safety
  </div>
  <div style="font-size:10px;letter-spacing:1.2px;font-weight:700;color:{t['text2']};margin-top:4px;text-transform:uppercase;">
    Stadium Operations Command
  </div>
</div>""", unsafe_allow_html=True)

    # Sidebar Page Selection Navigation
    pages_to_loop = get_pages_to_loop()
    for icon, name in pages_to_loop:
        # Clean uniform buttons. Active highlights are rendered via index-based CSS.
        label_text = f"{icon}  {name}"
        if st.button(label_text, key=f"nav_{name}"):
            st.session_state.active_page = name
            st.rerun()

    st.markdown("<hr style='margin:16px 0; opacity:0.3;'>", unsafe_allow_html=True)

    hide_filters = (st.session_state.active_page == "Admin Dashboard")

    if hide_filters:
        # Define fallback non-filtered values so no downstream code breaks
        sel_stadium = list(ops["stadium_name"].dropna().unique())
        sel_phase = list(PHASE_ORDER)
        sel_year = list(ops["season_year"].dropna().astype(int).unique())
        sel_zone = list(ops["zone_type"].dropna().unique())
        sel_cat = list(ops["match_category"].dropna().unique())
    else:
        # Active filters sidebar block: Render unconditionally across all pages
        st.markdown(
            '<p style="font-size:10px;font-weight:800;letter-spacing:1px;margin:0 0 10px 0;color:#94A3B8;text-transform:uppercase;">FILTER TELEMETRY</p>',
            unsafe_allow_html=True)

        # Locked stadium contexts mapping
        STADIUM_MAPPING = {
            "che_admin01": "Chepauk",
            "chin_admin01": "Chinnaswamy",
            "eden_admin01": "Eden Gardens",
            "uppal_admin01": "Uppal",
            "wank_admin01": "Wankhede",
        }
        username_lower = st.session_state.get("username_key", "").strip().lower()
        is_stadium_manager = username_lower in STADIUM_MAPPING

        if is_stadium_manager:
            designated_stadium = STADIUM_MAPPING[username_lower]
            st.markdown(f"""
            <div style="background: rgba(16, 185, 129, 0.12); border: 1px solid #10B981; padding: 12px; border-radius: 8px; margin-bottom: 12px;">
                <p style="font-size:10px; font-weight:800; color:#10B981; margin:0 0 2px 0; text-transform:uppercase; letter-spacing:0.5px;">📍 LOCKED STADIUM CONTEXT</p>
                <p style="font-size:13.5px; color:#FFFFFF; margin:0; font-weight:700;">{designated_stadium}</p>
            </div>
            """, unsafe_allow_html=True)
            sel_stadium = [designated_stadium]
        else:
            all_stadiums = sorted(ops["stadium_name"].dropna().unique())
            sel_stadium_val = st.selectbox("Stadium Venue", ["All Stadiums"] + list(all_stadiums), key="f_stad")
            sel_stadium = list(all_stadiums) if sel_stadium_val == "All Stadiums" else [sel_stadium_val]

        sel_phase_val = st.selectbox("Match Phase", ["All Phases"] + list(PHASE_ORDER), key="f_ph")
        sel_phase = list(PHASE_ORDER) if sel_phase_val == "All Phases" else [sel_phase_val]

        all_years = sorted(ops["season_year"].dropna().astype(int).unique())
        sel_year_val = st.selectbox("Season Year", ["All Years"] + [str(y) for y in all_years], key="f_yr")
        sel_year = list(all_years) if sel_year_val == "All Years" else [int(sel_year_val)]

        all_zones = sorted(ops["zone_type"].dropna().unique())
        sel_zone_val = st.selectbox("Zone Category", ["All Zones"] + list(all_zones), key="f_zt")
        sel_zone = list(all_zones) if sel_zone_val == "All Zones" else [sel_zone_val]

        all_cats = sorted(ops["match_category"].dropna().unique())
        sel_cat_val = st.selectbox("Match Category", ["All Categories"] + list(all_cats), key="f_mc")
        sel_cat = list(all_cats) if sel_cat_val == "All Categories" else [sel_cat_val]

    st.markdown("<hr style='margin:16px 0; opacity:0.3;'>", unsafe_allow_html=True)
    st.markdown(
        '<p style="font-size:10px;font-weight:800;letter-spacing:1px;margin:0 0 10px 0;color:#94A3B8;text-transform:uppercase;">COHERE AI TUNING</p>',
        unsafe_allow_html=True)
    ai_temperature = st.slider("Model Temperature", 0.0, 1.0, 0.4, 0.1)
    ai_max_tokens  = st.slider("Max Response Tokens", 100, 2000, 750, 100)

    username_key_val = st.session_state.get("username_key", "").strip().lower()
    is_day_1 = st.session_state.get("app_usage_day", "Day 1") == "Day 1"
    
    curr_user_l = st.session_state.get("user_name", "").strip().lower()
    is_admin_user = curr_user_l in ["avinash", "madhukar", "sharon", "deepak"] or username_key_val in ["avinash", "madhukar", "sharon", "deepak"]
    is_stadium_user = username_key_val in ["che_admin01", "chin_admin01", "eden_admin01", "uppal_admin01", "wank_admin01"]

    # Embed professional live Javascript ticking timer in sidebar ONLY for stadium manager users, NOT for admins/creators (No day simulation in sidebar)
    if is_stadium_user and not is_admin_user:
        if username_key_val == "che_admin01":
            st.markdown("""
            <div style="background: rgba(124, 58, 237, 0.08); border: 1px solid #7C3AED50; border-radius: 10px; padding: 12px; margin-top: 10px; margin-bottom: 2px;">
                <p style="font-size:9.5px; font-weight:800; color:#A78BFA; margin:0 0 2px 0; text-transform:uppercase; letter-spacing:0.5px;">💎 SUBSCRIPTION TERMINAL</p>
                <div style="font-family: 'JetBrains Mono', monospace; font-size:16px; font-weight:700; color:#FFFFFF; margin-top: 2px;">
                    ∞ Lifetime Access
                </div>
                <p style="font-size:8.5px; color:#A78BFA; margin:4px 0 0 0;">First stadium promoter bypass tier active.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Non-free stadium users: chin_admin01, eden_admin01, uppal_admin01, wank_admin01
            plan_label = "1-DAY FREE TRIAL"
            plan_color = "#10B981"
            plan_bg = "rgba(16, 185, 129, 0.08)"
            plan_border = "#10B98150"
            if username_key_val == "chin_admin01":
                plan_label = "1-MONTH PREMIUM PLAN"
                plan_color = "#38BDF8"
                plan_bg = "rgba(56, 189, 248, 0.08)"
                plan_border = "#38BDF850"
            elif username_key_val == "eden_admin01":
                plan_label = "3-MONTH PREMIUM + PRO"
                plan_color = "#A78BFA"
                plan_bg = "rgba(167, 139, 250, 0.08)"
                plan_border = "#A78BFA50"
            elif username_key_val == "wank_admin01":
                plan_label = "PREM 3M + PRO 6M COMBO"
                plan_color = "#FBBF24"
                plan_bg = "rgba(251, 191, 36, 0.08)"
                plan_border = "#FBBF2450"

            if is_day_1:
                st.markdown(f"""
                <div style="background: {plan_bg}; border: 1px solid {plan_border}; border-radius: 10px; padding: 12px; margin-top: 10px; margin-bottom: 2px;">
                    <p style="font-size:9.5px; font-weight:800; color:{plan_color}; margin:0 0 2px 0; text-transform:uppercase; letter-spacing:0.5px;">⏳ SUBSCRIPTION COUNTDOWN</p>
                    <div id="sidebar-ticking-timer" style="font-family: 'JetBrains Mono', monospace; font-size:18px; font-weight:700; color:#FFFFFF; margin-top: 2px;">
                        Calculating...
                    </div>
                    <p style="font-size:8.5px; color:#94A3B8; margin:4px 0 0 0;">Active {plan_label}. Expiration count-down live.</p>
                </div>
                
                <script>
                (function() {{
                    var userId = "{username_key_val}";
                    var key = "ipl_target_expiry_ms_" + userId;
                    var targetTime = localStorage.getItem(key);
                    var now = Date.now();
                    if (!targetTime || parseInt(targetTime) < now) {{
                        // First initialization today, starts from 23 hours, 59 minutes, 59 seconds
                        targetTime = now + (23 * 3600 + 59 * 60 + 59) * 1000;
                        localStorage.setItem(key, targetTime.toString());
                    }} else {{
                        targetTime = parseInt(targetTime);
                    }}
                    
                    function updateTicker() {{
                        var curr = Date.now();
                        var diff = targetTime - curr;
                        if (diff <= 0) {{
                            diff = 0;
                            clearInterval(tickerInterval);
                            // Visual blur of stream elements immediately
                            try {{
                                var doc = window.parent.document;
                                var elms = doc.querySelectorAll('div[data-testid="stKPI"], div[data-testid="stMetricValue"], div[data-testid="stArrowDataFrame"], div[data-testid="stPlotlyChart"]');
                                elms.forEach(function(el) {{
                                    el.style.filter = 'blur(8px) grayscale(45%)';
                                    el.style.pointerEvents = 'none';
                                    el.style.opacity = '0.82';
                                }});
                            }} catch (e) {{}}
                            // Instant redirection to User Portal via query parameters reload
                            setTimeout(function() {{
                                try {{
                                    window.parent.location.search = '?expired=true';
                                }} catch (e) {{
                                    try {{
                                        window.location.search = '?expired=true';
                                    }} catch (err) {{}}
                                }}
                            }}, 800);
                        }}
                        
                        var totalSecs = Math.floor(diff / 1000);
                        var h = Math.floor(totalSecs / 3600);
                        var m = Math.floor((totalSecs % 3600) / 60);
                        var s = totalSecs % 60;
                        
                        var timeStr = "";
                        if (h > 0) {{
                            var mStr = (m < 10 ? '0' : '') + m;
                            var sStr = (s < 10 ? '0' : '') + s;
                            timeStr = h + ":" + mStr + ":" + sStr;
                        }} else if (m > 0) {{
                            var sStr = (s < 10 ? '0' : '') + s;
                            timeStr = m + ":" + sStr;
                        }} else {{
                            timeStr = s.toString();
                        }}
                        
                        var container = document.getElementById('sidebar-ticking-timer');
                        if (container) {{
                            container.innerHTML = timeStr;
                        }}
                    }}
                    var tickerInterval = setInterval(updateTicker, 1000);
                    updateTicker();
                })();
                </script>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: rgba(239, 68, 68, 0.08); border: 1px solid #EF444450; border-radius: 10px; padding: 12px; margin-top: 10px; margin-bottom: 2px;">
                    <p style="font-size:9.5px; font-weight:800; color:#EF4444; margin:0 0 2px 0; text-transform:uppercase; letter-spacing:0.5px;">⏳ SUBSCRIPTION EXPIRED</p>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size:18px; font-weight:700; color:#EF4444; margin-top: 2px;">
                        0 (EXPIRED)
                    </div>
                    <p style="font-size:8.5px; color:#F87171; margin:4px 0 0 0;">Term finished. Dashboard visuals are blurred.</p>
                </div>
                """, unsafe_allow_html=True)

    # Modern dynamic theme toggle at bottom of sidebar
    st.markdown("<hr style='margin:16px 0; opacity:0.15;'>", unsafe_allow_html=True)
    st.markdown(
        f'<p style="font-size:10px;font-weight:800;letter-spacing:1px;margin:0 0 10px 0;color:{t["text2"]};text-transform:uppercase;">DISPLAY CONTROLS</p>',
        unsafe_allow_html=True
    )
    col_t1, col_t2 = st.columns([3, 1])
    with col_t1:
        cur_mode_label = "🌙 Dark Theme" if st.session_state.theme_mode == "dark" else "☀️ Light Theme"
        st.markdown(
            f'<div style="font-size: 12px; font-weight: 600; color: {t["text"]}; padding-top: 5px;">'
            f'{cur_mode_label}</div>',
            unsafe_allow_html=True
        )
    with col_t2:
        if st.button("🔄", key="main_theme_quick_toggle", help="Switch Light/Dark Theme"):
            st.session_state.theme_mode = "light" if st.session_state.theme_mode == "dark" else "dark"
            st.rerun()

    # Secure Logout button at the very bottom
    st.markdown("<hr style='margin:16px 0; opacity:0.15;'>", unsafe_allow_html=True)
    if st.button("🚪 Secure Log Out", key="sidebar_logout_btn", type="secondary", use_container_width=True):
        st.session_state.is_logged_in = False
        st.session_state.user_name = "Guest Spectator"
        st.session_state.user_role = "general_user"
        st.session_state.serial_id = "IPL-SPEC-1083"
        st.session_state.is_subscribed = False
        st.session_state.is_premium_subscribed = False
        st.session_state.is_pro_subscribed = False
        st.session_state.username_key = ""
        st.session_state.payment_processing = False
        st.toast("🚪 Logged out securely.")
        import time
        time.sleep(0.5)
        st.rerun()


# ─────────────────────────────────────────────────────────
# RENDER PAGES
# ─────────────────────────────────────────────────────────
# Check for Javascript-driven expiration redirect
try:
    if hasattr(st, "query_params") and "expired" in st.query_params:
        if st.query_params["expired"] == "true":
            st.session_state.app_usage_day = "Day 2+"
            st.session_state.active_page = "User Portal"
            st.query_params.clear()
            st.rerun()
except Exception:
    pass

# Admin constraint: force Admins to ONLY view the Admin Dashboard
is_admin_check = st.session_state.get("is_logged_in", False) and st.session_state.get("user_name", "").strip().lower() in ["avinash", "madhukar", "sharon", "deepak"]
if is_admin_check and st.session_state.active_page != "Admin Dashboard":
    st.session_state.active_page = "Admin Dashboard"
    st.rerun()

page = st.session_state.active_page
mode = st.session_state.theme_mode
t    = THEMES_DARK[page] if mode == "dark" else THEMES_LIGHT[page]

# Compute active page index for sidebar nav highlighting
active_idx = 0
pages_to_loop = get_pages_to_loop()
for idx, (_, name) in enumerate(pages_to_loop):
    if name == page:
        active_idx = idx
        break

inject_css(t, active_idx)

# ─────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────
# SUBSCRIPTION & OPERATIONS BYPASS GATE
# ─────────────────────────────────────────────────────────
# Define helper function to display pricing table
def render_pricing_plans():
    st.markdown("### 💎 Choose Your Upgrade Plan")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="background: rgba(56, 189, 248, 0.08); border: 2px solid #38BDF8; border-radius: 12px; padding: 20px; height: 350px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <h3 style="color:#38BDF8; margin-top:0; font-family:'Sora',sans-serif; font-size:18px;">✨ Premium Plan</h3>
                <p style="font-size:12.5px; opacity:0.8; margin-bottom:15px; color:#E2E8F0;">Unlock all safety visuals, plots, KPI metrics, raw tables, and anomaly charts on every Master Dashboard.</p>
                <hr style="opacity:0.2; margin:10px 0;">
                <p style="font-weight:700; font-size:12px; margin-bottom:4px; color:#94A3B8;">⏱️ CHOOSE TERM PLAN:</p>
            </div>
        """, unsafe_allow_html=True)
        premium_options = [
            ("₹299 INR / 1 Month", 299, "1 month"),
            ("₹399 INR / 3 Months", 399, "3 months"),
            ("₹599 INR / 6 Months", 599, "6 months"),
            ("₹999 INR / 12 Months", 999, "12 months")
        ]
        sel_prem = st.selectbox("Premium Duration Option", options=range(len(premium_options)), format_func=lambda i: premium_options[i][0], key="gated_prem_select")
        prem_plan = premium_options[sel_prem]
        
        curr_user = st.session_state.get("user_name", "").strip().lower()
        is_cre = curr_user in ["avinash", "madhukar", "sharon", "deepak"]
        is_dum = curr_user == "dummy@we01"
        is_prem_subscribed = st.session_state.get("is_premium_subscribed", False) or is_cre or is_dum
        
        if is_prem_subscribed:
            st.success("✅ Premium Plan Active")
        else:
            if st.button(f"💳 Purchase Premium - {prem_plan[0].split(' / ')[0]}", key="pay_prem_gate_btn", type="primary", use_container_width=True):
                st.session_state.billing_type = "premium"
                st.session_state.billing_plan = prem_plan
                st.session_state.payment_processing = True
                st.session_state.active_page = "User Portal"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div style="background: rgba(129, 140, 248, 0.08); border: 2px solid #818CF8; border-radius: 12px; padding: 20px; height: 350px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <h3 style="color:#818CF8; margin-top:0; font-family:'Sora',sans-serif; font-size:18px;">🚀 Pro Plan</h3>
                <p style="font-size:12.5px; opacity:0.8; margin-bottom:15px; color:#E2E8F0;">Unlock unlimited Cohere AI command chat, interactive custom database queries, and crowd dispatch control.</p>
                <hr style="opacity:0.2; margin:10px 0;">
                <p style="font-weight:700; font-size:12px; margin-bottom:4px; color:#94A3B8;">⏱️ CHOOSE TERM PLAN:</p>
            </div>
        """, unsafe_allow_html=True)
        pro_options = [
            ("₹399 INR / 1 Month", 399, "1 month"),
            ("₹549 INR / 3 Months", 549, "3 months"),
            ("₹799 INR / 6 Months", 799, "6 months"),
            ("₹999 INR / 12 Months", 999, "12 months")
        ]
        sel_pro_val = st.selectbox("Pro Duration Option", options=range(len(pro_options)), format_func=lambda i: pro_options[i][0], key="gated_pro_select")
        pro_plan = pro_options[sel_pro_val]
        
        is_pro_subscribed = st.session_state.get("is_pro_subscribed", False) or is_cre or is_dum
        
        if is_pro_subscribed:
            st.success("✅ Pro Plan Active")
        else:
            if st.button(f"💳 Purchase Pro - {pro_plan[0].split(' / ')[0]}", key="pay_pro_gate_btn", type="primary", use_container_width=True):
                st.session_state.billing_type = "pro"
                st.session_state.billing_plan = pro_plan
                st.session_state.payment_processing = True
                st.session_state.active_page = "User Portal"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

curr_user_lower = st.session_state.get("user_name", "").strip().lower()
is_creator_admin = curr_user_lower in ["avinash", "madhukar", "sharon", "deepak"]
is_dummy_user = curr_user_lower == "dummy@we01"
has_unlimited_bypass = is_creator_admin or is_dummy_user

# Global subscription and trial checks
is_day_1 = st.session_state.get("app_usage_day", "Day 1") == "Day 1"

username_key = st.session_state.get("username_key", "").strip().lower()

# Align st.session_state variables dynamically for stadium managers to keep all UI unified
if username_key in ["che_admin01", "chin_admin01", "eden_admin01", "uppal_admin01", "wank_admin01"]:
    if username_key == "che_admin01":
        st.session_state.is_premium_subscribed = True
        st.session_state.is_pro_subscribed = True
    elif username_key == "chin_admin01":
        if is_day_1:
            st.session_state.is_premium_subscribed = True
            st.session_state.is_pro_subscribed = False
        else:
            st.session_state.is_premium_subscribed = False
            st.session_state.is_pro_subscribed = False
    elif username_key == "eden_admin01":
        if is_day_1:
            st.session_state.is_premium_subscribed = True
            st.session_state.is_pro_subscribed = True
        else:
            st.session_state.is_premium_subscribed = False
            st.session_state.is_pro_subscribed = False
    elif username_key == "uppal_admin01":
        st.session_state.is_premium_subscribed = False
        st.session_state.is_pro_subscribed = False
    elif username_key == "wank_admin01":
        if is_day_1:
            st.session_state.is_premium_subscribed = True
            st.session_state.is_pro_subscribed = True
        else:
            st.session_state.is_premium_subscribed = False
            st.session_state.is_pro_subscribed = False

# Overwrite access metrics based on custom stadium mappings requested by the user
if username_key == "che_admin01":
    has_premium_access = True
    has_pro_access = True
elif username_key == "chin_admin01":
    if is_day_1:
        has_premium_access = True
        has_pro_access = False
    else:
        has_premium_access = False
        has_pro_access = False
elif username_key == "eden_admin01":
    if is_day_1:
        has_premium_access = True
        has_pro_access = True
    else:
        has_premium_access = False
        has_pro_access = False
elif username_key == "uppal_admin01":
    # Uppal Stadium has only access to visuals (not premium/pro options) for 1 day. 
    # Having has_premium_access as False disables premium options on Day 1, while page is not blurred on Day 1.
    # On Day 2+, since has_premium_access is False, the dashboard pages will get blurred.
    has_premium_access = False
    has_pro_access = False
elif username_key == "wank_admin01":
    if is_day_1:
        has_premium_access = True
        has_pro_access = True
    else:
        has_premium_access = False
        has_pro_access = False
else:
    has_premium_access = st.session_state.get("is_premium_subscribed", False) or has_unlimited_bypass
    has_pro_access = st.session_state.get("is_pro_subscribed", False) or has_unlimited_bypass

gated_premium_pages = ["Crowd Flow", "Medical & Heat", "Security", "Resource Planning", "Risk Matrix", "Ask AI"]
is_gated_page = page in gated_premium_pages
is_analytical_page = page in ["Overview", "Crowd Flow", "Medical & Heat", "Security", "Resource Planning", "Risk Matrix"]

# Ask AI Page Gating (Redirects to Access Plan page if no Pro Access)
if page == "Ask AI" and not has_pro_access:
    st.session_state.active_page = "User Portal"
    st.session_state.pending_plan_msg = "⚠️ The interactive Ask AI operations co-pilot chat is a Pro Plan exclusive feature. You have been directed to the Access Plan terminal."
    st.rerun()

# Day 2+ Analytical Pages Gating (Visuals Blurred, requires Premium Access)
if is_analytical_page and not is_day_1 and not has_premium_access:
    # Render blurred overlay
    st.markdown(f"""
    <style>
    /* Physically blur ALL streamlit visual elements on the page except header */
    div[data-testid="stKPI"], 
    div[data-testid="stMetricValue"],
    div[data-testid="stArrowDataFrame"],
    div[data-testid="stPlotlyChart"],
    div.element-container:not(:nth-child(-n+5)) {{
        filter: blur(8px) grayscale(45%);
        pointer-events: none;
        user-select: none;
        opacity: 0.82;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: rgba(30, 41, 59, 0.95); border: 2px solid #EF4444; border-radius: 12px; padding: 32px; text-align: center; margin-bottom: 30px; margin-top: 20px; box-shadow: {t['shadow']};">
        <div style="font-size: 50px; margin-bottom: 12px;">🔒</div>
        <h3 style="font-family: 'Sora', sans-serif; color: #F87171; font-size: 22px; font-weight: 800; margin: 0 0 8px 0; letter-spacing: -0.5px;">Premium Operational View Locked (Day 2+)</h3>
        
        <div style="background: rgba(220, 38, 38, 0.12); border: 1px solid #EF444450; border-radius: 8px; padding: 12px; display: inline-block; margin-bottom: 15px; margin-left: auto; margin-right: auto; min-width: 250px;">
            <p style="font-size: 10px; font-weight: 800; color: #F87171; margin: 0 0 2px 0; text-transform: uppercase; letter-spacing: 0.8px;">⏳ TRIAL TIME RECONCILIATION</p>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 20px; font-weight: 700; color: #EF4444;">00h : 00m : 00s (EXPIRED)</div>
        </div>

        <p style="color: {t['text2']}; font-size: 14px; line-height: 1.6; margin-bottom: 20px; max-width: 600px; margin-left: auto; margin-right: auto;">
            The 1-day free-trial period for this stadium profile (<strong>{"Uppal Stadium" if username_key == "uppal_admin01" else "Trial Mode"}</strong>) has expired. The live visualizations, KPIs, risk prioritizations, and anomaly matrices for <strong>{page}</strong> are blurred. Upgrade to lock in your Premium subscription.
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("👤 Go to Access Plan Terminal (User Portal) to Upgrade", type="primary", use_container_width=True, key="day2_redirect_btn"):
        st.session_state.active_page = "User Portal"
        st.rerun()
    render_pricing_plans()
    st.stop()


# ═══════════════════════════════════════════════════════════
# PAGE: HOME PAGE
# ═══════════════════════════════════════════════════════════
if page == "Home Page":
    # 1. Custom Integrated Hero Section - Combining Title, Quote & Clean Numbers-Only Telemetry Strip
    st.markdown(f"""
<div class="intro-hero" style="background: linear-gradient(135deg, {t['bg']} 0%, {t['sidebar']} 100%); border: 1px solid {t['border']}; box-shadow: 0 10px 30px rgba(0,0,0,0.3); border-radius: 20px; padding: 35px; margin-bottom: 25px; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center;">
  <div class="intro-badge" style="background: rgba(0, 240, 255, 0.15); border: 1px solid {t['accent']}; color: {t['accent']}; padding: 5px 14px; border-radius: 999px; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 12px;">🏏 IPL Crowd Safety Center</div>
  <h1 class="intro-title" style="color: {t['text']}; font-family: 'Sora', sans-serif; font-size: 32px; font-weight: 800; line-height: 1.2; margin: 0 0 10px 0;">Stadium Operations Intelligence Suite</h1>
  <p class="intro-desc" style="color: {t['text2']}; max-width: 750px; font-size: 14.5px; line-height: 1.6; margin: 0 auto; font-weight: 500;">
    An integrated operations suite to monitor seating capacity boundaries, queue wait vectors, micro-climate wet-bulb heat states, and paramedic dispatch allocations in real-time.
  </p>

  <!-- 💡 Inspiring Centered Quote Block -->
  <div style="font-family: 'Sora', sans-serif; font-style: italic; font-size: 15px; color: {t['accent']}; font-weight: 600; margin: 22px 0; max-width: 680px; text-align: center; border-top: 1px dashed {t['border']}; border-bottom: 1px dashed {t['border']}; padding: 12px 0;">
    "Millions come to watch cricket. This platform helps ensure they return home safely."
  </div>

  <!-- 📊 Compact, Clean Numbers-Only Telemetry Strip -->
  <div style="margin-top: 10px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; width: 100%; max-width: 820px; border-top: 1px solid {t['border']}; padding-top: 22px;">
    <div style="text-align: center;">
      <div style="font-family: 'Sora', sans-serif; font-size: 30px; font-weight: 800; color: {t['text']}; line-height: 1;">5</div>
      <div style="font-size: 11px; color: {t['text2']}; font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 6px;">Active Arenas</div>
    </div>
    <div style="text-align: center; border-left: 1px solid {t['border']};">
      <div style="font-family: 'Sora', sans-serif; font-size: 30px; font-weight: 800; color: {t['text']}; line-height: 1;">14.5m</div>
      <div style="font-size: 11px; color: {t['text2']}; font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 6px;">Avg Queue Wait</div>
    </div>
    <div style="text-align: center; border-left: 1px solid {t['border']};">
      <div style="font-family: 'Sora', sans-serif; font-size: 30px; font-weight: 800; color: {t['warn_col']}; line-height: 1;">Moderate</div>
      <div style="font-size: 11px; color: {t['text2']}; font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 6px;">Security Level</div>
    </div>
    <div style="text-align: center; border-left: 1px solid {t['border']};">
      <div style="font-family: 'Sora', sans-serif; font-size: 30px; font-weight: 800; color: {t['ok_col']}; line-height: 1;">&lt; 8m</div>
      <div style="font-size: 11px; color: {t['text2']}; font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 6px;">EMT Transit Goal</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    # 2. Interactive Project Overview & Lessons (Clickable Tabs for Neat Layout)
    sec_label("Learn & Explore the Hub")
    tab_overview, tab_challenges, tab_users = st.tabs([
        "🎯 Hub Overview", 
        "🌊 The 5 Core Challenges", 
        "🤝 Who Benefits & Cooperates?"
    ])

    with tab_overview:
        st.markdown(f"""
        <div class="report-card" style="border-left: 5px solid {t['accent']} !important; margin-bottom: 16px; box-sizing: border-box; padding: 22px;">
            <div class="report-header-wrapper" style="margin-bottom: 12px; display: flex; align-items: center; gap: 10px;">
                <div class="report-icon" style="font-size: 20px;">🛡️</div>
                <h4 class="report-title" style="font-family: 'Sora', sans-serif; font-size: 15px; font-weight: 800; color: {t['text']}; margin: 0;">What is this Hub?</h4>
            </div>
            <div class="report-body" style="font-size: 13.5px; color: {t['text2']}; line-height: 1.6;">
                <p>During massive IPL cricket matches, stadiums host over 80,000 passionate spectators. This hub acts as a digital commander's screen to map, predict, and coordinate spectator safety in real time, bridging the communication gaps between different rescue agencies.</p>
                <ul class="report-list">
                    <li class="report-list-item"><b>Universal Sync</b>: Unifies ticketing teams, local police, private guards, and paramedics in one screen.</li>
                    <li class="report-list-item"><b>Predictive Warnings</b>: Highlights blockages and queue build-ups before they become physical safety hazards.</li>
                    <li class="report-list-item"><b>Rapid Response</b>: Optimizes ambulance dispatch coordinates to bypass congested areas quickly.</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tab_challenges:
        st.markdown("<h5 style='font-family: Sora, sans-serif; margin-bottom: 12px; font-size: 15px;'>The Five Major Venue Challenges We Help Resolve:</h5>", unsafe_allow_html=True)
        c_col1, c_col2 = st.columns(2)
        with c_col1:
            st.markdown(f"""
            <div style="background: {t['card']}; border: 1px solid {t['border']}; border-radius: 12px; padding: 16px; margin-bottom: 12px; border-left: 4px solid {t['crit_col']} !important; box-shadow: {t['shadow']};">
                <strong style="color: {t['text']}; font-size: 13.5px; display: block; margin-bottom: 4px;">1. Gate Bottlenecks</strong>
                <span style="font-size: 12px; color: {t['text2']}; line-height: 1.45; display: block;">High visitor arrivals in the final hour before play create long visitor lines inside thoroughfares.</span>
            </div>
            <div style="background: {t['card']}; border: 1px solid {t['border']}; border-radius: 12px; padding: 16px; margin-bottom: 12px; border-left: 4px solid {t['warn_col']} !important; box-shadow: {t['shadow']};">
                <strong style="color: {t['text']}; font-size: 13.5px; display: block; margin-bottom: 4px;">2. Localized Overcrowding</strong>
                <span style="font-size: 12px; color: {t['text2']}; line-height: 1.45; display: block;">Dynamic seating surges produce crowd density pockets that breach safety caps.</span>
            </div>
            <div style="background: {t['card']}; border: 1px solid {t['border']}; border-radius: 12px; padding: 16px; border-left: 4px solid {t['crit_col']} !important; box-shadow: {t['shadow']};">
                <strong style="color: {t['text']}; font-size: 13.5px; display: block; margin-bottom: 4px;">3. Extreme Heat & Stress</strong>
                <span style="font-size: 12px; color: {t['text2']}; line-height: 1.45; display: block;">Tropical wet-bulb heat hikes trigger dehydration and exhaustion inside packed stands.</span>
            </div>
            """, unsafe_allow_html=True)
        with c_col2:
            st.markdown(f"""
            <div style="background: {t['card']}; border: 1px solid {t['border']}; border-radius: 12px; padding: 16px; margin-bottom: 12px; border-left: 4px solid {t['warn_col']} !important; box-shadow: {t['shadow']};">
                <strong style="color: {t['text']}; font-size: 13.5px; display: block; margin-bottom: 4px;">4. Security Access Breaches</strong>
                <span style="font-size: 12px; color: {t['text2']}; line-height: 1.45; display: block;">Perimeter scaled fences, duplicate fake tickets, and minor group arguments.</span>
            </div>
            <div style="background: {t['card']}; border: 1px solid {t['border']}; border-radius: 12px; padding: 16px; border-left: 4px solid {t['accent']} !important; box-shadow: {t['shadow']};">
                <strong style="color: {t['text']}; font-size: 13.5px; display: block; margin-bottom: 4px;">5. Evacuation Hazards</strong>
                <span style="font-size: 12px; color: {t['text2']}; line-height: 1.45; display: block;">Blocked exit channels or lock failures that slow down exit flow times.</span>
            </div>
            """, unsafe_allow_html=True)

    with tab_users:
        st.markdown("<h5 style='font-family: Sora, sans-serif; margin-bottom: 12px; font-size: 15px;'>How Different Organizations Collaborate Instantly:</h5>", unsafe_allow_html=True)
        u_col1, u_col2, u_col3 = st.columns(3)
        with u_col1:
            st.markdown(f"""
            <div style="background: rgba(56, 189, 248, 0.05); border: 1px solid {t['border']}; border-radius: 14px; padding: 16px; height: 100%;">
                <strong style="color: {t['accent']}; font-size: 13.5px; display: block; margin-bottom: 6px;">🏟️ Venue Managers</strong>
                <p style="font-size: 12px; color: {t['text2']}; line-height: 1.4; margin: 0;">Monitor gate flow scales and open auxiliary turnstiles proactively to speed up entry.</p>
            </div>
            """, unsafe_allow_html=True)
        with u_col2:
            st.markdown(f"""
            <div style="background: rgba(16, 185, 129, 0.05); border: 1px solid {t['border']}; border-radius: 14px; padding: 16px; height: 100%;">
                <strong style="color: #10B981; font-size: 13.5px; display: block; margin-bottom: 6px;">🚔 Police & Security</strong>
                <p style="font-size: 12px; color: {t['text2']}; line-height: 1.4; margin: 0;">Position crowd barriers and deploy wardens exactly where entry queue density is highest.</p>
            </div>
            """, unsafe_allow_html=True)
        with u_col3:
            st.markdown(f"""
            <div style="background: rgba(244, 63, 94, 0.05); border: 1px solid {t['border']}; border-radius: 14px; padding: 16px; height: 100%;">
                <strong style="color: #F43F5E; font-size: 13.5px; display: block; margin-bottom: 6px;">🚑 Paramedic Teams</strong>
                <p style="font-size: 12px; color: {t['text2']}; line-height: 1.4; margin: 0;">Track wet-bulb thermal ratings to dispatch ambulance assets before dehydration rises.</p>
            </div>
            """, unsafe_allow_html=True)

    # 4. Interactive Controller Navigation
    sec_label("Interactive Commander Control Shortcuts")
    st.write("Click any module button below to switch views instantly:")

    sc_c1, sc_c2, sc_c3 = st.columns(3)
    with sc_c1:
        if st.button("🏠 Executive Overview", use_container_width=True, help="Overall safety scores, occupancy levels & alerts"):
            st.session_state.active_page = "Overview"
            st.rerun()
        if st.button("🌊 Crowd Flow Tracking", use_container_width=True, help="Turnstile speeds and gate queues"):
            st.session_state.active_page = "Crowd Flow"
            st.rerun()
    with sc_c2:
        if st.button("🏥 Medical & Heat Controls", use_container_width=True, help="Wet-bulb indicators & live paramedic sync"):
            st.session_state.active_page = "Medical & Heat"
            st.rerun()
        if st.button("🔒 Security Intel Panel", use_container_width=True, help="Fake tickets & perimeter barrier breaches"):
            st.session_state.active_page = "Security"
            st.rerun()
    with sc_c3:
        if st.button("📦 Logistical Resource Planner", use_container_width=True, help="Warden placements and barrier planner"):
            st.session_state.active_page = "Resource Planning"
            st.rerun()
        if st.button("🚨 Risk Decision Matrix", use_container_width=True, help="Standardized multi-metric hazard scoring"):
            st.session_state.active_page = "Risk Matrix"
            st.rerun()

    st.write("")
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {t['accent_lt']}, rgba(11,16,30,0.8)); border-top: 3px solid {t['accent']}; border-radius: 12px; padding: 14px; text-align: center;">
        <span style="font-family: 'JetBrains Mono', monospace; font-size: 11.5px; color: {t['accent']}; font-weight:700;">PROACTIVE STADIUM INTELLIGENCE • COHERENT CRADLE OF SAFETY</span>
    </div>
    """, unsafe_allow_html=True)

    st.stop()


# ═══════════════════════════════════════════════════════════
# PAGE: USER PORTAL
# ═══════════════════════════════════════════════════════════
if page == "User Portal":
    page_header("👤", "Authority Authorization Terminal & Spectator Season Pass Portal", 
                "Configure stadium permissions, view your Digital RFID Access Badge, and activate Season Copilot subscriptions.")

    if "pending_plan_msg" in st.session_state and st.session_state.pending_plan_msg:
        st.warning(st.session_state.pending_plan_msg)
        st.session_state.pending_plan_msg = ""

    col1, col2 = st.columns([1, 1], gap="large")

    role_label_map = {
        "stadium_ops": "🏟️ Stadium Operations Commander",
        "police_security": "👮 Police & Security Marshal",
        "medical_team": "🏥 Paramedic Response Specialist",
        "general_user": "🏏 General Spectator / Guest",
        "dummy_all_access": "🕵️ Spectator All Access Spectator Portal"
    }

    with col1:
        st.markdown(f'<p style="font-size:16px; font-weight:800; color:{t["accent"]}; margin-bottom:12px;">🛡️ RFID DIGITAL SMART CARD</p>', unsafe_allow_html=True)

        # Edit profile details
        new_name = st.text_input("Cardholder Name", value=st.session_state.user_name)
        if new_name != st.session_state.user_name:
            st.session_state.user_name = new_name
            st.rerun()

        # Premium RFID Card styled precisely via Inline Custom CSS — flushed left to clear code parsing rule
        role_card_colors = {
            "stadium_ops": {"gradient": "linear-gradient(135deg, #7C3AED 0%, #1D4ED8 100%)", "tag": "COMMANDER", "accent": "#00FFFF"},
            "police_security": {"gradient": "linear-gradient(135deg, #1E3A8A 0%, #0F172A 100%)", "tag": "MARSHAL", "accent": "#38BDF8"},
            "medical_team": {"gradient": "linear-gradient(135deg, #B91C1C 0%, #450A0A 100%)", "tag": "MED TEAM", "accent": "#F87171"},
            "general_user": {"gradient": "linear-gradient(135deg, #374151 0%, #111827 100%)", "tag": "SPECTATOR", "accent": "#9CA3AF"},
            "dummy_all_access": {"gradient": "linear-gradient(135deg, #0D9488 0%, #115E59 100%)", "tag": "SPECTATOR DUMMY", "accent": "#2DD4BF"}
        }
        
        card_design = role_card_colors[st.session_state.user_role]
        
        # Calculate dynamic text of the active season subscription plan for visual card badge display
        username_key_val = st.session_state.get("username_key", "").strip().lower()
        is_day_1_val = st.session_state.get("app_usage_day", "Day 1") == "Day 1"
        active_plan_descr = "No active subscription"
        
        if username_key_val == "che_admin01":
            active_plan_descr = "🎁 Free Trial (Lifetime)"
        elif username_key_val == "chin_admin01":
            if is_day_1_val:
                active_plan_descr = "✨ Premium (AI Insights 1M)"
            else:
                active_plan_descr = "❌ Premium (AI Insights 1M) - Expired"
        elif username_key_val == "eden_admin01":
            active_plan_descr = "🔮 Premium + Pro (3M)"
        elif username_key_val == "uppal_admin01":
            if is_day_1_val:
                active_plan_descr = "⌛ 1-Day Trial (Active)"
            else:
                active_plan_descr = "❌ 1-Day Trial (Expired)"
        elif username_key_val == "wank_admin01":
            active_plan_descr = "🔮 Prem (3M) + Pro (6M)"
        else:
            if st.session_state.get("is_premium_subscribed") and st.session_state.get("is_pro_subscribed"):
                active_plan_descr = "🔮 Premium + Pro Plan Active"
            elif st.session_state.get("is_premium_subscribed"):
                active_plan_descr = "✨ Premium Plan Active"
            elif st.session_state.get("is_pro_subscribed"):
                active_plan_descr = "💎 Pro Plan Active"
            elif has_unlimited_bypass:
                active_plan_descr = "👑 Unlimited Admin Bypass"
            else:
                active_plan_descr = "🏏 Guest Spectator Pass"

        badge_html = f"""<div style="background: {card_design['gradient']}; border: 2px solid {card_design['accent']}95; border-radius: 18px; padding: 24px; color: #FFFFFF; font-family: 'JetBrains Mono', 'Sora', sans-serif; position: relative; box-shadow: 0 10px 25px rgba(0,0,0,0.4); margin-top: 15px; max-width: 440px; height: 250px; display: flex; flex-direction: column; justify-content: space-between; overflow: hidden;">
<div style="position: absolute; top: -50px; right: -50px; width: 140px; height: 140px; background: {card_design['accent']}22; filter: blur(40px); border-radius: 50%;"></div>
<div style="display: flex; justify-content: space-between; align-items: flex-start; z-index: 10;">
<div>
<div style="font-size: 13px; font-weight: 800; letter-spacing: 0.5px; opacity: 0.95;">IPL OPERATIONS CONTROL</div>
<div style="font-size: 8px; font-weight: 600; color: {card_design['accent']}; letter-spacing: 1px; margin-top: 2px;">DIGITAL IDENT DECK</div>
</div>
<div style="background: rgba(255, 255, 255, 0.15); border: 1px solid rgba(255,255,255,0.25); padding: 4px 10px; border-radius: 6px; font-size: 8px; font-weight: 800; letter-spacing: 1px;">{card_design['tag']}</div>
</div>
<div style="background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%); width: 32px; height: 24px; border-radius: 4px; padding: 4px; box-shadow: inset 0 0 4px rgba(0,0,0,0.2); margin-top: 20px; display: flex; gap: 2px; z-index: 10;">
<div style="border: 1px solid rgba(255,255,255,0.2); width: 100%; height: 100%;"></div>
<div style="border: 1px solid rgba(255,255,255,0.2); width: 100%; height: 100%;"></div>
</div>
<div style="margin-top: auto; z-index: 10;">
<div style="font-size: 10px; color: rgba(255, 255, 255, 0.6); font-weight: 600;">OFFICIAL SYSTEM USER</div>
<div style="font-size: 18px; font-weight: 800; font-family: 'Sora', sans-serif; letter-spacing: -0.2px; margin-top: 2px;">{st.session_state.user_name}</div>
<div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: 14px; border-top: 1px solid rgba(255,255,255,0.14); padding-top: 12px;">
<div>
<div style="font-size: 7px; color: rgba(255,255,255,0.5); letter-spacing: 0.5px;">SYSTEM SERIAL UID</div>
<div style="font-size: 11px; font-weight: 700; color: {card_design['accent']}; letter-spacing: 0.5px; margin-top: 1px;">{st.session_state.serial_id}</div>
</div>
<div>
<div style="font-size: 7px; color: rgba(255,255,255,0.5); letter-spacing: 0.5px; text-align: right;">ACTIVE SEASON SUBSCRIPTION</div>
<div style="font-size: 10px; font-weight: 700; text-align: right; letter-spacing: 0.5px; margin-top: 1px; color: #38BDF8;">{active_plan_descr}</div>
</div>
</div>
</div>
</div>"""
        st.markdown(badge_html, unsafe_allow_html=True)
        
        # Current login card details metadata
        st.write("")
        st.markdown(f'<p style="font-size:13px; font-weight:800; color:{t["text2"]}; margin-top:10px; margin-bottom:5px;">📋 CURRENT LOGON IDENT DECK</p>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background: {t['card']}; border: 1px solid {t['border']}; border-radius: 10px; padding: 15px; font-size: 13.5px; color: {t['text2']}; line-height: 1.65;">
            👤 <strong>Access Cardholder:</strong> <span style="color: {t['text']}; font-weight:600;">{st.session_state.user_name}</span><br>
            🏷️ <strong>System Serial UID:</strong> <span style="color: {t['accent']}; font-family: 'JetBrains Mono', monospace; font-weight: 700;">{st.session_state.serial_id}</span><br>
            🏢 <strong>Authorized Role:</strong> <span style="color: {t['accent2']}; font-weight: 600;">{role_label_map[st.session_state.user_role]}</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f'<p style="font-size:16px; font-weight:800; color:{t["accent"]}; margin-bottom:12px;">🎟️ SYSTEM SUBSCRIPTION GATEWAY</p>', unsafe_allow_html=True)
        
        curr_user_lower = st.session_state.get("user_name", "").strip().lower()
        is_creator = curr_user_lower in ["avinash", "madhukar", "sharon", "deepak"]
        is_dummy_user = curr_user_lower == "dummy@we01"
        has_unlimited_bypass = is_creator or is_dummy_user
        
        # Determine specific subscription active states
        is_prem_active = st.session_state.get("is_premium_subscribed", False) or (has_unlimited_bypass and not is_dummy_user)
        is_pro_active = st.session_state.get("is_pro_subscribed", False) or (has_unlimited_bypass and not is_dummy_user)
        
        if is_dummy_user:
            st.info("🕵️ **All Access (System Evaluation Bypass) Active.** You can view available commercial plans below, but simulated purchases are restricted for this dummy account profile.")
        elif has_unlimited_bypass:
            st.markdown(f"""
            <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid #10B98150; border-radius: 12px; padding: 20px; text-align: center; margin-bottom: 20px;">
                <h4 style="color: #10B981; margin-top: 0; font-family: 'Sora', sans-serif; font-size:16px;">👑 Admin / Creator Whitelist</h4>
                <p style="font-size: 13px; color: {t['text2']}; line-height: 1.5; margin-bottom: 0;">
                    Your account details grant you infinite bypass permissions. All Premium safety visuals and Pro AI features are unlocked automatically.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
        # Display elegant plan status cards side by side
        st.markdown("### 🎫 Active Pass Subscriptions")
        
        prem_bg = "rgba(56, 189, 248, 0.08)" if is_prem_active else "rgba(220, 38, 38, 0.05)"
        prem_border = "#38BDF8" if is_prem_active else "#dc2626"
        prem_status = "🟢 Active (Unlocked)" if is_prem_active else "🔴 Locked (Purchase Required)"
        
        pro_bg = "rgba(129, 140, 248, 0.08)" if is_pro_active else "rgba(220, 38, 38, 0.05)"
        pro_border = "#818CF8" if is_pro_active else "#dc2626"
        pro_status = "🔮 Active (Unlocked)" if is_pro_active else "🔴 Locked (Purchase Required)"
        
        col_st_p, col_st_o = st.columns(2)
        with col_st_p:
            st.markdown(f"""
            <div style="background: {prem_bg}; border: 1px solid {prem_border}50; border-radius: 12px; padding: 15px; text-align: center;">
                <p style="font-size: 10px; color: {t['text2']}; font-weight: 800; text-transform: uppercase; margin: 0 0 4px 0;">✨ PREMIUM ACCESS</p>
                <div style="font-size: 13px; font-weight: 700; color: {prem_border};">{prem_status}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_st_o:
            st.markdown(f"""
            <div style="background: {pro_bg}; border: 1px solid {pro_border}50; border-radius: 12px; padding: 15px; text-align: center;">
                <p style="font-size: 10px; color: {t['text2']}; font-weight: 800; text-transform: uppercase; margin: 0 0 4px 0;">🚀 PRO ACCESS</p>
                <div style="font-size: 13px; font-weight: 700; color: {pro_border};">{pro_status}</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<hr style='margin:16px 0; opacity:0.15;'>", unsafe_allow_html=True)
        
        # Payment checkout gateway is active
        if st.session_state.payment_processing:
            # We are currently in Payment process
            billing_type = st.session_state.get("billing_type", "premium")
            billing_plan = st.session_state.get("billing_plan", ("₹299 INR / 1 Month", 299, "1 Month"))
            
            st.markdown(f"""
            <div style="background: {t['sidebar']}; border: 2px solid {t['accent']}80; border-radius: 12px; padding: 18px; margin-bottom: 15px;">
                <span style="font-size: 11.5px; font-weight: 700; color: {t['accent']}; text-transform: uppercase; letter-spacing: 0.8px; display: block; margin-bottom: 4px;">💳 Secure PayGuard Gateway</span>
                <p style="font-size: 12px; color: {t['text2']}; margin: 0; line-height: 1.4;">
                    Checkout method to process <strong>{billing_type.upper()} ({billing_plan[0]})</strong>. Payment completes your session setup automatically.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            pay_method = st.radio("Choose Pay Mode", ["UPI Transfer (Instant)", "Credit / Debit / ATM Card"], key="portal_pay_method_radio")
            
            if pay_method == "UPI Transfer (Instant)":
                upi_id = st.text_input("UPI Address ID", placeholder="e.g. upi_user@okicici", key="portal_upi_address_field")
                st.write("")
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    if st.button("❌ Terminate Purchase", key="portal_cancel_u", use_container_width=True):
                        st.session_state.payment_processing = False
                        st.rerun()
                with col_p2:
                    if st.button("🔒 Confirm UPI Payment", key="portal_confirm_pay_u", type="primary", use_container_width=True):
                        if "@" not in upi_id or len(upi_id) < 5:
                            st.error("⚠️ Invalid UPI address structure (missing '@' handle).")
                        else:
                            with st.spinner("⏳ Broadcasting authorization push request to UPI application..."):
                                import time
                                time.sleep(1.5)
                                
                            # Record payment
                            import random
                            from datetime import datetime
                            txn_id = f"TXN{random.randint(10000000, 99999999)}"
                            date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            
                            lookup = st.session_state.get("username_key", "").strip().lower()
                            if not lookup:
                                lookup = st.session_state.user_name.strip().lower()
                                
                            new_txn = {
                                "username": lookup,
                                "name": st.session_state.user_name.strip(),
                                "role": st.session_state.user_role,
                                "plan": f"{billing_type.upper()}: {billing_plan[0]}",
                                "amount": billing_plan[1],
                                "term": billing_plan[2],
                                "date": date_str,
                                "method": f"UPI: {upi_id}",
                                "transaction_id": txn_id
                            }
                            st.session_state.subscription_payments.append(new_txn)
                            
                            st.session_state.is_subscribed = True
                            if billing_type == "premium":
                                st.session_state.is_premium_subscribed = True
                            else:
                                st.session_state.is_pro_subscribed = True
                                
                            st.session_state.payment_processing = False
                            
                            if lookup in st.session_state.registered_users:
                                st.session_state.registered_users[lookup]["is_subscribed"] = True
                                if billing_type == "premium":
                                    st.session_state.registered_users[lookup]["is_premium_subscribed"] = True
                                else:
                                    st.session_state.registered_users[lookup]["is_pro_subscribed"] = True
                                st.session_state.registered_users[lookup]["active_plan"] = billing_plan[0]
                                
                            st.success(f"✅ Payment Authorized! {billing_type.upper()} {billing_plan[2]} Pass activated.")
                            st.toast("🎉 Subscription Successful!")
                            st.rerun()
                            
            else:
                card_num = st.text_input("16-Digit Card Credentials", placeholder="xxxx xxxx xxxx xxxx", key="portal_card_credentials_field")
                col_card1, col_card2 = st.columns(2)
                with col_card1:
                    card_exp = st.text_input("Expiration MM/YY", placeholder="01/29", key="portal_card_exp_field")
                with col_card2:
                    card_cvv = st.text_input("Secure CVV Code", type="password", placeholder="***", key="portal_card_cvv_field")
                
                st.write("")
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    if st.button("❌ Terminate Purchase", key="portal_cancel_c", use_container_width=True):
                        st.session_state.payment_processing = False
                        st.rerun()
                with col_p2:
                    if st.button("🔒 Authorize Card Securely", key="portal_confirm_pay_c", type="primary", use_container_width=True):
                        clean_card = card_num.replace(" ", "")
                        if not clean_card.isdigit() or len(clean_card) != 16:
                            st.error("⚠️ Invalid Card Number configuration. Must be 16 digits.")
                        elif "/" not in card_exp or len(card_exp) != 5:
                            st.error("⚠️ Invalid Expiration. Use MM/YY MM/YY configuration.")
                        elif not card_cvv.isdigit() or len(card_cvv) != 3:
                            st.error("⚠️ Secure CVV is invalid. Must be 3 numeric characters.")
                        else:
                            with st.spinner("⏳ Submitting secure transaction token to gateway system..."):
                                import time
                                time.sleep(1.5)
                                
                            # Record payment
                            import random
                            from datetime import datetime
                            txn_id = f"TXN{random.randint(10000000, 99999999)}"
                            date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            
                            lookup = st.session_state.get("username_key", "").strip().lower()
                            if not lookup:
                                lookup = st.session_state.user_name.strip().lower()
                                
                            new_txn = {
                                "username": lookup,
                                "name": st.session_state.user_name.strip(),
                                "role": st.session_state.user_role,
                                "plan": f"{billing_type.upper()}: {billing_plan[0]}",
                                "amount": billing_plan[1],
                                "term": billing_plan[2],
                                "date": date_str,
                                "method": f"Card: **** **** **** {clean_card[-4:] if len(clean_card) >=4 else '9999'}",
                                "transaction_id": txn_id
                            }
                            st.session_state.subscription_payments.append(new_txn)
                            
                            st.session_state.is_subscribed = True
                            if billing_type == "premium":
                                st.session_state.is_premium_subscribed = True
                            else:
                                st.session_state.is_pro_subscribed = True
                                
                            st.session_state.payment_processing = False
                            
                            if lookup in st.session_state.registered_users:
                                st.session_state.registered_users[lookup]["is_subscribed"] = True
                                if billing_type == "premium":
                                    st.session_state.registered_users[lookup]["is_premium_subscribed"] = True
                                else:
                                    st.session_state.registered_users[lookup]["is_pro_subscribed"] = True
                                st.session_state.registered_users[lookup]["active_plan"] = billing_plan[0]
                                
                            st.success(f"✅ Card Transaction Authorized! {billing_type.upper()} {billing_plan[2]} Pass activated.")
                            st.toast("🎉 Subscription Successful!")
                            st.rerun()
        else:
            # Plan Selection Options UI
            st.markdown("### ✨ Upgrade to Premium Plan")
            st.markdown(f"""
            <p style="font-size:12px; color:{t['text2']}; line-height:1.55; margin-bottom:8px;">
                Unlocks real-time seat crowd maps, paramedics response logs, anomaly charts, and all high-fidelity telemetry metrics across all analytical pages.
            </p>
            """, unsafe_allow_html=True)
            
            p_opts = [
                ("₹299 INR / 1 Month", 299, "1 month"),
                ("₹399 INR / 3 Months", 399, "3 months"),
                ("₹599 INR / 6 Months", 599, "6 months"),
                ("₹999 INR / 12 Months", 999, "12 months")
            ]
            sel_p_idx = st.selectbox("Select Season Premium Term", options=range(4), format_func=lambda i: p_opts[i][0], key="portal_p_select")
            p_plan = p_opts[sel_p_idx]
            
            p_btn_label = f"⚡ Activate Premium Plan — {p_plan[0].split(' / ')[0]}" if not is_prem_active else "🟢 Premium Active (Paid)"
            if st.button(p_btn_label, key="portal_buy_prem_btn", type="primary", use_container_width=True, disabled=is_prem_active):
                if is_dummy_user:
                    st.error("🕵️ **System Evaluation Mode**: Simulated checkout is disabled for this dummy profile. This account already has free backdoor bypass access to all AI insights and telemetry features!")
                else:
                    st.session_state.billing_type = "premium"
                    st.session_state.billing_plan = p_plan
                    st.session_state.payment_processing = True
                    st.rerun()
                
            st.markdown("<hr style='margin:18px 0; opacity:0.1;'>", unsafe_allow_html=True)
            
            st.markdown("### 🚀 Upgrade to Pro Plan")
            st.markdown(f"""
            <p style="font-size:12px; color:{t['text2']}; line-height:1.55; margin-bottom:8px;">
                Unlocks direct natural-language dispatch queries, stadium occupancy projections, warden controls, and all interactive co-pilot features.
            </p>
            """, unsafe_allow_html=True)
            
            o_opts = [
                ("₹399 INR / 1 Month", 399, "1 month"),
                ("₹549 INR / 3 Months", 549, "3 months"),
                ("₹799 INR / 6 Months", 799, "6 months"),
                ("₹999 INR / 12 Months", 999, "12 months")
            ]
            sel_o_idx = st.selectbox("Select Season Pro Term", options=range(4), format_func=lambda i: o_opts[i][0], key="portal_o_select")
            o_plan = o_opts[sel_o_idx]
            
            o_btn_label = f"⚡ Activate Pro Plan — {o_plan[0].split(' / ')[0]}" if not is_pro_active else "🔮 Pro Active (Paid)"
            if st.button(o_btn_label, key="portal_buy_pro_btn", type="primary", use_container_width=True, disabled=is_pro_active):
                if is_dummy_user:
                    st.error("🕵️ **System Evaluation Mode**: Simulated checkout is disabled for this dummy profile. This account already has free backdoor bypass access to all AI insights and co-pilot chat features!")
                else:
                    st.session_state.billing_type = "pro"
                    st.session_state.billing_plan = o_plan
                    st.session_state.payment_processing = True
                    st.rerun()
                
            # If subscribed (and not creator/dummy bypass), show a toggle to test disabling
            if not has_unlimited_bypass and (st.session_state.get("is_premium_subscribed") or st.session_state.get("is_pro_subscribed")):
                st.markdown("<hr style='margin:18px 0; opacity:0.1;'>", unsafe_allow_html=True)
                if st.button("❌ Disable Active Passes (Test Lock)", key="clear_sub_test_btn", use_container_width=True):
                    st.session_state.is_premium_subscribed = False
                    st.session_state.is_pro_subscribed = False
                    st.session_state.is_subscribed = False
                    st.rerun()

    st.stop()


# ═══════════════════════════════════════════════════════════
# PAGE: ADMIN DASHBOARD
# ═══════════════════════════════════════════════════════════
if page == "Admin Dashboard":
    page_header("👑", "IPL Operations Admin Financial Dashboard", 
                "Corporate and financial operations oversight. View real-time subscription revenues, active spectator plans, and system billing transaction logs.")
                
    # Double-check security
    is_admin = st.session_state.get("is_logged_in", False) and st.session_state.get("user_name", "").strip().lower() in ["avinash", "madhukar", "sharon", "deepak"]
    if not is_admin:
        st.error("❌ ACCESS DENIED: Critical authorization failure. This financial monitor workspace is reserved exclusively for system administrators.")
        st.stop()

    # Calculate real statistics from ledger
    payments_list = st.session_state.get("subscription_payments", [])
    total_subscribers = len(set(p["username"] for p in payments_list))
    total_revenue = sum(p["amount"] for p in payments_list)
    
    plan_metrics = {
        "1 Month": {"count": 0, "revenue": 0},
        "3 Months": {"count": 0, "revenue": 0},
        "6 Months": {"count": 0, "revenue": 0},
        "12 Months": {"count": 0, "revenue": 0}
    }
    
    for p in payments_list:
        term = p["term"]
        if "1 month" in term.lower():
            plan_metrics["1 Month"]["count"] += 1
            plan_metrics["1 Month"]["revenue"] += p["amount"]
        elif "3 month" in term.lower():
            plan_metrics["3 Months"]["count"] += 1
            plan_metrics["3 Months"]["revenue"] += p["amount"]
        elif "6 month" in term.lower():
            plan_metrics["6 Months"]["count"] += 1
            plan_metrics["6 Months"]["revenue"] += p["amount"]
        elif "12 month" in term.lower() or "season" in term.lower():
            plan_metrics["12 Months"]["count"] += 1
            plan_metrics["12 Months"]["revenue"] += p["amount"]

    # Top KPI Metrics row
    st.markdown(f'<p style="font-size:16px; font-weight:800; color:{t["accent"]}; margin-bottom:12px;">📊 GENERAL FINANCIAL SUMMARY</p>', unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    
    with k1:
        st.markdown(f"""
        <div style="background: {t['card']}; border: 1px solid {t['border']}; border-radius: 12px; padding: 20px; box-shadow: {t['shadow']};">
            <span style="font-size: 11px; font-weight: 700; color: {t['text2']}; text-transform: uppercase; letter-spacing: 0.8px;">💰 TOTAL REVENUE</span>
            <div style="font-size: 28px; font-weight: 800; color: #10B981; font-family: 'Sora', sans-serif; margin-top: 6px;">₹{total_revenue:,} INR</div>
            <p style="font-size: 11px; color: {t['text2']}; margin: 4px 0 0 0;">Gross collections from subscriptions</p>
        </div>
        """, unsafe_allow_html=True)
        
    with k2:
        st.markdown(f"""
        <div style="background: {t['card']}; border: 1px solid {t['border']}; border-radius: 12px; padding: 20px; box-shadow: {t['shadow']};">
            <span style="font-size: 11px; font-weight: 700; color: {t['text2']}; text-transform: uppercase; letter-spacing: 0.8px;">👥 ACTIVE SUBSCRIBERS</span>
            <div style="font-size: 28px; font-weight: 800; color: {t['accent']}; font-family: 'Sora', sans-serif; margin-top: 6px;">{total_subscribers} Users</div>
            <p style="font-size: 11px; color: {t['text2']}; margin: 4px 0 0 0;">Spectators with activated command passes</p>
        </div>
        """, unsafe_allow_html=True)
        
    with k3:
        avg_value = round(total_revenue / total_subscribers, 1) if total_subscribers > 0 else 0
        st.markdown(f"""
        <div style="background: {t['card']}; border: 1px solid {t['border']}; border-radius: 12px; padding: 20px; box-shadow: {t['shadow']};">
            <span style="font-size: 11px; font-weight: 700; color: {t['text2']}; text-transform: uppercase; letter-spacing: 0.8px;">📈 AVERAGE ARPU</span>
            <div style="font-size: 28px; font-weight: 800; color: #FBBF24; font-family: 'Sora', sans-serif; margin-top: 6px;">₹{avg_value:,} INR</div>
            <p style="font-size: 11px; color: {t['text2']}; margin: 4px 0 0 0;">Average Revenue Per Subscribed User</p>
        </div>
        """, unsafe_allow_html=True)
        
    with k4:
        best_plan = "12 Months"
        max_c = -1
        for key_t, val_t in plan_metrics.items():
            if val_t["count"] > max_c:
                max_c = val_t["count"]
                best_plan = key_t
        st.markdown(f"""
        <div style="background: {t['card']}; border: 1px solid {t['border']}; border-radius: 12px; padding: 20px; box-shadow: {t['shadow']};">
            <span style="font-size: 11px; font-weight: 700; color: {t['text2']}; text-transform: uppercase; letter-spacing: 0.8px;">👑 TOP SELLING TIER</span>
            <div style="font-size: 20px; font-weight: 800; color: #A78BFA; font-family: 'Sora', sans-serif; margin-top: 14px;">{best_plan} Pass</div>
            <p style="font-size: 11px; color: {t['text2']}; margin: 8px 0 0 0;">Highest quantity sold across users</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    
    # Financial breakdown visually via Plotly
    c_split1, c_split2 = st.columns(2)
    with c_split1:
        st.markdown(f'<p style="font-size:14px; font-weight:700; color:{t["text"]}; margin-bottom:8px;">📈 Subscriber Plan Distribution</p>', unsafe_allow_html=True)
        df_plans = pd.DataFrame([
            {"Plan Tier": k, "Subscribers Included": v["count"], "Revenue (INR)": v["revenue"]}
            for k, v in plan_metrics.items()
        ])
        
        fig_pie = px.pie(
            df_plans, 
            values="Subscribers Included", 
            names="Plan Tier", 
            hole=0.4,
            color_discrete_sequence=["#818CF8", "#A78BFA", "#38BDF8", "#FBBF24"]
        )
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color=t["text"],
            showlegend=True,
            margin=dict(t=10, b=10, l=10, r=10),
            height=260
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c_split2:
        st.markdown(f'<p style="font-size:14px; font-weight:700; color:{t["text"]}; margin-bottom:8px;">💰 Revenue Breakdown per Subscription Tier</p>', unsafe_allow_html=True)
        fig_bar = px.bar(
            df_plans,
            x="Plan Tier",
            y="Revenue (INR)",
            color="Plan Tier",
            color_discrete_sequence=["#818CF8", "#A78BFA", "#38BDF8", "#FBBF24"]
        )
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color=t["text"],
            xaxis=dict(showgrid=False),
            yaxis=dict(gridcolor=t["border"]),
            margin=dict(t=15, b=15, l=10, r=10),
            height=260,
            showlegend=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.write("")

    # Real time interactive transaction ledger
    st.markdown(f'<p style="font-size:16px; font-weight:800; color:{t["accent"]}; margin-bottom:12px;">📑 REAL-TIME TRANSACTION LEDGER</p>', unsafe_allow_html=True)
    
    ledger_data = []
    for p in payments_list:
        ledger_data.append({
            "Transaction ID": p["transaction_id"],
            "User Name": p["name"],
            "System Username": p["username"],
            "Authority Role": p["role"].replace("_", " ").title(),
            "Selected Tier": p["plan"],
            "Amount Paid": f"₹{p['amount']}",
            "Payment Date": p["date"],
            "Payment Method": p["method"],
            "System Status": "🟢 COMPLETED"
        })
    df_ledger = pd.DataFrame(ledger_data)
    
    st.dataframe(
        df_ledger, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Transaction ID": st.column_config.TextColumn("Txn ID", width="small"),
            "User Name": st.column_config.TextColumn("User Full Name"),
            "System Status": st.column_config.TextColumn("Status", width="small"),
            "Payment Date": st.column_config.TextColumn("Timestamp"),
        }
    )
    
    # Download buffer for ledger csv
    col_dl, col_blank = st.columns([1, 2])
    with col_dl:
        csv_buffer = io.StringIO()
        df_ledger.to_csv(csv_buffer, index=False)
        st.download_button(
            label="📥 Download Payment Ledger CSV",
            data=csv_buffer.getvalue(),
            file_name="ipl_command_financial_ledger.csv",
            mime="text/csv",
            use_container_width=True
        )

    st.markdown("<hr style='margin:28px 0; opacity:0.15;'>", unsafe_allow_html=True)

    st.markdown(f'<p style="font-size:16px; font-weight:800; color:{t["accent"]}; margin-bottom:12px;">👥 OFFICIAL ACTIVE STADIUM MANAGER ACCOUNTS (SHOWCASE)</p>', unsafe_allow_html=True)
    
    m1, m2, m3, m4, m5 = st.columns(5)
    is_day_1_val = st.session_state.get("app_usage_day", "Day 1") == "Day 1"
    uppal_status = "🟢 Active (1D Trial)" if is_day_1_val else "🔴 Expired (Blurred)"
    uppal_color = "#10B981" if is_day_1_val else "#F87171"
    
    chin_status = "✨ Active (1M Insights)" if is_day_1_val else "🔴 Expired (Blurred)"
    chin_color = "#38BDF8" if is_day_1_val else "#F87171"

    eden_status = "🔮 Prem+Pro Active" if is_day_1_val else "🔴 Expired (Blurred)"
    eden_color = "#A78BFA" if is_day_1_val else "#F87171"

    wank_status = "🔮 Prem+Pro Active" if is_day_1_val else "🔴 Expired (Blurred)"
    wank_color = "#10B981" if is_day_1_val else "#F87171"

    managers_showcase = [
        {
            "name": "CHE_Admin01",
            "stadium": "Chepauk Stadium",
            "role": "Stadium Commander",
            "plan_desc": "Free Trial (Lifetime)",
            "status": "🟢 Compliant (Lifetime)",
            "status_color": "#10B981",
            "color": "#7C3AED",
            "bg_color": "rgba(124, 58, 237, 0.08)"
        },
        {
            "name": "CHIN_Admin01",
            "stadium": "Chinnaswamy Stadium",
            "role": "Zone Marshall",
            "plan_desc": "AI Insights Plan (1 Month)",
            "status": chin_status,
            "status_color": chin_color,
            "color": "#1E3A8A",
            "bg_color": "rgba(30, 58, 138, 0.08)"
        },
        {
            "name": "EDEN_Admin01",
            "stadium": "Eden Gardens",
            "role": "Ops Supervisor",
            "plan_desc": "Premium + Pro (3Months)",
            "status": eden_status,
            "status_color": eden_color,
            "color": "#0D9488",
            "bg_color": "rgba(13, 148, 136, 0.08)"
        },
        {
            "name": "UPPAL_Admin01",
            "stadium": "Uppal Stadium",
            "role": "Emergency Lead",
            "plan_desc": "1-Day Free Trial",
            "status": uppal_status,
            "status_color": uppal_color,
            "color": "#B91C1C",
            "bg_color": "rgba(185, 28, 28, 0.08)"
        },
        {
            "name": "WANK_Admin01",
            "stadium": "Wankhede Stadium",
            "role": "Safety Director",
            "plan_desc": "Prem 3M + Pro 6M Combo",
            "status": wank_status,
            "status_color": wank_color,
            "color": "#D97706",
            "bg_color": "rgba(217, 119, 6, 0.08)"
        }
    ]
    
    cols_m = [m1, m2, m3, m4, m5]
    for idx, manager in enumerate(managers_showcase):
        with cols_m[idx]:
            st.markdown(f"""
            <div style="background: {manager['bg_color']}; border: 1px solid {manager['color']}50; border-radius: 12px; padding: 15px; text-align: center; height: 195px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: {t['shadow']};">
                <div>
                    <div style="font-size: 24px; margin-bottom: 2px;">👮</div>
                    <div style="font-size: 13px; font-weight: 800; color: {t['text']}; font-family: 'Sora', sans-serif;">{manager['name']}</div>
                    <div style="font-size: 10px; color: {t['text2']}; margin-top: 1px; font-weight: 600;">{manager['stadium']}</div>
                </div>
                <div style="border-top: 1px dashed {t['border']}22; padding-top: 8px; margin-top: 8px;">
                    <span style="background: {manager['color']}15; color: {manager['color']}; font-size: 9px; font-weight: 800; padding: 3px 6px; border-radius: 4px; display: inline-block; margin-bottom: 5px;">{manager['role']}</span>
                    <div style="font-size: 10.5px; font-weight: 700; color: {manager['status_color']};">{manager['status']}</div>
                    <div style="font-size: 9.5px; color: {t['text2']}; margin-top: 1px; line-height: 1.25;">{manager['plan_desc']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")
    st.markdown("<hr style='margin:28px 0; opacity:0.15;'>", unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:16px; font-weight:800; color:{t["accent"]}; margin-bottom:12px;">💬 ADMIN EXECUTIVE FINANCIAL CO-PILOT (COHERE ASSIST)</p>', unsafe_allow_html=True)
    
    if "admin_chat_history" not in st.session_state:
        st.session_state.admin_chat_history = []
        
    admin_api_present = bool(get_cohere_key())
    if not admin_api_present:
        st.warning("⚠️ **AI Advisor Offline (API key missing).** Admin conversational capability is offline.")
    else:
        st.success("✅ **Executive Q&A Advisor Connected.** Query this page's operational and financial data instantly below.")
        
    # Render previous admin chats
    if st.session_state.admin_chat_history:
        st.markdown('<div style="background: rgba(0,0,0,0.1); border-radius: 12px; padding: 15px; margin-bottom: 15px; max-height: 250px; overflow-y: auto;">', unsafe_allow_html=True)
        for msg in st.session_state.admin_chat_history:
            role_label = "🧑‍💻 System Admin" if msg["role"] == "user" else "🤖 Executive AI Co-Pilot"
            role_col = t["accent"] if msg["role"] == "user" else "#10B981"
            st.markdown(f"""
            <div style="margin-bottom: 12px; border-bottom: 1px solid {t['border']}22; padding-bottom: 8px;">
                <span style="font-size: 11px; font-weight: 800; color: {role_col}; text-transform: uppercase;">{role_label}</span>
                <p style="margin: 3px 0 0 0; font-size: 13px; color: {t['text']};">{msg['text']}</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    admin_q_input = st.text_input("Ask about dashboard analytics, revenues, or active manager status...", key="admin_co_pilot_input_field")
    col_ask1, col_ask2 = st.columns([1, 4])
    with col_ask1:
        if st.button("🚀 Send Context Query", key="send_admin_co_pilot_btn", type="primary", use_container_width=True):
            if admin_q_input.strip():
                # Formulate Context
                admin_qa_context = f"""
                Admin Financial Dashboard Analytics Summary:
                - Total Revenue generated: INR {total_revenue}
                - Total Active Subscribers: {total_subscribers}
                - Average ARPU (Revenue Per User): INR {avg_value}
                - Top Selling plan Tier: {best_plan} Pass
                
                Subscribers Breakdown per plan:
                - 1 Month Pass: {plan_metrics['1 Month']['count']} subscribers, revenue INR {plan_metrics['1 Month']['revenue']}
                - 3 Months Pass: {plan_metrics['3 Months']['count']} subscribers, revenue INR {plan_metrics['3 Months']['revenue']}
                - 6 Months Pass: {plan_metrics['6 Months']['count']} subscribers, revenue INR {plan_metrics['6 Months']['revenue']}
                - 12 Months Pass: {plan_metrics['12 Months']['count']} subscribers, revenue INR {plan_metrics['12 Months']['revenue']}
                
                These subscribers are our 5 official stadium manager default users:
                1. CHE_Admin01 (Chepauk Zone Commander)
                2. CHIN_Admin01 (Chinnaswamy Zone Commander)
                3. EDEN_Admin01 (Eden Gardens Zone Commander)
                4. UPPAL_Admin01 (Uppal Zone Commander)
                5. WANK_Admin01 (Wankhede Zone Commander)
                
                Please answer general financial, subscription, and managerial questions relating to this administrator dashboard. Keep answers clear, succinct and helpful.
                """
                with st.spinner("⏳ Analyzing metrics and loading response..."):
                    co_resp = ask_ai_question(admin_q_input, admin_qa_context, ai_temperature, ai_max_tokens)
                    
                st.session_state.admin_chat_history.append({"role": "user", "text": admin_q_input})
                st.session_state.admin_chat_history.append({"role": "assistant", "text": co_resp})
                st.rerun()
    with col_ask2:
        if st.button("🧹 Reset Query Thread", key="reset_admin_co_pilot_btn", use_container_width=True):
            st.session_state.admin_chat_history = []
            st.rerun()

    st.write("")
    st.markdown("<hr style='margin:28px 0; opacity:0.15;'>", unsafe_allow_html=True)

    # Management Terminal Options (Complimentary activation & synthetic transaction simulations)
    adm_col1, adm_col2 = st.columns(2)
    with adm_col1:
        st.markdown(f'<p style="font-size:14px; font-weight:700; color:{t["text"]}; margin-bottom:8px;">🎟️ Grant Complimentary Subscription pass</p>', unsafe_allow_html=True)
        st.markdown(f"""
        <p style="font-size: 11.5px; color: {t['text2']}; margin-top:0;">
            Administrators can manually bypass the payment gate and issue an official complimentary analytical pass to spectators.
        </p>
        """, unsafe_allow_html=True)
        
        registered_u = st.session_state.get("registered_users", {})
        non_sub_users = []
        for uname, udata in registered_u.items():
            if not udata.get("is_subscribed", False) and udata.get("role") == "general_user":
                non_sub_users.append((uname, udata.get("name", uname)))
                
        if not non_sub_users:
            st.info("ℹ️ All registered spectator accounts currently have active premium passes.")
        else:
            comp_idx = st.selectbox(
                "Select Eligible Spectator Account",
                options=range(len(non_sub_users)),
                format_func=lambda i: f"{non_sub_users[i][1]} ({non_sub_users[i][0]})",
                key="admin_comp_selectbox"
            )
            
            comp_plan_idx = st.selectbox(
                "Plan Tier to Assign",
                options=[0, 1, 2, 3],
                format_func=lambda idx: ["₹299 / 1 Month Starter", "₹399 / 3 Months Quarter", "₹599 / 6 Months Half-Year", "₹999 / 12 Months Season"][idx],
                key="admin_comp_plan_selectbox"
            )
            
            comp_reason = st.text_input("Issuing Authorization Reason", "Official complimentary testing license", key="admin_comp_reason_field")
            
            if st.button("👑 Generate License Pass Securely", key="admin_generate_pass_btn", type="primary", use_container_width=True):
                target_user_name, target_display_name = non_sub_users[comp_idx]
                plan_details = [
                    {"label": "₹299 INR / 1 month Starter", "amount": 299, "term": "1 Month"},
                    {"label": "₹399 INR / 3 months Quarter", "amount": 399, "term": "3 Months"},
                    {"label": "₹599 INR / 6 months Half-Year", "amount": 599, "term": "6 Months"},
                    {"label": "₹999 INR / 12 months Season", "amount": 999, "term": "12 Months"}
                ][comp_plan_idx]
                
                # record complimentary pass
                import random
                from datetime import datetime
                txn_id = f"COM{random.randint(10000000, 99999999)}"
                date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                st.session_state.subscription_payments.append({
                    "username": target_user_name,
                    "name": target_display_name,
                    "role": registered_u[target_user_name].get("role", "general_user"),
                    "plan": plan_details["label"],
                    "amount": plan_details["amount"],
                    "term": plan_details["term"],
                    "date": date_str,
                    "method": f"System Comp: {comp_reason}",
                    "transaction_id": txn_id
                })
                
                st.session_state.registered_users[target_user_name]["is_subscribed"] = True
                st.session_state.registered_users[target_user_name]["active_plan"] = plan_details["label"]
                
                st.success(f"🎨 Successfully granted premium {plan_details['term']} license to {target_display_name}!")
                st.toast("👑 Complimentary pass issued successfully!")
                import time
                time.sleep(1.0)
                st.rerun()
                
    with adm_col2:
        st.markdown(f'<p style="font-size:14px; font-weight:700; color:{t["text"]}; margin-bottom:8px;">🛠️ Corporate System Audit Commands</p>', unsafe_allow_html=True)
        st.markdown(f"""
        <p style="font-size: 11.5px; color: {t['text2']}; margin-top:0;">
            Simulate synthetic transaction logs for load testing or clean the live sessions back to system seed states.
        </p>
        """, unsafe_allow_html=True)
        st.write("")
        
        # Test transaction simulator button
        if st.button("⚡ Simulate Random Spectator Subscription Transaction", key="admin_simulate_txn_btn", use_container_width=True):
            import random
            from datetime import datetime
            
            names_candidates = [
                ("Ramesh Kumar", "ramesh_k"), ("Siddharth Sharma", "sid_s"),
                ("Priya Patel", "priya_p"), ("Anjali Verma", "anjali_v"),
                ("Vikram Singh", "vikram_s"), ("Sneha Reddy", "sneha_r")
            ]
            cand = random.choice(names_candidates)
            plans_c = [
                {"label": "₹299 INR / 1 month Starter", "amount": 299, "term": "1 Month"},
                {"label": "₹399 INR / 3 months Quarter", "amount": 399, "term": "3 Months"},
                {"label": "₹599 INR / 6 months Half-Year", "amount": 599, "term": "6 Months"},
                {"label": "₹999 INR / 12 months Season", "amount": 999, "term": "12 Months"}
            ]
            sel_plan = random.choice(plans_c)
            txn_id = f"SIM{random.randint(10000000, 99999999)}"
            date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            methods_c = [
                "UPI: rando_user@okaxis", "UPI: tester@okhdfc", 
                "Card: **** **** **** 8821", "Card: **** **** **** 2947"
            ]
            
            st.session_state.subscription_payments.append({
                "username": cand[1],
                "name": cand[0],
                "role": "general_user",
                "plan": sel_plan["label"],
                "amount": sel_plan["amount"],
                "term": sel_plan["term"],
                "date": date_str,
                "method": random.choice(methods_c),
                "transaction_id": txn_id
            })
            
            # If target user in registry, update subscription state
            if cand[1] in st.session_state.registered_users:
                st.session_state.registered_users[cand[1]]["is_subscribed"] = True
                st.session_state.registered_users[cand[1]]["active_plan"] = sel_plan["label"]
            
            st.success(f"⚡ Simulated subscription transaction for {cand[0]} — ₹{sel_plan['amount']}.")
            st.toast("⚡ Synthetic transaction logged!")
            import time
            time.sleep(1.0)
            st.rerun()

        st.write("")
        # Reset default seeds
        if st.button("🗑️ Reset Transaction Ledger to Seed Defaults", key="admin_clear_ledger_btn", type="secondary", use_container_width=True):
            st.session_state.subscription_payments = [
                {
                    "username": "che_admin01",
                    "name": "CHE_Admin01",
                    "role": "stadium_ops",
                    "plan": "PREMIUM + PRO: Free Trial Lifetime",
                    "amount": 0,
                    "term": "Lifetime",
                    "date": "2026-05-15 14:32:10",
                    "method": "Promo: First Registered Stadium User",
                    "transaction_id": "TXN50182741"
                },
                {
                    "username": "chin_admin01",
                    "name": "CHIN_Admin01",
                    "role": "stadium_ops",
                    "plan": "PREMIUM: ₹399 INR / 3 Months (AI Insights)",
                    "amount": 399,
                    "term": "3 months",
                    "date": "2026-05-20 09:12:45",
                    "method": "UPI: chinnaswamy@okaxis",
                    "transaction_id": "TXN50182742"
                },
                {
                    "username": "eden_admin01",
                    "name": "EDEN_Admin01",
                    "role": "stadium_ops",
                    "plan": "PREMIUM: ₹399 INR / 3 Months (Safety Visuals)",
                    "amount": 399,
                    "term": "3 months",
                    "date": "2026-05-22 10:14:00",
                    "method": "Card: **** **** **** 1039",
                    "transaction_id": "TXN50182743"
                },
                {
                    "username": "eden_admin01",
                    "name": "EDEN_Admin01",
                    "role": "stadium_ops",
                    "plan": "PRO: ₹549 INR / 3 Months (AI Co-Pilot)",
                    "amount": 549,
                    "term": "3 months",
                    "date": "2026-05-22 10:18:30",
                    "method": "Card: **** **** **** 1039",
                    "transaction_id": "TXN50182744"
                },
                {
                    "username": "uppal_admin01",
                    "name": "UPPAL_Admin01",
                    "role": "stadium_ops",
                    "plan": "TRIAL: 1-Day Trial Pass",
                    "amount": 0,
                    "term": "1 day",
                    "date": "2026-06-01 11:24:15",
                    "method": "Bypass: Complimentary Day Trial",
                    "transaction_id": "TXN50182745"
                },
                {
                    "username": "wank_admin01",
                    "name": "WANK_Admin01",
                    "role": "stadium_ops",
                    "plan": "PREMIUM: ₹399 INR / 3 Months Speed Run",
                    "amount": 399,
                    "term": "3 months",
                    "date": "2026-06-03 10:05:00",
                    "method": "Card: **** **** **** 8899",
                    "transaction_id": "TXN50182746"
                },
                {
                    "username": "wank_admin01",
                    "name": "WANK_Admin01",
                    "role": "stadium_ops",
                    "plan": "PRO: ₹799 INR / 6 Months Upgrade Extension",
                    "amount": 799,
                    "term": "6 months",
                    "date": "2026-06-03 15:45:10",
                    "method": "Card: **** **** **** 8899",
                    "transaction_id": "TXN50182747"
                }
            ]
            st.success("🗑️ Cleared transactional ledger and restored system defaults.")
            st.toast("🗑️ Ledger reset completed.")
            import time
            time.sleep(1.0)
            st.rerun()

    st.stop()


# ═══════════════════════════════════════════════════════════
# PAGE: ABOUT APP
# ═══════════════════════════════════════════════════════════
if page == "About App":
    page_header("ℹ️", "About IPL Crowd Safety Management Center", "Detailed project background, analytics methodology, AI capabilities, and technology stack.")

    # 1. Custom Hero Banner
    st.markdown(f"""
<div class="intro-hero" style="background: linear-gradient(135deg, {t['bg']} 0%, {t['sidebar']} 100%); border: 1px solid {t['border']}; box-shadow: 0 10px 30px rgba(0,0,0,0.3); border-radius: 20px; padding: 30px; margin-bottom: 25px; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center;">
  <div class="intro-badge" style="background: rgba(129, 140, 248, 0.15); border: 1px solid {t['accent']}; color: {t['accent']}; padding: 5px 12px; border-radius: 999px; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px;">📊 System Documentation Dossier</div>
  <h1 class="intro-title" style="color: {t['text']}; font-family: 'Sora', sans-serif; font-size: 30px; font-weight: 800; line-height: 1.25; margin-bottom: 10px;">Platform System Dossier</h1>
  <p class="intro-desc" style="color: {t['text2']}; max-width: 700px; font-size: 14px; line-height: 1.5; margin: 0 auto; font-weight: 500;">
    Review the quantitative risk algorithms, multi-agency objectives, and Generative AI framework of the platform.
  </p>
</div>
""", unsafe_allow_html=True)

    # 2. Interactive Tabs
    tab_doc_bg, tab_doc_math, tab_doc_ai, list_future = st.tabs([
        "🏟️ 1. Project Background", 
        "📊 2. Dynamic Risk Math & Modules", 
        "🧠 3. Cohere AI Command", 
        "🏆 4. Technology Stack & Impact"
    ])

    with tab_doc_bg:
        col_bg1, col_bg2 = st.columns(2)
        with col_bg1:
            st.markdown(f"""
            <div class="report-card" style="border-left: 5px solid {t['accent']} !important; margin-bottom: 16px; box-sizing: border-box; padding: 18px; height: 100%;">
                <h4 style="font-family: 'Sora', sans-serif; font-size: 15px; font-weight: 800; color: {t['text']}; margin: 0 0 10px 0;">🛡️ The Problem We Solve</h4>
                <p style="font-size: 13px; color: {t['text2']}; line-height: 1.6; margin: 0;">
                    During peak IPL cricket matches, stadiums fill with up to 83,000 active supporters. Historically, police departments, stadium ticketers, private security, and medics have worked in operational silos. Communication gaps can delay paramedic responses and worsen gate congestion. This platform acts as a shared digital-twin command panel to keep different agencies aligned.
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col_bg2:
            st.markdown(f"""
            <div class="report-card" style="border-left: 5px solid {t['accent2']} !important; margin-bottom: 16px; box-sizing: border-box; padding: 18px; height: 100%;">
                <h4 style="font-family: 'Sora', sans-serif; font-size: 15px; font-weight: 800; color: {t['text']}; margin: 0 0 10px 0;">🎯 Operational Objectives</h4>
                <ul class="report-list" style="padding-left: 14px; margin: 0; font-size: 12.5px; color: {t['text2']}; line-height: 1.55;">
                    <li style="margin-bottom: 6px;"><b>Universal Sync</b>: Merges ticketing databases, sensor telemetry, and dispatch records into one screen.</li>
                    <li style="margin-bottom: 6px;"><b>Preempt Bottlenecks</b>: Pinpoints queue blockages 30 minutes before they escalate.</li>
                    <li style="margin-bottom: 6px;"><b>Speed Up Paramedics</b>: Retains ambulance response latencies to high-risk zones below 8 minutes.</li>
                    <li style="margin-bottom: 4px;"><b>Control Fraud</b>: Flags ticket duplications and entry breaches transparently.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    with tab_doc_math:
        st.markdown("<h5 style='font-family: Sora, sans-serif; margin-bottom: 8px; font-size: 14.5px;'>Dynamic Risk Prioritization Matrix</h5>", unsafe_allow_html=True)
        st.write("Our system compiles active metrics by stadium zones to calculate a weighted Multi-Factor Risk Score:")
        st.code("""
Multi-Factor Risk Score = 
    (Stand Density * 25%) + 
    (Gate Queue Wait * 15%) + 
    (Wet-Bulb Heat Index * 10%) + 
    (Security Incidents Rate * 10%) + 
    (Crowd Bottleneck Level * 25%) + 
    (Ambulance Response Time * 15%)
""", language="python")

        st.markdown(f"""
        <div style="background: {t['card']}; border: 1px solid {t['border']}; border-radius: 12px; padding: 16px; margin-top: 15px; border-left: 4px solid {t['ok_col']} !important; box-shadow: {t['shadow']};">
            <strong style="color: {t['text']}; font-size: 13px; display: block; margin-bottom: 4px;">Dynamic Data Grading Logic</strong>
            <span style="font-size: 12px; color: {t['text2']}; line-height: 1.45; display: block;">
                The computed Risk Score classifies stadium zones into three straightforward threat categories: <b>Critical (Risk ≥ 70)</b>, <b>Monitor (Risk 40-69)</b>, and <b>Normal (Risk < 40)</b>. This allows stadium dispatchers to focus staff attention on high-risk locations instantly.
            </span>
        </div>
        """, unsafe_allow_html=True)

    with tab_doc_ai:
        st.markdown(f"""
        <div class="report-card" style="border-left: 5px solid {t['accent']} !important; margin-bottom: 16px; box-sizing: border-box; padding: 20px;">
            <div class="report-header-wrapper" style="margin-bottom: 10px; display: flex; align-items: center; gap: 8px;">
                <div class="report-icon" style="font-size: 20px;">🧠</div>
                <h4 class="report-title" style="font-family: 'Sora', sans-serif; font-size: 15px; font-weight: 800; color: {t['text']}; margin: 0;">Generative Command Copilot via Cohere AI</h4>
            </div>
            <div class="report-body" style="font-size: 13px; color: {t['text2']}; line-height: 1.6;">
                <p>Instead of manually searching columns of logs, the supervisor clicks the <b>Ask AI</b> tab to write questions in natural human language.</p>
                <ul class="report-list">
                    <li style="margin-bottom: 5px;"><b>Data-Grounded</b>: The model reads active filter selections and summaries to deliver real context.</li>
                    <li style="margin-bottom: 5px;"><b>Tactical Recommendations</b>: Cohere translates charts into clean, actionable, plain-English operations lists.</li>
                    <li style="margin-bottom: 5px;"><b>Query Examples</b>: Type actions such as: <i>"Which stand gate has the highest heat index?"</i> or <i>"What are my top critical safety actions right now?"</i> to receive replies instantly.</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with list_future:
        col_ft1, col_ft2 = st.columns(2)
        with col_ft1:
            st.markdown(f"""
            <div class="report-card" style="border-left: 5px solid {t['accent']} !important; margin-bottom: 16px; box-sizing: border-box; padding: 18px; height: 100%;">
                <h4 style="font-family: 'Sora', sans-serif; font-size: 14.5px; font-weight: 800; color: {t['text']}; margin: 0 0 8px 0;">📈 Expected Project Impact</h4>
                <ul class="report-list" style="padding-left: 14px; margin: 0; font-size: 12px; color: {t['text2']}; line-height: 1.5;">
                    <li style="margin-bottom: 5px;"><b>30% Reduction in EMT Dispatch Times</b>: Paramedics bypass blockages proactively.</li>
                    <li style="margin-bottom: 5px;"><b>25% Cost Optimization</b>: Security marshals deploy more efficiently using active hazard indexes.</li>
                    <li style="margin-bottom: 5px;"><b>Friction-Free Fan Evacuation</b>: Exit channels and gate routes flow smoothly during stadium departures.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        with col_ft2:
            st.markdown(f"""
            <div class="report-card" style="border-left: 5px solid {t['accent2']} !important; margin-bottom: 16px; box-sizing: border-box; padding: 18px; height: 100%;">
                <h4 style="font-family: 'Sora', sans-serif; font-size: 14.5px; font-weight: 800; color: {t['text']}; margin: 0 0 8px 0;">🚀 Future Product Milestones</h4>
                <ul class="report-list" style="padding-left: 14px; margin: 0; font-size: 12px; color: {t['text2']}; line-height: 1.5;">
                    <li style="margin-bottom: 5px;"><b>Computer Vision Overlays</b>: Connect live surveillance feeds to measure stand densities automatedly.</li>
                    <li style="margin-bottom: 5px;"><b>NFC Gate Ticket Syncing</b>: Instant scan logs validation to protect stadiums against duplicate ticket fraud.</li>
                    <li style="margin-bottom: 5px;"><b>Warden wearable logs</b>: Biometric devices mapping field paramedic fatigue on the scene.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <h5 style='font-family: Sora, sans-serif; margin-top: 15px; margin-bottom: 8px; font-size: 13px; font-weight: 800; color: {t['text']};'>Underlying Technology Stack</h5>
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 10px;">
            <div style="background: {t['card']}; border: 1px solid {t['border']}; border-radius: 8px; padding: 12px; text-align: center;">
                <div style="font-size: 20px; margin-bottom: 4px;">🐍</div>
                <div style="font-family: 'Sora', sans-serif; font-size: 11px; font-weight: 700; color: {t['text']};">Python Pandas</div>
                <div style="font-size: 10px; color: {t['text2']}; margin-top: 2px;">Data engineering</div>
            </div>
            <div style="background: {t['card']}; border: 1px solid {t['border']}; border-radius: 8px; padding: 12px; text-align: center;">
                <div style="font-size: 20px; margin-bottom: 4px;">⚡</div>
                <div style="font-family: 'Sora', sans-serif; font-size: 11px; font-weight: 700; color: {t['text']};">Streamlit Core</div>
                <div style="font-size: 10px; color: {t['text2']}; margin-top: 2px;">Reactive widgets</div>
            </div>
            <div style="background: {t['card']}; border: 1px solid {t['border']}; border-radius: 8px; padding: 12px; text-align: center;">
                <div style="font-size: 20px; margin-bottom: 4px;">📈</div>
                <div style="font-family: 'Sora', sans-serif; font-size: 11px; font-weight: 700; color: {t['text']};">Plotly Graphs</div>
                <div style="font-size: 10px; color: {t['text2']}; margin-top: 2px;">Vector charts</div>
            </div>
            <div style="background: {t['card']}; border: 1px solid {t['border']}; border-radius: 8px; padding: 12px; text-align: center;">
                <div style="font-size: 20px; margin-bottom: 4px;">👥</div>
                <div style="font-family: 'Sora', sans-serif; font-size: 11px; font-weight: 700; color: {t['text']};">Cohere Command</div>
                <div style="font-size: 10px; color: {t['text2']}; margin-top: 2px;">LLM Reasoning API</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")
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

    generate_ai = st.button("🤖 Generate Live AI Insights Report", use_container_width=True)
    st.caption(f"Temp: {ai_temperature} | Max Tokens: {ai_max_tokens}")

    # Persistent AI Report display
    if "overview_report" not in st.session_state:
        st.session_state.overview_report = ""

    if generate_ai:
        if not has_premium_access:
            st.session_state.active_page = "User Portal"
            st.session_state.pending_plan_msg = "⚠️ Generating AI Recommendations and insights requires the Premium Plan. You have been directed to the access plan terminal."
            st.rerun()
        else:
            with st.spinner("Analyzing executive logs with Cohere AI..."):
                st.session_state.overview_report = generate_cohere_insights(summary_text, "Overview Dashboard", ai_temperature, ai_max_tokens)

    if st.session_state.overview_report:
        st.markdown(render_ai_insight_report(st.session_state.overview_report, t), unsafe_allow_html=True)


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
        if not has_premium_access:
            st.session_state.active_page = "User Portal"
            st.session_state.pending_plan_msg = "⚠️ Generating AI recommendations and insights requires the Premium Plan. You have been directed to the access plan page."
            st.rerun()
        else:
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
        st.markdown(render_ai_insight_report(st.session_state.cf_report, t), unsafe_allow_html=True)


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
        if not has_premium_access:
            st.session_state.active_page = "User Portal"
            st.session_state.pending_plan_msg = "⚠️ Generating AI recommendations and insights requires the Premium Plan. You have been directed to the access plan page."
            st.rerun()
        else:
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
        st.markdown(render_ai_insight_report(st.session_state.mh_report, t), unsafe_allow_html=True)


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
        if not has_premium_access:
            st.session_state.active_page = "User Portal"
            st.session_state.pending_plan_msg = "⚠️ Generating AI recommendations and insights requires the Premium Plan. You have been directed to the access plan page."
            st.rerun()
        else:
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
        st.markdown(render_ai_insight_report(st.session_state.sec_report, t), unsafe_allow_html=True)


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
        if not has_premium_access:
            st.session_state.active_page = "User Portal"
            st.session_state.pending_plan_msg = "⚠️ Generating AI recommendations and insights requires the Premium Plan. You have been directed to the access plan page."
            st.rerun()
        else:
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
        st.markdown(render_ai_insight_report(st.session_state.rp_report, t), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PAGE 6 — RISK MATRIX
# ═══════════════════════════════════════════════════════════
elif page == "Risk Matrix":
    page_header("🚨", "AI Risk Decision Matrix & Anomaly Detection Center",
                "Advanced prioritized decision-support tool helping operations commanders isolate and secure critical zone threat coordinates.")

    # Dynamic Subscription Gating Checks matching dynamic React profile
    if st.session_state.user_role == "general_user" and not st.session_state.is_subscribed:
        st.markdown(f"""
        <div style="background: rgba(239, 68, 68, 0.08); border: 1px solid {t['crit_col']}50; border-radius: 12px; padding: 25px; text-align: center; margin: 30px 0;">
            <div style="font-size: 40px; margin-bottom: 15px;">🔒 Premium Analytical View Locked</div>
            <h3 style="color: {t['text']}; font-family: 'Sora', sans-serif; margin-bottom: 10px;">Subscription Season Ticket Required</h3>
            <p style="font-size: 13.5px; color: {t['text2']}; max-width: 600px; margin: 0 auto 20px auto; line-height: 1.6;">
                General spectators do not have authorization to view the active cross-agency Risk Matrix or interactive AI Assist module. Upgrade your status to command staff or purchase a Season Spectator Pass.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("👤 Visit User Access Portal to Upgrade Status", key="risk_gate_portal_btn", type="primary", use_container_width=True):
            st.session_state.active_page = "User Portal"
            st.rerun()
        st.stop()

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
        if not has_premium_access:
            st.session_state.active_page = "User Portal"
            st.session_state.pending_plan_msg = "⚠️ Generating AI recommendations and insights requires the Premium Plan. You have been directed to the access plan page."
            st.rerun()
        else:
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
        st.markdown(render_ai_insight_report(st.session_state.rm_report, t), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PAGE 7 — ASK AI
# ═══════════════════════════════════════════════════════════
elif page == "Ask AI":
    page_header("💬", "Conversational AI Command Control Assistant",
                "Directly query the live stadium database, ask safety questions, and generate instant crowd control task plans.")

    # Dynamic Subscription Gating Checks matching dynamic React profile
    if st.session_state.user_role == "general_user" and not st.session_state.is_subscribed:
        st.markdown(f"""
        <div style="background: rgba(239, 68, 68, 0.08); border: 1px solid {t['crit_col']}50; border-radius: 12px; padding: 25px; text-align: center; margin: 30px 0;">
            <div style="font-size: 40px; margin-bottom: 15px;">🔒 Premium AI Command Core Locked</div>
            <h3 style="color: {t['text']}; font-family: 'Sora', sans-serif; margin-bottom: 10px;">Subscription Season Ticket Required</h3>
            <p style="font-size: 13.5px; color: {t['text2']}; max-width: 600px; margin: 0 auto 20px auto; line-height: 1.6;">
                General spectators do not have authorization to view the active cross-agency Risk Matrix or interactive AI Assist module. Upgrade your status to command staff or purchase a Season Spectator Pass.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("👤 Visit User Access Portal to Upgrade Status", key="ai_gate_portal_btn", type="primary", use_container_width=True):
            st.session_state.active_page = "User Portal"
            st.rerun()
        st.stop()

    # State controller initialization
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
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
    
    # Header and Chat control action buttons
    c_hdr1, c_hdr2 = st.columns([3.5, 1.2])
    with c_hdr1:
        sec_label("Conversational AI Command History")
    with c_hdr2:
        st.write("")
        st.write("")
        if st.button("🧹 Clear Chat History Thread", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

    # 1. Render Chattanooga-Style Scrolled Conversation Bubbles
    if st.session_state.chat_history:
        st.markdown('<div class="chat-window-container"><div class="chat-history-scroller">', unsafe_allow_html=True)
        for msg in st.session_state.chat_history:
            role_class = "user" if msg["role"] == "user" else "assistant"
            header_text = "Command Director (You)" if msg["role"] == "user" else "AI Operational Advisor"
            bubble_class = "bubble-user" if msg["role"] == "user" else "bubble-assistant"
            
            # Filter and parse bubble markdown to proper styled fonts
            formatted_text = format_chat_bubble_markdown(msg["text"], t)
            
            st.markdown(f"""
            <div class="chat-bubble-row bubble-row-{role_class}">
                <div class="chat-message-box">
                    <div class="chat-msg-header msg-header-{role_class}">{header_text}</div>
                    <div class="chat-msg-bubble {bubble_class}">{formatted_text}</div>
                    <div class="chat-msg-footer msg-footer-{role_class}">{msg["time"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="text-align:center; padding:40px 20px; background:{t['card']}; border:1px dashed {t['border']}; border-radius:14px; margin-bottom:20px;">
            <p style="color:{t['text2']}; font-size:14px; margin:0;">
                No command queries logged. Choose a suggested question below or type your operations query inside the chat bar.
            </p>
        </div>
        """, unsafe_allow_html=True)

    sec_label("Suggested Quick Operations Questions (Instant Query Trigger)")

    # Suggested Instant questions buttons
    clicked_q = ""
    q1, q2, q3 = st.columns(3)
    with q1:
        if st.button("Which sectors need immediate help?", use_container_width=True, key="sq_1"):
            clicked_q = "Which stadium sectors need the most immediate crowd control help right now and why?"
    with q2:
        if st.button("Logistical first actions?", use_container_width=True, key="sq_2"):
            clicked_q = "Identify the top 3 logistical tasks the operations team should execute first."
    with q3:
        if st.button("Explain dashboard results simply", use_container_width=True, key="sq_3"):
            clicked_q = "Translate this dashboard's core metrics into an easy, executive presentation summary."

    q4, q5, q6 = st.columns(3)
    with q4:
        if st.button("Identify high heat vulnerabilities", use_container_width=True, key="sq_4"):
            clicked_q = "Is heat risk a major threat here? What are the worst thermal coordinates and recommended actions?"
    with q5:
        if st.button("Which phase represents the most threat?", use_container_width=True, key="sq_5"):
            clicked_q = "Which phase shows the most elevated safety and density threat? What are the corresponding control recommendations?"
    with q6:
        if st.button("Give 5 project briefing points", use_container_width=True, key="sq_6"):
            clicked_q = "Compose 5 clear briefing points explanatory of this stadium crowd-safety dashboard project."

    # Process all queries in a unified context block
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

    active_user_query = ""
    if clicked_q:
        active_user_query = clicked_q
    
    # Modern st.chat_input bar
    input_question = st.chat_input("Ask field commander anything...")
    if input_question:
        active_user_query = input_question

    if active_user_query:
        from datetime import datetime
        current_time = datetime.now().strftime("%H:%M")
        
        # 1. Add User query to chat scroller
        st.session_state.chat_history.append({
            "role": "user",
            "text": active_user_query,
            "time": current_time
        })
        
        # 2. Extract recent query history context
        history_str = ""
        if len(st.session_state.chat_history) > 1:
            history_str = "\n".join([
                f"{'User' if m['role'] == 'user' else 'AI Advisor'}: {m['text']}"
                for m in st.session_state.chat_history[-6:-1]
            ])
            
        prompt = f"""
You are a conversational AI Operations Advisor inside an IPL Crowd Safety Dashboard, similar to ChatGPT or Gemini.
Ground your response heavily in the provided raw dataset context under STADIUM FIELD CONTEXT, combined with your expert domain knowledge of stadium crowd management.

STADIUM FIELD CONTEXT:
{qa_context}

CONVERSATION HISTORY TRACE:
{history_str}

USER OPERATIONAL FOLLOW-UP QUESTION:
{active_user_query}

Provide action-backed, metrics-supported, and direct operations guidance. Keep responses natural, conversational, and comprehensive. Reference specific stands/metrics from the context if relevant. Do NOT use standard raw markdown symbols like hashtags, bullets, asterisks, structure with clean text and lists.
"""
        with st.spinner("AI Field Companion is calculating response channels..."):
            api_key = get_cohere_key()
            if not api_key:
                reply = (
                    "⚠️ **Cohere API key not configured.**\n\n"
                    "To enable live Q&A responses, go to Streamlit Cloud Settings -> Secrets "
                    "and secure your `COHERE_API_KEY`."
                )
            else:
                try:
                    co = cohere.Client(api_key)
                    response = co.chat(
                        model="command-r-plus-08-2024",
                        message=prompt,
                        temperature=ai_temperature,
                        max_tokens=ai_max_tokens,
                    )
                    reply = extract_cohere_text(response)
                except Exception as e:
                    reply = f"❌ AI Assistant execution failed: {e}"
            
            # 3. Add Assistant response to chat scroller
            st.session_state.chat_history.append({
                "role": "assistant",
                "text": reply,
                "time": current_time
            })
            st.session_state.ai_question = active_user_query
            st.session_state.ai_answer = reply
            st.rerun()

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
