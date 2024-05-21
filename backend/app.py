from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from fpdf import FPDF
from PIL import Image
from pymongo import MongoClient
import datetime
import hashlib
import heapq
import nltk
import os
import pytesseract
import textwrap

app = Flask(__name__)
CORS(app)

host = os.environ.get('MONGO_HOST', 'localhost') 
port = os.environ.get('MONGO_PORT', '27017')
connection_string = f'mongodb://{host}:{port}/'

client = MongoClient(connection_string)
collection = client.scriptscribe.users

def validate_creds(username, password):
    if not username:
        return jsonify({
            'message': 'username cannot be empty',
            'isSuccessful': False
            }), 200
    elif not password:
        return jsonify({
            'message': 'password cannot be empty',
            'isSuccessful': False
            }), 200

def check_user(username):
    users = list(collection.find())
    for user in users:
        if user.get('username') == username:
            return True
    return False

def salty_pass(username, password):
    salt = 'scriptscribeftw'
    salted_pass = username + salt + password

    hashed_pass = hashlib.md5(salted_pass.encode())
    return hashed_pass.hexdigest()

@app.route('/api/login', methods=['POST'])
def auth():
    def user_auth(username, password):
        users = list(collection.find())
        for user in users:
            if user.get('username') == username and user.get('password') == salty_pass(username, password):
                return True
        return False

    data = request.get_json()
    username = data['username']
    password = data['password']

    response = validate_creds(username, password)
    if response:
        return response
    
    if not check_user(username):
        return jsonify({
            'message': 'user does not exist',
            'isSuccessful': False
            }), 200

    if user_auth(username, password):
        return jsonify({
            'message': 'logged in',
            'isSuccessful': True
            }), 200
    else:
        return jsonify({
            'message': 'incorrect password',
            'isSuccessful': False
            }), 200
    
@app.route('/api/signup', methods=['POST'])
def signup():
    def add_user(username, hashed_pass):
        new_user = {
            'username': username,
            'password': hashed_pass
        }
        inserted_id = collection.insert_one(new_user).inserted_id
        return inserted_id

    data = request.get_json()
    username = data['username']
    password = data['password']

    response = validate_creds(username, password)
    if response:
        return response

    if check_user(username):
        return jsonify({
            'message': 'username already taken',
            'isSuccessful': False
            }), 200

    hashed_pass = salty_pass(username, password)

    if (add_user(username, hashed_pass)):
        return jsonify({
            'message': 'signed up',
            'isSuccessful': True
            }), 200

@app.route('/api/ocr', methods=['POST'])
def ocr():
    if 'image' not in request.files:
        return jsonify({
            'message': 'No file uploaded',
            'isSuccessful': False
            }), 200

    file = request.files['image']
    img = Image.open(file.stream)
    
    custom_config = r"--psm 1 --oem 3"
    recognized_text = pytesseract.image_to_string(img, config=custom_config)
    recognized_text = recognized_text.replace('\n', ' ')

    return jsonify({
        'text': recognized_text,
        'isSuccessful': True
        }), 200

@app.route('/api/summarize', methods=['POST'])
def summarize():
    data = request.get_json()

    if 'text' not in data:
        return jsonify({
            'message': 'Text field is required',
            'isSuccessful': False
            }), 200

    text = data['text']
    summary_ratio = float(data['summaryLevel']) / 100
    sentences = nltk.sent_tokenize(text)
    num_sentences = len(sentences)

    summary_length = int(num_sentences * summary_ratio)
    if summary_length <= 0:
        summary_length = 1

    word_frequencies = {}
    for word in nltk.word_tokenize(text):
        if word.lower() not in nltk.corpus.stopwords.words('english'):
            if word.lower() not in word_frequencies:
                word_frequencies[word.lower()] = 1
            else:
                word_frequencies[word.lower()] += 1

    maximum_frequency = max(word_frequencies.values())
    for word in word_frequencies:
        word_frequencies[word] = word_frequencies[word] / maximum_frequency

    sentence_scores = {}
    for sentence in sentences:
        for word in nltk.word_tokenize(sentence.lower()):
            if word in word_frequencies:
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = word_frequencies[word]
                else:
                    sentence_scores[sentence] += word_frequencies[word]

    num_sentences = min(summary_length, len(sentences))
    summary_sentences = heapq.nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)

    return jsonify({
        'summary': summary,
        'isSuccessful': True
        }), 200

@app.route('/api/exportpdf', methods=['POST'])
def exportPdf():
    data = request.get_json()

    if 'text' not in data or 'summary' not in data:
        return jsonify({
            'message': 'Text and summary fields are required',
            'isSuccessful': False
        }), 400

    for file in os.listdir():
        if file.endswith('.pdf'):
            os.remove(file)

    text = data['text']
    summary = data['summary']

    a4_width_mm = 210
    pt_to_mm = 0.3528
    fontsize_pt = 10
    fontsize_mm = fontsize_pt * pt_to_mm
    margin_bottom_mm = 10
    character_width_mm = 7 * pt_to_mm
    width_text = a4_width_mm / character_width_mm

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    pdf.add_page()
    
    pdf.set_font('Courier', 'B', 16)
    pdf.cell(200, 10, txt="ScriptScribe", ln=1, align='C')

    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200 - 10, pdf.get_y())
    pdf.ln(10)

    pdf.set_font('Courier', 'B', fontsize_pt)
    process_text(pdf, "Input:", width_text, fontsize_mm)
    pdf.set_font('Courier', '', fontsize_pt)
    process_text(pdf, text, width_text, fontsize_mm)

    pdf.ln(10)

    pdf.set_font('Courier', 'B', fontsize_pt)
    process_text(pdf, "Summary:", width_text, fontsize_mm)
    pdf.set_font('Courier', '', fontsize_pt)
    process_text(pdf, summary, width_text, fontsize_mm)

    current_time = datetime.datetime.now()
    timestamp = current_time.strftime("%y%m%d_%H%M%S")
    pdf_path = f"scriptscribe_exported-{timestamp}.pdf"
    pdf.output(pdf_path, 'F')

    if not os.path.exists(pdf_path):
        return jsonify({
            'message': 'PDF file not found',
            'isSuccessful': False
        }), 500

    return send_file(pdf_path, as_attachment=True), 200

def process_text(pdf, text, width_text, fontsize_mm):
    lines = text.split('\n')
    for line in lines:
        wrapped_lines = textwrap.wrap(line, width_text)
        for wrapped_line in wrapped_lines:
            pdf.multi_cell(0, fontsize_mm, wrapped_line)
        if len(wrapped_lines) > 1:
            pdf.ln()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
