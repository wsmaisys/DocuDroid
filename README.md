# DocuDroid

DocuDroid is an intelligent document assistant that combines the power of LLMs with document analysis capabilities. It provides a modern, interactive interface for chatting, analyzing PDFs, and extracting insights from web content.

![DocuDroid Interface](DocuDroid Image.png)

## Features

- 🤖 **General Chat**: Engage in natural conversations with the AI assistant
- 📄 **PDF Analysis**: Upload and analyze PDF documents
- 🌐 **Web Content Analysis**: Extract and analyze content from web URLs
- 💬 **Real-time Processing**: Live status updates for document processing
- 🎯 **Multi-mode Operation**: Switch seamlessly between chat, PDF, and web modes
- 🔍 **Smart Context**: Maintains context for more relevant responses
- 🎨 **Modern UI**: Clean, responsive dark theme interface

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Mistral AI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/docudroid.git
cd docudroid
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your Mistral AI API key:
```env
MISTRAL_API_KEY=your_api_key_here
```

4. Run the application:
```bash
python -m uvicorn api:app --reload
```

5. Open your browser and navigate to `http://localhost:8000`

## Usage

### General Chat Mode
- Select "General Chat" mode
- Type your question and get instant responses

### PDF Analysis Mode
1. Switch to "PDF Chat" mode
2. Upload your PDF document
3. Ask questions about the document content
4. Get contextual responses based on the document

### Web Content Mode
1. Switch to "Web Chat" mode
2. Enter URLs to analyze
3. Ask questions about the web content
4. Get insights from the processed web pages

## API Documentation

The API documentation is available at `/docs.html` when running the application. It includes:
- Endpoint descriptions
- Request/response formats
- Error handling
- Usage examples

## Project Structure

```
docudroid/
├── api.py              # FastAPI application and routes
├── chat_manager.py     # Core chat and document processing logic
├── pdfloader.py        # PDF processing utilities
├── webloader.py        # Web content processing utilities
├── static/
│   ├── index.html     # Main application UI
│   └── docs.html      # API documentation
└── .env               # Environment variables
```

## Technologies Used

- **Backend**:
  - FastAPI
  - LangChain
  - Mistral AI
  - Python 3.13

- **Frontend**:
  - HTML5
  - CSS3
  - JavaScript
  - Marked.js for Markdown rendering

## Features in Detail

### PDF Processing
- Chunks documents for efficient processing
- Creates vector embeddings for semantic search
- Maintains session-based document context

### Web Content Analysis
- Extracts main content from web pages
- Processes multiple URLs simultaneously
- Creates searchable knowledge base from web content

### Chat Interface
- Real-time status updates
- Markdown support
- Code syntax highlighting
- Responsive design
- Dark theme for reduced eye strain

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This is a demonstration of AI capabilities and should not be used as an official or authoritative source. Always verify important information independently.

## Acknowledgments

- Built with [Mistral AI](https://mistral.ai)
- Powered by [LangChain](https://www.langchain.com)
- Uses [FastAPI](https://fastapi.tiangolo.com)