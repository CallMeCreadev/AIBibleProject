import sqlite3

# Dictionary mapping book names to numbers
bible_books = {
    "Genesis": 1,
    "Exodus": 2,
    "Leviticus": 3,
    "Numbers": 4,
    "Deuteronomy": 5,
    "Joshua": 6,
    "Judges": 7,
    "Ruth": 8,
    "First Samuel": 9,
    "Second Samuel": 10,
    "First Kings": 11,
    "Second Kings": 12,
    "First Chronicles": 13,
    "Second Chronicles": 14,
    "Ezra": 15,
    "Nehemiah": 16,
    "Esther": 17,
    "Job": 18,
    "Psalms": 19,
    "Proverbs": 20,
    "Ecclesiastes": 21,
    "Solomon": 22,
    "Isaiah": 23,
    "Jeremiah": 24,
    "Lamentations": 25,
    "Ezekiel": 26,
    "Daniel": 27,
    "Hosea": 28,
    "Joel": 29,
    "Amos": 30,
    "Obadiah": 31,
    "Jonah": 32,
    "Micah": 33,
    "Nahum": 34,
    "Habakkuk": 35,
    "Zephaniah": 36,
    "Haggai": 37,
    "Zechariah": 38,
    "Malachi": 39,
    "Matthew": 40,
    "Mark": 41,
    "Luke": 42,
    "Saint John": 43,
    "Apostles": 44,
    "Romans": 45,
    "First Corinthians": 46,
    "Second Corinthians": 47,
    "Galatians": 48,
    "Ephesians": 49,
    "Philippians": 50,
    "Colossians": 51,
    "First Thessalonians": 52,
    "Second Thessalonians": 53,
    "First Timothy": 54,
    "Second Timothy": 55,
    "Titus": 56,
    "Philemon": 57,
    "Hebrews": 58,
    "James": 59,
    "First Peter": 60,
    "Second Peter": 61,
    "First John": 62,
    "Second John": 63,
    "Third John": 64,
    "Jude": 65,
    "Revelations": 66
}

# Reverse dictionary for easy lookup of book names by their ID
books_by_id = {v: k for k, v in bible_books.items()}


# Function to check if a column exists in a table
def column_exists(cursor, table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [info[1] for info in cursor.fetchall()]
    return column_name in columns


# Connect to SQLite database
conn = sqlite3.connect('bible.db')
cursor = conn.cursor()

# Check and add new column if it does not already exist
if not column_exists(cursor, 'Bible', 'bible_book'):
    cursor.execute('ALTER TABLE Bible ADD COLUMN bible_book TEXT')

# Fetch all distinct chapter_ids
cursor.execute('SELECT DISTINCT chapter_id FROM Bible')
chapter_ids = cursor.fetchall()

# Update each chapter_id with the corresponding book name
for chapter_id_tuple in chapter_ids:
    chapter_id = chapter_id_tuple[0]
    book_name = books_by_id.get(chapter_id, "Unknown Book")

    # Update the verses with the current book name
    cursor.execute('UPDATE Bible SET bible_book = ? WHERE chapter_id = ?',
                   (book_name, chapter_id))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Assigned bible book names based on chapter IDs.")
