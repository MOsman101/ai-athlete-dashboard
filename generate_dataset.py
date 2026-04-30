import os
import pandas as pd
import numpy as np

POSITIONS = [
    "Goalkeeper",
    "Defender",
    "Full Back",
    "Midfielder",
    "Attacking Midfielder",
    "Winger",
    "Forward"
]


def calculate_readiness_score(hrv, training_load, fatigue_score, recovery_hours, sleep_hours):
    readiness = (
        100
        - (fatigue_score * 6)
        - (training_load * 0.25)
        + (recovery_hours * 4)
        + (sleep_hours * 2.5)
        + (hrv * 0.15)
    )
    return round(max(0, min(100, readiness)), 1)


def calculate_injury_risk(training_load, fatigue_score, recovery_hours, sleep_hours, hrv, previous_injury_flag):
    risk_formula = (
        (training_load * 0.03)
        + (fatigue_score * 0.9)
        - (recovery_hours * 0.5)
        - (sleep_hours * 0.35)
        - (hrv * 0.02)
        + (previous_injury_flag * 1.0)
    )
    return 1 if risk_formula > 4.8 else 0


def generate_synthetic_dataset(num_athletes=30, sessions_per_athlete=12, seed=42):
    np.random.seed(seed)
    rows = []

    start_date = pd.Timestamp("2026-01-01")

    for athlete_num in range(1, num_athletes + 1):
        athlete_id = f"Athlete_{athlete_num:03d}"
        athlete_name = f"Player {athlete_num:03d}"
        position = np.random.choice(POSITIONS)
        age = np.random.randint(18, 34)
        previous_injury_flag = np.random.binomial(1, 0.28)

        base_hr = np.random.normal(72, 5)
        base_hrv = np.random.normal(58, 8)
        base_load = np.random.normal(70, 10)
        base_fatigue = np.random.normal(5, 1.5)
        base_recovery = np.random.normal(8, 1.2)
        base_sleep = np.random.normal(7.2, 0.8)

        for session in range(1, sessions_per_athlete + 1):
            session_date = start_date + pd.Timedelta(days=session * 3)

            heart_rate = round(np.clip(base_hr + np.random.normal(0, 4), 45, 110), 1)
            hrv = round(np.clip(base_hrv + np.random.normal(0, 6), 20, 100), 1)
            training_load = round(np.clip(base_load + np.random.normal(0, 10), 20, 120), 1)
            fatigue_score = round(np.clip(base_fatigue + np.random.normal(0, 1.2), 1, 10), 1)
            recovery_hours = round(np.clip(base_recovery + np.random.normal(0, 1.0), 3, 12), 1)
            sleep_hours = round(np.clip(base_sleep + np.random.normal(0, 0.8), 3, 10), 1)

            readiness_score = calculate_readiness_score(
                hrv,
                training_load,
                fatigue_score,
                recovery_hours,
                sleep_hours
            )

            injury_risk = calculate_injury_risk(
                training_load,
                fatigue_score,
                recovery_hours,
                sleep_hours,
                hrv,
                previous_injury_flag
            )

            rows.append({
                "athlete_id": athlete_id,
                "athlete_name": athlete_name,
                "position": position,
                "age": age,
                "session_number": session,
                "session_date": session_date.strftime("%Y-%m-%d"),
                "heart_rate": heart_rate,
                "hrv": hrv,
                "training_load": training_load,
                "fatigue_score": fatigue_score,
                "recovery_hours": recovery_hours,
                "sleep_hours": sleep_hours,
                "previous_injury_flag": previous_injury_flag,
                "readiness_score": readiness_score,
                "injury_risk": injury_risk
            })

    return pd.DataFrame(rows)


def main():
    os.makedirs("data", exist_ok=True)
    df = generate_synthetic_dataset()
    output_path = os.path.join("data", "synthetic_athlete_dataset.csv")
    df.to_csv(output_path, index=False)
    print(f"Dataset created successfully: {output_path}")
    print(df.head())


if __name__ == "__main__":
    main()