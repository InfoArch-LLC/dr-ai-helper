import os

class Config:
    STORAGE_PATH = os.getenv("STORAGE_PATH", "storage")
    DB_PATH = os.getenv("DB_PATH", "db")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "MyFilesCollection")
    DEBUG = os.getenv("DEBUG", True)