import pandas as pd


DATASET_PATH = "data/athlete csv for dashboard.csv"


def load_dataset(path=DATASET_PATH):
    df = pd.read_csv(path)
    df["session_date"] = pd.to_datetime(df["session_date"])
    return df


def get_athlete_list(df):
    return sorted(df["athlete_id"].unique().tolist())


def get_athlete_history(df, athlete_id):
    athlete_df = df[df["athlete_id"] == athlete_id].copy()
    athlete_df = athlete_df.sort_values("session_date")
    return athlete_df


def get_latest_athlete_record(df, athlete_id):
    athlete_df = get_athlete_history(df, athlete_id)
    return athlete_df.iloc[-1]


def get_latest_records_for_all_athletes(df):
    latest_df = df.sort_values("session_date").groupby("athlete_id").tail(1).copy()
    return latest_df.sort_values("athlete_id")