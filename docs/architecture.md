# Arquitetura do Sistema - CurriculoMatch AI

## 1. Visao Geral

O **CurriculoMatch AI** e um agente de IA baseado na arquitetura de grafos de estado utilizando o **LangGraph**. A aplicacao automatiza a triagem de curriculos, orquestrando um fluxo de trabalho que extrai informacoes de um curriculo (PDF) e de uma descricao de vaga (TXT), compara os dados utilizando um LLM e gera um relatorio estruturado de compatibilidade.

**Classificacao:** Sistema Hibrido (workflow deterministico + agente LLM com memoria persistente).

**Continuidade do Mini-Projeto:** A versao do modulo 2 (CLI + LangGraph + 3 tools) foi mantida funcional e evoluida para atender todos os requisitos do projeto final M2.2.

---

## 2. Camadas da Arquitetura

O sistema esta estruturado em 7 camadas principais:

### 2.1. Interface (UI)
Responsavel pela interacao visual do usuario com o agente.
- **Streamlit:** Interface web com 3 abas (Nova Analise, Historico, Comparar).
- **CLI (main.py):** Ponto de entrada de linha de comando (mantido para compatibilidade).

### 2.2. API (Backend)
Camada de servicos REST que expoe o agente para consumidores externos.
- **FastAPI:** Endpoints REST para analise, historico e health check.
- **Validacao:** Pydantic schemas para request/response.
- **Rate Limit:** Controle de requisicoes por IP.

### 2.3. Agente (Core)
O nucleo inteligente da aplicacao, responsavel por orquestrar o fluxo de execucao definido no LangGraph.
- **Responsabilidades:**
  - Controlar a transicao entre os nos (etapas do fluxo).
  - Gerenciar e atualizar o **Estado (State)** compartilhado.
  - Chamar as ferramentas (Tools) necessarias.
  - Solicitar a extracao de dados e a analise preditiva ao modelo de IA (LLM).
  - Gerenciar **memoria persistente** via checkpointer PostgreSQL.
  - Aplicar **seguranca** (sanitizacao, aprovacao humana).

### 2.4. Ferramentas (Tools)
Modulos isolados responsaveis pela interacao com o sistema de arquivos e extracao de dados brutos.
- **PDF Reader:** Abre o arquivo PDF do curriculo e extrai o texto puro.
- **Job Reader:** Abre o arquivo de texto da vaga e carrega a descricao.
- **Report Writer:** Cria a pasta de saida (se necessario) e salva o relatorio final em formato Markdown.

### 2.5. Persistencia (Database)
Armazenamento relacional para memoria de longo prazo do agente.
- **PostgreSQL:** Banco de dados para o checkpointer LangGraph.
- **Checkpointer (PostgresSaver):** Persiste estado do grafo entre execucoes.
- **Historico:** Analises anteriores de candidatos e vagas.

### 2.6. Observabilidade
Sinais correlacionados para investigacao e auditoria do agente.
- **Logs Estruturados (JSON):** Cada no loga timestamp, duracao, status, tokens.
- **Traces (LangSmith):** Spans por no com latencia e decisoes.
- **Metricas:** Contador de execucoes, taxa de erro, latencia media.

### 2.7. Integracao Externa
Conexao com servicos e automacoes low-code.
- **n8n:** Orquestrador visual para gatilhos (email, webhook) e saidas (Slack, email).
- **Webhook:** Endpoint para receber curriculos automaticamente.

---

## 3. Estado Compartilhado (State)

Todo o contexto da execucao e mantido em um estado compartilhado entre os nos do grafo, definido pela estrutura `AgentState`. Isso evita o reposicionamento de dados e garante que cada etapa tenha o contexto completo em memoria.

```python
class AgentState(TypedDict):
    # Entradas e Validacoes
    curriculum_path: str
    job_path: str
    is_valid: bool
    error_message: Optional[str]

    # Dados Brutos Extraidos
    curriculum_text: str
    job_description: str

    # Dados Estruturados (Saida da LLM na etapa de Extracao)
    extracted_information: Dict[str, Any]

    # Resultados Finais da Analise
    compatibility_score: int
    analysis: str

    # Saida Final
    report: str

    # --- CAMPOS NOVOS (Projeto Final) ---
    history: List[AnalysisRecord]        # Historico de analises anteriores
    approval_required: bool              # Gate de aprovacao humana
    approval_decision: Optional[str]     # "approved" | "rejected"
    correlation_id: str                  # ID unico para observabilidade
    metadata: Dict[str, Any]            # Latencia, tokens, versoes
```

---

## 4. Fluxo de Execucao (LangGraph Workflow)

A execucao segue um pipeline direcionado e sequencial (com paralelizacao), onde cada passo e processado como um **No (Node)** no grafo:

```text
[ START ]
   |
(1) validate_inputs      -> Valida os arquivos de entrada.
   |
   +-- [condicional] --> END (se invalido)
   |
(2) sanitize_inputs      -> Sanitiza textos contra prompt injection.
   |
(3) load_history         -> Recupera analises anteriores do PostgreSQL.
   |
   +--- read_curriculum --+  (PARALELO)
   |                      |
   +--- read_job ---------+
   |
(4) extract_information  -> O LLM extrai dados estruturados da vaga e do curriculo.
   |
(5) analyze_match        -> O LLM cruza os dados, calcula a compatibilidade e redige a analise.
   |
(6) request_approval     -> Pausa execucao aguardando aprovacao humana (se necessario).
   |
   +-- [condicional] --> END (se rejeitado)
   |
(7) generate_report      -> Formata a analise gerada em um documento Markdown.
   |
(8) save_report          -> Utiliza o Report Writer para persistir o relatorio em disco.
   |
[ END ]
```

---

## 5. Integracao com LLM e Prompts

A inteligencia do sistema baseia-se em chamadas estruturadas ao modelo de linguagem atraves do **LangChain**, empregando dois *prompts* principais:

1. **Prompt de Extracao:** Converte texto nao estruturado (curriculo e vaga) em um formato JSON estruturado (contendo nome, habilidades, experiencias, formacao, idiomas e requisitos).
2. **Prompt de Analise:** Compara o JSON extraido, inferindo o percentual de compatibilidade, identificando pontos fortes/fracos e fornecendo recomendacoes claras de melhoria.

**Configuracao do Modelo:** O modelo e configurado via variavel de ambiente (`LLM_MODEL`), suportando multiplos provedores (Groq, OpenAI, Ollama local).

---

## 6. Seguranca e Governanca

- **Protecao de Credenciais:** A aplicacao utiliza um padrao unificado de credenciais gerenciadas estritamente via variaveis de ambiente (`.env`).
- **Sanitizacao de Entradas:** Textos sao sanitizados contra padroes de prompt injection antes de serem enviados ao LLM.
- **Aprovacao Humana:** No `request_approval` pausa execucao antes de salvar relatorio, aguardando confirmacao do usuario.
- **Cenario Adversarial:** PDF de teste com injection嵌入o demonstra que o agente ignora injecoes e mantem regras originais.
- **Validacao Pydantic:** Todas as entradas da API sao validadas com schemas rigorosos.

---

## 7. Observabilidade

- **Logs Estruturados:** Cada no loga JSON com timestamp, correlation_id, duracao, status e tokens.
- **Traces:** LangSmith registra spans por no com latencia e decisoes.
- **Investigacao:** Script `scripts/analyze_execution.py` reconstrui execucoes completas a partir dos logs.
- **Tratamento de Falhas:** Tenacity wrapper com retry, timeout e fallback nas chamadas LLM.
