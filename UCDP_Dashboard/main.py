import streamlit as st
from Tabs.tab_two import tab_two as t2
from Tabs.tab_three import tab_three as t3
from Tabs.tab_four import tab_four as t4

# Page Configuration
st.set_page_config(
    page_title = "",
    layout = "wide"
)

# Header
st.title("📈 Walking Frames ")
st.markdown("-> Insert description for dashboard.")

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Overview",
    "Trends (Time Series)",
    "Comparisons (Animated)",
    "Regional Analysis",
    "Geospatial Heatmaps",
    "Summary"
])

# Tab 1: Overview
with tab1:
    st.header("Overview")
    st.write("->description")
    
    # Example: Import streamlit visualisations
    st.write("Yes.....")

# Tab 2: Trends
with tab2:
    t2_inst = t2()
    t2_inst.display()

# Tab 3: Comparisons
with tab3:
    t3_inst = t3()
    t3_inst.display()

# Tab 4: Regional Analysis
with tab4:
    t4_inst = t4()
    t4_inst.display()

# Tab 5: Geospatial Heatmaps
with tab5:
    st.header("Geospatial heatmaps")
    st.write("->description")
    
    # Example: Import streamlit visualisations
    st.write("Yes.....")

# Tab 6: Summary
with tab6:
    st.header("Summary")
    st.write("->description")
    
    # Example: Import streamlit visualisations
    st.write("Yes.....")

