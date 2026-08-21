# Bloco 10: API REST com FastAPI

## Descrição
Expor o agente LangGraph como API REST para que a interface web (Streamlit) e automações externas (n8n) possam consumir a análise de compatibilidade remotamente. A API deve validar entradas, retornar respostas estruturadas e tratar erros de forma padronizada.

## Dependências Novas
```txt
fastapi==0.115.12
uvicorn[standard]==0.34.3
python-multipart==0.0.20
```

## Estrutura de Arquivos
```
api/
  __init__.py
  main.py             # FastAPI app, rotas, startup/shutdown
  schemas.py          # Pydantic models: AnalyzeRequest, AnalyzeResponse, HistoryItem
  dependencies.py     # Rate limit, validação, inicialização do grafo
```

## Endpoints

### POST /analyze
Análise individual de 1 currículo × 1 vaga.

**Request (multipart/form-data):**
- `curriculum`: UploadFile (PDF)
- `job_title`: str
- `job_description`: str

**Response (200):**
```json
{
  "analysis_id": "uuid",
  "candidate_name": "João Silva",
  "job_title": "Desenvolvedor Python",
  "score": 87,
  "report": "# Relatório de Aderência...",
  "status": "completed",
  "created_at": "2026-08-21T14:30:00Z"
}
```

**Response (422):** Validação falhou (PDF inválido, campos obrigatórios ausentes).

### POST /analyze/batch
Múltiplos currículos × 1 vaga. Retorna ranking.

**Request (multipart/form-data):**
- `curriculos`: List[UploadFile] (PDFs)
- `job_title`: str
- `job_description`: str

**Response (200):**
```json
{
  "batch_id": "uuid",
  "results": [
    {"candidate_name": "João", "score": 87, "analysis_id": "uuid"},
    {"candidate_name": "Maria", "score": 92, "analysis_id": "uuid"}
  ],
  "ranking": ["Maria", "João"]
}
```

### GET /history
Lista análises anteriores (paginado).

**Query params:** `page=1`, `limit=10`, `candidate_name=`, `job_title=`

**Response (200):**
```json
{
  "items": [{"analysis_id": "uuid", "candidate_name": "João", "score": 87, "created_at": "..."}],
  "total": 25,
  "page": 1,
  "pages": 3
}
```

### GET /history/{analysis_id}
Detalhe de uma análise específica.

### GET /health
Health check com status do banco e LLM.

## Critérios de Aceite
- [ ] Criar `api/schemas.py` com Pydantic models para request/response.
- [ ] Criar `api/main.py` com FastAPI app e endpoints documentados.
- [ ] Criar `api/dependencies.py` com inicialização do grafo + checkpointer.
- [ ] Validar uploads: máximo 10MB, apenas PDF, extensão verificada.
- [ ] Validar campos obrigatórios (job_title, job_description) com Pydantic.
- [ ] Retornar erros em formato JSON padronizado `{"detail": "mensagem"}`.
- [ ] Adicionar CORS middleware para permitir Streamlit.
- [ ] Executar com `uvicorn api.main:app --reload` sem erros.
- [ ] Documentar endpoints no README.md (seção "Tool e Integração").

## Dependências
- Bloco 9 (Memória) — checkpointer para persistir análises via API
- Bloco 3 (Estado) — AgentState para o grafo

## Branch Sugerida
`feature/10-api-fastapi`
