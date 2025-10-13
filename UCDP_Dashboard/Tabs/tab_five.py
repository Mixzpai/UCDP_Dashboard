import streamlit as st
import plotly.express as px
from Dataset.dataset import UCDP_Data


class tab_five:
    def __init__(self):
        self.data_handler = UCDP_Data()

    def display(self):
        st.header("Geographic Distribution of Deaths")
        st.write(
            "This tab shows an animated choropleth map of conflict-related deaths by country. "
            "Use the sidebar to filter by year range, violence type, and specific countries."
        )

        # Sidebar controls
        st.sidebar.header("Tab 5 Controls")
        year_min, year_max = self.data_handler.get_year_range()
        year_range = st.sidebar.slider("Select Year Range", year_min, year_max, (2000, 2020), key = "slider_tab5")

        violence_types = {
            "sb_total_deaths_best_cy": "State-based",
            "ns_total_deaths_best_cy": "Non-state",
            "os_total_deaths_best_cy": "One-sided",
            "cumulative_total_deaths_in_orgvio_best_cy": "All types (cumulative)"
        }
        type_selected = st.sidebar.selectbox(
            "Select Type of Violence",
            options = list(violence_types.keys()),
            format_func = lambda x: violence_types[x],
            key="selectbox_tab5"
        )

        countries = st.sidebar.multiselect(
            "Select Countries",
            self.data_handler.get_countries(),
            default = [],
            key="multiselect_tab5"
        )

        # Filter and clean data
        filtered = self.data_handler.filter_data(year_range, countries)
        filtered = self.data_handler.clean_death_counts(filtered)

        if filtered.empty:
            st.info("No data available for the selected filters.")
            return

        # Animated choropleth map
        st.subheader("Geographic Distribution of Deaths")
        fig_map = px.choropleth(
            filtered,
            locations = "country_cy",
            locationmode = "country names",
            color = type_selected,
            hover_name = "country_cy",
            animation_frame = "year_cy",
            title=f"Conflict Deaths by Country (Animated) – {violence_types[type_selected]}",
            color_continuous_scale="Reds"
        )
        # Make the figure larger and improve layout for readability
        fig_map.update_layout(
            height = 750,
            title_x = 0.5,
            title_font = dict(size = 20),
            margin = dict(l = 20, r = 20, t = 90, b = 20),
        )

        # Disable interactive panning/zooming while preserving hover and animation
        fig_map.update_layout(dragmode=False)

        # Remove modebar buttons that allow zooming/panning and keep the chart responsive
        config = {
            "responsive": True,
            "scrollZoom": False,
            "modeBarButtonsToRemove": [
                "zoom2d",
                "pan2d",
                "zoomIn2d",
                "zoomOut2d",
                "autoScale2d",
                "resetScale2d",
                "select2d",
                "lasso2d",
            ],
            "displaylogo": False,
        }

        st.plotly_chart(fig_map, use_container_width = True, config = config)
