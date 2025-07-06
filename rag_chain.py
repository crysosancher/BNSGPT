from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os

load_dotenv()
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

vector_store = QdrantVectorStore(
    client=client,
    collection_name="law-knowledge",
    embedding=embeddings
)

llm = OllamaLLM(model="deepseek-r1")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a senior law consultant. Answer precisely, formally, and cite sections."),
    ("human", "{question}")
])

chain = prompt | llm

def ask_question_stream(question: str):
    docs = vector_store.similarity_search(question)
    context = "\n\n".join([doc.page_content for doc in docs])
    final_question = f"{context}\n\nQuestion: {question}"

    for chunk in chain.stream({"question": final_question}):
        yield chunk  # just yield the chunk directly
