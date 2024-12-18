from langchain_community.vectorstores import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

def process_query(query, db_path, embedding, cached_llm, prompt):
    vector_store = Chroma(persist_directory=db_path, embedding_function=embedding)
    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": 10, "score_threshold": 0.4},
    )

    document_chain = create_stuff_documents_chain(cached_llm, prompt)
    chain = create_retrieval_chain(retriever, document_chain)
    result = chain.invoke({"input": query})

    return result["answer"]

def format_string_to_html(answer_string):

    return "xx"
