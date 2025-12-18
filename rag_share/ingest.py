"""Run this script to load/reload DOCX data into Milvus."""

from rag.loader import load_multiple_docx, find_docx_files
from rag.vectorstore import create_vectorstore


def ingest():
    docx_files = find_docx_files("data")

    if not docx_files:
        print("No .docx files found in data/ directory")
        return

    print(f"Found files: {docx_files}")
    docs = load_multiple_docx(docx_files)

    print(f"\n--- Sample chunk ---")
    print(docs[0].page_content)
    print(f"Metadata: {docs[0].metadata}")

    create_vectorstore(docs)
    print("\nIngestion complete!")


if __name__ == "__main__":
    ingest()
