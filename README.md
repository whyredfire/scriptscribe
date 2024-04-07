# ScriptScribe

## Setting up virutal env
```
python -m venv venv
pip3 install -r requirements.txt
```

## Download NLTK data
```
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

## Running test cases
```
curl -X POST -F "image=@test.jpg" http://127.0.0.1:5000/ocr
curl -X POST -H "Content-Type: application/json" -d @test.json http://127.0.0.1:5000/summarize
```