import sqlite3

connection = sqlite3.connect('tech_support')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Questions (
id INTEGER PRIMARY KEY,
nickname TEXT NOT NULL,
question TEXT NOT NULL
)
''')

connection.commit()
connection.close()
