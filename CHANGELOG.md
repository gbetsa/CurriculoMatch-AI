# Changelog - CurriculoMatch AI

Todas as mudancas notaveis neste projeto serao documentadas neste arquivo.

O formato e baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [1.0.0] - 2026-08-29

### Adicionado
- **Sistema completo de triagem de curriculos** com LangGraph + Groq
- **API REST** (FastAPI) com endpoints /analyze, /analyze/batch, /history, /health
- **Interface Streamlit** com abas Nova Analise e Comparar
- **Guardrails n8n** com AI Agent para deteccao de prompt injection
- **Memoria persistente** via PostgreSQL checkpointer (PostgresSaver)
- **Seguranca multi-camada**: regex PT+EN, n8n AI Agent, sanitize_inputs
- **Human-in-the-loop**: aprovacao/rejeicao de analises
- **Observabilidade**: structlog (logs JSON), correlation ID, script de investigacao
- **Resiliencia**: retry com tenacity, fallback para LLM local
- **CI/CD**: GitHub Actions com 7 jobs (lint, typecheck, test-unit, test-integration, test-api, test-e2e, docker-build)
- **85+ testes**: unitarios, integracao, E2E, seguranca
- **Code review com IA** e analise de logs
- **Deteccao de anomalias** com tendencia de falha
- **Documentacao completa**: system prompts, refinement log, design decisions, reproduction guide

### Corrigido
- Falsos-negativos por variacao de nomenclatura (REGRA DE OURO)
- Schema Pydantic dividido para evitar perda de tokens
- concurrent update de is_valid nos nos paralelos do LangGraph
- Rate limit do Groq (troca de modelo para qwen/qwen3.8-27b)

### Removido
- analyze_injection (LLM-based) do workflow (mantido via regex)
- Endpoint /approve do Streamlit (mantido na API)
- Tab de historico do Streamlit (mantido via API)

---

## [0.9.0] - 2026-08-28

### Adicionado
- Guardrails n8n com AI Agent (Groq) para deteccao de injection
- Workflow batch com 18 nodes
- Streamlit sem fallback para API direta
- Padroes PT+EN de injection (29 padroes)

### Corrigido
- n8n Code node: this.helpers.httpRequest ao inves de fetch
- Batch: validate_file_upload dentro de try/except
- API: resposta 200 com _blocked para injection

---

## [0.8.0] - 2026-08-27

### Adicionado
- API REST completa (FastAPI)
- Endpoints: /analyze, /analyze/batch, /history, /health
- Streamlit UI com 3 abas (Nova Analise, Historico, Comparar)
- Rate limiting por IP
- Validacao de upload (PDF, 10MB max)
- CORS configurado

---

## [0.7.0] - 2026-08-26

### Adicionado
- Historico de analises similares via PostgreSQL
- Busca por mesmo candidato (+100) e mesmo cargo (+50)
- Prompt atualizado com secao 5 (Historico)
- 6 testes unitarios para history_query

---

## [0.6.0] - 2026-08-25

### Adicionado
- Seguranca anti-injection (regex)
- Sanitizacao de textos de entrada
- Human-in-the-loop (request_approval)
- Cenario adversarial documentado
- 15 testes de seguranca

---

## [0.5.0] - 2026-08-24

### Adicionado
- Nos de execucao do LangGraph (9 nodes)
- Workflow completo com arestas condicionais
- Schema Pydantic (ExtractedInformation)
- Tools: read_pdf, read_txt, save_report
- Prompts: extract_prompt, analyze_prompt

---

## [0.4.0] - 2026-08-23

### Adicionado
- Estado compartilhado (AgentState)
- Checkpointer PostgreSQL (PostgresSaver)
- Paralelizacao read_curriculum | read_job
- .env.example com todas as variaveis

---

## [0.3.0] - 2026-08-22

### Adicionado
- Observabilidade: structlog, correlation ID
- Resiliencia: tenacity (retry + fallback)
- Script de investigacao de execucoes
- 26 testes de observabilidade

---

## [0.2.0] - 2026-08-21

### Adicionado
- Suite de testes (unit + integration + e2e)
- CI/CD com GitHub Actions
- Code review com IA
- Matriz de risco e plano de testes

---

## [0.1.0] - 2026-08-20

### Adicionado
- Setup inicial do projeto
- Ambiente virtual e dependencias
- Estrutura de diretorios
- Dockerfile
- requirements.txt
