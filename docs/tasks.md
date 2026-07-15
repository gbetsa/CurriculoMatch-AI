# Tarefas de Implementação - CurriculoMatch AI

- [x] **Bloco 1: Configuração do Ambiente e Estrutura Base**
  - [x] Criar ambiente virtual (`python -m venv venv`).
  - [x] Criar `requirements.txt` com as dependências (incluindo `langchain-groq`).
  - [x] Criar `.env.example` e estrutura para `.env`.
  - [x] Criar diretórios: `input/`, `output/`, `graph/`, `tools/`, `prompts/`.

- [x] **Bloco 2: Implementação das Ferramentas (Tools)**
  - [x] Implementar `tools/pdf_reader.py` (pymupdf).
  - [x] Implementar `tools/job_reader.py` (leitura TXT utf-8).
  - [x] Implementar `tools/report_writer.py` (criação de diretório output e arquivo md).

- [x] **Bloco 3: Estado Compartilhado e Esquemas**
  - [x] Implementar `graph/state.py` com o `AgentState`.
  - [x] Implementar Pydantic schemas: `CurriculumData`, `JobData`, `ExtractedInformation`.

- [x] **Bloco 4: Criação dos Prompts**
  - [x] Implementar `prompts/extract_prompt.py`.
  - [x] Implementar `prompts/analyze_prompt.py`.

- [x] **Bloco 5: Nós de Execução (Nodes)**
  - [x] Implementar `graph/nodes.py` com todos os nós (`validate_inputs`, `read_curriculum`, `read_job`, `extract_information`, `analyze_match`, `generate_report`, `save_report`).

- [x] **Bloco 6: Orquestração (Workflow)**
  - [x] Implementar `graph/workflow.py` com `StateGraph`, arestas e compilação do grafo.

- [x] **Bloco 7: Ponto de Entrada (main.py)**
  - [x] Implementar `main.py` para invocação do sistema e passagem do estado inicial.

- [ ] **Bloco 8: Testes e Validação**
  - [ ] Adicionar arquivo PDF de currículo e TXT da vaga em `input/`.
  - [ ] Executar pipeline e verificar saída em `output/relatorio.md`.
