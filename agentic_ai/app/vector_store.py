import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
INDEX_DIR = "index/faiss_index"

def index_document(file_path):
    """
    Handles both PDF and TXT files to prevent server crashes.
    """
    try:
        # Determine the correct loader based on file extension
        if file_path.lower().endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file_path.lower().endswith(".txt"):
            loader = TextLoader(file_path)
        else:
            return "Unsupported file format. Please upload PDF or TXT."

        # Load and process the document
        docs = loader.load()
        
        # Create or update the FAISS index
        vector_db = FAISS.from_documents(docs, embeddings)
        
        # Ensure the directory exists before saving
        os.makedirs("index", exist_ok=True)
        vector_db.save_local(INDEX_DIR)
        
        return f"File '{os.path.basename(file_path)}' indexed successfully!"
    
    except Exception as e:
        # Returns the actual error message to the Swagger UI
        return f"Indexing error: {str(e)}"

def query_document(query):
    """
    Queries the local vector store with a distance threshold.
    """
    if not os.path.exists(INDEX_DIR):
        return None
        
    try:
        # Load the index safely
        vector_db = FAISS.load_local(
            INDEX_DIR, 
            embeddings, 
            allow_dangerous_deserialization=True
        )
        
        # Search for the most relevant context
        results = vector_db.similarity_search_with_score(query, k=2)
        
        # Threshold check: 0 is a perfect match, higher numbers are less relevant
        if not results or results[0][1] > 1.5:
            return None
            
        return results[0][0].page_content
    except Exception:
        return None