from langchain_community.document_loaders import PyPDFLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_mistralai import MistralAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

# Load API keys
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("MISTRAL_API_KEY not found in .env file")

# Global dictionary to store user-uploaded vector stores
USER_VECTOR_STORES = {}

class PDFToolInput(BaseModel):
    user_id: str = Field(description="Unique identifier for the user/session")
    action: str = Field(description="Action to perform: 'upload' or 'query'")
    query: str = Field(default="", description="Question to ask about the PDF content (required for query action)")
    file_path: str = Field(default="", description="Path to the PDF file (required for upload action)")

def pdf_tool_func(user_id: str, action: str, query: str = "", file_path: str = "") -> str:
    """
    Tool to upload and query PDF documents.
    
    Use this tool when users ask questions about uploaded PDFs, contracts, documents, etc.
    
    Args:
        user_id (str): Unique identifier for the user/session  
        action (str): "upload" to index a PDF, or "query" to search uploaded PDFs
        query (str): Question to ask about the PDF content (required for query)
        file_path (str): Path to the PDF file (required for upload)

    Returns:
        str: Success message for upload, or relevant content for query
    """
    if action == "upload":
        if not file_path:
            return "❌ file_path required for upload."

        try:
            loader = PyPDFLoader(file_path)
            pages = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=100,
                separators=["\n\n", "\n", ".", "!", "?", " ", ""]
            )
            docs = text_splitter.split_documents(pages)

            vector_store = InMemoryVectorStore.from_documents(
                docs,
                MistralAIEmbeddings(model="mistral-embed", api_key=api_key)
            )
            USER_VECTOR_STORES[user_id] = vector_store
            return f"✅ PDF uploaded and indexed successfully for user {user_id}. Contains {len(docs)} text chunks. You can now query this document."

        except Exception as e:
            return f"❌ Error uploading PDF: {str(e)}"

    elif action == "query":
        if user_id not in USER_VECTOR_STORES:
            return "❌ No PDF has been uploaded yet. Please upload a PDF first before querying."

        if not query:
            return "❌ Please provide a query/question to search the PDF."

        try:
            vector_store = USER_VECTOR_STORES[user_id]
            results = vector_store.similarity_search_with_score(query, k=5)
            
            if not results:
                return "❌ No relevant content found in the uploaded PDF for your query."
            
            # Format the results better
            context_parts = []
            for i, (doc, score) in enumerate(results, 1):
                context_parts.append(f"--- Relevant Section {i} (Relevance: {score:.3f}) ---\n{doc.page_content.strip()}")
            
            context = "\n\n".join(context_parts)
            return f"Here's the relevant information from the uploaded PDF:\n\n{context}"

        except Exception as e:
            return f"❌ Error querying PDF: {str(e)}"

    else:
        return "❌ Invalid action. Use 'upload' to index a PDF or 'query' to search it."

# Wrap as StructuredTool with better description
pdf_tool = StructuredTool.from_function(
    func=pdf_tool_func,
    name="pdf_tool",
    description="""Use this tool to work with PDF documents. 
    
    IMPORTANT: When users ask questions about 'the document', 'this PDF', 'the contract', or refer to uploaded content, use this tool with action='query' to search the uploaded PDF.
    
    Actions:
    - 'upload': Index a PDF file (requires file_path)
    - 'query': Search uploaded PDF content (requires query with the user's question)
    
    Examples of when to use with action='query':
    - User asks: "What is the contract period?" → Use pdf_tool(action="query", query="contract period")
    - User asks: "What are the terms?" → Use pdf_tool(action="query", query="terms and conditions")
    - User asks: "Summarize the document" → Use pdf_tool(action="query", query="document summary key points")
    """,
    args_schema=PDFToolInput
)