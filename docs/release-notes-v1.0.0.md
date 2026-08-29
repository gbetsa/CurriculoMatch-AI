# Release Notes - v1.0.0

**Data:** 29 de Agosto de 2026

**Tag:** v1.0.0

---

## Resumo

Primeira versao completa do CurriculoMatch AI — agente autônomo de triagem de curriculos com LangGraph, API REST, interface Streamlit, guardrails n8n e pipeline CI/CD.

## Features

### Core
- Agente LangGraph com 8 nos de execucao
- Extracao via LLM com Structured Output (Pydantic)
- Analise de compatibilidade com REGRA DE OURO anti-alucinacao
- Relatorio Markdown com score, pontos fortes, gaps e recomendacao

### API REST (FastAPI)
- `POST /analyze` — analise individual
- `POST /analyze/batch` — analise em lote com ranking
- `GET /history` — historico paginado
- `GET /history/{id}` — detalhes de uma analise
- `GET /health` — health check

### Interface (Streamlit)
- Aba Nova Analise: upload PDF + campos de vaga
- Aba Comparar: upload multiplos PDFs com ranking

### Guardrails (n8n)
- Validacao de dados (PDF magic bytes, campos obrigatorios)
- AI Agent para deteccao de prompt injection (Groq)
- Workflow batch com 18 nodes

### Seguranca
- Sanitizacao anti-injection (29 padroes PT+EN)
- Human-in-the-loop (aprovacao/rejeicao)
- Rate limiting por IP (100 req/min)
- Validacao de upload (PDF, 10MB max)

### Memoria
- Checkpointer PostgreSQL (PostgresSaver)
- Historico de analises similares
- Busca por candidato (+100) e cargo (+50)

### Observabilidade
- Logs JSON estruturados (structlog)
- Correlation ID para rastreabilidade
- Traces opcionais (LangSmith)
- Script de investigacao de execucoes

### Resiliencia
- Retry com tenacity (3 tentativas, backoff exponencial)
- Fallback para LLM local (Ollama)

### QA
- 85+ testes (unit, integracao, e2e, seguranca)
- Code review com IA
- Analise de logs com IA
- Deteccao de anomalias

### CI/CD
- GitHub Actions com 7 jobs paralelos
- Ruff + Black (lint/format)
- Docker build

## Bug Fixes

- Falsos-negativos por variacao de nomenclatura
- Schema Pydantic dividido para evitar perda de tokens
- concurrent update de is_valid nos nos paralelos
- Rate limit do Groq (modelo trocado para qwen/qwen3.8-27b)

## Breaking Changes

- Endpoint `/approve` removido do Streamlit (mantido na API)
- Tab de historico removida do Streamlit (mantido via API)

## Dependencias Principais

- Python 3.12+
- LangGraph 1.2.11
- LangChain + LangChain-Groq
- FastAPI + Uvicorn
- Streamlit 1.45.1
- PostgreSQL 15+ (checkpointer)
- n8n (guardrails)

## Como Atualizar

```bash
git pull origin main
pip install -r requirements.txt
cp .env.example .env  # configurar chaves
docker-compose up -d  # subir todos os servicos
```
