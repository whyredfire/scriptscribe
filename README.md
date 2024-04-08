# ScriptScribe

ScriptScribe is a tool designed to facilitate text processing tasks such as optical character recognition (OCR) and text summarization.

## Getting Started

### Setting up a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment:
```bash
# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

Install required packages:
```bash
pip install -r requirements.txt
```

### Downloading NLTK Data

Before running the tool, ensure NLTK data is downloaded for text processing:

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

## Dependencies

The project dependencies are listed in `requirements.txt` and can be installed using pip:

```bash
pip install -r requirements.txt
```

## Usage

### OCR (Optical Character Recognition)

To perform OCR on an image file (`test.jpg` in this example), use `curl` to send a POST request to the local server:

```bash
curl -X POST -F "image=@test.jpg" http://127.0.0.1:5000/ocr
```

### Text Summarization

For text summarization, provide a JSON file (`test.json` in this example) containing the text to be summarized. Send a POST request with the JSON data to the local server:

```bash
curl -X POST -H "Content-Type: application/json" -d @test.json http://127.0.0.1:5000/summarize
```

### Exporting summary

For exporting summary, provide a JSON file (`test_pdf.json` in this example) containing the text and its summary. Send a POST request with the JSON data to the local server:

```bash
curl -X POST -H "Content-Type: application/json" -d @test_pdf.json http://127.0.0.1:5000/exportpdf --output test.pdf
```