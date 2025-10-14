# main.py — Sidebar shows only the active view's controls
import streamlit as st
from Tabs.tab_two import tab_two as T2
from Tabs.tab_three import tab_three as T3
from Tabs.tab_four import tab_four as T4
from Tabs.tab_five import tab_five as T5

st.set_page_config(page_title="", layout="wide")
st.title("📈 Walking Frames ")
st.markdown("-> Insert description for dashboard.")

# ---- Tab registry (name -> class) ----
TABS = {
    "Overview": None,
    "Trends (Time Series)": T2,
    "Comparisons (Animated)": T3,
    "Regional Analysis": T4,
    "Geospatial Heatmaps": T5,
    "Summary": None,
}

# ---- Keep track of active tab in session state ----
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Overview"

# ---- Render a tab-like header (buttons) ----
tab_names = list(TABS.keys())
cols = st.columns(len(tab_names))
for i, name in enumerate(tab_names):
    is_active = (st.session_state.active_tab == name)
    if cols[i].button(name, type="primary" if is_active else "secondary", use_container_width=True):
        st.session_state.active_tab = name

st.markdown("---")

# ---- Clear sidebar first, then render ONLY the active view's controls ----
st.sidebar.empty()
active = st.session_state.active_tab

# ---- Render main content + per-view sidebar ----
if active == "Overview":
    st.header("Overview")
    st.write("->description")
    st.write("Yes.....")

elif active == "Trends (Time Series)":
    T2().display(st.sidebar)

elif active == "Comparisons (Animated)":
    T3().display(st.sidebar)

elif active == "Regional Analysis":
    T4().display(st.sidebar)

elif active == "Geospatial Heatmaps":
    T5().display(st.sidebar)

elif active == "Summary":
    st.header("Summary")
    st.write("->description")
    st.write("Yes.....")
