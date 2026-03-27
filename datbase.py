import sqlite3

conn = sqlite3.connect("spam.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    prediction TEXT
)
""")

conn.commit()
conn.close()

print("Database created successfully ✅")