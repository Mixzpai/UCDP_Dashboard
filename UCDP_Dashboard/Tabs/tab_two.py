import streamlit as st
import plotly.express as px
from Dataset.dataset import UCDP_Data

class tab_two:
    def __init__(self):
        self.data_handler = UCDP_Data()

    def display(self, sidebar):
        st.header("Trends")
        st.write(
            "The Trends tab shows how different types of conflict deaths change over time. "
            "Users can filter by year, violence type, and country to view interactive line charts "
            "that reveal major shifts and patterns in global violence."
        )

        # Sidebar controls (rendered into the provided container)
        sidebar.header("Tab 2 Controls")
        filters = sidebar.expander("Filters", expanded=False)
        year_min, year_max = self.data_handler.get_year_range()
        year_range = filters.slider("Year range", year_min, year_max, (2000, 2020), key = "slider_tab2")

        violence_types = {
            "sb_total_deaths_best_cy": "State-based",
            "ns_total_deaths_best_cy": "Non-state",
            "os_total_deaths_best_cy": "One-sided",
            "cumulative_total_deaths_in_orgvio_best_cy": "All types (cumulative)"
        }
        type_selected = filters.selectbox(
            "Type",
            options = list(violence_types.keys()),
            format_func = lambda x: violence_types[x]
        )

        countries = filters.multiselect(
            "Countries",
            self.data_handler.get_countries(),
            default = [],
            key="multiselect_tab2"
        )

        # Filter and clean data
        filtered = self.data_handler.filter_data(year_range, countries)
        filtered = self.data_handler.clean_death_counts(filtered)

        self.time_series_analysis(filtered, type_selected, violence_types)

    def time_series_analysis(self, filtered, type_selected, violence_types):
        st.subheader(f"Total Deaths per Year ({violence_types[type_selected]})")
        deaths_per_year = filtered.groupby("year_cy")[type_selected].sum().reset_index()
        fig_time = px.line(
            deaths_per_year,
            x = "year_cy",
            y = type_selected,
            title = f"Deaths Over Time ({violence_types[type_selected]})",
            labels = {type_selected: "Deaths", "year_cy": "Year"}
        )
        
        st.plotly_chart(fig_time, use_container_width=True)
