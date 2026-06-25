import sqlite3

conn = sqlite3.connect('delivery.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_name TEXT NOT NULL
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS routes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    destination TEXT NOT NULL,
    distance INTEGER NOT NULL
)
''')

conn.commit()
conn.close()

print("Database Created Successfully!")