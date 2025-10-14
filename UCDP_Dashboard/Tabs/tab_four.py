import streamlit as st
import plotly.express as px
import pandas as pd
from Dataset.dataset import UCDP_Data

class tab_four:
    def __init__(self):
        self.data_handler = UCDP_Data()

    def display(self, sidebar):
        st.header("Regional Analysis")
        st.write(
            "The Regional Analysis tab provides insights into conflict-related deaths across different regions. "
            "Users can filter data by year, violence type, region, and country to explore patterns and trends. "
            "Interactive bar charts display total deaths per year by region and a breakdown of deaths by country "
            "within the selected region, helping users understand the geographical distribution of violence."
        )

        # Sidebar controls (render into provided container)
        sidebar.header("Tab 4 Controls")
        filters = sidebar.expander("Filters", expanded=True)
        year_min, year_max = self.data_handler.get_year_range()
        year_range = filters.slider("Year range", year_min, year_max, (2000, 2020), key = "slider_tab4")

        violence_types = {
            "sb_total_deaths_best_cy": "State-based",
            "ns_total_deaths_best_cy": "Non-state",
            "os_total_deaths_best_cy": "One-sided",
            "cumulative_total_deaths_in_orgvio_best_cy": "All types (cumulative)"
        }
        type_selected = filters.selectbox(
            "Type",
            options = list(violence_types.keys()),
            format_func = lambda x: violence_types[x],
            key="selectbox_tab4"
        )

        # Allow user to pick whether to compare countries within a region or compare regions
        compare_mode = filters.radio(
            "Compare",
            ("Countries in a Region", "Regions vs Regions"),
            key = "radio_compare_mode_tab4"
        )

        regions = list(self.data_handler.get_regions())

        if compare_mode == "Countries in a Region":
            region_selected = filters.selectbox(
                "Region",
                options = regions,
                index = 0,
                key="selectbox_region_tab4"
            )

            countries = filters.multiselect(
                "Countries",
                options = list(self.data_handler.get_countries_by_region(region_selected)),
                default = [],
                key="multiselect_tab4"
            )

            # Filter and clean data for the selected region (countries optional)
            filtered = self.data_handler.filter_data(year_range, countries, region=region_selected)
            filtered = self.data_handler.clean_death_counts(filtered)

            # If no countries chosen, pick top 5 countries by cumulative deaths in region
            if not countries:
                top_countries = (
                    filtered.groupby("country_cy")[list(violence_types.keys())]
                    .sum()
                    .sum(axis=1)
                    .sort_values(ascending=False)
                    .head(5)
                    .index
                    .tolist()
                )
                countries = top_countries

            self.compare_countries_in_region(filtered, type_selected, violence_types, region_selected, countries)

        else:
            # Regions vs Regions mode
            selected_regions = filters.multiselect(
                "Regions",
                options = regions,
                default = regions[:3],
                key="multiselect_regions_tab4"
            )

            # Filter data for year range (regions selected later when aggregating)
            filtered = self.data_handler.filter_data(year_range)
            filtered = self.data_handler.clean_death_counts(filtered)

            if not selected_regions:
                selected_regions = regions[:2]

            self.compare_regions(filtered, type_selected, violence_types, selected_regions)

    def regional_analysis(self, filtered, type_selected, violence_types, region_selected):
        st.subheader(f"Total Deaths per Year in {region_selected} ({violence_types[type_selected]})")
        deaths_per_year = filtered.groupby("year_cy")[type_selected].sum().reset_index()
        fig_region_time = px.bar(
            deaths_per_year,
            x = "year_cy",
            y = type_selected,
            title = f"Total Deaths Over Time in {region_selected} ({violence_types[type_selected]})",
            labels = {type_selected: "Deaths", "year_cy": "Year"}
        )
        st.plotly_chart(fig_region_time, use_container_width = True)

    def compare_countries_in_region(self, filtered, type_selected, violence_types, region_selected, countries):
        st.subheader(f"Compare Countries in {region_selected} ({violence_types[type_selected]})")
        if filtered.empty:
            st.info("No data available for the selected filters.")
            return

        # Aggregate deaths per year per country
        agg = (
            filtered[filtered["country_cy"].isin(countries)]
            .groupby(["year_cy", "country_cy"])[type_selected]
            .sum()
            .reset_index()
        )

        if agg.empty:
            st.info("No data for the selected countries in this region.")
            return

        fig = px.line(
            agg,
            x = "year_cy",
            y = type_selected,
            color = "country_cy",
            title = f"{violence_types[type_selected]} over time by country in {region_selected}",
            labels = {type_selected: "Deaths", "year_cy": "Year", "country_cy": "Country"}
        )
        st.plotly_chart(fig, use_container_width = True)

        # Also show a stacked bar of total deaths per country across the selected years
        total_by_country = (
            agg.groupby("country_cy")[type_selected].sum().reset_index().sort_values(type_selected, ascending = False)
        )

        fig2 = px.bar(
            total_by_country,
            x = type_selected,
            y = "country_cy",
            orientation = "h",
            title = f"Total {violence_types[type_selected]} in {region_selected} (selected years)",
            labels = {type_selected: "Deaths", "country_cy": "Country"}
        )
        st.plotly_chart(fig2, use_container_width = True)

    def compare_regions(self, filtered, type_selected, violence_types, selected_regions):
        st.subheader(f"Compare Regions ({violence_types[type_selected]})")

        # Aggregate deaths per year per region
        agg = (
            filtered[filtered["region_cy"].isin(selected_regions)]
            .groupby(["year_cy", "region_cy"])[type_selected]
            .sum()
            .reset_index()
        )

        if agg.empty:
            st.info("No data available for the selected regions in the chosen year range.")
            return

        # Line chart: regions over time
        fig = px.line(
            agg,
            x = "year_cy",
            y = type_selected,
            color = "region_cy",
            title = f"{violence_types[type_selected]} over time by region",
            labels = {type_selected: "Deaths", "year_cy": "Year", "region_cy": "Region"}
        )
        st.plotly_chart(fig, use_container_width=True)

        # Bar chart: total deaths per region across selected years
        total_by_region = (
            agg.groupby("region_cy")[type_selected].sum().reset_index().sort_values(type_selected, ascending = False)
        )
        fig2 = px.bar(
            total_by_region,
            x = type_selected,
            y = "region_cy",
            orientation = "h",
            title = f"Total {violence_types[type_selected]} by region (selected years)",
            labels = {type_selected: "Deaths", "region_cy": "Region"}
        )
        st.plotly_chart(fig2, use_container_width = True)

