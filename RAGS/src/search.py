import os
from dotenv import load_dotenv
from src.vectorstore import FaissVectorStore
from langchain.chat_models import init_chat_model
from src.data_loader import load_all_documents

load_dotenv()

class RAGSearch:
    def __init__(self, persist_dir: str = 'faiss_store', embedding_model: str = 'all-MiniLm-L6-v2', llm_model: str = 'groq:qwen/qwen3-32b'):
        self.vectorestore = FaissVectorStore(persist_dir, embedding_model)
        faiss_path = os.path.join(persist_dir, 'faiss_index')
        meta_path = os.path.join(persist_dir, 'metadata.pkl')
        if not (os.path.exists(faiss_path) and os.path.exists(meta_path)):
            docs = load_all_documents('data')
            self.vectorestore.build_from_documents(docs)
        else:
            self.vectorestore.load()
        self.llm = init_chat_model(model=llm_model)
        print(f'[INFO] LLm initialized: {llm_model}')
    
    def search_and_summarise(self, query:str, top_k: int = 5)-> str:
        results = self.vectorestore.query(query, top_k=top_k)
        texts = [r['metadata'].get('text', '') for r in results if r['metadata']]
        context = "\n\n".join(texts)
        if not context:
            return "No relevant documents found"
        prompt = f'''Summarise the following context for the query: "{query}" \n\nContext: {context}\n\nSummary:'''
        response = self.llm.invoke([prompt])
        return response.content
    
    
if __name__  == "__main__":
    rag_search = RAGSearch()
    query = "What is global protect used for?"
    summary = rag_search.search_and_summarise(query, top_k=3)
    print('Summary: ', summary)
