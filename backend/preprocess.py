import pandas as pd


FEATURE_COLUMNS = [
    "heart_rate",
    "hrv",
    "training_load",
    "fatigue_score",
    "recovery_hours",
    "sleep_hours",
    "previous_injury_flag"
]


def get_feature_matrix(df):
    return df[FEATURE_COLUMNS].copy()


def get_target_vector(df):
    return df["injury_risk"].copy()


def prepare_single_input(
    heart_rate,
    hrv,
    training_load,
    fatigue_score,
    recovery_hours,
    sleep_hours,
    previous_injury_flag
):
    return pd.DataFrame([{
        "heart_rate": heart_rate,
        "hrv": hrv,
        "training_load": training_load,
        "fatigue_score": fatigue_score,
        "recovery_hours": recovery_hours,
        "sleep_hours": sleep_hours,
        "previous_injury_flag": previous_injury_flag
    }])