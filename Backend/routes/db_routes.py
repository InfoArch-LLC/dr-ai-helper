from flask import Blueprint, request, jsonify
from services.db_service import upload_and_process_file, clean_database
from utils import get_embedding
from config import Config

db_blueprint = Blueprint("db", __name__)

@db_blueprint.route("/upload_file", methods=["POST"])
def upload_file():
    file = request.files["file"]
    try:
        file_name = upload_and_process_file(file, Config.STORAGE_PATH, Config.DB_PATH, get_embedding())
        return jsonify({"status": "Successfully uploaded", "filename": file_name})
    
    except ValueError as e:
        return jsonify({"status": str(e)}), 400

@db_blueprint.route("/clean_db", methods=["POST"])
def clean_db():
    try:
        clean_database(Config.DB_PATH, get_embedding())
        return jsonify({"status": "DB Successfully cleaned"})
    
    except Exception as e:
        return jsonify({"status": "Error cleaning DB", "message": str(e)}), 500