# Rag-based-financial-products-chatbot-



A conversational chatbot that answers natural language questions about bank deposit products using Retrieval-Augmented Generation (RAG).

## Tech Stack

- **LLM** — LLaMA 4 via [Groq API](https://console.groq.com)
- **Vector DB** — Milvus (self-hosted via Docker)
- **Embeddings** — `paraphrase-multilingual-MiniLM-L12-v2`
- **Framework** — LangChain

## Setup

**1. Clone the repo and install dependencies**
```bash
git clone <your-repo-url>
cd rag_best
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

**2. Set up environment variables**
```bash
cp .env.example .env
# Add your GROQ_API_KEY to .env
```

**3. Start Milvus**
```bash
docker compose up -d
```

**4. Ingest documents**
```bash
python ingest.py
```

**5. Run the chatbot**
```bash
python main.py
```

## Project Structure

```
├── data/                  # Source documents (.docx)
├── rag/
│   ├── loader.py          # Section-aware DOCX parser
│   ├── vectorstore.py     # Milvus vector store setup
│   ├── chain.py           # RAG chain with chat history
│   └── config.py          # Config and environment vars
├── ingest.py              # One-time document ingestion
├── main.py                # Chat interface
└── docker-compose.yml     # Milvus + MinIO + Attu
```
