import logging

from dotenv import load_dotenv

from observability import configure_langsmith, setup_logging
from search import search_prompt

load_dotenv()
setup_logging()
configure_langsmith()

logger = logging.getLogger(__name__)


def main():
    chain = search_prompt()

    if not chain:
        logger.error("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return

    print("Faça sua pergunta (Ctrl+C para sair):\n")

    while True:
        try:
            question = input("PERGUNTA: ").strip()
            if not question:
                continue
            logger.debug("Processando pergunta: %s", question)
            answer = chain(question)
            print(f"RESPOSTA: {answer}\n")
        except (KeyboardInterrupt, EOFError):
            print("\nEncerrando chat.")
            logger.info("Chat encerrado pelo usuário.")
            break


if __name__ == "__main__":
    main()