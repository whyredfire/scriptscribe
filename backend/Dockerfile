FROM python:3.12.2-slim

WORKDIR /app

RUN apt-get update && apt-get install tesseract-ocr wget unzip -y

COPY requirements.txt .
RUN pip install -r requirements.txt

ENV NLTK_DATA=/usr/share/nltk_data
RUN mkdir -p /usr/share/nltk_data/tokenizers /usr/share/nltk_data/corpora
RUN wget -q -P /usr/share/nltk_data/tokenizers https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/tokenizers/punkt.zip && \
    wget -q -P /usr/share/nltk_data/corpora https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/stopwords.zip && \
    wget -q -P /usr/share/nltk_data/corpora https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/wordnet.zip && \
    unzip /usr/share/nltk_data/tokenizers/punkt.zip -d /usr/share/nltk_data/tokenizers && \
    unzip /usr/share/nltk_data/corpora/stopwords.zip -d /usr/share/nltk_data/corpora && \
    unzip /usr/share/nltk_data/corpora/wordnet.zip -d /usr/share/nltk_data/corpora && \
    rm /usr/share/nltk_data/tokenizers/punkt.zip && \
    rm /usr/share/nltk_data/corpora/stopwords.zip && \
    rm /usr/share/nltk_data/corpora/wordnet.zip

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
