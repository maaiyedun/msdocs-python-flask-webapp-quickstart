from flask import Flask, request, render_template, jsonify
from unidecode import unidecode
import string

app = Flask(__name__)

def remove_non_ascii(text):
    return ''.join(c for c in text if ord(c) < 128)

def process_text(text):
    text = remove_non_ascii(text)
    text = text.lower()
    return text

def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))

def count_letters_and_words(text):
    letters = sum(c.isalpha() for c in text)
    words = len(text.split())
    return letters, words

def letter_frequency(text, letters='aeiou'):
    total_chars = len(text)
    frequency = {letter: text.count(letter) / total_chars for letter in letters}
    return frequency

def compare_frequencies(freq1, freq2):
    diff = sum((freq1[letter] - freq2[letter]) ** 2 for letter in freq1) / 5
    return diff

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_files():
    files = [request.files['file1'], request.files['file2'], request.files['file3']]
    texts = [process_text(f.read().decode('latin-1')) for f in files]

    texts[2] = remove_punctuation(texts[2])
    letters, words = count_letters_and_words(texts[2])

    freq1 = letter_frequency(texts[0])
    freq2 = letter_frequency(texts[1])
    freq3 = letter_frequency(texts[2])

    diff1 = compare_frequencies(freq3, freq1)
    diff2 = compare_frequencies(freq3, freq2)

    closer = "File 1" if diff1 < diff2 else "File 2"

    processed_text3 = ' '.join(word for word in texts[2].split() if len(word) >= 3)

    result = {
        "file3": {
            "total_letters": letters,
            "total_words": words,
            "closer_to": closer,
            "processed_text": processed_text3
        }
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
