
import pandas as pd
import streamlit as st

class UCDP_Data:
    def __init__(self, filepath = "Dataset/organizedviolencecy_v25_1.csv"):
        self.filepath = filepath
        self.data = self.load_data()
        
    def load_data(self):
        df = pd.read_csv(self.filepath)
        return df

    def get_year_range(self):
        return int(self.data["year_cy"].min()), int(self.data["year_cy"].max())

    def get_countries(self):
        return self.data["country_cy"].dropna().unique()

    def filter_data(self, year_range, countries=None):
        filtered = self.data[(self.data["year_cy"] >= year_range[0]) & (self.data["year_cy"] <= year_range[1])]
        if countries:
            filtered = filtered[filtered["country_cy"].isin(countries)]
        return filtered

    def clean_death_counts(self, df):
        for col in ["sb_total_deaths_best_cy", "ns_total_deaths_best_cy", "os_total_deaths_best_cy"]:
            df[col] = df[col].fillna(0).astype(int)
        return df