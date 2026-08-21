# Tarefas de Implementacao - CurriculoMatch AI

## Mini-Projeto (Modulo 2) - CONCLUIDO

- [x] **Bloco 1: Configuracao do Ambiente e Estrutura Base**
  - [x] Criar ambiente virtual (`python -m venv venv`).
  - [x] Criar `requirements.txt` com as dependencias (incluindo `langchain-groq`).
  - [x] Criar `.env.example` e estrutura para `.env`.
  - [x] Criar diretorios: `input/`, `output/`, `graph/`, `tools/`, `prompts/`.

- [x] **Bloco 2: Implementacao das Ferramentas (Tools)**
  - [x] Implementar `tools/pdf_reader.py` (pymupdf).
  - [x] Implementar `tools/job_reader.py` (leitura TXT utf-8).
  - [x] Implementar `tools/report_writer.py` (criacao de diretorio output e arquivo md).

- [x] **Bloco 3: Estado Compartilhado e Esquemas**
  - [x] Implementar `graph/state.py` com o `AgentState`.
  - [x] Implementar Pydantic schemas: `CurriculumData`, `JobData`, `ExtractedInformation`.

- [x] **Bloco 4: Criacao dos Prompts**
  - [x] Implementar `prompts/extract_prompt.py`.
  - [x] Implementar `prompts/analyze_prompt.py`.

- [x] **Bloco 5: Nos de Execucao (Nodes)**
  - [x] Implementar `graph/nodes.py` com todos os nos (`validate_inputs`, `read_curriculum`, `read_job`, `extract_information`, `analyze_match`, `generate_report`, `save_report`).

- [x] **Bloco 6: Orquestracao (Workflow)**
  - [x] Implementar `graph/workflow.py` com `StateGraph`, arestas e compilacao do grafo.

- [x] **Bloco 7: Ponto de Entrada (main.py)**
  - [x] Implementar `main.py` para invocacao do sistema e passagem do estado inicial.

- [x] **Bloco 8: Testes e Validacao**
  - [x] Adicionar arquivo PDF de curriculo e TXT da vaga em `input/`.
  - [x] Executar pipeline e verificar saida em `output/relatorio.md`.

---

## Projeto Final (M2.2 - 60% da Nota)

- [ ] **Bloco 9: Memoria e Checkpointer PostgreSQL**
  - [ ] Criar `graph/checkpointer.py` com PostgresSaver configurado via DATABASE_URL.
  - [ ] Atualizar `graph/state.py` com novos campos: history, correlation_id, metadata.
  - [ ] Criar no `load_history` em `graph/nodes.py` que recupera historico do PostgreSQL.
  - [ ] Atualizar `graph/workflow.py` para compilar grafo com checkpointer.
  - [ ] Adicionar DATABASE_URL ao `.env.example`.
  - [ ] Testar que segunda execucao com mesmo candidato recupera historico.
  - [ ] Branch: `feature/09-memory-checkpoint`

- [ ] **Bloco 10: API REST com FastAPI**
  - [ ] Criar `api/schemas.py` com Pydantic models para request/response.
  - [ ] Criar `api/main.py` com FastAPI app e endpoints documentados.
  - [ ] Criar `api/dependencies.py` com inicializacao do grafo + checkpointer.
  - [ ] Validar uploads: maximo 10MB, apenas PDF.
  - [ ] Retornar erros em formato JSON padronizado.
  - [ ] Adicionar CORS middleware para Streamlit.
  - [ ] Executar com `uvicorn api.main:app --reload` sem erros.
  - [ ] Branch: `feature/10-api-fastapi`

- [ ] **Bloco 11: Interface Web com Streamlit**
  - [ ] Criar `streamlit_app.py` com layout de 3 abas.
  - [ ] Aba 1: upload PDF + campos de vaga -> chama API -> exibe relatorio.
  - [ ] Aba 2: tabela com historico -> chama API -> paginacao funcional.
  - [ ] Aba 3: multiplos PDFs + vaga -> chama API batch -> ranking comparativo.
  - [ ] Tratar erros de conexao com API.
  - [ ] Executar com `streamlit run streamlit_app.py` sem erros.
  - [ ] Branch: `feature/11-streamlit-ui`

- [ ] **Bloco 12: Seguranca, Governanca e Limites de Autonomia**
  - [ ] Criar `graph/security.py` com funcao `sanitize_text()`.
  - [ ] Adicionar no `sanitize_inputs` ao grafo.
  - [ ] Adicionar no `request_approval` ao grafo.
  - [ ] Criar endpoint `POST /approve/{analysis_id}` na API.
  - [ ] Atualizar Streamlit com botao de aprovacao.
  - [ ] Criar `tests/test_security.py` com cenario adversarial.
  - [ ] Criar PDF de teste com injection em `tests/fixtures/`.
  - [ ] Branch: `feature/12-security-governance`

- [ ] **Bloco 13: Observabilidade e Resiliencia**
  - [ ] Criar `graph/observability.py` com structlog configurado.
  - [ ] Atualizar todos nos para logar inicio/fim com correlation_id.
  - [ ] Criar `graph/resilience.py` com wrapper tenacity para LLM.
  - [ ] Criar `scripts/analyze_execution.py` para investigacao.
  - [ ] Adicionar `logs/` ao `.gitignore`.
  - [ ] Adicionar LANGCHAIN_TRACING_V2 ao `.env.example`.
  - [ ] Branch: `feature/13-observability`

- [ ] **Bloco 14: IA para QA e Testes Inteligentes**
  - [ ] Criar `docs/qa/ai_code_review.md` com analise de 1 PR real.
  - [ ] Criar `tests/test_integration.py` com pelo menos 3 testes.
  - [ ] Criar `tests/test_e2e.py` com pelo menos 2 testes via TestClient.
  - [ ] Criar `docs/qa/risk_matrix.md` com matriz risco x impacto.
  - [ ] Todos os testes passarem com `pytest tests/`.
  - [ ] Branch: `feature/14-qa-ai-tests`

- [ ] **Bloco 15: DevOps Inteligente e Deteccao de Falhas**
  - [ ] Atualizar `.github/workflows/ci.yml` com typecheck + testes e2e + docker build.
  - [ ] Criar `scripts/analyze_ci_logs.py` que le logs e gera analise com IA.
  - [ ] Criar `scripts/detect_anomaly.py` com simulacao + deteccao.
  - [ ] Gerar `docs/evidencias/ci_log_analysis.md`.
  - [ ] Gerar `docs/evidencias/anomaly_report.md` com tendencia.
  - [ ] Branch: `feature/15-devops-anomaly`

- [ ] **Bloco 16: Low-Code / No-Code (n8n)**
  - [ ] Instalar n8n localmente (Docker).
  - [ ] Criar workflow com pelo menos 1 gatilho (email ou webhook).
  - [ ] Workflow integra com API POST /analyze.
  - [ ] Workflow produz saida observavel (Slack ou email).
  - [ ] Exportar workflow como `lowcode/n8n_workflow.json`.
  - [ ] Criar `docs/lowcode/reproduction_guide.md`.
  - [ ] Branch: `feature/16-lowcode-n8n`

- [ ] **Bloco 17: Prompts, Modelos e Refinamento**
  - [ ] Criar `docs/prompts/system_prompts.md` com todos prompts consolidados.
  - [ ] Criar `docs/prompts/refinement_log.md` com 1 ciclo completo.
  - [ ] Atualizar `.env.example` com todas variaveis novas.
  - [ ] Verificar que nenhum valor real de chave aparece no .env.example.
  - [ ] Branch: `feature/17-prompts-refinement`

- [ ] **Bloco 18: Documentacao, Organizacao e Entrega Final**
  - [ ] Reescrever README.md com todas 10 secoes obrigatorias.
  - [ ] Criar GitHub Project (Kanban) com 11 cards.
  - [ ] Mover cards durante desenvolvimento.
  - [ ] Organizar `/docs` com subpastas (prompts, qa, evidencias, lowcode, architecture).
  - [ ] Criar `docker-compose.yml` funcional.
  - [ ] Criar `Dockerfile` funcional.
  - [ ] Gravar video (10 min max) e publicar no YouTube (nao listado).
  - [ ] Inserir link do video no README.md.
  - [ ] Submeter links no AVA antes do prazo.
  - [ ] Branch: `feature/18-final-delivery`
