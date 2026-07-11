# Ferramentas do Agente (tools.md)

## 1. Visão Geral

No ecossistema do LangGraph e LangChain, **Tools (Ferramentas)** são componentes isolados de código que o agente (ou os nós do grafo) utiliza para interagir com recursos externos ao código (neste caso, o sistema de arquivos local). 

No **CurriculoMatch AI**, as lógicas de leitura e escrita são encapsuladas em arquivos separados dentro da pasta `tools/`. Isso garante que a lógica principal não fique acoplada à leitura de arquivos, facilitando a manutenção futura (ex: substituir o leitor de PDF local por uma API de OCR na nuvem, sem quebrar o grafo).

---

## 2. Detalhamento das Ferramentas

### 2.1. PDF Reader (`tools/pdf_reader.py`)

Responsável por extrair o conteúdo textual dos currículos anexados.

- **Dependência Principal**: `pymupdf` (importado no código como `fitz`). É escolhida por ser uma das bibliotecas mais rápidas e consistentes para extração de texto em Python.
- **Entrada (Input)**: `file_path: str` (O caminho para o arquivo do currículo).
- **Saída (Output)**: `str` (String crua contendo o texto extraído de todas as páginas concatenado).
- **Tratamento de Exceções e Edge-cases**:
  - Captura `FileNotFoundError` (caminho incorreto).
  - Lida com PDFs corrompidos.
  - Retorna avisos caso o PDF seja baseado unicamente em imagens escaneadas (sem camada de texto). Nessas situações, a ferramenta retorna uma mensagem de erro controlada para que o grafo interrompa a execução graciosamente.

### 2.2. Job Reader (`tools/job_reader.py`)

Responsável por carregar o documento que descreve os requisitos da vaga.

- **Dependência Principal**: Bibliotecas nativas do Python (`open()`).
- **Entrada (Input)**: `file_path: str` (O caminho para o arquivo `.txt` da vaga).
- **Saída (Output)**: `str` (Texto limpo da vaga).
- **Tratamento de Exceções**:
  - Lida primariamente com *Encoding*. Deve forçar a leitura utilizando `utf-8` ou detectar o *charset* (ex: caso seja salvo no Bloco de Notas do Windows como ANSI/cp1252) para evitar problemas de caracteres quebrando palavras acentuadas (essencial para o idioma Português).

### 2.3. Report Writer (`tools/report_writer.py`)

Responsável pela materialização da resposta gerada pela LLM em um documento palpável para o usuário final.

- **Dependência Principal**: `pathlib` para manipulação segura de caminhos e diretórios cross-platform (Windows/Linux/Mac).
- **Entrada (Input)**: 
  - `content: str`: O texto formatado em Markdown gerado pelo nó do grafo.
  - `output_path: str` (Opcional, com padrão apontando para `output/relatorio.md`).
- **Saída (Output)**: Não possui (ou retorna um `bool` de sucesso para o nó pai).
- **Fluxo Operacional**:
  1. Utiliza `pathlib.Path` para checar se o diretório alvo (`output/`) existe.
  2. Cria o diretório via `.mkdir(parents=True, exist_ok=True)` caso esteja ausente.
  3. Abre o arquivo final e escreve o conteúdo em `utf-8`.

---

## 3. Injeção Determinística vs. LLM-Calling

Uma nota importante sobre o design arquitetural: embora o LangChain possua decoradores como `@tool` que permitem que a LLM decida autônoma e dinamicamente quando invocar uma ferramenta (via *Function Calling*), o **CurriculoMatch AI** opta por **não utilizar Function Calling de ferramentas dinâmico**.

**Motivo:** Como o fluxo (Ler CV -> Ler Vaga -> Analisar) é invariável e imutável, as ferramentas são injetadas **deterministicamente** dentro da lógica procedural dos *Nodes* (Nós).

Isso resulta em:
1. Maior velocidade de execução (zero overhead da IA ter que deduzir que precisa invocar uma ferramenta).
2. Menor custo de tokens.
3. Tratamento de exceções absoluto, sem risco de *alucinação* da LLM invocando arquivos incorretos.
