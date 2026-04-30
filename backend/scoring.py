def calculate_readiness_score(
    heart_rate,
    hrv,
    training_load,
    fatigue_score,
    recovery_hours,
    sleep_hours
):
    readiness_score = (
        100
        - (fatigue_score * 6)
        - (training_load * 0.25)
        + (recovery_hours * 4)
        + (sleep_hours * 2.5)
        + (hrv * 0.15)
    )
    readiness_score = max(0, min(100, round(readiness_score, 1)))
    return readiness_score


def generate_performance_summary(training_load, fatigue_score, recovery_hours):
    if training_load > 85 and fatigue_score >= 7:
        return "Current workload and fatigue levels suggest closer monitoring is required before further high-intensity activity."
    if training_load > 65 and recovery_hours < 7:
        return "Moderate workload combined with limited recovery suggests that athlete readiness may begin to decline if conditions persist."
    return "Current athlete condition appears stable, with no immediate concerns indicated by the synthetic monitoring profile."