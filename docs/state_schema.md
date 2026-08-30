# Esquema de Estado e Dados (state_schema.md)

## 1. Visao Geral do Estado (AgentState)

No LangGraph, o estado (`State`) atua como a memoria central compartilhada entre todos os nos durante a execucao de um grafo. No **CurriculoMatch AI**, utilizamos um `TypedDict` nativo do Python para definir as propriedades que transitam de no em no.

**Evolucao do Mini-Projeto:** O `AgentState` original foi expandido com campos para historico, aprovacao humana, observabilidade e metadata.

```python
from typing import TypedDict, Optional, Dict, Any, List
from pydantic import BaseModel, Field

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
    history: List[Dict[str, Any]]       # Historico de analises anteriores (do checkpointer)
    approval_required: bool             # Gate de aprovacao humana
    approval_decision: Optional[str]    # "approved" | "rejected"
    correlation_id: str                 # ID unico para observabilidade
    metadata: Dict[str, Any]           # Latencia, tokens, versoes do modelo
```

### 1.1. Descricao dos Atributos Originais
- **`curriculum_path` / `job_path`**: Caminhos para os arquivos de entrada (`.pdf` e `.txt`).
- **`is_valid`**: Flag booleana definida no no de validacao. Se `False`, o roteamento condicional interrompe o fluxo para `END`.
- **`error_message`**: Armazena mensagens de erro caso a execucao falhe (ex: "Arquivo nao encontrado", "Falha de parser da LLM").
- **`curriculum_text` / `job_description`**: Strings brutas contendo todo o conteudo bruto dos arquivos lidos pelo *PDF Reader* e *Job Reader*.
- **`extracted_information`**: O dicionario mais importante do fluxo. Ele abriga a saida estruturada (JSON) formatada pelo modelo de linguagem baseada nos esquemas Pydantic.
- **`compatibility_score`**: Numero inteiro (0-100) refletindo a pontuacao calculada pelo agente de analise cruzada.
- **`analysis`**: O raciocinio logico gerado pela LLM em formato de texto, justificando a nota, destacando pontos fortes, fracos e sugerindo melhorias.
- **`report`**: A consolidacao final de todas as variaveis acima formatadas em um elegante arquivo Markdown.

### 1.2. Descricao dos Atributos Novos (Projeto Final)
- **`history`**: Lista de analises anteriores recuperada do PostgreSQL via checkpointer. Permite comparar candidatos e verificar evolucao.
- **`approval_required`**: Flag que indica se a execucao deve pausar para aprovacao humana antes de salvar.
- **`approval_decision`**: Decisao do usuario: `"approved"` (salva) ou `"rejected"` (cancela).
- **`correlation_id`**: UUID unico gerado no inicio da execucao, propagado em todos os logs e traces para correlacao.
- **`metadata`**: Dicionario com metricas da execucao: latencia por no, tokens utilizados, modelo utilizado, versoes.

---

## 2. Modelos de Extracao (Pydantic Schemas)

Para garantir que a LLM extraia os dados de forma deterministica e consistente no no de extracao (`extract_information_node`), o LangChain utiliza o conceito de **Structured Output** forcando o LLM a aderir estritamente aos esquemas definidos pelo **Pydantic**.

O atributo `extracted_information` no `AgentState` reflete a versao em dicionario serializada do modelo Pydantic mestre abaixo:

### 2.1. Modelo do Curriculo (`CurriculumData`)
```python
from pydantic import BaseModel, Field
from typing import List

class CurriculumData(BaseModel):
    nome: str = Field(description="Nome completo do candidato")
    email: str = Field(description="Endereco de e-mail do candidato")
    telefone: str = Field(description="Telefone de contato do candidato")
    habilidades: List[str] = Field(
        description="Lista de TODAS as hard skills, competencias, softwares e linguagens listadas explicitamente nas secoes de 'Habilidades', 'Stacks' ou 'Skills'."
    )
    ferramentas_projetos_experiencias: List[str] = Field(
        default_factory=list,
        description="Lista exaustiva de TODAS as tecnologias, bibliotecas (ex: Vite, Express), ORMs (ex: Sequelize) e ferramentas citadas DENTRO dos textos descritivos das Experiencias e Projetos Realizados.",
    )
    experiencias: List[str] = Field(
        description="Lista detalhada de cargos, empresas, atividades e PROJETOS, mantendo as tecnologias e ferramentas citadas no texto original."
    )
    formacao: str = Field(description="Nivel academico, graduacoes ou cursos listados")
    idiomas: List[str] = Field(
        description="Idiomas mencionados e seu respectivo nivel de fluencia"
    )
```

### 2.2. Modelo da Vaga (`JobData`)
```python
class JobData(BaseModel):
    cargo: str = Field(description="Nome ou titulo da vaga anunciada")
    tecnologias: List[str] = Field(
        description="Linguagens de programacao, frameworks e tecnologias exigidas"
    )
    requisitos: List[str] = Field(
        description="Requisitos tecnicos e comportamentais obrigatorios"
    )
    diferenciais: List[str] = Field(
        description="Conhecimentos extras que contam como diferencial (Nice-to-have)"
    )
```

### 2.3. O Schema Consolidado (`ExtractedInformation`)
A LLM e instruida a retornar esse objeto unificado, analisando os textos brutos do curriculo e da vaga simultaneamente para garantir que ambos tenham os mesmos criterios extraidos de forma limpa.

```python
class ExtractedInformation(BaseModel):
    candidato: CurriculumData
    vaga: JobData
```

---

## 3. Modelos de Resposta da API (Pydantic Schemas)

### 3.1. Request de Analise
```python
from pydantic import BaseModel, Field
from fastapi import UploadFile

class AnalyzeRequest(BaseModel):
    job_title: str = Field(..., min_length=3, max_length=200)
    job_description: str = Field(..., min_length=20, max_length=10000)
```

### 3.2. Response de Analise
```python
class AnalyzeResponse(BaseModel):
    analysis_id: str
    candidate_name: str
    job_title: str
    score: int
    report: str
    status: str  # "completed" | "pending_approval" | "error"
    created_at: str
```

### 3.3. Response de Historico
```python
class HistoryItem(BaseModel):
    analysis_id: str
    candidate_name: str
    job_title: str
    score: int
    created_at: str

class HistoryResponse(BaseModel):
    items: List[HistoryItem]
    total: int
    page: int
    pages: int
```

---

## 4. Modelo de Historico (AnalysisRecord)

```python
class AnalysisRecord(BaseModel):
    analysis_id: str
    candidate_name: str
    job_title: str
    score: int
    report: str
    created_at: str
    correlation_id: str
```

---

## 5. Dinamica do Estado no Grafo

1. **Atualizacao Parcial**: No design do LangGraph, um no so precisa retornar o dicionario com as **chaves que ele quer atualizar ou inserir**. O motor interno do LangGraph mescla essas chaves de volta no estado global.
2. **Persistencia**: Graças a utilizacao de `TypedDict` e tipos built-in/Pydantic, esse modelo de estado permite que o projeto possua memoria transacional acoplando ao estado um banco PostgreSQL. Isso permite auditar e depurar o momento exato em que a IA cometeu um erro (funcionalidade de *Time Travel* do LangGraph).
3. **Observabilidade**: O campo `correlation_id` e propagado em todos os logs e traces, permitindo reconstruir execucoes completas a partir de um ID unico.
