import hashlib
import mysql.connector
from backend.db import get_connection


ROLE_ACCESS = {
    "Admin": [
        "Executive Overview",
        "Athlete Analysis",
        "Privacy",
        "System Logs"
    ],
    "Coach": [
        "Executive Overview",
        "Athlete Analysis"
    ],
    "Analyst": [
        "Executive Overview",
        "Athlete Analysis",
        "Privacy"
    ],
    "Viewer": [
        "Executive Overview",
        "Privacy"
    ]
}


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_login(username, password):
    password_hash = hash_password(password)

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT username, role
        FROM users
        WHERE username = %s AND password_hash = %s
        """,
        (username, password_hash)
    )

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if user:
        return True, user["role"]

    return False, None


def register_user(username, password):
    username = username.strip()

    if not username or not password:
        return False, "Username and password are required."

    if len(username) < 4:
        return False, "Username must be at least 4 characters long."

    if len(password) < 8:
        return False, "Password must be at least 8 characters long."

    password_hash = hash_password(password)
    default_role = "Viewer"

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (username, password_hash, role)
            VALUES (%s, %s, %s)
            """,
            (username, password_hash, default_role)
        )
        connection.commit()
        return True, "Account created successfully. You can now log in as a Viewer."

    except mysql.connector.IntegrityError:
        return False, "Username already exists. Please choose another username."

    finally:
        cursor.close()
        connection.close()


def get_accessible_pages(role):
    return ROLE_ACCESS.get(role, [])