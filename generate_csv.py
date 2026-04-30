import os
import pandas as pd
import random
from datetime import date, timedelta

random.seed(123)

positions = [
    "Goalkeeper",
    "Centre Back",
    "Left Back",
    "Right Back",
    "Defensive Midfielder",
    "Central Midfielder",
    "Attacking Midfielder",
    "Left Winger",
    "Right Winger",
    "Forward",
    "Striker"
]

clubs = [
    "Northbridge FC",
    "Riverside United",
    "Kingsport Athletic",
    "Westhaven City",
    "Eastgate Rovers",
    "Southmoor Albion",
    "Lakeview Town",
    "Hillcrest Wanderers",
    "Oakfield FC",
    "Metro Sporting",
    "Harbour Vale",
    "Redstone Athletic"
]

def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))

def calculate_readiness_score(hrv, training_load, fatigue_score, recovery_hours, sleep_hours):
    score = (
        100
        - (fatigue_score * 6)
        - (training_load * 0.25)
        + (recovery_hours * 4)
        + (sleep_hours * 2.5)
        + (hrv * 0.15)
    )
    return round(clamp(score, 0, 100), 1)

def calculate_injury_risk(training_load, fatigue_score, recovery_hours, sleep_hours, hrv, previous_injury_flag):
    formula = (
        (training_load * 0.03)
        + (fatigue_score * 0.9)
        - (recovery_hours * 0.5)
        - (sleep_hours * 0.35)
        - (hrv * 0.02)
        + (previous_injury_flag * 1.0)
    )
    return 1 if formula > 4.8 else 0

def build_dataset():
    athlete_ids = random.sample(range(101, 999), 20)
    rows = []
    start = date(2026, 1, 1)

    for athlete_num in range(1, 21):
        athlete_id = f"ATH-{athlete_ids[athlete_num - 1]}"
        athlete_name = f"Player {athlete_num}"
        club = random.choice(clubs)
        position = random.choice(positions)
        age = random.randint(18, 33)
        previous_injury_flag = 1 if random.random() < 0.28 else 0

        base_hr = random.gauss(72, 5)
        base_hrv = random.gauss(58, 8)
        base_load = random.gauss(70, 10)
        base_fatigue = random.gauss(5, 1.5)
        base_recovery = random.gauss(8, 1.2)
        base_sleep = random.gauss(7.2, 0.8)

        for session in range(1, 13):
            session_date = start + timedelta(days=session * random.choice([2, 3, 4]))
            heart_rate = round(clamp(base_hr + random.gauss(0, 4), 45, 110), 1)
            hrv = round(clamp(base_hrv + random.gauss(0, 6), 20, 100), 1)
            training_load = round(clamp(base_load + random.gauss(0, 10), 20, 120), 1)
            fatigue_score = round(clamp(base_fatigue + random.gauss(0, 1.2), 1, 10), 1)
            recovery_hours = round(clamp(base_recovery + random.gauss(0, 1.0), 3, 12), 1)
            sleep_hours = round(clamp(base_sleep + random.gauss(0, 0.8), 3, 10), 1)

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
                "club": club,
                "position": position,
                "age": age,
                "session_number": session,
                "session_date": session_date.isoformat(),
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
    df = build_dataset()
    output_path = os.path.join("data", "athlete data for dashboard.csv")
    df.to_csv(output_path, index=False)
    print(f"CSV created successfully: {output_path}")
    print(df.head())

if __name__ == "__main__":
    main()