from flask import Flask
from flask_cors import CORS

from modules.auth.routes import auth_bp
from modules.core.routes import core_bp

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.register_blueprint(auth_bp)
app.register_blueprint(core_bp)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
