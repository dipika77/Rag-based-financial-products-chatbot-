import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MILVUS_HOST = "localhost"
MILVUS_PORT = "19530"
COLLECTION_NAME = "bfc_deposits"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
LLM_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
TOP_K = 5
