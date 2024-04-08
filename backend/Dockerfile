FROM python:3.12.2-slim

WORKDIR /app

RUN apt-get update && apt-get install tesseract-ocr -y

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
