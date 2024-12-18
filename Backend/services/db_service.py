from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PDFPlumberLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

def upload_and_process_file(file, storage_path, db_path, embedding):
    file_name = file.filename
    file_extension = os.path.splitext(file_name)[1].lower()
    save_path = os.path.join(storage_path, file_name)
    file.save(save_path)

    if file_extension == ".pdf":
        loader = PDFPlumberLoader(save_path)
    elif file_extension == ".txt":
        loader = TextLoader(save_path)
    else:
        raise ValueError("Unsupported file type")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=30)
    docs_loader = loader.load_and_split(text_splitter)

    for doc in docs_loader:
        print("\n****     Inicio     ****")
        print(doc.page_content)
        print("****      Fin     ****\n")

    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=80)
    chunks = text_splitter.split_documents(docs_loader)

    Chroma.from_documents(documents=chunks, embedding=embedding, persist_directory=db_path)

    return file_name

def clean_database(db_path, embedding):
    vectordb = Chroma(persist_directory=db_path, embedding_function=embedding)
    vectordb.delete_collection()
