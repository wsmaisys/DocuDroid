from fastapi import FastAPI, HTTPException, BackgroundTasks, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
import os
import uuid
import tempfile
import shutil
from chat_manager import chat_manager

app = FastAPI(
    title="DocuDroid API",
    description="DocuDroid - Intelligent Document Assistant API",
    version="1.0.0"
)

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve index.html at root
@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

@app.get("/api.html")
async def read_api_docs():
    return FileResponse("static/api.html")

@app.get("/appinfo.html")
async def read_app_info():
    return FileResponse("static/appinfo.html")

class ChatRequest(BaseModel):
    message: str
    thread_id: str
    mode: str = "general"  # "general", "pdf", or "web"

class WebUploadRequest(BaseModel):
    thread_id: str
    urls: List[str]

@app.on_event("startup")
async def startup_event():
    print("🚀 Starting Chat Manager API")
    print("📁 Checking environment...")
    if os.getenv("MISTRAL_API_KEY"):
        print("✅ MISTRAL_API_KEY found")
    else:
        print("❌ MISTRAL_API_KEY not found")

@app.post("/session/init")
async def init_session():
    """Initialize a new chat session"""
    thread_id = str(uuid.uuid4())
    chat_manager.init_user_session(thread_id)
    print(f"🆕 Created new session: {thread_id}")
    return {
        "thread_id": thread_id,
        "message": "Welcome! You can:\n1. Chat generally\n2. Upload PDFs for analysis\n3. Share URLs for web content analysis"
    }

@app.post("/chat")
async def chat(request: ChatRequest):
    """Handle chat requests based on mode"""
    print(f"📨 Received chat request: {request.dict()}")
    
    try:
        if request.mode == "pdf":
            response = chat_manager.query_pdf(request.thread_id, request.message)
        elif request.mode == "web":
            response = chat_manager.query_web(request.thread_id, request.message)
        else:  # general chat
            response = chat_manager.chat(request.message)
        
        print(f"✅ Generated response for thread {request.thread_id}")
        return {"response": response}
        
    except Exception as e:
        print(f"❌ Error in chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload/pdf")
async def upload_pdf(
    thread_id: str = Form(...),
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Handle PDF file upload"""
    print(f"📄 Received PDF upload for thread {thread_id}")
    
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            tmp_path = tmp_file.name
        
        # Initialize processing status
        process_id = chat_manager.start_pdf_processing(thread_id, file.filename)
        
        def process_pdf():
            try:
                result = chat_manager.upload_pdf(thread_id, tmp_path, file.filename, process_id)
                print(f"✅ PDF processing completed for {file.filename}")
            except Exception as e:
                error_msg = f"❌ Error processing PDF '{file.filename}': {str(e)}"
                print(error_msg)
            finally:
                try:
                    os.unlink(tmp_path)
                except:
                    pass
        
        background_tasks.add_task(process_pdf)
        
        return {
            "status": "processing",
            "message": f"📄 Processing PDF: {file.filename}...",
            "filename": file.filename,
            "process_id": process_id
        }
        
    except Exception as e:
        print(f"❌ Error in PDF upload: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status/{process_id}")
async def check_status(process_id: str):
    """Check processing status"""
    status = chat_manager.get_processing_status(process_id)
    if not status:
        raise HTTPException(status_code=404, detail="Process not found")
    return status

@app.post("/upload/web")
async def upload_web(request: WebUploadRequest):
    """Handle web content upload"""
    print(f"🌐 Processing URLs for thread {request.thread_id}")
    
    try:
        result = chat_manager.upload_web_content(request.thread_id, request.urls)
        return {
            "status": "success",
            "message": result
        }
    except Exception as e:
        print(f"❌ Error in web upload: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🚀 Starting FastAPI server...")
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)