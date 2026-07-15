# CurriculoMatch AI 🚀

## 1. Descrição do Problema
O processo de triagem de currículos é uma das etapas mais demoradas e onerosas para profissionais de Recursos Humanos e Recrutamento Tech. Um recrutador médio passa horas analisando dezenas de PDFs, buscando manualmente as tecnologias e competências exigidas pela vaga. Muitas vezes, bons candidatos são descartados por conta de leitura superficial de projetos (falha humana) ou fadiga.

## 2. Objetivo do Agente
O **CurriculoMatch AI** é um agente autônomo projetado para automatizar essa triagem de forma inteligente e profunda. Ele lê o currículo do candidato e a descrição da vaga, extrai todas as hard skills, softwares, certificações e metodologias descritas no documento, e cruza essas informações para gerar um relatório estruturado. O agente emite um score de aderência, destaca os pontos fortes, identifica gaps e fornece um veredito (Avança/Não Avança).

---

## 3. Arquitetura e Fluxo com LangGraph
A inteligência do agente é orquestrada pelo **LangGraph**, que implementa uma máquina de estados (`StateGraph`). O estado compartilhado (`AgentState`) trafega as informações extraídas entre cada nó.

### Nós de Execução (Nodes) e Fluxo:
1. **Validação (`validate_inputs`)**: Verifica se os arquivos de entrada (PDF e TXT) existem no diretório. Possui uma aresta condicional de *fail-fast* (encerra o fluxo se faltar arquivo).
2. **Leitura de Currículo (`read_curriculum`) e Leitura de Vaga (`read_job`)**: Nós independentes que consomem ferramentas locais para converter os arquivos em strings puras.
3. **Extração (`extract_information`)**: Utiliza LLM (Groq/Llama3) e *Structured Outputs* (Pydantic) para minerar as habilidades do currículo e os requisitos da vaga.
4. **Análise (`analyze_match`)**: Cruza os dados estruturados para identificar o "Match". Esse nó contém *system prompts* com regras estritas contra falsos-negativos (ex: ignorar "Express.js" se a vaga pedir "Express").
5. **Geração e Salvamento (`generate_report` e `save_report`)**: Consolida o *match* em Markdown e aciona a ferramenta de escrita.

---

## 4. Ferramentas Integradas
O agente faz uso de ferramentas externas (*tools* codificadas em Python) para interagir com o ambiente real:
* **`read_pdf` (PyMuPDF)**: Abre o arquivo binário do currículo e extrai o texto preservando a integridade das palavras.
* **`read_txt`**: Ferramenta de sistema de arquivos com *fallback* automático de codificação (UTF-8 e CP1252) para ler a descrição da vaga.
* **`save_report` (`pathlib`)**: Ferramenta de I/O de escrita estruturada que grava a análise do agente na pasta de outputs.

---

## 5. Como Usar (Instruções de Execução)

### 5.1. Pré-requisitos e Instalação
É altamente recomendado o uso de um ambiente virtual:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```
Instale as dependências:
```bash
pip install -r requirements.txt
```

### 5.2. Chave de API
O sistema utiliza a API da Groq (Llama3).
1. Renomeie o arquivo `.env.example` para `.env`
2. Adicione sua chave: `GROQ_API_KEY=sua_chave_aqui`

### 5.3. Executando o Agente
1. Coloque **1 Currículo (PDF)** e **1 Vaga (TXT)** dentro da pasta `input/`. *(Nota: O `.gitignore` protege seus dados sensíveis de irem para o GitHub).*
2. Execute a automação correspondente ao seu sistema operacional:
   - **Windows:** Dê um duplo-clique em `run.bat` (ou execute `.\run.bat` no terminal).
   - **Linux/macOS:** Execute `./run.sh`

---

## 6. Exemplos de Entrada e Saída

### Exemplo de Entrada (Vaga em `.txt`)
```text
Vaga: Desenvolvedor Front-end
Requisitos: 
- Sólidos conhecimentos em React.js e Next.js.
- Experiência em estilização com TailwindCSS.
- Versionamento com Git e GitHub.
```

### Exemplo de Saída (Relatório em `.md`)
```markdown
# Relatório de Aderência Curricular
**Score Final:** 100/100

## Pontos Fortes e Habilidades Identificadas
- React.js: Demonstrado em 2 projetos na experiência profissional.
- Next.js: Experiência comprovada com SEO e SSR.
- TailwindCSS e Git encontrados nas descrições de ferramentas.

## Gaps (Habilidades Faltantes)
- Nenhum gap estrutural encontrado.

## Veredito e Recomendação
**AVANÇA.** O candidato apresenta todos os requisitos fundamentais para a vaga.
```

---

## 7. Principais Decisões Tomadas
* **LLM Groq + Llama 3 70B:** Selecionados devido à baixa latência (velocidade ultrarrápida), crucial para análise de centenas de currículos em produção.
* **Separação Pydantic:** O esquema de extração de dados foi dividido em `habilidades` gerais e `ferramentas_projetos_experiencias` para evitar que a LLM "esquecesse" ferramentas devido a limites de output (token loss) e alucinasse gaps injustos.
* **Early Exit / Fail-Fast:** Implementou-se arestas condicionais no LangGraph para interromper a execução antes de gastar cota da API caso o currículo ou a vaga não estejam na pasta.
* **Regra de Ouro (Anti-Alucinação):** Forçou-se o *system prompt* do avaliador a ser complacente com variações textuais (ex: Node = Node.js).

## 8. Limitações da Solução
* **PDFs como Imagens:** A ferramenta `PyMuPDF` não realiza OCR (Optical Character Recognition). Portanto, currículos exportados como imagens estáticas sem texto indexável não serão lidos adequadamente.
* **Limite de Janela de Contexto:** Embora robusto, currículos exageradamente grandes (mais de 10 páginas) combinados com vagas muito longas podem estourar a janela de contexto de modelos abertos.
* **Falsos-Positivos Linguísticos:** Se um candidato mentir ou listar dezenas de bibliotecas em uma seção de "tags de SEO" no currículo, a IA pode pontuá-lo de forma irrealisticamente positiva.
