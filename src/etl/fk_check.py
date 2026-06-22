import sqlite3

conn = sqlite3.connect("output/nifty100.db")

cursor = conn.cursor()

cursor.execute(
    "PRAGMA foreign_key_check;"
)

rows = cursor.fetchall()

print("FK Issues Found:", len(rows))

for row in rows[:20]:
    print(row)

conn.close()