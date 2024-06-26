from flask import Flask, request, render_template, jsonify
import string
import nltk
from nltk.util import ngrams
from collections import defaultdict, Counter
import os

app = Flask(__name__)

def load_stopwords(filepath):
    with open(filepath, 'r') as file:
        stopwords = file.read().splitlines()
    return set(stopwords)

def process_text_line(line, stopwords, letter_frequency, bigram_frequency, total_word_count, filtered_word_count, prev_words):
    # Convert to lowercase
    line = line.lower()
    # Remove punctuation
    line = line.translate(str.maketrans('', '', string.punctuation))
    # Split into words
    words = line.split()
    # Update total word count
    total_word_count += len(words)
    # Remove stop words
    filtered_words = [word for word in words if word not in stopwords]
    filtered_word_count += len(filtered_words)

    # Update letter frequency
    for word in filtered_words:
        for letter in word:
            letter_frequency[letter] += 1

    # Update bigram frequency
    bigrams = list(ngrams(prev_words + filtered_words, 2))
    for bigram in bigrams:
        bigram_frequency[bigram] += 1
    
    return total_word_count, filtered_word_count, filtered_words[-1:]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    if file:
        stopwords = load_stopwords('StopWords.txt')
        letter_frequency = defaultdict(int)
        bigram_frequency = defaultdict(int)
        total_word_count = 0
        filtered_word_count = 0
        prev_words = []

        try:
            for line in file:
                line = line.decode('utf-8')
                total_word_count, filtered_word_count, prev_words = process_text_line(line, stopwords, letter_frequency, bigram_frequency, total_word_count, filtered_word_count, prev_words)
            
            bigram_freq = {f"{w1} {w2}": freq for (w1, w2), freq in bigram_frequency.items()}
            
            return jsonify({
                "total_words": total_word_count,
                "word_count": filtered_word_count,
                "letter_frequency": dict(letter_frequency),
                "bigram_frequency": bigram_freq
            })
        except Exception as e:
            return jsonify({"error": str(e)})

if __name__ == '__main__':
    nltk.download('punkt')
    app.run(debug=True)
