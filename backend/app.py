from flask import Flask

from src.routes.auth import auth_bp
from src.routes.core import core_bp


def on_startup():
    import nltk

    nltk.download("punkt")
    nltk.download("punkt_tab")
    nltk.download("stopwords")
    nltk.download("wordnet")


on_startup()

app = Flask(__name__)

app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(core_bp, url_prefix="/api")
