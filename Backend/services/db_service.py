import os
import logging
from typing import List, Set
from werkzeug.datastructures import FileStorage
from utils import get_embedding, remove_dR_article_date, extract_pdf_text
from langchain_community.vectorstores import Chroma
from langchain_experimental.text_splitter import SemanticChunker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS: Set[str] = {".pdf", ".txt"}

def is_allowed_file(file_name: str) -> bool:
    return os.path.splitext(file_name)[1].lower() in ALLOWED_EXTENSIONS

def concatenate_page_content(documents: List) -> str:
    return "".join(document.page_content for document in documents)

def save_file(file: FileStorage, storage_path: str) -> str:
    file_name = file.filename
    save_path = os.path.join(storage_path, file_name)
    file.save(save_path)
    return save_path

def process_text(file_path: str) -> str:
    loaded_text = extract_pdf_text(file_path)
    return remove_dR_article_date(loaded_text)

def create_documents_from_text(text: str, embedding) -> List:
    text_splitter = SemanticChunker(get_embedding(), breakpoint_threshold_type='percentile', breakpoint_threshold_amount=100)
    chunks = text_splitter.split_text(text)
    return text_splitter.create_documents(chunks)

def process_file(file: FileStorage, storage_path: str, db_path: str, embedding) -> str:
    try:
        if not is_allowed_file(file.filename):
            raise ValueError("Unsupported file type")
        
        save_path = save_file(file, storage_path)
        formatted_text = process_text(save_path)
        created_documents = create_documents_from_text(formatted_text, embedding)
        
        Chroma.from_documents(documents=created_documents, embedding=embedding, persist_directory=db_path)

        return file.filename
    
    except ValueError as ve:
        logger.error(f"ValueError: {ve}")
        raise
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        raise

def get_pdf_routes(folder_path: str) -> List[str]:
    rutas_pdf = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".pdf"):
                ruta_completa = os.path.join(root, file)
                rutas_pdf.append(ruta_completa)
    return rutas_pdf

def process_pdf(route: str, text_splitter, embedding, db_path: str) -> None:
    try:
        loaded_text = extract_pdf_text(route)
        formatted_text = remove_dR_article_date(loaded_text)
        chunks = text_splitter.split_text(formatted_text)
        created_documents = text_splitter.create_documents(chunks)
        Chroma.from_documents(documents=created_documents, embedding=embedding, persist_directory=db_path)
    except Exception as e:
        logger.error(f"Error processing file {route}: {e}")
        raise

def process_all_files(storage_path: str, db_path: str, embedding) -> None:
    try:
        if not os.path.exists(storage_path):
            logger.error(f"The folder '{storage_path}' does not exist.")
            return
        
        archivos = [f for f in os.listdir(storage_path) if f.endswith('.pdf')]
    
        if not archivos:
            logger.info("No PDF files found in the folder.")
            return

        pdf_routes = get_pdf_routes(storage_path)
        text_splitter = SemanticChunker(get_embedding(), breakpoint_threshold_type='percentile', breakpoint_threshold_amount=100)

        for route in pdf_routes:
            process_pdf(route, text_splitter, embedding, db_path)
    
    except Exception as e:
        logger.error(f"Error processing files: {e}")
        raise

def clean_database(db_path, embedding):
    try:
        vectordb = Chroma(persist_directory=db_path, embedding_function=embedding)
        vectordb.delete_collection()
    
    except Exception as e:
        logger.error(f"Error cleaning database : {e}")
        raise