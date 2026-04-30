def anonymise_athlete_id(athlete_id):
    return athlete_id.replace("ATH-", "ID-")


def get_privacy_status():
    return {
        "anonymisation": "Enabled",
        "storage": "Local Only",
        "consent": "Verified",
        "data_type": "Synthetic Only",
        "data_minimisation": "Applied"
    }


def get_access_matrix():
    return [
        {
            "Role": "Admin",
            "Access Level": "Full",
            "Permissions": "Access all pages, all athlete data, logs, and privacy controls"
        },
        {
            "Role": "Coach",
            "Access Level": "Operational",
            "Permissions": "Access overview and athlete analysis pages only"
        },
        {
            "Role": "Analyst",
            "Access Level": "Analytical",
            "Permissions": "Access overview, athlete analysis, and privacy pages"
        },
        {
            "Role": "Viewer",
            "Access Level": "Restricted",
            "Permissions": "Access overview and privacy pages only"
        }
    ]