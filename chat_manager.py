from langchain_mistralai import ChatMistralAI
from typing import Optional, Dict, List
from pdfloader import pdf_tool_func
from webloader import upload_webpages, query_webpages
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("mistral_api_key")

# Initialize LLM
llm = ChatMistralAI(model="mistral-small-latest")

class ChatManager:
    def __init__(self):
        self.user_contexts: Dict[str, dict] = {}
        self.processing_status: Dict[str, dict] = {}
    
    def init_user_session(self, user_id: str) -> None:
        """Initialize a new user session"""
        if user_id not in self.user_contexts:
            self.user_contexts[user_id] = {
                "pdf_loaded": False,
                "web_loaded": False
            }
    
    def start_pdf_processing(self, user_id: str, filename: str) -> str:
        """Initialize PDF processing status"""
        process_id = f"pdf_{user_id}_{filename}"
        self.processing_status[process_id] = {
            "status": "processing",
            "message": f"📄 Processing PDF: {filename}..."
        }
        return process_id

    def update_pdf_status(self, process_id: str, status: str, message: str):
        """Update PDF processing status"""
        if process_id in self.processing_status:
            self.processing_status[process_id] = {
                "status": status,
                "message": message
            }

    def get_processing_status(self, process_id: str) -> dict:
        """Get current processing status"""
        return self.processing_status.get(process_id, {})

    def upload_pdf(self, user_id: str, file_path: str, filename: str, process_id: str) -> str:
        """Upload and process a PDF file"""
        try:
            result = pdf_tool_func(
                user_id=user_id,
                action="upload",
                file_path=file_path
            )
            self.user_contexts[user_id]["pdf_loaded"] = True
            success_message = f"✅ PDF '{filename}' uploaded and processed successfully. {result}"
            self.update_pdf_status(process_id, "completed", success_message)
            return success_message
        except Exception as e:
            error_message = f"❌ Error processing PDF '{filename}': {str(e)}"
            self.update_pdf_status(process_id, "error", error_message)
            return error_message
    
    def upload_web_content(self, user_id: str, urls: List[str]) -> str:
        """Upload and process web content"""
        if not user_id:
            return "❌ Error: No session ID provided. Please refresh the page and try again."
        
        if not urls:
            return "❌ Error: No URLs provided. Please enter a valid URL."

        try:
            # Initialize user context if not exists
            if user_id not in self.user_contexts:
                self.init_user_session(user_id)
                
            result = upload_webpages(user_id, urls)
            self.user_contexts[user_id]["web_loaded"] = True
            return result
        except ValueError as ve:
            return f"❌ Validation Error: {str(ve)}"
        except Exception as e:
            error_msg = str(e)
            if "Invalid user_id" in error_msg:
                return "❌ Session Error: Please refresh the page and try again."
            elif "Invalid URLs" in error_msg:
                return "❌ Invalid URL format. Please check the URL and try again."
            else:
                return f"❌ Error: Could not process web content. {error_msg}"
    
    def query_pdf(self, user_id: str, query: str) -> str:
        """Query PDF content"""
        if not self.user_contexts.get(user_id, {}).get("pdf_loaded"):
            return "No PDF content has been loaded yet. Please upload a PDF first."
        
        try:
            context = pdf_tool_func(
                user_id=user_id,
                action="query",
                query=query
            )
            system_prompt = """You are DocuDroid, an intelligent document assistant. Your primary function is to help users understand documents. """
            response = llm.invoke(
                f"{system_prompt}\n\nAnswer the question using this context:\n\n{context}\n\nQuestion: {query}"
            )
            return response.content
        except Exception as e:
            return f"Error querying PDF: {str(e)}"
    
    def query_web(self, user_id: str, query: str) -> str:
        """Query web content"""
        if not self.user_contexts.get(user_id, {}).get("web_loaded"):
            return "No web content has been loaded yet. Please add some URLs first."
        
        try:
            context = query_webpages(user_id, query)
            system_prompt = """You are DocuDroid, an intelligent document assistant. Your primary function is to help users understand web content."""
            response = llm.invoke(
                f"{system_prompt}\n\nAnswer the question using this context:\n\n{context}\n\nQuestion: {query}"
            )
            return response.content
        except Exception as e:
            return f"Error querying web content: {str(e)}"
    
    def chat(self, query: str) -> str:
        """General chat without context"""
        try:
            system_prompt = """You are DocuDroid, an intelligent document assistant. Your primary function is to help users interact with documents and web content. Briefly mention your capabilities (handling PDFs and web content)."""
            response = llm.invoke(f"{system_prompt}\n\nHuman: {query}")
            return response.content
        except Exception as e:
            return f"Error in chat: {str(e)}"

# Create a global chat manager instance
chat_manager = ChatManager()