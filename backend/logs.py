from datetime import datetime
import pandas as pd


def create_log_entry(event, status="Success", details=""):
    return {
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Event": event,
        "Status": status,
        "Details": details
    }


def initialise_logs():
    return []


def add_log(logs_list, event, status="Success", details=""):
    logs_list.append(create_log_entry(event, status, details))
    return logs_list


def get_logs_dataframe(logs_list):
    if not logs_list:
        return pd.DataFrame(columns=["Time", "Event", "Status", "Details"])
    return pd.DataFrame(logs_list)