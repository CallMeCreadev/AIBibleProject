import os
import sqlite3
import gensim
import spacy
from rake_nltk import Rake
import nltk
import gensim.downloader as api

# Download necessary NLTK data
nltk.download('stopwords')

# Initialize RAKE
rake = Rake()

# Load and save GloVe model to local file if not already saved
glove_model_path = os.path.join('assets', 'glove-wiki-gigaword-100.gz')
if not os.path.exists(glove_model_path):
    model = api.load("glove-wiki-gigaword-100")
    model.save_word2vec_format(glove_model_path)


# Load SpaCy model from the asset folder
def load_spacy_model():
    model_path = os.path.join(os.path.dirname(__file__), 'assets/en_core_web_md')
    return spacy.load(model_path)


nlp = load_spacy_model()


# Load Gensim Word2Vec model from a local file
def load_glove_model():
    glove_file = os.path.join('assets', 'glove-wiki-gigaword-100.gz')
    model = gensim.models.KeyedVectors.load_word2vec_format(glove_file, binary=False)
    return model


word_vectors = load_glove_model()


# Function to generate related words list using RAKE, Gensim, and SpaCy
def generate_related_words(verse):
    # Extract keywords with RAKE
    rake.extract_keywords_from_text(verse)
    keywords = rake.get_ranked_phrases()

    # Find similar words with Gensim
    related_words = set()
    for keyword in keywords:
        try:
            related_words.update([word for word, _ in word_vectors.most_similar(keyword)])
        except KeyError:
            continue

    # Expand keywords using SpaCy
    doc = nlp(" ".join(keywords))
    for token in doc:
        related_words.add(token.lemma_)
        for similar_token in token.vocab:
            if similar_token.is_lower and similar_token.prob >= -15:
                related_words.add(similar_token.orth_)

    return list(related_words)


# Connect to SQLite database
conn = sqlite3.connect('bible.db')
cursor = conn.cursor()

# Add new column if not already present
cursor.execute('ALTER TABLE Bible ADD COLUMN spacy_gensim_keys TEXT')

# Fetch verses
cursor.execute('SELECT Chapter, Verse_Number, Verse FROM Bible')
verses = cursor.fetchall()

# Track progress
total_verses = len(verses)
print(f"Total number of verses to process: {total_verses}")

for i, (chapter, verse_number, verse) in enumerate(verses):
    related_words = generate_related_words(verse)
    related_words_str = ', '.join(related_words)
    cursor.execute('UPDATE Bible SET spacy_gensim_keys = ? WHERE Chapter = ? AND Verse_Number = ?',
                   (related_words_str, chapter, verse_number))

    # Print progress every 100 records
    if (i + 1) % 15 == 0:
        print(f"Processed {i + 1} out of {total_verses} verses")

# Commit changes and close the connection
conn.commit()
conn.close()
