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
│   └── chat.py              # CLI interativo
└── README.md
```

---

## Tecnologias utilizadas

- **LangChain** — orquestração de LLM e pipeline de documentos
- **OpenAI** — embeddings (`text-embedding-3-small`) e LLM (`gpt-5-nano`)
- **PostgreSQL + pgVector** — armazenamento e busca vetorial
- **Docker Compose** — banco de dados isolado em container