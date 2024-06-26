from flask import Flask, request, render_template, redirect, url_for
import os
import string

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'txt'}

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file1' not in request.files or 'file2' not in request.files or 'file3' not in request.files:
        return redirect(request.url)
    
    file1 = request.files['file1']
    file2 = request.files['file2']
    file3 = request.files['file3']
    
    if file1 and allowed_file(file1.filename):
        file1.save(os.path.join(app.config['UPLOAD_FOLDER'], 'file1.txt'))
    if file2 and allowed_file(file2.filename):
        file2.save(os.path.join(app.config['UPLOAD_FOLDER'], 'file2.txt'))
    if file3 and allowed_file(file3.filename):
        file3.save(os.path.join(app.config['UPLOAD_FOLDER'], 'file3.txt'))

    return redirect(url_for('process_files'))

@app.route('/process')
def process_files():
    file1_path = os.path.join(app.config['UPLOAD_FOLDER'], 'file1.txt')
    file2_path = os.path.join(app.config['UPLOAD_FOLDER'], 'file2.txt')
    file3_path = os.path.join(app.config['UPLOAD_FOLDER'], 'file3.txt')

    with open(file3_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    text_processed, char_count, word_count = process_text_file(text)

    similarity = compare_files(file1_path, file2_path, text_processed)

    final_text = remove_short_words(text_processed)

    result = {
        'char_count': char_count,
        'word_count': word_count,
        'similarity': similarity,
        'final_text': final_text
    }
    
    return render_template('result.html', result=result)

def process_text_file(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    char_count = len(text)
    word_count = len(text.split())
    return text, char_count, word_count

def compare_files(file1_path, file2_path, text):
    with open(file1_path, 'r', encoding='utf-8') as f1, open(file2_path, 'r', encoding='utf-8') as f2:
        text1 = f1
