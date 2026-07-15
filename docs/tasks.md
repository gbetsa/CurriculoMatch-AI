# Tarefas de Implementação - CurriculoMatch AI

- [ ] **Bloco 1: Configuração do Ambiente e Estrutura Base**
  - [ ] Criar ambiente virtual (`python -m venv venv`).
  - [ ] Criar `requirements.txt` com as dependências (incluindo `langchain-groq`).
  - [ ] Criar `.env.example` e estrutura para `.env`.
  - [ ] Criar diretórios: `input/`, `output/`, `graph/`, `tools/`, `prompts/`.

- [ ] **Bloco 2: Implementação das Ferramentas (Tools)**
  - [ ] Implementar `tools/pdf_reader.py` (pymupdf).
  - [ ] Implementar `tools/job_reader.py` (leitura TXT utf-8).
  - [ ] Implementar `tools/report_writer.py` (criação de diretório output e arquivo md).

- [ ] **Bloco 3: Estado Compartilhado e Esquemas**
  - [ ] Implementar `graph/state.py` com o `AgentState`.
  - [ ] Implementar Pydantic schemas: `CurriculumData`, `JobData`, `ExtractedInformation`.

- [ ] **Bloco 4: Criação dos Prompts**
  - [ ] Implementar `prompts/extract_prompt.py`.
  - [ ] Implementar `prompts/analyze_prompt.py`.

- [ ] **Bloco 5: Nós de Execução (Nodes)**
  - [ ] Implementar `graph/nodes.py` com todos os nós (`validate_inputs`, `read_curriculum`, `read_job`, `extract_information`, `analyze_match`, `generate_report`, `save_report`).

- [ ] **Bloco 6: Orquestração (Workflow)**
  - [ ] Implementar `graph/workflow.py` com `StateGraph`, arestas e compilação do grafo.

- [ ] **Bloco 7: Ponto de Entrada (main.py)**
  - [ ] Implementar `main.py` para invocação do sistema e passagem do estado inicial.

- [ ] **Bloco 8: Testes e Validação**
  - [ ] Adicionar arquivo PDF de currículo e TXT da vaga em `input/`.
  - [ ] Executar pipeline e verificar saída em `output/relatorio.md`.
