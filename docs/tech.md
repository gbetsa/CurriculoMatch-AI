# Tech.md

# Documento Técnico

## Projeto

**CurriculoMatch AI**

---

# Objetivo

Desenvolver um agente de IA utilizando **Python** e **LangGraph** para realizar a triagem inicial de currículos, comparando um currículo em PDF com uma descrição de vaga e gerando um relatório de compatibilidade.

---

# Stack

## Linguagem

* Python 3.12+

## Frameworks

* LangGraph
* LangChain

## Modelo de IA

* Agnóstico / Adaptativo (Suporta qualquer LLM compatível com LangChain, como OpenAI, Grok, Anthropic, Llama, configurável por variável de ambiente)

## Bibliotecas

* langgraph
* langchain
* Pacotes de provedor conforme necessidade (ex: langchain-openai, langchain-xai, langchain-anthropic)
* python-dotenv
* pydantic
* pymupdf (fitz)
* pathlib

---

# Estrutura do Projeto

```text
curriculomatch-ai/

├── graph/
│   ├── state.py
│   ├── nodes.py
│   └── workflow.py
│
├── tools/
│   ├── pdf_reader.py
│   ├── job_reader.py
│   └── report_writer.py
│
├── prompts/
│   ├── analyze_prompt.py
│   └── extract_prompt.py
│
├── input/
│   ├── curriculo.pdf
│   └── vaga.txt
│
├── output/
│   └── relatorio.md
│
├── main.py
├── README.md
├── requirements.txt
├── .env
└── .env.example
```

---

# Arquitetura

O projeto será dividido em quatro camadas.

## 1. Entrada

Responsável por localizar e validar os arquivos enviados pelo usuário.

Entrada:

* input/curriculo.pdf
* input/vaga.txt

---

## 2. Ferramentas (Tools)

Ferramentas responsáveis por acessar arquivos.

### PDF Reader

Responsabilidades:

* abrir PDF
* extrair texto
* retornar string

---

### Job Reader

Responsabilidades:

* abrir vaga.txt
* retornar texto

---

### Report Writer

Responsabilidades:

* criar pasta output se necessário
* salvar relatório em Markdown

---

## 3. Agente

Responsável por:

* controlar o fluxo
* armazenar contexto
* chamar ferramentas
* solicitar análise ao modelo
* gerar resposta final

---

## 4. Saída

Arquivo:

```text
output/relatorio.md
```

---

# Fluxo do LangGraph

```text
START

↓

validate_inputs

↓

read_curriculum

↓

read_job

↓

extract_information

↓

analyze_match

↓

generate_report

↓

save_report

↓

END
```

---

# State

Todo o contexto será compartilhado através do State do LangGraph.

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

Cada nó poderá ler e atualizar essas informações.

---

# Nós

## validate_inputs

Responsável por:

* verificar existência dos arquivos
* validar extensão
* validar conteúdo

Entrada:

* caminho dos arquivos

Saída:

* state atualizado

---

## read_curriculum

Utiliza:

PDF Reader

Responsável por:

* extrair texto do currículo

Atualiza:

```text
curriculum_text
```

---

## read_job

Utiliza:

Job Reader

Atualiza:

```text
job_description
```

---

## extract_information

Responsável por identificar:

Currículo:

* nome
* email
* telefone
* habilidades
* formação
* experiências
* idiomas

Vaga:

* cargo
* tecnologias
* requisitos
* diferenciais

Atualiza:

```text
extracted_information
```

---

## analyze_match

Responsável por:

* comparar currículo e vaga
* calcular compatibilidade
* produzir análise

Atualiza:

```text
compatibility_score

analysis
```

---

## generate_report

Responsável por montar o relatório final em Markdown.

Atualiza:

```text
report
```

---

## save_report

Utiliza:

Report Writer

Responsável por salvar o relatório.

---

# Ferramentas

## PDF Reader

Entrada

```text
input/curriculo.pdf
```

Saída

```python
str
```

---

## Job Reader

Entrada

```text
input/vaga.txt
```

Saída

```python
str
```

---

## Report Writer

Entrada

```python
str
```

Saída

```text
output/relatorio.md
```

---

# Prompts

O projeto utilizará dois prompts principais.

## Prompt de Extração

Objetivo:

Extrair informações estruturadas do currículo e da vaga.

Saída esperada:

```json
{
  "nome": "",
  "habilidades": [],
  "experiencias": [],
  "formacao": "",
  "idiomas": [],
  "requisitos": []
}
```

---

## Prompt de Análise

Objetivo:

Comparar currículo e vaga.

O modelo deverá gerar:

* resumo
* compatibilidade
* pontos fortes
* pontos de melhoria
* recomendações

---

# Tratamento de Erros

O agente deverá tratar:

* currículo inexistente
* vaga inexistente
* PDF vazio
* vaga vazia
* erro na leitura do PDF
* erro ao salvar relatório

Em caso de erro, a execução será interrompida com uma mensagem descritiva.

---

# Segurança

* Utilizar `.env` para armazenar as credenciais de forma genérica (ex: `LLM_API_KEY`, `LLM_PROVIDER`).
* Nunca versionar `.env`.
* Disponibilizar apenas `.env.example`.
* Validar entradas antes do processamento.

---

# Dependências

```text
langgraph
langchain
langchain-openai (ou pacote do provedor escolhido)
python-dotenv
pymupdf
pydantic
```

---

# Execução

Instalar dependências:

```bash
pip install -r requirements.txt
```

Adicionar:

```text
input/curriculo.pdf
input/vaga.txt
```

Executar:

```bash
python main.py
```

O relatório será gerado automaticamente em:

```text
output/relatorio.md
```

---

# Próximas Evoluções

* Suporte a múltiplos currículos.
* Comparação entre candidatos.
* Interface web com Streamlit.
* Exportação em PDF.
* Histórico de análises.
* Ranking de candidatos.
* Integração com APIs de recrutamento.
