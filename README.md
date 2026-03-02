# Desafio MBA Engenharia de Software com IA - Full Cycle

Sistema de ingestão e busca semântica de PDFs usando LangChain, OpenAI e PostgreSQL com pgVector.

---

## Pré-requisitos

- Python 3.12+
- Docker e Docker Compose
- Chave de API da OpenAI

---

## Configuração

1. Clone o repositório e entre na pasta do projeto:

   ```bash
   git clone <url-do-repositorio>
   cd mba-ia-desafio-ingestao-busca
   ```

2. Copie o arquivo de variáveis de ambiente e preencha os valores:

   ```bash
   cp .env.example .env
   ```

   Edite o `.env` com suas credenciais:

   ```env
   OPENAI_API_KEY=sk-...
   OPENAI_EMBEDDING_MODEL=text-embedding-3-small
   PGVECTOR_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
   PGVECTOR_COLLECTION=minha_colecao
   PDF_PATH=./document.pdf
   ```

3. Adicione o arquivo `document.pdf` na raiz do projeto.

4. Crie e ative o ambiente virtual, depois instale as dependências:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

---

## Execução

### 1. Subir o banco de dados

```bash
docker compose up -d
```

Isso inicia o PostgreSQL com a extensão pgVector já habilitada.

### 2. Ingerir o PDF

```bash
python src/ingest.py
```

Lê o `document.pdf`, divide em chunks de 1000 caracteres (overlap 150), gera embeddings com OpenAI e armazena os vetores no pgVector.

### 3. Iniciar o chat

```bash
python src/chat.py
```

Abre um chat interativo no terminal. Digite sua pergunta e receba respostas baseadas exclusivamente no conteúdo do PDF.

```
Faça sua pergunta (Ctrl+C para sair):

PERGUNTA: Qual o faturamento da empresa?
RESPOSTA: O faturamento foi de 10 milhões de reais.

PERGUNTA: Qual a capital da França?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.
```

---

## Estrutura do projeto

```
├── docker-compose.yml       # PostgreSQL + pgVector
├── requirements.txt         # Dependências Python
├── .env.example             # Template de variáveis de ambiente
├── document.pdf             # PDF para ingestão
├── src/
│   ├── ingest.py            # Ingestão do PDF no banco vetorial
│   ├── search.py            # Busca semântica e chamada ao LLM
│   ├── chat.py              # CLI interativo
│   └── observability.py     # Logging estruturado, timing e LangSmith
└── README.md
```

---

## Observabilidade

O projeto conta com três camadas de observabilidade:

### Logging estruturado

Todos os scripts emitem logs com timestamp, nível e contexto:

```
2026-03-02 10:00:00 [INFO] __main__: Carregando PDF: ./document.pdf
2026-03-02 10:00:01 [INFO] __main__: PDF carregado: 12 página(s)
2026-03-02 10:00:01 [INFO] __main__: Documento dividido em 48 chunks
2026-03-02 10:00:04 [INFO] __main__: ingest_pdf concluído em 3.42s
```

### Métricas de tempo

O decorador `@timed` em `ingest_pdf` e os timers internos em `chain` registram:
- Tempo total de ingestão
- Tempo de busca vetorial (similarity search)
- Tempo de resposta da LLM
- Scores de similaridade dos documentos recuperados

### LangSmith (tracing distribuído)

Para habilitar o rastreamento completo das chamadas LangChain no dashboard do [LangSmith](https://smith.langchain.com):

1. Crie uma conta e gere uma API Key em https://smith.langchain.com
2. Preencha as variáveis no `.env`:

   ```env
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_API_KEY=ls__...
   LANGCHAIN_PROJECT=mba-ia-desafio-ingestao-busca
   ```

3. Execute normalmente — todas as chamadas ao LLM e à busca vetorial serão enviadas automaticamente ao LangSmith.

> Com `LANGCHAIN_TRACING_V2=false` ou sem a `LANGCHAIN_API_KEY`, o sistema funciona normalmente sem enviar dados ao LangSmith.

---

## Tecnologias utilizadas

- **LangChain** — orquestração de LLM e pipeline de documentos
- **OpenAI** — embeddings (`text-embedding-3-small`) e LLM (`gpt-5-nano`)
- **PostgreSQL + pgVector** — armazenamento e busca vetorial
- **Docker Compose** — banco de dados isolado em container
- **LangSmith** — tracing e observabilidade das chamadas LangChain