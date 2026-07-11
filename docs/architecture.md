# Arquitetura do Sistema - CurriculoMatch AI

## 1. Visão Geral
O **CurriculoMatch AI** é um agente de IA baseado na arquitetura de grafos de estado utilizando o **LangGraph**. A aplicação automatiza a triagem de currículos, orquestrando um fluxo de trabalho que extrai informações de um currículo (PDF) e de uma descrição de vaga (TXT), compara os dados utilizando um LLM e gera um relatório estruturado de compatibilidade.

---

## 2. Camadas da Arquitetura

O sistema está estruturado em quatro camadas principais:

### 2.1. Entrada (Input)
Responsável por receber, localizar e validar os arquivos enviados pelo usuário para análise.
- **Arquivos:** `input/curriculo.pdf` e `input/vaga.txt`.
- **Validação:** Checa a existência, extensão e o conteúdo inicial dos arquivos.

### 2.2. Ferramentas (Tools)
Módulos isolados responsáveis pela interação com o sistema de arquivos e extração de dados brutos.
- **PDF Reader:** Abre o arquivo PDF do currículo e extrai o texto puro.
- **Job Reader:** Abre o arquivo de texto da vaga e carrega a descrição.
- **Report Writer:** Cria a pasta de saída (se necessário) e salva o relatório final em formato Markdown.

### 2.3. Agente (Core)
O núcleo inteligente da aplicação, responsável por orquestrar o fluxo de execução definido no LangGraph.
- **Responsabilidades:** 
  - Controlar a transição entre os nós (etapas do fluxo).
  - Gerenciar e atualizar o **Estado (State)** compartilhado.
  - Chamar as ferramentas (Tools) necessárias.
  - Solicitar a extração de dados e a análise preditiva ao modelo de IA (LLM).

### 2.4. Saída (Output)
Responsável pela consolidação e persistência do resultado da análise.
- **Arquivo de Saída:** `output/relatorio.md`

---

## 3. Estado Compartilhado (State)

Todo o contexto da execução é mantido em um estado compartilhado entre os nós do grafo, definido pela estrutura `AgentState`. Isso evita o reprocessamento de dados e garante que cada etapa tenha o contexto completo em memória.

```python
class AgentState(TypedDict):
    curriculum_path: str
    job_path: str
    curriculum_text: str
    job_description: str
    extracted_information: dict
    compatibility_score: int
    analysis: str
    report: str
```

---

## 4. Fluxo de Execução (LangGraph Workflow)

A execução segue um pipeline direcionado e sequencial, onde cada passo é processado como um **Nó (Node)** no grafo:

```text
[ START ]
   ↓
(1) validate_inputs      -> Valida os arquivos de entrada.
   ↓
(2) read_curriculum      -> Utiliza o PDF Reader para extrair o texto do currículo.
   ↓
(3) read_job             -> Utiliza o Job Reader para extrair o texto da vaga.
   ↓
(4) extract_information  -> O LLM extrai dados estruturados da vaga e do currículo.
   ↓
(5) analyze_match        -> O LLM cruza os dados, calcula a compatibilidade e redige a análise.
   ↓
(6) generate_report      -> Formata a análise gerada em um documento Markdown.
   ↓
(7) save_report          -> Utiliza o Report Writer para persistir o relatório em disco.
   ↓
[ END ]
```

---

## 5. Integração com LLM e Prompts

A inteligência do sistema baseia-se em chamadas estruturadas ao modelo de linguagem através do **LangChain**, empregando dois *prompts* principais:

1. **Prompt de Extração:** Converte texto não estruturado (currículo e vaga) em um formato JSON estruturado (contendo nome, habilidades, experiências, formação, idiomas e requisitos).
2. **Prompt de Análise:** Compara o JSON extraído, inferindo o percentual de compatibilidade, identificando pontos fortes/fracos e fornecendo recomendações claras de melhoria.

---

## 6. Tratamento de Erros e Segurança

- **Resiliência do Fluxo:** Se um arquivo for inválido, estiver ausente ou vazio, a execução (o fluxo do grafo) é interrompida no nó correspondente, emitindo uma mensagem descritiva sem quebrar o sistema de forma abrupta.
- **Segurança de Credenciais:** A aplicação utiliza um padrão unificado de credenciais (ex: `LLM_API_KEY`, `LLM_PROVIDER`, `LLM_MODEL_NAME`), sendo gerenciadas estritamente via variáveis de ambiente (`.env`). Essas variáveis abstraem as chaves específicas (como OpenAI ou Grok), evitando que fiquem no código-fonte ou sejam expostas.
