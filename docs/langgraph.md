# Fluxo de Execucao - LangGraph (langgraph.md)

## 1. Visao Geral

O coracao do **CurriculoMatch AI** e orquestrado atraves de um Grafo de Estado (State Graph) construido com a biblioteca `langgraph`.
O grafo define o ciclo de vida completo do agente, mapeando o roteamento logico desde o carregamento dos arquivos ate a persistencia do relatorio final. Esta arquitetura baseada em grafos garante modularidade, facil rastreabilidade e tratamento de erros eficiente.

**Evolucao do Mini-Projeto:** O grafo original (7 nos sequenciais) foi evoluido com paralelizacao, checkpointer PostgreSQL, novos nos de seguranca e aprovacao humana.

---

## 2. A Estrutura do Grafo

A execucao do sistema e tratada como um fluxo direcional de nos (nodes) interconectados por arestas (edges).

### 2.1. O Estado (State)
Todas as operacoes no grafo orbitam em torno de um `AgentState`. A cada transicao de no, o no atual recebe o `State` da execucao anterior, realiza suas operacoes e retorna apenas as chaves do estado que foram atualizadas.

**Evolucao:** O `AgentState` agora inclui campos para historico, aprovacao humana, correlation_id e metadata de observabilidade.

### 2.2. Os Nos (Nodes)
Os nos sao funcoes Python puras (ou instancias configuradas) que executam uma tarefa especifica de dominio de forma isolada.

#### Nos Existentes (Mantidos)

1. **`validate_inputs`**:
   - **Responsabilidade**: Verifica se os arquivos do curriculo (`.pdf`) e da vaga (`.txt`) existem nos caminhos fornecidos e se possuem tamanho e extensoes validos.
   - **Mutacao no Estado**: Sinaliza se a execucao pode continuar ou se ocorreu um erro fatal.

2. **`read_curriculum_node`**:
   - **Responsabilidade**: Aciona a *tool* (ferramenta) de PDF Reader para extrair todo o texto bruto do curriculo.
   - **Mutacao no Estado**: Atualiza o campo `curriculum_text`.

3. **`read_job_node`**:
   - **Responsabilidade**: Aciona a *tool* de Job Reader para extrair o texto descritivo da vaga.
   - **Mutacao no Estado**: Atualiza o campo `job_description`.

4. **`extract_information`**:
   - **Responsabilidade**: Envia os textos brutos (vaga e curriculo) para a LLM configurada junto com o *Prompt de Extracao*, exigindo o retorno em um formato JSON rigoroso (via *Structured Output* do LangChain).
   - **Mutacao no Estado**: Atualiza o campo `extracted_information` (Objeto JSON estruturado).

5. **`analyze_match`**:
   - **Responsabilidade**: Submete os dados estruturados a LLM com o *Prompt de Analise*. A LLM raciocina sobre os dados, identifica lacunas, pontos fortes e estipula o percentual de aderencia.
   - **Mutacao no Estado**: Atualiza os campos `compatibility_score` (numerico) e `analysis` (texto descritivo/recomendacoes).

6. **`generate_report`**:
   - **Responsabilidade**: Formata todas as informacoes coletadas, a pontuacao e a analise final em um documento unico, aplicando a estilizacao do Markdown (titulos, listas, negritos).
   - **Mutacao no Estado**: Atualiza o campo `report` com a string final formatada.

7. **`save_report_node`**:
   - **Responsabilidade**: Chama a *tool* de Report Writer para salvar o Markdown final no diretorio `output/`.
   - **Mutacao no Estado**: Nenhuma (Apenas operacao de I/O final).

#### Nos Novos (Projeto Final)

8. **`sanitize_inputs`**:
   - **Responsabilidade**: Detecta e neutraliza padroes de prompt injection nos textos antes de enviar ao LLM.
   - **Mutacao no Estado**: Atualiza `curriculum_text` e `job_description` sanitizados.

9. **`load_history`**:
   - **Responsabilidade**: Recupera analises anteriores do mesmo candidato/vaga via checkpointer PostgreSQL.
   - **Mutacao no Estado**: Atualiza `history` com lista de `AnalysisRecord`.

10. **`request_approval`**:
    - **Responsabilidade**: Pausa execucao aguardando aprovacao humana antes de salvar relatorio.
    - **Mutacao no Estado**: Define `approval_required = True`. No fluxo API, retorna `status: "pending_approval"`. No fluxo Streamlit, mostra botao de confirmacao.

---

## 3. Arestas e Roteamento (Edges)

As arestas definem a direcao do fluxo de execucao. O sistema utiliza arestas sequenciais simples, roteamento condicional e **paralelizacao**.

### 3.1. Fluxo Principal (Sequencial + Paralelo)
No caminho feliz (sem erros), o grafo flui na seguinte ordem:

```text
START
  -> validate_inputs
  -> sanitize_inputs
  -> load_history
  -> [read_curriculum | read_job]  (PARALELO)
  -> extract_information
  -> analyze_match
  -> request_approval
  -> generate_report
  -> save_report
  -> END
```

### 3.2. Paralelizacao
Os nos `read_curriculum` e `read_job` sao executados em paralelo, pois nao dependem um do outro. Isso reduz o tempo total de execucao.

```python
# Em workflow.py
graph.add_edge("load_history", "read_curriculum")
graph.add_edge("load_history", "read_job")    # FAN-OUT

graph.add_edge("read_curriculum", "extract_information")
graph.add_edge("read_job", "extract_information")  # FAN-IN
```

### 3.3. Arestas Condicionais (Conditional Edges)
Decisoes logicas de desvio ou parada ocorrem baseadas no estado atual:

- **Roteamento de Validacao (Pos `validate_inputs`)**:
  - `is_valid == True` -> Aresta segue para `sanitize_inputs`.
  - `is_valid == False` -> Aresta condicional desvia diretamente para `END`, encerrando a execucao prematuramente de forma controlada.

- **Roteamento de Resiliencia de LLM (Pos `extract_information`)**:
  - Caso a LLM falhe ao devolver um JSON valido, o estado registra a falha. Uma aresta condicional avalia o erro e, se critico, desvia o fluxo para `END`, impedindo o desperdicio de tokens no no de analise.

- **Roteamento de Aprovacao (Pos `request_approval`)**:
  - `approval_decision == "approved"` -> Aresta segue para `generate_report`.
  - `approval_decision == "rejected"` ou timeout -> Aresta vai para `END`.

---

## 4. Checkpointer (Memoria Persistente)

O grafo utiliza `PostgresSaver` para persistir estado entre execucoes:

```python
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg_pool import ConnectionPool

pool = ConnectionPool(os.getenv("DATABASE_URL"), max_size=10)
checkpointer = PostgresSaver(pool)

app = build_graph().compile(checkpointer=checkpointer)
```

**Beneficios:**
- Historico de analises acessivel para comparacao
- Time-travel debugging (inspecionar estado em qualquer ponto)
- Retomada de execucoes interrompidas

---

## 5. Compilacao e Execucao

A definicao do grafo e declarativa. O LangGraph utiliza a classe `StateGraph` associada ao `AgentState` para compilar o fluxo.

```python
# Exemplo conceitual da definicao do fluxo na arquitetura:
workflow = StateGraph(AgentState)

# 1. Adicao dos Nos
workflow.add_node("validate_inputs", validate_inputs)
workflow.add_node("sanitize_inputs", sanitize_inputs)
workflow.add_node("load_history", load_history)
workflow.add_node("read_curriculum", read_curriculum_node)
workflow.add_node("read_job", read_job_node)
workflow.add_node("extract_information", extract_information)
workflow.add_node("analyze_match", analyze_match)
workflow.add_node("request_approval", request_approval)
workflow.add_node("generate_report", generate_report)
workflow.add_node("save_report", save_report_node)

# 2. Definicao do Ponto de Entrada
workflow.set_entry_point("validate_inputs")

# 3. Definicao de Arestas e Logica Condicional
workflow.add_conditional_edges("validate_inputs", check_validation_logic)
workflow.add_edge("validate_inputs", "sanitize_inputs")
workflow.add_edge("sanitize_inputs", "load_history")

# 4. Paralelizacao
workflow.add_edge("load_history", "read_curriculum")
workflow.add_edge("load_history", "read_job")
workflow.add_edge("read_curriculum", "extract_information")
workflow.add_edge("read_job", "extract_information")

# 5. Fluxo Sequencial
workflow.add_edge("extract_information", "analyze_match")
workflow.add_edge("analyze_match", "request_approval")
workflow.add_conditional_edges("request_approval", check_approval)
workflow.add_edge("generate_report", "save_report")

# 6. Compilacao com Checkpointer
app = workflow.compile(checkpointer=checkpointer)
```

Esta separacao arquitetural estrita garante que as operacoes de disco (I/O), a logica de processamento de strings, e as camadas de interacao com os modelos generativos fiquem 100% isoladas, facilitando a adicao de novos nos futuramente.
