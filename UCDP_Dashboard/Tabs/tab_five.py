import streamlit as st
import plotly.express as px
from Dataset.dataset import UCDP_Data


class tab_five:
    def __init__(self):
        self.data_handler = UCDP_Data()

    def display(self, sidebar):
        st.header("Geographic Distribution of Deaths")
        st.write(
            "This tab shows an animated choropleth map of conflict-related deaths by country. "
            "Use the sidebar to filter by year range, violence type, and specific countries."
        )

        # Sidebar controls
        sidebar.header("Tab 5 Controls")
        filters = sidebar.expander("Filters", expanded=True)
        year_min, year_max = self.data_handler.get_year_range()
        year_range = filters.slider("Year range", year_min, year_max, (2000, 2020), key = "slider_tab5")

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
            key="selectbox_tab5"
        )

        countries = filters.multiselect(
            "Countries",
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

        speed = st.session_state.get("speed_slider_tab5_main", 800)

        # Animated choropleth map
        # st.subheader("Geographic Distribution of Deaths")
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

        if 'updatemenus' in fig_map.layout and len(fig_map.layout.updatemenus) > 0:
            try:
                fig_map.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = int(speed)
                fig_map.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = int(speed) // 2
                fig_map.layout.updatemenus[0].buttons[0].args[1]['transition']['easing'] = 'linear'
            except Exception:
                pass

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

        st.slider("Animation Duration (ms)", min_value=100, max_value=2000, step=100, value=800, key="speed_slider_tab5_main",
                    help="Adjust how quickly the animation plays — higher values = slower animation.")
