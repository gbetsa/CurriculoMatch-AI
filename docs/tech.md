# Tech.md

# Documento Tecnico

## Projeto

**CurriculoMatch AI**

---

# Objetivo

Desenvolver um agente de IA utilizando **Python** e **LangGraph** para realizar a triagem inicial de curriculos, comparando um curriculo em PDF com uma descricao de vaga e gerando um relatorio de compatibilidade.

**Evolucao:** A solucao agora inclui API REST, interface web, memoria persistente, seguranca, observabilidade, testes E2E, DevOps inteligente e automacao low-code.

---

# Stack

## Linguagem

* Python 3.12+

## Frameworks

* LangGraph (orquestracao de agentes)
* LangChain (integracao com LLMs)
* FastAPI (API REST)
* Streamlit (interface web)

## Banco de Dados

* PostgreSQL (checkpointer LangGraph via PostgresSaver)

## Modelo de IA

* Agnostico / Adaptativo (Suporta qualquer LLM compativel com LangChain)
* Configuravel via variavel de ambiente `LLM_MODEL`
* Provedores suportados: Groq (padrao), OpenAI, Ollama (fallback local)

## Bibliotecas Principais

* langgraph + langgraph-checkpoint-postgres
* langchain + langchain-groq
* fastapi + uvicorn + python-multipart
* streamlit
* psycopg[pool] (driver PostgreSQL)
* structlog (logs estruturados)
* tenacity (retry/timeout/fallback)
* langsmith (traces)
* pydantic
* pymupdf (leitura de PDF)
* python-dotenv

## Ferramentas de Qualidade

* pytest + pytest-mock (testes)
* ruff / flake8 (lint)
* mypy (type check)
* black (formatacao)

## Low-Code

* n8n (automacao visual, self-hosted via Docker)

## Observabilidade

* structlog (logs JSON estruturados)
* LangSmith (traces por no)
* Tenacity (tratamento de falhas com retry/timeout/fallback)

---

# Estrutura do Projeto

```text
curriculomatch-ai/
├── api/
│   ├── main.py              # FastAPI endpoints
│   ├── schemas.py           # Pydantic request/response
│   └── dependencies.py      # Rate limit, validacao
├── streamlit_app.py         # Interface web
├── graph/
│   ├── state.py             # AgentState v2 + AnalysisRecord
│   ├── nodes.py             # Nos do grafo (originais + novos)
│   ├── workflow.py          # Grafo com paralelizacao + checkpointer
│   ├── checkpointer.py      # PostgresSaver config
│   ├── observability.py     # Logs estruturados + correlation_id
│   ├── resilience.py        # Tenacity wrapper para LLM
│   └── security.py          # Sanitizacao + aprovacao humana
├── tools/
│   ├── pdf_reader.py        # Leitura de PDF (PyMuPDF)
│   ├── job_reader.py        # Leitura de TXT (UTF-8/CP1252)
│   └── report_writer.py     # Escrita de relatorio Markdown
├── prompts/
│   ├── extract_prompt.py    # Prompt de extracao estruturada
│   └── analyze_prompt.py    # Prompt de analise de compatibilidade
├── tests/
│   ├── test_tools.py        # Testes unitarios das tools
│   ├── test_nodes.py        # Testes unitarios dos nos
│   ├── test_integration.py  # Testes de integracao (grafo completo)
│   ├── test_e2e.py          # Testes E2E (API -> Grafo -> Resposta)
│   └── test_security.py     # Testes de cenario adversarial
├── lowcode/
│   └── n8n_workflow.json    # Workflow exportado do n8n
├── scripts/
│   ├── analyze_ci_logs.py   # IA analisa logs do CI
│   ├── analyze_execution.py # Reconstrui execucao a partir dos logs
│   └── detect_anomaly.py    # Deteccao de anomalias + tendencia
├── docs/
│   ├── prompts/
│   │   ├── system_prompts.md
│   │   └── refinement_log.md
│   ├── qa/
│   │   ├── ai_code_review.md
│   │   ├── test_plan.md
│   │   └── risk_matrix.md
│   ├── evidencias/
│   │   ├── ci_log_analysis.md
│   │   ├── anomaly_report.md
│   │   └── execution_trace.json
│   ├── lowcode/
│   │   └── reproduction_guide.md
│   └── architecture/
│       └── diagram.mmd
├── input/
│   ├── curriculo.pdf        # Dados de teste (nao versionados)
│   └── vaga.txt             # Dados de teste (nao versionados)
├── output/
│   └── relatorio.md         # Relatorios gerados (nao versionados)
├── logs/                    # Logs JSON estruturados (nao versionados)
├── .github/
│   └── workflows/ci.yml     # Pipeline CI/CD
├── docker-compose.yml       # API + Streamlit + PostgreSQL + n8n
├── Dockerfile               # Container da API
├── main.py                  # CLI original (mantido)
├── requirements.txt         # Dependencias com versoes fixadas
├── .env.example             # Variaveis de ambiente (sem valores reais)
├── .gitignore               # Protecao de segredos e dados
└── README.md                # Documentacao completa
```

---

# Arquitetura

O projeto esta dividido em 7 camadas.

## 1. Interface (UI)

Responsavel pela interacao visual do usuario.

* Streamlit (3 abas: Nova Analise, Historico, Comparar)
* CLI (main.py) mantido para compatibilidade

---

## 2. API (Backend)

Camada de servicos REST.

* FastAPI com endpoints: /analyze, /analyze/batch, /history, /health
* Validacao Pydantic em todas as entradas
* Rate limit e CORS configurados

---

## 3. Agente (Core)

Responsavel por:

* controlar o fluxo via LangGraph
* armazenar contexto no AgentState
* chamar ferramentas deterministicamente
* solicitar analise ao modelo de IA (LLM)
* gerar resposta final estruturada
* gerenciar memoria persistente (PostgreSQL)
* aplicar seguranca (sanitizacao, aprovacao)

---

## 4. Ferramentas (Tools)

Ferramentas responsaveis por acessar arquivos locais.

### PDF Reader

Responsabilidades:

* abrir PDF
* extrair texto
* retornar string

### Job Reader

Responsabilidades:

* abrir vaga.txt
* retornar texto

### Report Writer

Responsabilidades:

* criar pasta output se necessario
* salvar relatorio em Markdown

---

## 5. Persistencia (Database)

* PostgreSQL com PostgresSaver (checkpointer LangGraph)
* Historico de analises acessivel para comparacao
* Time-travel debugging

---

## 6. Observabilidade

* Logs JSON estruturados (structlog)
* Traces por no (LangSmith)
* Metricas: latencia, tokens, taxa de erro
* Script de investigacao de execucoes

---

## 7. Integracao Externa

* n8n (automacao visual: email/webhook -> API -> Slack)
* Webhook para curriculos automaticos

---

# Fluxo do LangGraph

```text
START
  |
validate_inputs
  |
sanitize_inputs
  |
load_history
  |
+-- read_curriculum --+  (PARALELO)
|                     |
+-- read_job ---------+
  |
extract_information
  |
analyze_match
  |
request_approval
  |
generate_report
  |
save_report
  |
END
```

---

# State

Todo o contexto sera compartilhado atraves do State do LangGraph.

```python
class AgentState(TypedDict):
    # Original
    curriculum_path: str
    job_path: str
    curriculum_text: str
    job_description: str
    extracted_information: dict
    compatibility_score: int
    analysis: str
    report: str

    # Novo (Projeto Final)
    history: List[Dict[str, Any]]
    approval_required: bool
    approval_decision: Optional[str]
    correlation_id: str
    metadata: Dict[str, Any]
```

Cada no podera ler e atualizar essas informacoes.

---

# Nos

## validate_inputs

Responsavel por:

* verificar existencia dos arquivos
* validar extensao
* validar conteudo

## sanitize_inputs

Responsavel por:

* detectar padroes de prompt injection
* sanitizar textos antes de enviar ao LLM

## load_history

Responsavel por:

* recuperar analises anteriores do PostgreSQL
* popular campo history no estado

## read_curriculum

Utiliza: PDF Reader
Atualiza: curriculum_text

## read_job

Utiliza: Job Reader
Atualiza: job_description

## extract_information

Responsavel por identificar dados estruturados do curriculo e da vaga.
Atualiza: extracted_information

## analyze_match

Responsavel por:

* comparar curriculo e vaga
* calcular compatibilidade
* produzir analise

Atualiza: compatibility_score, analysis

## request_approval

Responsavel por:

* pausar execucao para aprovacao humana
* aguardar decisao do usuario

Atualiza: approval_required, approval_decision

## generate_report

Responsavel por montar o relatorio final em Markdown.
Atualiza: report

## save_report

Utiliza: Report Writer
Responsavel por salvar o relatorio.

---

# Ferramentas

## PDF Reader

Entrada: input/curriculo.pdf
Saida: str

## Job Reader

Entrada: input/vaga.txt
Saida: str

## Report Writer

Entrada: str
Saida: output/relatorio.md

---

# Prompts

O projeto utiliza dois prompts principais.

## Prompt de Extracao

Objetivo: Extrair informacoes estruturadas do curriculo e da vaga.
Saida esperada: JSON com CurriculumData + JobData

## Prompt de Analise

Objetivo: Comparar curriculo e vaga.
Saida esperada: Markdown com score, pontos fortes, gaps, recomendacoes.

---

# Tratamento de Erros

O agente trata:

* curriculo inexistente
* vaga inexistente
* PDF vazio ou corrompido
* falha de leitura
* falha de extracao LLM (com retry + fallback)
* falha ao salvar relatorio

Em caso de erro, a execucao e interrompida com mensagem descritiva ou desvia para END.

---

# Seguranca

* Utilizar `.env` para armazenar credenciais (LLM_API_KEY, DATABASE_URL, etc.)
* Nunca versionar `.env`
* Disponibilizar apenas `.env.example`
* Validar entradas com Pydantic antes do processamento
* Sanitizar textos contra prompt injection
* Aprovacao humana antes de acoes destrutivas
* Cenario adversarial testado e documentado

---

# Dependencias

```text
langgraph==1.2.9
langgraph-checkpoint-postgres==1.2.9
langchain==1.3.13
langchain-groq==1.1.3
langchain-core==1.4.9
fastapi==0.115.12
uvicorn[standard]==0.34.3
python-multipart==0.0.20
streamlit==1.45.1
requests==2.32.3
psycopg[pool]==3.1.18
structlog==25.4.0
tenacity==9.1.2
langsmith==0.3.4
python-dotenv==1.2.2
pydantic==2.13.4
pymupdf==1.28.0
pytest==8.3.4
pytest-mock==3.14.0
```

---

# Execucao

## Opcao 1: CLI

```bash
python main.py --curriculo input/curriculo.pdf --vaga input/vaga.txt
```

## Opcao 2: Docker Compose

```bash
docker-compose up
```

Servicos: API (:8000), Streamlit (:8501), PostgreSQL (:5432), n8n (:5678)

## Opcao 3: Manual

```bash
# Terminal 1 - API
uvicorn api.main:app --reload

# Terminal 2 - Streamlit
streamlit run streamlit_app.py
```

---

# Possiveis Evolucoes

* Exportacao em PDF do relatorio
* Integracao com APIs de recrutamento (LinkedIn, Gupy)
* Suporte a OCR para PDFs baseados em imagem
* Dashboard de metricas em tempo real
* Notificacoes push para recrutadores
* Multi-idioma (inglues, espanhol)
