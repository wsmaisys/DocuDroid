# DocuDroid App Information Sheet

## Overview
DocuDroid is an AI-powered application that enables intelligent document analysis and web content exploration through Large Language Model (LLM) technology. Built as a Real-Time Retrieval-Augmented Generation (RAG) system, the app provides three distinct modes for interacting with different content types, showcasing the transformative potential of AI in information retrieval and analysis.

## Core Features & Operational Modes

### 1. General Mode - AI Chat Assistant
**Technology**: Fine-tuned Mistral LLM with prompt engineering optimization

**How to Use**:
- Select "General Chat" from the mode selector
- Type your questions or prompts directly into the chat interface
- Engage in natural conversation on any topic

**Key Capabilities**:
- Handles broad knowledge queries and conceptual discussions
- Context-aware conversations with session memory
- Knowledge base current through June 2025
- Maintains conversation history until app restart, refresh, or closure

**Best Use Cases**: General inquiries, concept explanations, brainstorming, and educational discussions

### 2. PDF Mode - Document Analysis
**Technology**: LangChain PDFLoader with Recursive Text Splitter and vector search

**How to Use**:
1. Select "PDF Mode" from the interface
2. Upload your PDF file using the file selector
3. Wait for document processing completion
4. Ask specific questions about the document content

**Technical Implementation**:
- **Text Chunking**: 1,000 character segments with 200-character overlap
- **Embedding**: Mistral Embed Model for semantic vector representation
- **Storage**: In-memory vector store for fast retrieval
- **Search**: Cosine similarity-based semantic search
- **Retrieval**: Top 2 most relevant chunks (k=2) fed to LLM for response generation

**Limitations**: Works with text-based PDFs only; image-converted PDF files are not supported

**Best Use Cases**: Research paper analysis, legal document review, technical manual queries, academic content exploration

### 3. Web Mode - Webpage Content Analysis
**Technology**: LangChain WebLoader with Recursive Text Splitter and vector search

**How to Use**:
1. Select "Web Mode" from the interface
2. Paste the target webpage URL into the input field
3. Wait for content scraping and processing
4. Query the webpage content through natural language

**Technical Implementation**:
- **Content Extraction**: Automated web scraping with text extraction
- **Text Chunking**: 1,000 character segments with 200-character overlap
- **Embedding**: Mistral Embed Model for semantic vector representation
- **Storage**: In-memory vector store for rapid access
- **Search**: Cosine similarity-based semantic search
- **Retrieval**: Top 2 most relevant chunks (k=2) processed by LLM

**Limitations**: May experience difficulties with JavaScript-heavy websites or dynamic content

**Best Use Cases**: News article analysis, blog post summarization, research content extraction, competitive analysis

## Technical Architecture

### RAG Implementation
DocuDroid operates as a Real-Time RAG system, combining:
- **Retrieval Component**: Semantic search through vector embeddings
- **Augmentation Component**: Context injection from relevant document chunks
- **Generation Component**: LLM response synthesis based on retrieved context

### Memory Management
- Session-based context retention for continuous conversations
- In-memory vector storage for optimal performance
- Automatic cleanup on app restart or closure

### Embedding Strategy
- Utilizes Mistral Embed Model for high-quality semantic representations
- Optimized chunk sizing balances context preservation with search precision
- Overlap strategy ensures important information isn't lost at chunk boundaries

## Effective Usage Tips

**For PDF Analysis**:
- Ask specific questions rather than broad summaries for better results
- Reference page numbers or sections when seeking targeted information
- Follow up with clarifying questions to dive deeper into topics

**For Web Content**:
- Ensure URLs are accessible and not behind paywalls
- Verify the webpage has loaded properly before processing
- Consider the website's structure when formulating queries

**For General Chat**:
- Build on previous questions within the same session for context-aware responses
- Use clear, specific language for more accurate results
- Take advantage of the June 2025 knowledge cutoff for recent information

## System Requirements & Performance
- Requires stable internet connection for LLM processing
- Processing time varies based on document size and complexity
- Real-time response generation with minimal latency for most queries

---
*DocuDroid represents the next generation of document interaction, transforming static content into dynamic, queryable knowledge bases through advanced AI technology.*