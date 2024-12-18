from flask import Blueprint, request, jsonify
from services.llm_service import process_query
from utils import get_cached_llm, get_prompt, get_embedding
from config import Config

llm_blueprint = Blueprint("llm", __name__)

@llm_blueprint.route("/ask_storage", methods=["POST"])
def ask_storage():
    query = request.json.get("query")
    result = process_query(query, Config.DB_PATH, get_embedding(), get_cached_llm(), get_prompt())
    
    return jsonify({"answer": result})