import pandas as pd
import streamlit as st
import plotly.express as px
from Dataset.dataset import UCDP_Data

class tab_three:
    def __init__(self):
        self.data_handler = UCDP_Data()

    def display(self, sidebar):
        st.header("Animated Deaths Over Time")
        st.write(
            "The Animated Deaths tab presents a dynamic bar chart showing how deaths from state-based, "
            "non-state, and one-sided conflicts change over time. It highlights the top 10 most affected "
            "countries each year, allowing users to track shifts in conflict intensity and compare how "
            "different types of violence evolve across nations. Users can also filter and compare specific "
            "countries through the sidebar controls."
        )


        # Sidebar controls (render into provided container)
        sidebar.header("Tab 3 Controls")
        filters = sidebar.expander("Filters", expanded=True)
        year_min, year_max = self.data_handler.get_year_range()
        year_range = filters.slider("Year range", year_min, year_max, (2000, 2020), key = "slider_tab3")
        countries = filters.multiselect(
            "Countries",
            self.data_handler.get_countries(),
            default = []
        )

        # Filter and clean data
        filtered = self.data_handler.filter_data(year_range, countries)
        filtered = self.data_handler.clean_death_counts(filtered)

        # Melt the data
        melted = filtered.melt(
            id_vars = ["year_cy", "country_cy"],
            value_vars = ["sb_total_deaths_best_cy", "ns_total_deaths_best_cy", "os_total_deaths_best_cy"],
            var_name = "Conflict Type",
            value_name = "Deaths"
        )

        conflict_type_labels = {
            "sb_total_deaths_best_cy": "State-based",
            "ns_total_deaths_best_cy": "Non-state",
            "os_total_deaths_best_cy": "One-sided"
        }
        melted["Conflict Type"] = melted["Conflict Type"].map(conflict_type_labels)

        # Find total deaths by country across the selected range and pick top N overall
        total_deaths = (
            melted.groupby(["year_cy", "country_cy"])['Deaths']
            .sum()
            .reset_index()
        )

        # Choose a stable set of top countries across the entire selected range.
        # Take the top N by summed deaths over the filtered years.
        N = min(10, melted['country_cy'].nunique())
        top_countries = (
            total_deaths.groupby('country_cy')['Deaths']
            .sum()
            .nlargest(N)
            .index
            .tolist()
        )

        merged = melted[melted['country_cy'].isin(top_countries)].copy()

        # Fix category order so the countries keep the same vertical position across frames
        country_order = top_countries
        merged['country_cy'] = pd.Categorical(merged['country_cy'], categories=country_order[::-1], ordered=True)

        # Compute a fixed x-axis range based on max total deaths across countries and years
        max_total = total_deaths.groupby(['year_cy', 'country_cy'])['Deaths'].sum().max()

        speed = st.session_state.get("speed_slider_tab3_main", 800)

        fig = px.bar(
            merged,
            x = "Deaths",
            y = "country_cy",
            color = "Conflict Type",
            orientation = "h",
            animation_frame = "year_cy",
            animation_group = "country_cy",
            barmode = "group",
            category_orders={'country_cy': country_order[::-1]},
            labels = {"country_cy": "Country", "Deaths": "Number of Deaths"},
            title = "Animated Deaths by Conflict Type and Country Over Time"
        )
        # Adjust layout for horizontal bar chart
        fig.update_layout(
            yaxis_tickangle = 0,
            margin = dict(l = 120, b = 120),
            xaxis = dict(range=[0, max_total * 1.1])
        )
        

        # Make the animation transitions smoother and adjust play button controls
        if 'updatemenus' in fig.layout and len(fig.layout.updatemenus) > 0:
            try:
                fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = speed
                fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = speed /2
                fig.layout.updatemenus[0].buttons[0].args[1]['transition']['easing'] = 'linear'
            except Exception:
                pass
        st.plotly_chart(fig, use_container_width = True)
        st.slider("Animation Duration (ms)", min_value=100, max_value=2000, step=100, value=800, key="speed_slider_tab3_main",
                    help="Adjust how quickly the animation plays — higher values = slower animation.")
        