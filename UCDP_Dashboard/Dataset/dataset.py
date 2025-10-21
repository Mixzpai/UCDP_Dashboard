from pathlib import Path
import os
import pandas as pd

class UCDP_Data:
    def __init__(self, filepath: str | os.PathLike | None = None, filename: str = "organizedviolencecy_v25_1.csv"):
        self.filepath = self._resolve_path(filepath, filename)
        self.data = self.load_data()

    def _resolve_path(self, filepath, filename) -> Path | None:
        if filepath is not None and hasattr(filepath, "read"):
            return filepath

        # Env override (e.g., UCDP_DATA_PATH=/mount/src/.../Dataset/organizedviolencecy_v25_1.csv)
        env_path = os.environ.get("UCDP_DATA_PATH")
        if env_path and Path(env_path).exists():
            return Path(env_path)

        # If explicit path string/pathlike provided
        if filepath:
            p = Path(filepath)
            if p.exists():
                return p

        # Resolve relative to this file (preferred default)
        here = Path(__file__).resolve()
        dataset_dir = here.parent  # .../UCDP_Dashboard/Dataset
        candidate = dataset_dir / filename
        if candidate.exists():
            return candidate

        # Common fallbacks
        fallbacks = [
            Path.cwd() / "Dataset" / filename,
            Path.cwd() / filename,
            dataset_dir.parent / "Dataset" / filename,
            dataset_dir.parent / filename,
        ]
        for c in fallbacks:
            if c.exists():
                return c

        # Nothing found -> leave as None to trigger helpful error in load_data
        self._not_found_error(filename, [candidate, *fallbacks])
        return None  # unreachable

    def _not_found_error(self, filename: str, searched: list[Path]) -> None:
        paths = "\n  - " + "\n  - ".join(str(p) for p in searched)
        raise FileNotFoundError(
            f"Could not find '{filename}'. I looked in:{paths}\n\n"
            "Fixes:\n"
            "• Put the CSV in UCDP_Dashboard/Dataset/ and commit it (case-sensitive!)\n"
            "• Or set env UCDP_DATA_PATH to an absolute path\n"
            "• Or pass an absolute path/file-like when creating UCDP_Data(...)\n"
            "• On Streamlit Cloud, ensure the file is in the repo (not .gitignored)."
        )

    def load_data(self) -> pd.DataFrame:
        df = pd.read_csv(self.filepath, low_memory=False)

        # Ensure year column exists
        if "year_cy" not in df.columns:
            raise KeyError("Missing required column: 'year_cy'")

        # Coerce year and optional string columns if present
        df["year_cy"] = pd.to_numeric(df["year_cy"], errors="coerce").astype("Int64")
        if "country_cy" in df.columns:
            df["country_cy"] = df["country_cy"].astype("string")
        if "region_cy" in df.columns:
            df["region_cy"] = df["region_cy"].astype("string")

        # Coerce deaths to integers; if missing, create the column filled with 0
        death_cols = ["sb_total_deaths_best_cy", "ns_total_deaths_best_cy", "os_total_deaths_best_cy"]
        for col in death_cols:
            if col not in df.columns:
                df[col] = 0
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype("Int64")

        return df

    def get_year_range(self):
        return int(self.data["year_cy"].min()), int(self.data["year_cy"].max())

    def get_countries(self):
        return self.data["country_cy"].dropna().unique()

    def filter_data(self, year_range, countries=None, region=None):
        filtered = self.data[
            (self.data["year_cy"] >= year_range[0]) & (self.data["year_cy"] <= year_range[1])
        ]
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
            if col not in df.columns:
                df[col] = 0
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype("Int64")
        return df
