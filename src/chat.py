from search import search_prompt


def main():
    chain = search_prompt()

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return

    print("Faça sua pergunta (Ctrl+C para sair):\n")

    while True:
        try:
            question = input("PERGUNTA: ").strip()
            if not question:
                continue
            answer = chain(question)
            print(f"RESPOSTA: {answer}\n")
        except (KeyboardInterrupt, EOFError):
            print("\nEncerrando chat.")
            break


if __name__ == "__main__":
    main()