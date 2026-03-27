import pandas as pd

def clean_data():
    print("Loading raw data...")
    df = pd.read_csv("data/raw_generation.csv")

    print(f"Raw data shape: {df.shape}")
    print(df.dtypes)
    print(df.head())

    # Rename columns for clarity
    df = df.rename(columns={
        "period": "timestamp",
        "respondent": "region",
        "respondent-name": "region_name",
        "type": "data_type",
        "type-name": "data_type_name",
        "value": "generation_mwh",
        "value-units": "units"
    })

    # Parse timestamp into a proper datetime column
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Convert generation to numeric, force errors to NaN
    df["generation_mwh"] = pd.to_numeric(df["generation_mwh"], errors="coerce")

    # Drop rows with missing generation values
    missing = df["generation_mwh"].isna().sum()
    print(f"Dropping {missing} rows with missing generation values")
    df = df.dropna(subset=["generation_mwh"])

    # Engineer new features
    df["date"] = df["timestamp"].dt.date
    df["hour"] = df["timestamp"].dt.hour
    df["month"] = df["timestamp"].dt.month
    df["day_of_week"] = df["timestamp"].dt.day_name()

    # Rolling 7-day average (based on sorted timestamp)
    df = df.sort_values("timestamp").reset_index(drop=True)
    df["rolling_7day_avg"] = df["generation_mwh"].rolling(window=168).mean()

    # Daily total generation
    daily_totals = df.groupby("date")["generation_mwh"].sum().reset_index()
    daily_totals.columns = ["date", "daily_total_mwh"]
    df = df.merge(daily_totals, on="date", how="left")

    # Capacity factor proxy (normalize each hour against the max observed)
    max_generation = df["generation_mwh"].max()
    df["capacity_factor_pct"] = (df["generation_mwh"] / max_generation * 100).round(2)

    print(f"\nCleaned data shape: {df.shape}")
    print(df.head())

    df.to_csv("data/cleaned_generation.csv", index=False)
    print("\nSaved to data/cleaned_generation.csv")

    return df

if __name__ == "__main__":
    clean_data()