from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_milvus import Milvus
from .config import EMBEDDING_MODEL, MILVUS_HOST, MILVUS_PORT, COLLECTION_NAME


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def create_vectorstore(documents):
    """Create a new vectorstore from documents (drops old data)."""
    embeddings = get_embeddings()
    vectorstore = Milvus.from_documents(
        documents=documents,
        embedding=embeddings,
        connection_args={"host": MILVUS_HOST, "port": MILVUS_PORT},
        collection_name=COLLECTION_NAME,
        drop_old=True,
    )
    print(f"Stored {len(documents)} documents in collection '{COLLECTION_NAME}'")
    return vectorstore


def get_vectorstore():
    """Connect to existing vectorstore."""
    embeddings = get_embeddings()
    return Milvus(
        embedding_function=embeddings,
        connection_args={"host": MILVUS_HOST, "port": MILVUS_PORT},
        collection_name=COLLECTION_NAME,
    )
