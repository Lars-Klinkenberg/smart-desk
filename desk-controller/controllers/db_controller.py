# Module Imports
import logging
import os
import mariadb

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME")

    )
except mariadb.Error as e:
    logging.error(f"Error connecting to MariaDB Platform: {e}")
    raise SystemExit(e) from e

# Get Cursor
cur = conn.cursor()
cur.execute("SELECT * FROM desk")
data = cur.fetchall()
conn.close()
# Print Result-set
for row in data:
    print(f"First Name: {row}")