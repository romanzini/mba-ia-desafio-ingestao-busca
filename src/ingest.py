import logging
import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

from observability import configure_langsmith, setup_logging, timed

load_dotenv()
setup_logging()
configure_langsmith()

logger = logging.getLogger(__name__)

for k in ("OPENAI_API_KEY", "PGVECTOR_URL", "PGVECTOR_COLLECTION", "PDF_PATH"):
    if not os.getenv(k):
        raise RuntimeError(f"Environment variable {k} is not set")

PDF_PATH = os.getenv("PDF_PATH")
PGVECTOR_URL = os.getenv("PGVECTOR_URL")
PGVECTOR_COLLECTION = os.getenv("PGVECTOR_COLLECTION")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


@timed
def ingest_pdf():
    logger.info("Carregando PDF: %s", PDF_PATH)
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    logger.info("PDF carregado: %d página(s)", len(documents))

    splits = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        add_start_index=False,
    ).split_documents(documents)
    logger.info("Documento dividido em %d chunks", len(splits))

    if not splits:
        raise SystemExit(0)

    logger.info("Gerando embeddings com modelo '%s'...", OPENAI_EMBEDDING_MODEL)
    embeddings = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)

    vectorstore = PGVector(
        connection=PGVECTOR_URL,
        collection_name=PGVECTOR_COLLECTION,
        embeddings=embeddings,
    )

    logger.info("Armazenando vetores na coleção '%s'...", PGVECTOR_COLLECTION)
    vectorstore.add_documents(splits)
    logger.info("Ingestão concluída: %d chunks armazenados no pgVector.", len(splits))


if __name__ == "__main__":
    ingest_pdf()