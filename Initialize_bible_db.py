import re
import sqlite3

# Connect to SQLite database (or create it)
conn = sqlite3.connect('bible.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Bible (
    Chapter TEXT,
    Verse_Number TEXT,
    Verse TEXT
)
''')

# Read the Bible text file
with open('bible.txt', 'r') as file:
    lines = file.readlines()

chapter = None

# Regex pattern to match verse numbers
verse_pattern = re.compile(r'(\d+:\d+)(?=\s)')

for line in lines:
    line = line.strip()
    # Check for a new chapter by detecting "####" marker
    if line.startswith('####'):
        chapter = line[5:].strip()
    else:
        # Find all verse numbers in the line
        matches = list(verse_pattern.finditer(line))

        if matches:
            for i, match in enumerate(matches):
                verse_number = match.group(1)
                start = match.end()
                end = matches[i + 1].start() if i + 1 < len(matches) else len(line)
                verse_text = line[start:end].strip()
                cursor.execute('INSERT INTO Bible (Chapter, Verse_Number, Verse) VALUES (?, ?, ?)',
                               (chapter, verse_number, verse_text))

# Commit changes and close the connection
conn.commit()
conn.close()
