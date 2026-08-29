# Contribuindo com o CurriculoMatch AI

Obrigado por contribuir! Este guia explica como configurar o ambiente, rodar testes e enviar alteracoes.

---

## Pre-requisitos

- Python 3.12+
- PostgreSQL 15+ (opcional, para checkpointer)
- Docker + Docker Compose (opcional, para n8n)
- Git

## Setup do Ambiente

```bash
# 1. Clonar o repositorio
git clone https://github.com/gbetsa/CurriculoMatch-AI.git
cd CurriculoMatch-AI

# 2. Criar ambiente virtual
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variaveis de ambiente
cp .env.example .env
# Editar .env com suas chaves (GROQ_API_KEY, DATABASE_URL)

# 5. Rodar testes
pytest tests/ -v
```

## Estrutura do Projeto

```
CurriculoMatch-AI/
├── api/                    # API REST (FastAPI)
│   ├── main.py            # Endpoints principais
│   ├── schemas.py         # Modelos Pydantic da API
│   └── dependencies.py    # Rate limiter, validacao, grafo
├── graph/                  # Agente LangGraph
│   ├── workflow.py         # Definicao do grafo
│   ├── nodes.py            # Nos de execucao
│   ├── state.py            # AgentState (TypedDict)
│   ├── security.py         # Anti-injection regex
│   ├── observability.py    # structlog + helpers
│   ├── resilience.py       # tenacity (retry + fallback)
│   ├── checkpointer.py     # PostgreSQL PostgresSaver
│   └── history_query.py    # Query de analises similares
├── prompts/                # System prompts
│   ├── extract_prompt.py   # Prompt de extracao
│   └── analyze_prompt.py   # Prompt de analise
├── tools/                  # Ferramentas de I/O
│   ├── pdf_reader.py       # Leitura de PDF (PyMuPDF)
│   ├── job_reader.py       # Leitura de TXT
│   └── report_writer.py    # Escrita de relatorios
├── tests/                  # Suite de testes
├── lowcode/                # n8n workflows
├── docs/                   # Documentacao
├── streamlit_app.py        # Interface web
├── main.py                 # CLI entrypoint
└── run.py                  # Launcher (API + Streamlit)
```

## Commits

Utilizamos [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

# Exemplos:
feat(auth): adicionar login com OAuth
fix(api): corrigir rate limit em /analyze
docs(readme): atualizar secao de instalacao
test(security): adicionar cenario adversarial
refactor(nodes): simplificar extract_information
```

**Types:** feat, fix, docs, test, refactor, style, chore, ci

## Branches

- `develop` — branch principal de desenvolvimento
- `feature/*` — novas funcionalidades
- `fix/*` — correcoes de bugs
- `docs/*` — documentacao

### Fluxo

1. Criar branch a partir de `develop`:
   ```bash
   git checkout develop
   git checkout -b feature/minha-feature
   ```
2. Implementar e commits
3. Push e abrir PR para `develop`
4. Aguardar CI passar
5. Merge apos aprovacao

## Testes

```bash
# Todos os testes (exceto checkpointer)
pytest tests/ -v --ignore=tests/test_checkpointer.py

# Apenas unitarios
pytest tests/test_security.py tests/test_nodes.py tests/test_tools.py -v

# Apenas integracao
pytest tests/test_integration.py -v

# Apenas E2E
pytest tests/test_e2e.py -v

# Com cobertura
pytest tests/ --cov=graph --cov=api --cov-report=term-missing
```

## Formatacao

```bash
# Lint
ruff check . --fix

# Formatacao
black .
```

O CI roda Ruff + Black automaticamente. PRs que nao passarem no lint serao bloqueados.

## Docker

```bash
# Build da imagem
docker build -t curriculomatch-ai .

# Executar API
docker run -p 8000:8000 --env-file .env curriculomatch-ai

# Full stack (API + Streamlit + PostgreSQL + n8n)
docker-compose up -d
```

## Pull Requests

1. Titulo claro seguindo Conventional Commits
2. Descricao com o que foi feito e por que
3. Testes passando no CI
4.Lint e Black sem erros
5. Documentacao atualizada (se aplicavel)

## Issues

Ao abrir uma issue, inclua:
- Descricao clara do problema ou sugestao
- Passos para reproduzir (se bug)
- Comportamento esperado vs atual
- Screenshots (se aplicavel)

## Licença

Este projeto e para fins academicos (Projeto Avaliativo Modulo 2).
