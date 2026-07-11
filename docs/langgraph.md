# Fluxo de Execução - LangGraph (langgraph.md)

## 1. Visão Geral

O coração do **CurriculoMatch AI** é orquestrado através de um Grafo de Estado (State Graph) construído com a biblioteca `langgraph`.
O grafo define o ciclo de vida completo do agente, mapeando o roteamento lógico desde o carregamento dos arquivos até a persistência do relatório final. Esta arquitetura baseada em grafos garante modularidade, fácil rastreabilidade e tratamento de erros eficiente.

---

## 2. A Estrutura do Grafo

A execução do sistema é tratada como um fluxo direcional de nós (nodes) interconectados por arestas (edges).

### 2.1. O Estado (State)
Todas as operações no grafo orbitam em torno de um `AgentState`. A cada transição de nó, o nó atual recebe o `State` da execução anterior, realiza suas operações e retorna apenas as chaves do estado que foram atualizadas.

### 2.2. Os Nós (Nodes)
Os nós são funções Python puras (ou instâncias configuradas) que executam uma tarefa específica de domínio de forma isolada.

1. **`validate_inputs_node`**:
   - **Responsabilidade**: Verifica se os arquivos do currículo (`.pdf`) e da vaga (`.txt`) existem nos caminhos fornecidos e se possuem tamanho e extensão válidos.
   - **Mutação no Estado**: Sinaliza se a execução pode continuar ou se ocorreu um erro fatal.

2. **`read_curriculum_node`**:
   - **Responsabilidade**: Aciona a *tool* (ferramenta) de PDF Reader para extrair todo o texto bruto do currículo.
   - **Mutação no Estado**: Atualiza o campo `curriculum_text`.

3. **`read_job_node`**:
   - **Responsabilidade**: Aciona a *tool* de Job Reader para extrair o texto descritivo da vaga.
   - **Mutação no Estado**: Atualiza o campo `job_description`.

4. **`extract_information_node`**:
   - **Responsabilidade**: Envia os textos brutos (vaga e currículo) para a LLM configurada junto com o *Prompt de Extração*, exigindo o retorno em um formato JSON rigoroso (via *Structured Output* do LangChain).
   - **Mutação no Estado**: Atualiza o campo `extracted_information` (Objeto JSON estruturado).

5. **`analyze_match_node`**:
   - **Responsabilidade**: Submete os dados estruturados à LLM com o *Prompt de Análise*. A LLM raciocina sobre os dados, identifica lacunas, pontos fortes e estipula o percentual de aderência.
   - **Mutação no Estado**: Atualiza os campos `compatibility_score` (numérico) e `analysis` (texto descritivo/recomendações).

6. **`generate_report_node`**:
   - **Responsabilidade**: Formata todas as informações coletadas, a pontuação e a análise final em um documento único, aplicando a estilização do Markdown (títulos, listas, negritos).
   - **Mutação no Estado**: Atualiza o campo `report` com a string final formatada.

7. **`save_report_node`**:
   - **Responsabilidade**: Chama a *tool* de Report Writer para salvar o Markdown final no diretório `output/`.
   - **Mutação no Estado**: Nenhuma (Apenas operação de I/O final).

---

## 3. Arestas e Roteamento (Edges)

As arestas definem a direção do fluxo de execução. O sistema utiliza arestas sequenciais simples e roteamento condicional para lidar com resiliência.

### 3.1. Fluxo Principal (Sequencial)
No caminho feliz (sem erros), o grafo flui estritamente na seguinte ordem:
`START` ➔ `validate_inputs` ➔ `read_curriculum` ➔ `read_job` ➔ `extract_information` ➔ `analyze_match` ➔ `generate_report` ➔ `save_report` ➔ `END`

### 3.2. Arestas Condicionais (Conditional Edges)
Decisões lógicas de desvio ou parada ocorrem baseadas no estado atual:

- **Roteamento de Validação (Pós `validate_inputs`)**:
  - `is_valid == True` ➜ Aresta segue para `read_curriculum_node`.
  - `is_valid == False` ➜ Aresta condicional desvia diretamente para `END`, encerrando a execução prematuramente de forma controlada.

- **Roteamento de Resiliência de LLM (Pós `extract_information`)**:
  - Caso a LLM falhe ao devolver um JSON válido, o estado registra a falha. Uma aresta condicional avalia o erro e, se crítico, desvia o fluxo para `END`, impedindo o desperdício de tokens no nó de análise.

---

## 4. Compilação e Execução

A definição do grafo é declarativa. O LangGraph utiliza a classe `StateGraph` associada ao `AgentState` para compilar o fluxo.

```python
# Exemplo conceitual da definição do fluxo na arquitetura:
workflow = StateGraph(AgentState)

# 1. Adição dos Nós
workflow.add_node("validate_inputs", validate_inputs_node)
workflow.add_node("read_curriculum", read_curriculum_node)
# ... outros nós

# 2. Definição do Ponto de Entrada
workflow.set_entry_point("validate_inputs")

# 3. Definição de Arestas e Lógica Condicional
workflow.add_conditional_edges("validate_inputs", check_validation_logic)
workflow.add_edge("read_curriculum", "read_job")
# ... outras arestas sequenciais

# 4. Compilação
app = workflow.compile()
```

Esta separação arquitetural estrita garante que as operações de disco (I/O), a lógica de processamento de strings, e as camadas de interação com os modelos generativos fiquem 100% isoladas, facilitando a adição de novos nós futuramente (ex: um nó de pesquisa no LinkedIn do candidato).
