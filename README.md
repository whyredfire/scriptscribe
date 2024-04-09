# ScriptScribe

ScriptScribe is a tool designed to facilitate text processing tasks such as optical character recognition (OCR) and text summarization.

## Deploying the webapp

### Frontend

```bash
cd frontend
docker build -t scriptscribe-frontend .

docker run -d -p 80:80 scriptscribe-backend
```

### Backend

```bash
cd backend
docker build -t scriptscribe-backend .

docker run -d -p 5000:5000 scriptscribe-backend
```

<details open> 
<summary>
<h2>Testing API endpoints</h2>
</summary>

### OCR (Optical Character Recognition)

To perform OCR on an image file (`test.jpg` in this example), use `curl` to send a POST request to the local server:

```bash
curl -X POST -F "image=@tests/test.jpg" http://0.0.0.0:5000/ocr
```

### Text summarization

For text summarization, provide a JSON file (`test.json` in this example) containing the text to be summarized. Send a POST request with the JSON data to the local server:

```bash
curl -X POST -H "Content-Type: application/json" -d @tests/test.json http://0.0.0.0:5000/summarize
```

### Exporting summary

For exporting summary, provide a JSON file (`test_pdf.json` in this example) containing the text and its summary. Send a POST request with the JSON data to the local server:

```bash
curl -X POST -H "Content-Type: application/json" -d @tests/test_pdf.json http://0.0.0.0:5000/exportpdf --output tests/test.pdf
```
</details>