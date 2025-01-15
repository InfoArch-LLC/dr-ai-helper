#from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain.prompts import PromptTemplate
import pdfplumber

def get_cached_llm():
    return ChatOllama(model="llama3.1")
    #return Ollama(model="llama3.1")

def get_embedding():
    return FastEmbedEmbeddings()

def get_prompt():
    return PromptTemplate.from_template("""
        You are a technical assistant for dReveal company, skilled at extracting and synthesizing information from provided documents.

        **Task:**
        Given the following 'Context', provide a concise and informative response for the 'Query'. If the context is insufficient to provide a definitive answer, state "Insufficient information to provide a specific answer." and don't give further information.
        
        **Context:** {context}
                                        
        **Query:** {input}
    """)

def remove_dR_article_date(text):
    lineas = text.split('\n')
    lineas = [linea for linea in lineas if "AArrttiiccllee" not in linea]
    
    return '\n'.join(lineas)

def fix_dR_article_date(text):
    lineas = text.split('\n')

    for i, linea in enumerate(lineas):
        if "AArrttiiccllee" in linea:
            nueva_linea = ''.join([linea[j] for j in range(len(linea)) if j % 2 == 0])
            lineas[i] = nueva_linea
    
    return '\n'.join(lineas)

def extract_pdf_text(file_path):
    texto_completo = ""
        
    with pdfplumber.open(file_path) as pdf:
        for pagina in pdf.pages:
            texto_completo += pagina.extract_text() + "\n"
    
    return texto_completo