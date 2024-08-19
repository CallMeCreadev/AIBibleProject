import sqlite3
import random

# Function to fetch matching verses based on related words and selectable field
def fetch_matching_verses(prompt, top_n=10, select_n=3):
    related_words_set = set(prompt.split())

    conn = sqlite3.connect('bible.db')
    cursor = conn.cursor()

    cursor.execute("SELECT bible_book, Verse_Number, Verse, spacy_gensim_keys FROM Bible")
    verses = cursor.fetchall()

    matching_verses = []
    for chapter, verse_number, verse, spacy_gensim_keys in verses:
        if spacy_gensim_keys:
            verse_related_words_set = set(spacy_gensim_keys.split(', '))
            common_words = related_words_set.intersection(verse_related_words_set)
            matching_verses.append((chapter, verse_number, verse, len(common_words)))

    # Sort verses by the number of matching words (descending)
    matching_verses.sort(key=lambda x: x[3], reverse=True)

    # Select top N matching verses
    top_n_verses = matching_verses[:top_n]

    # Randomly select M verses from the top N
    selected_verses = random.sample(top_n_verses, min(select_n, len(top_n_verses)))

    conn.close()
    return selected_verses


