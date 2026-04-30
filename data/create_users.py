import hashlib
import mysql.connector


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


users = [
    ("admin01", hash_password("AdminPass123"), "Admin"),
    ("coach01", hash_password("CoachPass123"), "Coach"),
    ("analyst01", hash_password("AnalystPass123"), "Analyst"),
    ("viewer01", hash_password("ViewerPass123"), "Viewer"),
]

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Aymen2008.",
    database="ai_athlete_dashboard"
)

cursor = connection.cursor()

query = """
INSERT INTO users (username, password_hash, role)
VALUES (%s, %s, %s)
"""

cursor.executemany(query, users)
connection.commit()

print("Users inserted successfully.")

cursor.close()
connection.close()