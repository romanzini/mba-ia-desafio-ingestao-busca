# Git Workflow — Como Enviar Alterações

Guia passo a passo para enviar código alterado para o Git em uma nova branch e criar um Pull Request.

## 1. Verificar as mudanças atuais

```bash
git status
git diff
```

Isso mostra:
- Arquivos modificados
- Arquivos não rastreados
- Diferenças entre working directory e staging area

## 2. Criar e trocar para uma nova branch

```bash
git checkout -b feat/add-observability
```

Sugestões de nomes de branch por tipo de mudança:

| Padrão | Exemplo | Uso |
|--------|---------|-----|
| `feat/` | `feat/add-observability` | Novas funcionalidades |
| `improve/` | `improve/langsmith-tracing` | Melhorias |
| `fix/` | `fix/pdf-path-issue` | Correções de bugs |
| `docs/` | `docs/update-readme` | Documentação |
| `refactor/` | `refactor/code-cleanup` | Reorganização de código |

## 3. Staged as mudanças

```bash
git add .
```

Ou para adicionar arquivos específicos:

```bash
git add src/observability.py src/ingest.py src/search.py src/chat.py .env .env.example README.md
```

## 4. Criar um commit com mensagem descritiva

```bash
git commit -m "feat: add observability with logging and LangSmith tracing

- Add observability.py with structured logging and LangSmith configuration
- Enhance ingest.py with detailed logs and execution timing
- Enhance search.py with tracing, similarity scores, and token metrics
- Enhance chat.py with logging initialization
- Update .env variables for LangSmith support
- Add observability section to README"
```

**Recomendações:**
- Primeira linha: tipo de mudança + título (até 50 caracteres)
- Linhas seguintes: detalhes (até 72 caracteres cada)
- Use bullets (`-`) para listar mudanças

## 5. Fazer push da branch para o repositório remoto

```bash
git push -u origin feat/add-observability
```

Flags:
- `-u` — define a branch upstream (necessário primeira vez)
- `origin` — nome do repositório remoto (padrão)

## 6. Criar o Pull Request no GitHub

### Opção A: Via interface web

1. Acesse seu repositório no GitHub
2. Uma mensagem aparecerá sugerindo: **"Compare & pull request"**
3. Clique nela

### Opção B: Via GitHub CLI

Se tiver `gh` instalado:

```bash
gh pr create --title "Add observability with logging and LangSmith" \
  --body "Adds structured logging, timing metrics, and LangSmith tracing integration"
```

## 7. Preencher a PR

### Título
```
Add observability with logging and LangSmith tracing
```

### Descrição

```markdown
## Melhorias implementadas

- Logging estruturado em todos os scripts (`ingest.py`, `search.py`, `chat.py`)
- Métricas de tempo de execução com decorator `@timed`
- Integração com LangSmith para rastreamento distribuído (@traceable)
- Documentação de observabilidade no README
- Variáveis de ambiente para configuração do LangSmith

## Arquivos alterados

- `src/observability.py` — novo módulo de observabilidade
- `src/ingest.py` — logs e timing de ingestão
- `src/search.py` — tracing do RAG chain, scores e tokens
- `src/chat.py` — inicialização de logging
- `.env` e `.env.example` — variáveis LangSmith
- `README.md` — seção Observabilidade

## Como testar

1. Preencher `LANGCHAIN_API_KEY` no `.env`:
   ```env
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_API_KEY=ls__... (sua chave do LangSmith)
   ```

2. Executar conforme instruções no README:
   ```bash
   docker compose up -d
   python src/ingest.py
   python src/chat.py
   ```

3. Verificar:
   - Logs estruturados no console com timestamps
   - Tempos de execução após cada operação
   - Traces no dashboard do LangSmith (https://smith.langchain.com)

## Checklist

- [ ] Código testado localmente
- [ ] Logs aparecem corretamente no terminal
- [ ] Nenhuma chave de API sensível foi commitada
- [ ] README foi atualizado com novas instruções
- [ ] Commits têm mensagens claras e descritivas
```

## Fluxo completo em um exemplo

```bash
# 1. Criar e trocar para nova branch
git checkout -b feat/add-observability

# 2. Ver o que mudou
git status

# 3. Adicionar tudo
git add .

# 4. Commits com mensagens descritivas
git commit -m "feat: create observability module

- Add setup_logging() for structured logging
- Add @timed decorator for execution metrics
- Add configure_langsmith() for tracing setup"

git commit -m "feat: enhance ingest.py with observability

- Add logging at each ingestão stage
- Add @timed decorator to measure total time"

# 5. Push para remoto
git push -u origin feat/add-observability

# 6. No GitHub: criar PR
# Ou via CLI:
gh pr create --title "Add observability with logging and LangSmith" \
  --body "See PR description"
```

## Comandos úteis

| Comando | Descrição |
|---------|-----------|
| `git branch` | Listar branches locais |
| `git branch -a` | Listar todas as branches (local + remoto) |
| `git log --oneline` | Ver histórico de commits resumido |
| `git diff main` | Ver diferenças entre branch atual e main |
| `git reset HEAD~1` | Desfazer último commit (mantendo mudanças) |
| `git stash` | Guardar mudanças temporariamente |
| `git pull origin main` | Atualizar branch local com main remoto |

## Boas práticas

✅ **Faça:**
- Commits pequenos e focados em uma mudança
- Mensagens de commit claras e em inglês ou português consistente
- Push frequente para evitar conflitos
- Criar PR mesmo para features incompletas (use `[WIP]` no título)
- Revisar o `git diff` antes de fazer commit

❌ **Evite:**
- Commits enormes com múltiplas mudanças
- Mensagens genéricas ("fix", "update", "change")
- Committear arquivos sensíveis (chaves, senhas)
- Fazer force push (`git push -f`) em branches compartilhadas
- Commitar código que não funciona

## Referências

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Conventional Commits](https://www.conventionalcommits.org/)
