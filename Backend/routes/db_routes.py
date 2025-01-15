from flask import Blueprint, request, jsonify, abort
from services.db_service import process_file, clean_database, process_all_files
from utils import get_embedding
from config import Config
import logging

db_blueprint = Blueprint("db", __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@db_blueprint.route("/upload_file", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    if not file:
        logger.error("No file provided")
        abort(400, description="No file provided")

    try:
        file_name = process_file(file, Config.STORAGE_PATH, Config.DB_PATH, get_embedding())
        return jsonify({"status": "Successfully uploaded", "filename": file_name})
    
    except ValueError as e:
        logger.error(f"Error: {str(e)}")
        abort(400, description=str(e))

@db_blueprint.route("/upload_all_files", methods=["POST"])
def upload_all_files():
    try:
        process_all_files(Config.STORAGE_PATH, Config.DB_PATH, get_embedding())
        return jsonify({"status": "Successfully uploaded"})
    
    except ValueError as e:
        logger.error(f"Error: {str(e)}")
        abort(400, description=str(e))

@db_blueprint.route("/clean_db", methods=["POST"])
def clean_db():
    try:
        clean_database(Config.DB_PATH, get_embedding())
        return jsonify({"status": "DB Successfully cleaned"})
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        abort(500, description=str(e))