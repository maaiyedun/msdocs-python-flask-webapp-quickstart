from flask import Flask, request, render_template, jsonify
import nltk
from nltk.util import bigrams
import re

nltk.download('punkt')

app = Flask(__name__)

def letter_frequency(text):
    frequencies = {}
    for char in text:
        if char.isalpha():
            frequencies[char] = frequencies.get(char, 0) + 1
    return frequencies

def word_count(text):
    words = re.findall(r'\b\w+\b', text)
    return len(words)

def words_starting_with(text, letters):
    words = re.findall(r'\b\w+\b', text)
    return [word for word in words if word[0].lower() in letters.lower()]

def remove_stopwords(text, stopwords):
    words = re.findall(r'\b\w+\b', text)
    filtered_words = [word for word in words if word.lower() not in stopwords]
    return ' '.join(filtered_words)

def find_bigrams(words):
    return list(bigrams(words))

def load_stopwords(filepath):
    with open(filepath, 'r') as file:
        stopwords = file.read().splitlines()
    return set(stopwords)

def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    if file:
        stopwords = load_stopwords('StopWords.txt')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        string_input = request.form['string_input']
        char_input = request.form['char_input']
        text_input = request.form['text_input']

        # Task 10
        frequencies = letter_frequency(text_input)
        total_chars = sum(frequencies.values())
        letter_freqs = {char: (count, count/total_chars) for char, count in frequencies.items() if char in string_input}

        replaced_text = ''
        for char in text_input:
            if char in string_input:
                replaced_text += char_input
            else:
                replaced_text += char
        

        #replaced_text = ''.join([char_input if char in string_input else char for char in text_input])

        # Task 11
        total_words = len(text_input.split())
        words_with_string_chars = words_starting_with(text_input, string_input)

        # Task 12
        with open('StopWords.txt', 'r') as file:
            stopwords = set(file.read().split())

        filtered_text = remove_stopwords(text_input, stopwords.lower())
        bigrams_list = find_bigrams(words_with_string_chars)

        return render_template('index.html', letter_freqs=letter_freqs,replaced_text=replaced_text, total_words=total_words,
                               words_with_string_chars=words_with_string_chars, bigrams_list=bigrams_list)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
