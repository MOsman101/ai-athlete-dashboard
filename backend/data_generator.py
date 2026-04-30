import pandas as pd
import numpy as np


def generate_synthetic_data(n=300, seed=42):
    np.random.seed(seed)

    df = pd.DataFrame({
        "athlete_id": [f"Athlete_{i:03d}" for i in range(1, n + 1)],
        "heart_rate": np.random.normal(72, 8, n).clip(45, 110),
        "hrv": np.random.normal(58, 10, n).clip(20, 100),
        "training_load": np.random.normal(70, 15, n).clip(20, 120),
        "fatigue_score": np.random.normal(5, 2, n).clip(1, 10),
        "recovery_hours": np.random.normal(8, 1.5, n).clip(3, 12),
        "sleep_hours": np.random.normal(7.2, 1.2, n).clip(3, 10),
        "previous_injury_flag": np.random.binomial(1, 0.28, n)
    })

    risk_formula = (
        (df["training_load"] * 0.03)
        + (df["fatigue_score"] * 0.9)
        - (df["recovery_hours"] * 0.5)
        - (df["sleep_hours"] * 0.35)
        - (df["hrv"] * 0.02)
        + (df["previous_injury_flag"] * 1.0)
    )

    df["injury_risk"] = np.where(risk_formula > 4.8, 1, 0)

    readiness = (
        100
        - (df["fatigue_score"] * 6)
        - (df["training_load"] * 0.25)
        + (df["recovery_hours"] * 4)
        + (df["sleep_hours"] * 2.5)
        + (df["hrv"] * 0.15)
    )

    df["readiness_score"] = readiness.clip(0, 100).round(1)

    return df


def get_dashboard_dataset():
    return generate_synthetic_data()