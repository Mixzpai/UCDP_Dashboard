import streamlit as st

class tab_one:
    def display(self,sidebar):
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
        st.markdown(
            """
            ### **Introduction to the Case**

            Organised violence has continued to destabilise global peace long after the Cold War. Since 1989, violence in the world has shifted from large interstate wars to fragmented intrastate conflicts and non-state violence, resulting in persistent human suffering. Using structured data from the Uppsala Conflict Data Program (UCDP), this data analysis investigates how geopolitical change reshaped conflict size and distribution across regions between the years 1989 and 2024.  

            The early 1990s were a time where there was optimism that the end of the Cold War marked the end of major wars and there would be global peace. What actually happened is that violence just changed shape; instead of large interstate wars, there was instead an increase in civil wars, non-state conflicts, and one-sided attacks. The central message that the dataset conveys is that although large inter-state wars did decline after the Cold War, organised violence persisted in different forms, shifting toward civil wars, regional conflicts, and non-state violence.  

            ### **Goal and Narrative**
            The goal of the dataset is to visualise patterns and reveal drivers of organised violence to support understanding of political instability. The story follows global fatalities starting from the 1989 period of post-Cold War optimism, through the surge in organised violence after 2000 and the fragmentation of conflict in the 2010s-2020s. As well as the global perspective of organised violence that the dataset presents, the dataset also tells more localised stories of regional organised-violence hotspots throughout the studied time period, such as surges in violence reflecting events in Rwanda, Syria, Yemen, Ethiopia, and Ukraine.  

            ### **Target Audience**
            The target audience of the dataset really is anyone curious to observe patterns in violence in our world, although it may be of particular interest to academics and students studying data science, political science, and international relations, particularly those studying conflict prevention, stability, and humanitarian policy.  

            ### **Introduction to the Dataset**
            The dataset analysis uses the UCDP Country-Year Dataset on Organised Violence v25.1, a georeferenced event dataset recording all incidents since 1989 involving at least one death caused by organised actors. Each record includes event IDs, actors and dyads, geographical coordinates, the time of the event, and best/low/high fatality estimates. The data points originate from verified sources such as BBC Monitoring, NGOs, and local media. The dataset enables temporal and regional comparison of state-based, non-state, and one-sided conflicts.  

            ### **Summary of Dataset Analysis**

            #### Scope & Method 

            The UCDP data was cleaned, normalised, and derived fields were added for analysis (continent, UN_region, fatalities_total, and decade.) The analysis examines global trends, conflict-type contrasts, regional patterns, and concentration of fatalities by decade.  

            #### Findings  

            **Global perspective:** a sharp post-Cold War decline in violence was observed, followed by significant peaks in the 2000s and 2010s (Syria, Iraq, Yemen), and a later rise in the 2020s (Ukraine). 

            **Observed trends in conflict types:** state-based violence persists throughout the dataset as the violence type resulting in the highest total fatalities. Non-state conflicts surged after 2010, and one-sided civilian killings are seen to occur in episodic spikes (Rwanda 1994, Darfur, ISIS 2014-16). 

            **Regional patterns:** Africa and Asia dominate overall fatalities, while the Middle East peaks in 2010s, and Europe’s fatalities by organised violence increased post-2020. 

            ### **Hypothesis**
            Mapping organised violence over time and by type will reveal how its epicentres shift, providing insight into how patterns of global organised violence evolve alongside political and ideological change.  
                    
        """
        )
             

        sidebar.subheader("How to Use")
        sidebar.write(
            """
            Use the navigation tabs to explore each analytical dimension:
            
            - **Trends (Time Series):** Observe changes in deaths by conflict type over time  
            - **Comparisons (Animated):** Compare how different countries and violence types evolve dynamically  
            - **Regional Analysis:** Examine conflict distribution across world regions  
            - **Geospatial Heatmaps:** Visualize where conflict intensity is concentrated on the map  
            """
        )

        sidebar.info("Tip: Use sidebar filters in each tab to refine by year range, country, and conflict type.")

        st.caption("Data source: [Uppsala Conflict Data Program (UCDP) – GED](https://ucdp.uu.se/downloads/)")
