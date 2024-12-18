import sqlite3
import database

conn = sqlite3.connect('Zia.db')
c = conn.cursor()

print("Users:")
c.execute("SELECT * FROM users")
for row in c.fetchall():
    print(row)

conn.close()