import datetime
import heapq
import os
import textwrap
from flask import Blueprint, jsonify, request, send_file
from fpdf import FPDF
from PIL import Image
import nltk
import pytesseract

from src.utils.auth import token_required

core_bp = Blueprint("core", __name__)


@core_bp.route("/api/ocr", methods=["POST"])
@token_required
def ocr():
    if "image" not in request.files:
        return jsonify({"message": "No file uploaded"}), 400

    file = request.files["image"]
    img = Image.open(file.stream)

    custom_config = r"--psm 1 --oem 3"
    recognized_text = pytesseract.image_to_string(img, config=custom_config)
    recognized_text = recognized_text.replace("\n", " ")

    return jsonify({"text": recognized_text}), 200


@core_bp.route("/api/summarize", methods=["POST"])
@token_required
def summarize():
    data = request.get_json()

    if "text" not in data:
        return jsonify({"message": "Text field is required"}), 400

    text = data["text"]

    # assume summaryLevel 30 if not provided
    if "summaryLevel" not in data:
        summary_ratio = 0.3
    else:
        summary_ratio = float(data["summaryLevel"]) / 100

    sentences = nltk.sent_tokenize(text)
    num_sentences = len(sentences)

    summary_length = int(num_sentences * summary_ratio)
    if summary_length <= 0:
        summary_length = 1

    word_frequencies = {}
    for word in nltk.word_tokenize(text):
        if word.lower() not in nltk.corpus.stopwords.words("english"):
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
    summary_sentences = heapq.nlargest(
        num_sentences, sentence_scores, key=sentence_scores.get
    )
    summary = " ".join(summary_sentences)

    return jsonify({"summary": summary}), 200


@core_bp.route("/api/exportpdf", methods=["POST"])
@token_required
def exportPdf():
    data = request.get_json()

    if "text" not in data or "summary" not in data:
        return jsonify({"message": "Text and summary fields are required"}), 400

    for file in os.listdir():
        if file.endswith(".pdf"):
            os.remove(file)

    text = data["text"]
    summary = data["summary"]

    a4_width_mm = 210
    pt_to_mm = 0.3528
    fontsize_pt = 10
    fontsize_mm = fontsize_pt * pt_to_mm
    margin_bottom_mm = 10
    character_width_mm = 7 * pt_to_mm
    width_text = a4_width_mm / character_width_mm

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    pdf.add_page()

    pdf.set_font("Courier", "B", 16)
    pdf.cell(200, 10, txt="ScriptScribe", ln=1, align="C")

    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200 - 10, pdf.get_y())
    pdf.ln(10)

    pdf.set_font("Courier", "B", fontsize_pt)
    process_text(pdf, "Input:", width_text, fontsize_mm)
    pdf.set_font("Courier", "", fontsize_pt)
    process_text(pdf, text, width_text, fontsize_mm)

    pdf.ln(10)

    pdf.set_font("Courier", "B", fontsize_pt)
    process_text(pdf, "Summary:", width_text, fontsize_mm)
    pdf.set_font("Courier", "", fontsize_pt)
    process_text(pdf, summary, width_text, fontsize_mm)

    current_time = datetime.datetime.now()
    timestamp = current_time.strftime("%y%m%d_%H%M%S")
    pdf_path = f"scriptscribe_exported-{timestamp}.pdf"
    pdf.output(pdf_path, "F")

    if not os.path.exists(pdf_path):
        return jsonify({"message": "PDF file not found"}), 500

    return send_file(pdf_path, as_attachment=True), 200


def process_text(pdf, text, width_text, fontsize_mm):
    lines = text.split("\n")
    for line in lines:
        wrapped_lines = textwrap.wrap(line, width_text)
        for wrapped_line in wrapped_lines:
            pdf.multi_cell(0, fontsize_mm, wrapped_line)
        if len(wrapped_lines) > 1:
            pdf.ln()
