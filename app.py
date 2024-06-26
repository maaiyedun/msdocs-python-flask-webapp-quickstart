from flask import Flask, request, render_template, jsonify
import string
import nltk
from nltk.util import ngrams
from collections import Counter

app = Flask(__name__)

def load_stopwords(filepath):
    with open(filepath, 'r') as file:
        stopwords = file.read().splitlines()
    return set(stopwords)

def process_text(text, stopwords):
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Split into words
    words = text.split()
    # Remove stop words
    filtered_words = [word for word in words if word.lower() not in stopwords]
    # Calculate word count
    word_count = len(filtered_words)
    # Calculate letter frequency
    letter_frequency = {}
    for word in filtered_words:
        for letter in word:
            if letter in letter_frequency:
                letter_frequency[letter] += 1
            else:
                letter_frequency[letter] = 1
    # Calculate bigrams
    bigrams = list(ngrams(filtered_words, 2))
    bigram_freq = Counter(bigrams)
    return word_count, letter_frequency, bigram_freq

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
        text = file.read().decode('utf-8')
        word_count, letter_frequency, bigram_freq = process_text(text, stopwords)
        bigram_freq = {f"{w1} {w2}": freq for (w1, w2), freq in bigram_freq.items()}
        return jsonify({
            "word_count": word_count,
            "letter_frequency": letter_frequency,
            "bigram_frequency": bigram_freq
        })

if __name__ == '__main__':
    nltk.download('punkt')
    app.run(debug=True)
