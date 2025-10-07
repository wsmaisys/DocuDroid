# 🤖 DocuDroid - AI-Powered Document Assistant

## 🎯 Overview
DocuDroid is an intelligent document processing and chat interface that combines the power of Mistral AI with a user-friendly web interface. Perfect for analyzing documents, answering questions, and extracting insights from your content.

## 🚀 Features
- 📄 PDF document processing and analysis
- 🌐 Web content extraction and processing
- 💬 Interactive chat interface
- 🧠 Powered by Mistral AI
- 🔒 Secure document handling
- ⚡ Fast and efficient processing

## 🛠️ Requirements
- Mistral API key
- Docker installed on your system
- Port 8080 available on your host

## 🏃‍♂️ Quick Start
```bash
# Pull the image
docker pull wasimansariiitm/docudroid:latest

# Run the container
docker run -d \
  -p 8080:8080 \
  -e MISTRAL_API_KEY=your_mistral_api_key \
  wasimansariiitm/docudroid:latest
```

## 🌐 Access the Application
Once running, access the application at:
```
http://localhost:8080
```

## 💡 Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| MISTRAL_API_KEY | Your Mistral AI API key | Yes |
| PORT | Server port (default: 8080) | No |

## 🏷️ Tags
- `latest`: Most recent version
- `1.0.0`: Stable release

## 🐳 Image Details
- Base Image: python:3.11-slim-bullseye
- Image Size: ~430MB
- Exposed Port: 8080

## 🔒 Security
- Runs as non-root user
- Minimal base image
- Regular security updates

## 💪 Health Check
The container includes built-in health checks that monitor the application's status.

## 📝 Usage Example
```bash
# Run with custom port
docker run -d \
  -p 3000:8080 \
  -e MISTRAL_API_KEY=your_mistral_api_key \
  wasimansariiitm/docudroid:latest

# Check logs
docker logs container_id

# Stop container
docker stop container_id
```

## 🛡️ Built With
- FastAPI
- Uvicorn
- LangChain
- Mistral AI
- Python 3.11

## 📫 Support
For issues and feature requests, please visit our [GitHub repository](https://github.com/wsmaisys/DocuDroid).

## 📜 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🌟 Contributing
Contributions are welcome! Feel free to submit pull requests to help improve DocuDroid.

---
🔄 Last Updated: October 7, 2025