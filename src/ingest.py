import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

for k in ("OPENAI_API_KEY", "PGVECTOR_URL", "PGVECTOR_COLLECTION", "PDF_PATH"):
    if not os.getenv(k):
        raise RuntimeError(f"Environment variable {k} is not set")

PDF_PATH = os.getenv("PDF_PATH")
PGVECTOR_URL = os.getenv("PGVECTOR_URL")
PGVECTOR_COLLECTION = os.getenv("PGVECTOR_COLLECTION")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def ingest_pdf():
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    splits = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        add_start_index=False,
    ).split_documents(documents)

    if not splits:
        raise SystemExit(0)

    embeddings = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)

    vectorstore = PGVector(
        connection=PGVECTOR_URL,
        collection_name=PGVECTOR_COLLECTION,
        embeddings=embeddings,
    )

    vectorstore.add_documents(splits)
    print(f"Ingestão concluída: {len(splits)} chunks armazenados no pgVector.")


if __name__ == "__main__":
    ingest_pdf()