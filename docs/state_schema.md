# Esquema de Estado e Dados (state_schema.md)

## 1. Visão Geral do Estado (AgentState)

No LangGraph, o estado (`State`) atua como a memória central compartilhada entre todos os nós durante a execução de um grafo. No **CurriculoMatch AI**, utilizamos um `TypedDict` nativo do Python para definir as propriedades que transitam de nó em nó.

```python
from typing import TypedDict, Optional, Dict, Any

class AgentState(TypedDict):
    # Entradas e Validações
    curriculum_path: str
    job_path: str
    is_valid: bool
    error_message: Optional[str]

    # Dados Brutos Extraídos
    curriculum_text: str
    job_description: str

    # Dados Estruturados (Saída da LLM na etapa de Extração)
    extracted_information: Dict[str, Any]

    # Resultados Finais da Análise
    compatibility_score: int
    analysis: str
    
    # Saída Final
    report: str
```

### 1.1. Descrição dos Atributos
- **`curriculum_path` / `job_path`**: Caminhos para os arquivos de entrada (`.pdf` e `.txt`).
- **`is_valid`**: Flag booleana definida no nó de validação. Se `False`, o roteamento condicional interrompe o fluxo para `END`.
- **`error_message`**: Armazena mensagens de erro caso a execução falhe (ex: "Arquivo não encontrado", "Falha de parser da LLM").
- **`curriculum_text` / `job_description`**: Strings brutas contendo todo o conteúdo bruto dos arquivos lidos pelo *PDF Reader* e *Job Reader*.
- **`extracted_information`**: O dicionário mais importante do fluxo. Ele abriga a saída estruturada (JSON) formatada pelo modelo de linguagem baseada nos esquemas Pydantic.
- **`compatibility_score`**: Número inteiro (0-100) refletindo a pontuação calculada pelo agente de análise cruzada.
- **`analysis`**: O raciocínio lógico gerado pela LLM em formato de texto, justificando a nota, destacando pontos fortes, fracos e sugerindo melhorias.
- **`report`**: A consolidação final de todas as variáveis acima formatadas em um elegante arquivo Markdown.

---

## 2. Modelos de Extração (Pydantic Schemas)

Para garantir que a LLM extraia os dados de forma determinística e consistente no nó de extração (`extract_information_node`), o LangChain utiliza o conceito de **Structured Output** forçando o LLM a aderir estritamente aos esquemas definidos pelo **Pydantic**. 

O atributo `extracted_information` no `AgentState` reflete a versão em dicionário serializada do modelo Pydantic mestre abaixo:

### 2.1. Modelo do Currículo (`CurriculumData`)
```python
from pydantic import BaseModel, Field
from typing import List

class CurriculumData(BaseModel):
    nome: str = Field(description="Nome completo do candidato")
    email: str = Field(description="Endereço de e-mail do candidato")
    telefone: str = Field(description="Telefone de contato do candidato")
    habilidades: List[str] = Field(description="Lista de habilidades técnicas e ferramentas")
    experiencias: List[str] = Field(description="Resumo dos cargos e empresas em que o candidato já trabalhou")
    formacao: str = Field(description="Nível acadêmico, graduações ou cursos listados")
    idiomas: List[str] = Field(description="Idiomas mencionados e seu respectivo nível de fluência")
```

### 2.2. Modelo da Vaga (`JobData`)
```python
class JobData(BaseModel):
    cargo: str = Field(description="Nome ou título da vaga anunciada")
    tecnologias: List[str] = Field(description="Linguagens de programação, frameworks e tecnologias exigidas")
    requisitos: List[str] = Field(description="Requisitos técnicos e comportamentais obrigatórios")
    diferenciais: List[str] = Field(description="Conhecimentos extras que contam como diferencial (Nice-to-have)")
```

### 2.3. O Schema Consolidado (`ExtractedInformation`)
A LLM é instruída a retornar esse objeto unificado, analisando os textos brutos do currículo e da vaga simultaneamente para garantir que ambos tenham os mesmos critérios extraídos de forma limpa.

```python
class ExtractedInformation(BaseModel):
    candidato: CurriculumData
    vaga: JobData
```

---

## 3. Dinâmica do Estado no Grafo

1. **Atualização Parcial**: No design do LangGraph, um nó só precisa retornar o dicionário com as **chaves que ele quer atualizar ou inserir**. O motor interno do LangGraph mescla essas chaves de volta no estado global.
2. **Persistência**: Graças à utilização de `TypedDict` e tipos built-in/Pydantic, esse modelo de estado permite que futuramente o projeto possua memória transacional acoplando ao estado um banco SQLite. Isso permite auditar e depurar o momento exato em que a IA cometeu um erro (funcionalidade de *Time Travel* do LangGraph).
