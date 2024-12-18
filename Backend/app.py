from flask import Flask
from flask_cors import CORS
from routes.llm_routes import llm_blueprint
from routes.db_routes import db_blueprint

app = Flask(__name__)

def create_app():
    app.register_blueprint(llm_blueprint, url_prefix="/api/llm")
    app.register_blueprint(db_blueprint, url_prefix="/api/db")

CORS(app)

if __name__ == "__main__":
    create_app()
    app.run(host="0.0.0.0", port=8080, debug=False)