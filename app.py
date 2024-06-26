from flask import Flask, request, render_template, jsonify
import string
import nltk
from nltk.util import ngrams
from collections import Counter, defaultdict
import os

app = Flask(__name__)

def load_stopwords(filepath):
    with open(filepath, 'r') as file:
        stopwords = file.read().split()
    return set(stopwords)

def process_text_chunk(chunk, stopwords, letter_frequency, bigram_frequency):
    # Remove punctuation
    chunk = chunk.translate(str.maketrans('', '', string.punctuation))
    # Split into words
    words = chunk.split()
    # Remove stop words and update counts
    filtered_words = [word for word in words if word.lower() not in stopwords]
    
    # Update letter frequency
    for word in filtered_words:
        for letter in word:
            letter_frequency[letter] += 1
    
    # Update bigram frequency
    bigrams = list(ngrams(filtered_words, 2))
    for bigram in bigrams:
        bigram_frequency[bigram] += 1
    
    return len(filtered_words)

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
        word_count = 0
        
        while True:
            chunk = file.read(1024 * 1024).decode('utf-8')  # Read file in 1MB chunks
            if not chunk:
                break
            word_count += process_text_chunk(chunk, stopwords, letter_frequency, bigram_frequency)
        
        bigram_freq = {f"{w1} {w2}": freq for (w1, w2), freq in bigram_frequency.items()}
        
        return jsonify({
            "word_count": word_count,
            "letter_frequency": dict(letter_frequency),
            "bigram_frequency": bigram_freq
        })

if __name__ == '__main__':
    nltk.download('punkt')
    app.run(debug=True)
