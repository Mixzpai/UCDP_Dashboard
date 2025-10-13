import pandas as pd

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

    def filter_data(self, year_range, countries=None, region = None):
        """Return rows within the year_range and optional country and region filters.

        year_range: tuple(min_year, max_year)
        countries: list-like of country names or None
        region: region name (string) or None
        """
        filtered = self.data[(self.data["year_cy"] >= year_range[0]) & (self.data["year_cy"] <= year_range[1])]
        if region:
            filtered = filtered[filtered["region_cy"] == region]
        if countries:
            # allow passing a single country as string
            if isinstance(countries, str):
                countries = [countries]
            filtered = filtered[filtered["country_cy"].isin(countries)]
        return filtered

    def get_regions(self):
        """Return sorted unique regions present in the dataset."""
        return sorted(self.data["region_cy"].dropna().unique())

    def get_countries_by_region(self, region):
        """Return unique countries for a given region."""
        if region is None:
            return self.get_countries()
        return self.data.loc[self.data["region_cy"] == region, "country_cy"].dropna().unique()

    def clean_death_counts(self, df):
        for col in ["sb_total_deaths_best_cy", "ns_total_deaths_best_cy", "os_total_deaths_best_cy"]:
            df[col] = df[col].fillna(0).astype(int)
        return df
