from src.data_loader import load_all_documents
from src.vectorstore import FaissVectorStore
from src.search import RAGSearch


if __name__ == '__main__':
    docs = load_all_documents('data')
    store = FaissVectorStore('faiss_store')
    store.load()

    rag_search =RAGSearch()
    query = 'What are the differenct phases of data ingestion?'
    summary = rag_search.search_and_summarise(query, top_k=3)
    print('Summary: ', summary)