from langchain_community.llms import Ollama
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain.prompts import PromptTemplate

def get_cached_llm():
    return Ollama(model="llama3.1")

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
