from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.vectorstores.in_memory import InMemoryVectorStore
from langchain_mistralai import MistralAIEmbeddings
import os
from dotenv import load_dotenv

# Load env variables
load_dotenv()
api_key = os.getenv("mistral_api_key")
if not api_key:
    raise ValueError("MISTRAL_API_KEY not found in .env file")

# Store vector stores per user
web_vector_stores = {}

def upload_webpages(user_id: str, urls: list[str]):
    """
    Load webpages, chunk them, and create embeddings in memory.
    """
    try:
        if not user_id or not isinstance(user_id, str):
            raise ValueError(f"Invalid user_id: {user_id}")
        if not urls or not isinstance(urls, list):
            raise ValueError(f"Invalid URLs: {urls}")

        loader = WebBaseLoader(urls)
        docs = loader.load()

        # Split into chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            separators=["\n\n", "\n", ".", "!", "?", " ", ""]
        )
        chunks = splitter.split_documents(docs)

        # Create in-memory vector store
        vector_store = InMemoryVectorStore.from_documents(
            chunks,
            MistralAIEmbeddings(model="mistral-embed", api_key=api_key)
        )

        # Save per user
        web_vector_stores[user_id] = vector_store
        return f"🌐 Successfully processed {len(urls)} URLs with {len(chunks)} chunks."
    except ValueError as ve:
        raise ValueError(f"Configuration error: {str(ve)}")
    except Exception as e:
        raise Exception(f"Error processing web content: {str(e)}")

def query_webpages(user_id: str, query: str, k: int = 3):
    """
    Query the in-memory vector store for the user.
    """
    if user_id not in web_vector_stores:
        return "No webpages found for this user. Please upload first."

    vector_store = web_vector_stores[user_id]
    results = vector_store.similarity_search_with_score(query, k=k)

    # Format result context
    context = "\n\n".join([doc.page_content for doc, _ in results])
    return context