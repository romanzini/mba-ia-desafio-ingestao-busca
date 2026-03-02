import logging
import os
import time

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_postgres import PGVector
from langsmith import traceable

from observability import setup_logging

load_dotenv()
setup_logging()

logger = logging.getLogger(__name__)

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""


def search_prompt(question=None):
    pgvector_url = os.getenv("PGVECTOR_URL")
    pgvector_collection = os.getenv("PGVECTOR_COLLECTION")
    openai_embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

    if not pgvector_url or not pgvector_collection:
        logger.error("PGVECTOR_URL ou PGVECTOR_COLLECTION não configurados.")
        return None

    embeddings = OpenAIEmbeddings(model=openai_embedding_model)
    vectorstore = PGVector(
        connection=pgvector_url,
        collection_name=pgvector_collection,
        embeddings=embeddings,
    )
    llm = ChatOpenAI(model="gpt-5-nano")
    logger.info("Vectorstore e LLM inicializados. Coleção: '%s'", pgvector_collection)

    @traceable(name="rag_chain")
    def chain(pergunta: str) -> str:
        logger.info("Pergunta recebida: %s", pergunta)

        t0 = time.perf_counter()
        results = vectorstore.similarity_search_with_score(pergunta, k=10)
        search_elapsed = time.perf_counter() - t0
        logger.info(
            "Busca vetorial: %d resultado(s) em %.2fs — scores: %s",
            len(results),
            search_elapsed,
            [round(score, 4) for _, score in results],
        )

        contexto = "\n\n".join(doc.page_content for doc, _ in results)
        prompt = PROMPT_TEMPLATE.format(contexto=contexto, pergunta=pergunta)

        t1 = time.perf_counter()
        response = llm.invoke(prompt)
        llm_elapsed = time.perf_counter() - t1
        logger.info(
            "LLM respondeu em %.2fs — tokens de uso: %s",
            llm_elapsed,
            getattr(response, "usage_metadata", "n/a"),
        )

        return response.content

    return chain