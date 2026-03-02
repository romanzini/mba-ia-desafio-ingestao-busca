import functools
import logging
import os
import time


def setup_logging() -> None:
    """Configure structured console logging for the project."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def timed(func):
    """Decorator that logs execution time of a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        logger.info("Iniciando %s...", func.__name__)
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.info("%s concluído em %.2fs", func.__name__, elapsed)
        return result
    return wrapper


def configure_langsmith() -> None:
    """
    Enables LangSmith tracing when LANGCHAIN_API_KEY is present.
    LangChain reads LANGCHAIN_TRACING_V2 and LANGCHAIN_API_KEY automatically,
    so this function just validates the configuration and logs the status.
    """
    logger = logging.getLogger(__name__)

    api_key = os.getenv("LANGCHAIN_API_KEY")
    tracing = os.getenv("LANGCHAIN_TRACING_V2", "false").lower()
    project = os.getenv("LANGCHAIN_PROJECT", "default")

    if tracing == "true" and api_key:
        logger.info("LangSmith tracing ATIVADO — projeto: %s", project)
    else:
        logger.info(
            "LangSmith tracing DESATIVADO "
            "(defina LANGCHAIN_TRACING_V2=true e LANGCHAIN_API_KEY para ativar)"
        )
