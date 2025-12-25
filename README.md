# BNSGPT - Legal AI Assistant 🏛️⚖️

A Retrieval-Augmented Generation (RAG) chatbot system specialized in Indian legal matters, particularly focusing on the **Bharatiya Nyaya Sanhita 2023** (BNS). This AI-powered legal assistant uses advanced NLP to provide insights and answers based on legal documents.

## 🌟 Features

- **RAG-powered**: Retrieves relevant legal information from a vector database before generating responses
- **FastAPI Backend**: High-performance REST API with streaming support
- **Qdrant Vector Store**: Cloud-based vector database for efficient semantic search
- **Ollama Integration**: Uses DeepSeek-R1 model for intelligent legal reasoning
- **PDF Document Processing**: Automatically ingests and processes legal documents

## 🏗️ Architecture

```
[Client/Frontend]
      |
      v
[FastAPI Backend] (/query endpoint)
      |
      v
[LangChain RAG Chain]
      |
      +---> [Qdrant Vector DB] (retrieves relevant context)
      |
      +---> [Ollama LLM: DeepSeek-R1] (generates response)
```

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** (Python 3.10 or higher recommended)
- **Ollama** - Download and install from [ollama.ai](https://ollama.ai/)
- **Git** (for cloning the repository)
- **Qdrant Account** - Sign up for a free account at [Qdrant Cloud](https://cloud.qdrant.io/)

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/crysosancher/BNSGPT.git
cd BNSGPT
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# On Linux/Mac
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages including:
- FastAPI & Uvicorn (API server)
- LangChain & LangChain Community (RAG framework)
- Qdrant Client (vector database)
- Sentence Transformers (embeddings)
- PyPDF (PDF processing)
- And more...

### Step 4: Install Ollama Model

Make sure Ollama is running, then pull the DeepSeek-R1 model:

```bash
ollama pull deepseek-r1:latest
```

**Note**: This model is large (~40GB). Ensure you have sufficient disk space and a stable internet connection.

## ⚙️ Configuration

### Step 1: Set Up Environment Variables

Copy the sample environment file:

```bash
cp .env.sample .env
```

### Step 2: Edit the `.env` File

Open `.env` in your favorite text editor and configure the following:

```env
# Qdrant Cloud Configuration
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_URL=https://your-cluster.qdrant.io

# Ollama Model (default is deepseek-r1:latest)
OLLAMA_MODEL=deepseek-r1:latest

# Optional: Database API (if needed)
db_api=
```

**How to get Qdrant credentials:**
1. Sign up at [Qdrant Cloud](https://cloud.qdrant.io/)
2. Create a new cluster (free tier available)
3. Copy your **API Key** and **Cluster URL**
4. Paste them into your `.env` file

## 📚 Adding Legal Documents

### Step 1: Add PDF Files

Place your legal PDF documents in the `knowledge_base/` directory:

```bash
# The repository already includes:
knowledge_base/Bharatiya_Nyaya_Sanhita,_2023.pdf

# You can add more PDFs:
cp /path/to/your/legal-document.pdf knowledge_base/
```

### Step 2: Update ingest.py (if needed)

If you add new PDF files, edit `ingest.py` to include them:

```python
# In ingest.py, update the files list:
files = [
    "knowledge_base/Bharatiya_Nyaya_Sanhita,_2023.pdf",
    "knowledge_base/your_new_document.pdf"  # Add your new file here
]
```

### Step 3: Run the Ingestion Script

This script will:
- Load your PDF documents
- Split them into manageable chunks
- Generate embeddings using HuggingFace's sentence transformers
- Upload everything to your Qdrant cloud database

```bash
python ingest.py
```

**Expected output:**
```
Loading file: knowledge_base/Bharatiya_Nyaya_Sanhita,_2023.pdf
✅ Uploaded XXX chunks to Qdrant cloud!
```

**Note**: The first run will download the embedding model (~80MB). Subsequent runs will be faster.

## 🎯 Running the Application

### Start the FastAPI Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Options:**
- `--reload`: Auto-reload on code changes (useful for development)
- `--host 0.0.0.0`: Make server accessible from other machines
- `--port 8000`: Port number (change if 8000 is in use)

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

The API will be available at: **http://localhost:8000**

## 💬 Using the API

### API Endpoint: `/query`

**Method:** POST

**Request Format:**
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Section 498A of BNS 2023?"}'
```

**Python Example:**
```python
import requests

url = "http://localhost:8000/query"
payload = {"question": "What are the punishments for theft under BNS 2023?"}

response = requests.post(url, json=payload, stream=True)

# Stream the response
for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
    if chunk:
        print(chunk, end='', flush=True)
```

**JavaScript/Node.js Example:**
```javascript
const response = await fetch('http://localhost:8000/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ question: 'What is theft according to BNS?' })
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  console.log(decoder.decode(value));
}
```

### Interactive Testing

Visit the FastAPI interactive docs at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📁 Project Structure

```
BNSGPT/
├── main.py                 # FastAPI application (REST API with /query endpoint)
├── ingest.py              # Document ingestion script (PDFs → Qdrant)
├── rag_chain.py           # LangChain RAG chain configuration
├── requirements.txt       # Python dependencies
├── .env.sample            # Environment variables template
├── .env                   # Your actual environment variables (not in git)
├── .gitignore             # Git ignore rules
├── knowledge_base/        # Store your PDF documents here
│   └── Bharatiya_Nyaya_Sanhita,_2023.pdf
└── prompts/
    └── prompt.py          # System prompts for the LLM
```

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError"

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "Connection to Qdrant failed"

**Solutions:**
1. Verify your `.env` file has correct `QDRANT_URL` and `QDRANT_API_KEY`
2. Check your internet connection
3. Ensure your Qdrant cluster is running (check Qdrant Cloud dashboard)
4. Verify the collection name is "law-knowledge" (or update `rag_chain.py` accordingly)

### Issue: "Ollama model not found"

**Solution:**
```bash
# Check if Ollama is running
ollama list

# Pull the model again
ollama pull deepseek-r1:latest

# If you want to use a different model, update .env:
OLLAMA_MODEL=llama2
```

### Issue: "Ingestion is very slow"

**Causes & Solutions:**
- **Large PDF files**: This is normal. The first run downloads the embedding model (~80MB)
- **Slow internet**: Uploading to Qdrant cloud requires good internet connection
- **Limited RAM**: Close other applications, embeddings require memory

### Issue: "Port 8000 already in use"

**Solution:**
```bash
# Use a different port
uvicorn main:app --reload --port 8080

# Then access at http://localhost:8080
```

### Issue: Response is too slow

**Possible causes:**
1. **Large model**: DeepSeek-R1 is a large model, inference may be slow on CPU
2. **No GPU**: Consider using a smaller model if you don't have a GPU
3. **Qdrant latency**: Cloud vector search may have some latency

**Solutions:**
- Use a smaller, faster model like `llama2` or `mistral`
- Reduce the number of retrieved documents in `rag_chain.py`
- Consider running Qdrant locally instead of cloud

## 🛠️ Advanced Configuration

### Changing the Embedding Model

Edit `ingest.py` and `rag_chain.py`:

```python
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"  # Alternative model
)
```

### Adjusting Chunk Size

In `ingest.py`, modify the text splitter:

```python
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,    # Increase for more context per chunk
    chunk_overlap=50   # Increase to maintain continuity
)
```

### Changing the Number of Retrieved Documents

In `rag_chain.py`, modify the similarity search:

```python
docs = vector_store.similarity_search(question, k=4)  # Change k value
```

## 📝 License

[Add your license information here]

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Disclaimer**: This is an AI-powered legal assistant for informational purposes only. It should not be considered as legal advice. Always consult with a qualified legal professional for legal matters.
