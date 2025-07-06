from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

# Load env
load_dotenv()
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# Step 1: Load PDFs
files = ["knowledge_base/Bharatiya_Nyaya_Sanhita,_2023.pdf"]
pages = []
for f in files:
    print(f"Loading file: {f}")
    loader = PyPDFLoader(f)
    pages.extend(loader.load())

# Step 2: Split text
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(pages)

# Step 3: Embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Step 4: Push to Qdrant cloud
vector_store = Qdrant.from_documents(
    docs,
    embeddings,
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    collection_name="law-knowledge"
)

print(f"✅ Uploaded {len(docs)} chunks to Qdrant cloud!")
