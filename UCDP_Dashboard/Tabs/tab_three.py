import streamlit as st
import plotly.express as px
from Dataset.dataset import UCDP_Data

class tab_three:
    def __init__(self):
        self.data_handler = UCDP_Data()

    def display(self):
        st.header("Animated Deaths by Conflict Type Over Time")
        st.write("This animation shows the changes in deaths for each conflict type over the years.")

        # Sidebar controls
        st.sidebar.header("Tab 3 Controls")
        year_min, year_max = self.data_handler.get_year_range()
        year_range = st.sidebar.slider("Select Year Range", year_min, year_max, (2000, 2020), key="slider_tab3")
        countries = st.sidebar.multiselect(
            "Select Countries",
            self.data_handler.get_countries(),
            default=[]
        )

        # Filter and clean data
        filtered = self.data_handler.filter_data(year_range, countries)
        filtered = self.data_handler.clean_death_counts(filtered)

        # Prepare data for animation
        import pandas as pd
        # Melt the data
        melted = filtered.melt(
            id_vars=["year_cy", "country_cy"],
            value_vars=["sb_total_deaths_best_cy", "ns_total_deaths_best_cy", "os_total_deaths_best_cy"],
            var_name="Conflict Type",
            value_name="Deaths"
        )

        conflict_type_labels = {
            "sb_total_deaths_best_cy": "State-based",
            "ns_total_deaths_best_cy": "Non-state",
            "os_total_deaths_best_cy": "One-sided"
        }
        melted["Conflict Type"] = melted["Conflict Type"].map(conflict_type_labels)

        # Find top 10 countries by total deaths for each year
        total_deaths = (
            melted.groupby(["year_cy", "country_cy"])['Deaths']
            .sum()
            .reset_index()
        )
        top10_per_year = (
            total_deaths.sort_values(["year_cy", "Deaths"], ascending=[True, False])
            .groupby("year_cy")
            .head(10)
        )

        # Filter melted to only include top 10 countries for each year
        merged = pd.merge(
            melted,
            top10_per_year[["year_cy", "country_cy"]],
            on=["year_cy", "country_cy"],
            how="inner"
        )

        fig = px.bar(
            merged,
            x="Deaths",
            y="country_cy",
            color="Conflict Type",
            orientation="h",
            animation_frame="year_cy",
            animation_group="country_cy",
            barmode="group",
            labels={"country_cy": "Country", "Deaths": "Number of Deaths"},
            title="Animated Deaths by Conflict Type and Country Over Time"
        )
        # Adjust layout for horizontal bar chart
        fig.update_layout(
            yaxis_tickangle=0,
            margin=dict(l=120, b=120)
        )
        st.plotly_chart(fig, use_container_width=True)
