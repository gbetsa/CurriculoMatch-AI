# Bloco 14: IA para QA e Testes Inteligentes

## Descrição
Utilizar IA para analisar código do projeto (code review), gerar ou refinar testes automatizados (integração, aceitação ou E2E) e priorizar cenários por risco/impacto. Documentar como a IA auxiliou em cada etapa.

## Estrutura de Arquivos
```
tests/
  test_integration.py   # Testes de integração (grafo completo com mock LLM)
  test_e2e.py           # Testes E2E (API → Grafo → Banco → Resposta)
docs/qa/
  ai_code_review.md     # Evidência de code review com IA
  test_plan.md          # Plano de testes com priorização por risco
  risk_matrix.md        # Matriz risco × impacto
```

## Componentes

### 1. Code Review com IA
- Selecionar 1 PR real do projeto (ex: PR #14 — orquestração do workflow)
- Usar IA (Copilot/Claude/ChatGPT) para analisar o diff
- Documentar em `docs/qa/ai_code_review.md`:
  - Diff analisado (arquivo + linhas)
  - Problemas encontrados pela IA
  - Sugestões aceitas vs rejeitadas (com justificativa)

### 2. Testes de Integração (`test_integration.py`)
Testar o grafo completo com LLM mockada:
- Teste: fluxo happy path (PDF + vaga válidos → relatório gerado)
- Teste: falha de validação (PDF inexistente → END sem gastar tokens)
- Teste: falha de leitura (PDF corrompido → error_message no estado)
- Mock: `ChatGroq` substituído por `RunnableLambda` que retorna JSON predefinido

### 3. Testes E2E (`test_e2e.py`)
Testar via API (FastAPI TestClient):
- Teste: POST /analyze com PDF + vaga → 200 + relatório
- Teste: POST /analyze sem PDF → 422
- Teste: GET /health → 200
- Requer: banco PostgreSQL de teste (pode ser Docker ou SQLite fallback)

### 4. Priorização por Risco
Matriz de risco × impacto:
| Cenário | Risco | Impacto | Prioridade |
|---------|-------|---------|------------|
| Análise completa falha | Alto | Alto | P0 |
| Score incorreto (falso positivo) | Médio | Alto | P1 |
| Falha de leitura PDF | Baixo | Médio | P2 |
| Timeout na API | Médio | Médio | P2 |

**Justificativa P0**: "Teste E2E de análise completa é prioridade porque uma regressão nesse fluxo torna a aplicação inútil para o usuário."

## Critérios de Aceite
- [ ] Criar `docs/qa/ai_code_review.md` com análise de 1 PR real documentada.
- [ ] Criar `tests/test_integration.py` com pelo menos 3 testes (happy path, validação, falha leitura).
- [ ] Criar `tests/test_e2e.py` com pelo menos 2 testes via FastAPI TestClient.
- [ ] Criar `docs/qa/risk_matrix.md` com matriz risco × impacto.
- [ ] Justificar no `docs/qa/test_plan.md` por que o teste E2E de análise é P0.
- [ ] Todos os testes passarem com `pytest tests/`.
- [ ] Documentar no README.md (seção "QA, Observabilidade e DevOps").

## Dependências
- Bloco 10 (API) — para testes E2E via TestClient
- Bloco 5 (Nós) — mocks dos nodes para testes de integração
- Bloco 8 (Testes existentes) — base de testes unitários

## Branch Sugerida
`feature/14-qa-ai-tests`
