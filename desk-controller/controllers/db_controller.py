# Module Imports
import mariadb
import sys

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="deskController",
        password="pw1234",
        host="localhost",
        port=3306,
        database="standing_desk"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()
cur.execute("SELECT * FROM desk")
data = cur.fetchall()
conn.close()
# Print Result-set
for row in data:
    print(f"First Name: {row}")