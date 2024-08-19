import sqlite3


# Function to check if a column exists in a table
def column_exists(cursor, table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [info[1] for info in cursor.fetchall()]
    return column_name in columns


# Connect to SQLite database
conn = sqlite3.connect('bible.db')
cursor = conn.cursor()

# Check and add new column if it does not already exist
if not column_exists(cursor, 'Bible', 'chapter_id'):
    cursor.execute('ALTER TABLE Bible ADD COLUMN chapter_id INTEGER')

# Fetch all verses and chapters
cursor.execute('SELECT Chapter, Verse_Number FROM Bible')
verses = cursor.fetchall()

# Initialize variables
chapter_id = 0
current_chapter = None

# Update each verse with chapter ID
for chapter, verse_number in verses:
    # Check if this is a new chapter
    if chapter != current_chapter:
        chapter_id += 1
        current_chapter = chapter

    # Update the verse with the current chapter ID
    cursor.execute('UPDATE Bible SET chapter_id = ? WHERE Chapter = ? AND Verse_Number = ?',
                   (chapter_id, chapter, verse_number))

# Commit changes and close the connection
conn.commit()
conn.close()

print(f"Assigned chapter IDs up to: {chapter_id}")
