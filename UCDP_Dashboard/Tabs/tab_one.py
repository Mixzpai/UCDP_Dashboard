import streamlit as st

class tab_one:
    def display(self):
        st.header("Overview")
        st.write(
            """
            This dashboard provides an interactive exploration of **global conflict patterns**
            using data from the **Uppsala Conflict Data Program (UCDP) – Georeferenced Event Dataset (GED)**.
            It allows users to visualize how organized violence evolves over time and across regions,
            identifying trends, comparisons, and spatial concentrations of conflict activity.
            """
        )

        st.subheader("Purpose")
        st.write(
            """
            The goal of this dashboard is to **analyze temporal, spatial, and categorical dimensions**
            of violent conflicts. By combining time-series trends, regional breakdowns,
            and geospatial visualizations, the dashboard helps reveal:
            
            - 📈 Shifts in violence intensity over time  
            - ⚔️ Differences between conflict types (state-based, non-state, one-sided)  
            - 🌍 Regional hotspots and concentration of conflict activity  
            - 📊 Country-level comparisons and aggregate summaries
            """
        )

        st.subheader("Key Metric")
        st.write(
            """
            Throughout this analysis, **deaths (best estimate)** serve as the **primary quantifying metric** for measuring
            the magnitude and impact of conflicts. Each visualization and comparison is based on the
            reported number of fatalities per event, allowing for consistent cross-country and
            temporal evaluation of violence intensity.
            """
        )

        st.subheader("How to Use")
        st.write(
            """
            Use the navigation tabs above to explore each analytical dimension:
            
            - **Trends (Time Series):** Observe changes in deaths by conflict type over time  
            - **Comparisons (Animated):** Compare how different countries and violence types evolve dynamically  
            - **Regional Analysis:** Examine conflict distribution across world regions  
            - **Geospatial Heatmaps:** Visualize where conflict intensity is concentrated on the map  
            """
        )

        st.info("Tip: Use sidebar filters in each tab to refine by year range, country, and conflict type.")

        st.caption("Data source: [Uppsala Conflict Data Program (UCDP) – GED](https://ucdp.uu.se/downloads/)")
