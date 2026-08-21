# Bloco 13: Observabilidade e Resiliência

## Descrição
Implementar dois sinais de observabilidade correlacionados (logs estruturados + traces) para investigar execuções do agente, identificar erros, latência e decisões relevantes. Aplicar tratamento de falhas com retry, timeout e fallback nas chamadas LLM.

## Dependências Novas
```txt
structlog==25.4.0
tenacity==9.1.2
langsmith==0.3.4
```

## Estrutura de Arquivos
```
graph/observability.py   # Configuração de logs estruturados + correlation_id
graph/resilience.py      # Wrapper tenacity para chamadas LLM
logs/                    # Diretório para logs JSON (em .gitignore)
scripts/
  analyze_execution.py   # Script que reconstrói execução a partir dos logs
```

## Componentes

### 1. Logs Estruturados (JSON)
Cada nó do grafo loga ao iniciar e ao finalizar:
```json
{
  "timestamp": "2026-08-21T14:30:00.123Z",
  "level": "INFO",
  "correlation_id": "uuid-da-execucao",
  "node": "extract_information",
  "event": "node_started",
  "input_summary": {"curriculum_length": 3200, "job_length": 450},
  "duration_ms": null
}
```
Ao finalizar:
```json
{
  "timestamp": "2026-08-21T14:30:02.463Z",
  "level": "INFO",
  "correlation_id": "uuid-da-execucao",
  "node": "extract_information",
  "event": "node_completed",
  "status": "success",
  "duration_ms": 2340,
  "tokens_used": {"prompt": 1200, "completion": 800},
  "model": "llama-3.3-70b-versatile"
}
```

### 2. Traces via LangSmith
- Configurar `LANGCHAIN_TRACING_V2=true` e `LANGCHAIN_API_KEY` no `.env`
- Cada execução gera um trace com spans por nó
- Alternativa caso LangSmith não esteja disponível: logs JSON bastam como "segundo sinal"

### 3. Tratamento de Falhas (Tenacity)
```python
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((APIError, TimeoutError, ConnectionError)),
    before_sleep=log_retry_attempt
)
def call_llm_with_fallback(prompt, model="groq"):
    try:
        return groq_llm.invoke(prompt)
    except Exception:
        return ollama_llm.invoke(prompt)  # Fallback local
```

### 4. Script de Investigação
`scripts/analyze_execution.py`:
- Recebe um `correlation_id`
- Busca todos os logs com esse ID
- Reconstrói: sequência de nós, tempos, erros, decisões
- Gera relatório em Markdown em `docs/evidencias/execution_trace.json`

## Critérios de Aceite
- [ ] Criar `graph/observability.py` com configurador de `structlog` e helper `get_logger(correlation_id)`.
- [ ] Atualizar todos os nós em `graph/nodes.py` para logar início/fim com correlation_id.
- [ ] Criar `graph/resilience.py` com wrapper `call_llm_with_fallback` usando tenacity.
- [ ] Atualizar `graph/nodes.py` para usar o wrapper nas chamadas LLM.
- [ ] Criar `scripts/analyze_execution.py` que reconstrói execução a partir dos logs.
- [ ] Adicionar `logs/` ao `.gitignore`.
- [ ] Adicionar `LANGCHAIN_TRACING_V2` e `LANGCHAIN_API_KEY` ao `.env.example`.
- [ ] Documentar sinais de observabilidade no README.md (seção "QA, Observabilidade e DevOps").
- [ ] Demonstração: logs de 1 execução mostrando correlation_id único, tempos por nó, status.

## Dependências
- Bloco 5 (Nós) — para instrumentar os nodes existentes
- Bloco 9 (Memória) — correlation_id propagado no estado

## Branch Sugerida
`feature/13-observability`
