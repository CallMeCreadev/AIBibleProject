import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('bible.db')
cursor = conn.cursor()

# Add a new column called 'page' if it doesn't exist
cursor.execute("ALTER TABLE bible ADD COLUMN page INTEGER")

# Fetch all records to update the page number
cursor.execute("SELECT rowid FROM bible")
rows = cursor.fetchall()

# Initialize the page number
page = 1

# Update the page number for every 20 records
for index, row in enumerate(rows):
    rowid = row[0]
    cursor.execute("UPDATE bible SET page = ? WHERE rowid = ?", (page, rowid))

    # Increment the page number every 20 records
    if (index + 1) % 20 == 0:
        page += 1

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Page numbers updated successfully.")
