# DocuDroid

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Deployment Status](https://img.shields.io/badge/deployment-active-success)](https://docudroid-114168985695.us-central1.run.app)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

DocuDroid is an intelligent document analysis and chat platform that harnesses the power of Large Language Models (LLMs) through Mistral AI. It provides a modern, interactive interface for document analysis, web content processing, and natural language interactions.

🌐 **[Try DocuDroid Live](https://docudroid-114168985695.us-central1.run.app)**

![DocuDroid Interface](static/DocuDroid%20Image.png)

## 🌟 Key Features

- 🤖 **Intelligent Chat**: Natural language conversations powered by Mistral AI
- 📄 **PDF Analysis**: Upload and analyze PDF documents with semantic search capabilities
- 🌐 **Web Content Processing**: Extract and analyze content from web URLs
- 💬 **Context-Aware**: Maintains conversation context for more relevant responses
- 🚀 **Real-time Processing**: Live status updates and instant responses
- � **Modern UI**: Clean, responsive interface with dark theme
- ☁️ **Cloud Deployment**: Hosted on Google Cloud Run for scalability

## 💡 Use Cases

### Document Analysis
- **Contract Review**: Extract key terms, dates, and obligations
- **Research Papers**: Summarize findings and extract methodologies
- **Technical Documentation**: Quick navigation and understanding of complex docs
- **Legal Documents**: Extract clauses and analyze legal language

### Web Research
- **Content Aggregation**: Analyze multiple web sources simultaneously
- **Market Research**: Extract insights from various web pages
- **Competitive Analysis**: Process and compare information from different sources
- **Knowledge Base Creation**: Build searchable knowledge bases from web content

## 🚀 Getting Started

### Prerequisites
- Python 3.11 or higher
- Mistral AI API key ([Get one here](https://mistral.ai))

### Local Development Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/wsmaisys/DocuDroid.git
   cd DocuDroid
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   Create a `.env` file:
   ```env
   MISTRAL_API_KEY=your_api_key_here
   TEXT_EMBEDDING=https://api.mistral.ai/v1/embeddings
   TEXT_EMBEDDING_MODEL=mistral-embed
   ```

4. **Run the Application**
   ```bash
   uvicorn api:app --host 0.0.0.0 --port 8000
   ```

### 🐳 Docker Deployment

```bash
docker build -t docudroid .
docker run -p 8000:8000 --env-file .env docudroid
```

## 🏗️ Architecture

### Component Overview
```
DocuDroid/
├── api.py              # FastAPI application and endpoints
├── chat_manager.py     # Core chat and document processing
├── pdfloader.py        # PDF processing with vector store
├── webloader.py        # Web content extraction and analysis
├── static/            # Frontend assets and UI
└── .env              # Configuration
```

### Technology Stack
- **Backend**:
  - FastAPI: High-performance web framework
  - LangChain: LLM application framework
  - Mistral AI: State-of-the-art language model
  - InMemoryVectorStore: Efficient document retrieval

- **Frontend**:
  - Modern HTML5 & CSS3
  - Vanilla JavaScript for lightweight performance
  - Responsive design principles

- **Deployment**:
  - Google Cloud Run
  - Cloud Build for CI/CD
  - Docker containerization

## 🔧 API Endpoints

### PDF Processing
- `POST /upload_pdf`
  - Upload and process PDF documents
  - Returns processing status and document ID

### Web Content
- `POST /process_urls`
  - Process multiple web URLs
  - Returns extracted content summary

### Chat Interface
- `POST /chat`
  - Process chat messages with context
  - Returns AI-generated responses

## 🌟 Advantages

1. **Efficient Document Processing**
   - Fast semantic search using vector embeddings
   - Intelligent chunking for better context preservation
   - Multi-document context management

2. **Flexible Architecture**
   - Modular design for easy extensions
   - Scalable cloud deployment
   - Stateless architecture for reliability

3. **Enhanced User Experience**
   - Real-time processing feedback
   - Intuitive interface
   - Context-aware responses

4. **Security & Privacy**
   - Environment-based configuration
   - No permanent storage of documents
   - Secure cloud deployment

## 🛠️ Configuration

### Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| MISTRAL_API_KEY | Mistral AI API key | Yes |
| TEXT_EMBEDDING | Embedding API endpoint | Yes |
| TEXT_EMBEDDING_MODEL | Model for embeddings | Yes |
| PORT | Server port (default: 8000) | No |

## 📈 Performance Optimization

- Uses InMemoryVectorStore for fast document retrieval
- Efficient document chunking for better context
- Optimized web content extraction
- Containerized deployment for consistent performance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Mistral AI](https://mistral.ai) - LLM provider
- [LangChain](https://www.langchain.com) - LLM framework
- [FastAPI](https://fastapi.tiangolo.com) - Web framework
- [Google Cloud](https://cloud.google.com) - Cloud platform

## 📞 Support

- Report issues on [GitHub Issues](https://github.com/wsmaisys/DocuDroid/issues)
- For major changes, please open an issue first to discuss what you would like to change

---

Built with ❤️ by [wsmaisys](https://github.com/wsmaisys)