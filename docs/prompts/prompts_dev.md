# Registro de Interações (Prompts) - CurriculoMatch AI

Este documento registra as interações (entradas do usuário e saídas da IA) durante o desenvolvimento do projeto.

---

### Planejamento - Elaboração do Plano de Tasks
**Data:** 15 de Julho de 2026, 14:38

**Objetivo:**
Analisar a documentação (steerings em /docs) e gerar um plano de tarefas organizado em blocos para a construção do projeto.

**Prompt Utilizado (Entrada do Usuário):**
> "Com base nas steerings em /docs, elabore um plano de task para iniciarmos o projeto, as task devem ser separadas em blocos, desde a instalação de dependecias, ambiente virtual e finalização do projeto."

**Padrão de Prompting:** Zero-shot / Task-oriented
> Forneceu um contexto direto e um comando claro (elaborar plano de task dividido em blocos) sem necessidade de exemplos, direcionando a IA para analisar o diretório e estruturar o plano.

**Resultado e Ação (Saída da IA):**
Foi lida a documentação técnica (product.md, tech.md, architecture.md, state_schema.md, etc.) e elaborado o artefato de *Plano de Implementação*, dividindo o desenvolvimento em 8 Blocos lógicos e estruturados.

---

### Planejamento - Criação de Specs e GitHub Kanban
**Data:** 15 de Julho de 2026, 14:42

**Objetivo:**
Definir o modelo Groq, criar um checklist em Markdown das tasks e gerar as especificações (specs) para registrar como Issues no GitHub.

**Prompt Utilizado (Entrada do Usuário):**
> "Escolha do Provedor de LLM: Inicialmente, vamos começar com a LLM do groq, mas o projeto deve ser adaptaivo para qualquer LLM. A adição do PDF e .txt da vaga, sera feita depois, para o teste do projeto, gere um arquivo com essas task para seguirmos e adicione na pasta /docs"
>
> *(Ação adicional)*: "Antes de inciarmos de fato, vamos organizar melhor esse projeto, em /docs as task devem ser detalhadas e estar dentro de /specs. Com esses detalhes, vamos criar Issues no github para o quadro kanben."

**Padrão de Prompting:** Few-shot iterativo / Clarification
> O usuário iterou sobre as perguntas abertas do plano, respondendo às dúvidas, refinando as regras de aceitação e adicionando uma restrição arquitetural nova (criação de arquivos na pasta specs e integração com GH CLI).

**Resultado e Ação (Saída da IA):**
- Foi criado o arquivo `/docs/tasks.md` contendo um checklist resumido.
- A estrutura de diretório `/docs/specs/` foi criada e populada com 8 arquivos Markdown detalhando os requisitos e critérios de aceite para os Blocos 1 a 8.
- Utilizou-se o `gh` (GitHub CLI) para disparar a criação automática de 8 Issues diretamente no repositório.

---

### Documentação - Registro Histórico de Interações
**Data:** 15 de Julho de 2026, 14:47

**Objetivo:**
Criar/atualizar o arquivo de registro cronológico (prompts_dev.md) com as entradas e saídas da conversa entre o usuário e a IA.

**Prompt Utilizado (Entrada do Usuário):**
> "Adicione em /docs/prompts o registro de nossa interação, com a entrada e saida da conversa"
> *(Correção)*: "Cada resgistro deve ter o padrão de prompt utilizado como esta definido em /docs/prompts.md"

**Padrão de Prompting:** Constraint-based / Zero-shot
> O usuário especificou um requisito estrito para a saída da IA: aderir rigidamente a um template contido em um arquivo de documentação pré-existente (`/docs/prompts.md`).

**Resultado e Ação (Saída da IA):**
Atualização do arquivo `/docs/prompts/prompts_dev.md` aplicando o template obrigatório para todas as interações anteriores e a atual.

---

### Implementação - Configuração do Ambiente e Diretórios (Bloco 1)
**Data:** 15 de Julho de 2026, 14:55

**Objetivo:**
Iniciar a execução das especificações do Bloco 1 (01_setup.md), criar uma nova branch seguindo o GitFlow, atualizar o status da tarefa no Kanban para "In Progress", e prosseguir até a conclusão (commit, PR e fechamento da issue).

**Prompt Utilizado (Entrada do Usuário):**
> "Proximo passo deve ser iniciarmos a specs 01_setup.md. Para isso inicie uma nova branch com base no arquivo gitflow.md. Na quadro kanban a task deve ser gerenciada por colunas, no momento estamos em "Backlog", mas temos "Ready", "In Progress", "In Review" e "Done"."

**Padrão de Prompting:** Workflow / Process-oriented
> Instruiu a IA a seguir um fluxo de trabalho específico estabelecido em documentos paralelos (`gitflow.md` e regras de integração com GitHub Projects), definindo não apenas o código a ser gerado, mas o processo operacional e de versionamento.

**Resultado e Ação (Saída da IA):**
- Verificado status do Git e feito checkout para `develop`.
- Criada a branch `feature/01-setup`.
- Item do projeto atualizado para a coluna "In progress" usando a CLI.
- Criados ambiente virtual, arquivos (`requirements.txt`, `.env.example`) e diretórios vazios estruturais (`input`, `output`, `graph`, `tools`, `prompts`) com marcadores `.gitkeep`.
- As alterações foram commitadas seguindo o Conventional Commits, o Pull Request foi aberto para a branch `develop`, e a Issue #1 foi devidamente atualizada com um comentário detalhado (asignada para `gbetsa`) e então concluída.

---

### Workflow - Regra de Documentação Rígida em Commits e PRs
**Data:** 15 de Julho de 2026, 15:00

**Objetivo:**
Melhorar a qualidade da documentação do versionamento. O usuário apontou que as mensagens de commit e o corpo dos Pull Requests estavam excessivamente simplistas.

**Prompt Utilizado (Entrada do Usuário):**
> "Ótimo, apenas uma coisa devemos melhorar no fluxo. Commit 5a4d54a [...] O commit e PR ficou muito simples, tudo que desenvolvido, deve estar documentado de forma rigida."

**Padrão de Prompting:** Feedback / Constraint-based
> O usuário forneceu um feedback corretivo sobre uma saída anterior, impondo uma nova restrição (constraint) de qualidade que deve ser aplicada a todas as futuras interações do GitFlow.

**Resultado e Ação (Saída da IA):**
- A restrição foi assimilada. A partir do Bloco 2, todos os commits conterão corpo estendido e detalhado.
- Os Pull Requests passarão a incluir o detalhamento técnico profundo de tudo que foi implementado, os arquivos tocados e os critérios de aceite cumpridos.
- Este registro foi adicionado ao log de prompts (`prompts_dev.md`).

---

### Implementação - Ferramentas de Leitura/Escrita e CI/CD (Bloco 2)
**Data:** 15 de Julho de 2026, 15:08

**Objetivo:**
Executar o Bloco 2 criando as ferramentas (Tools) para leitura de PDFs e TXTs, gravação do relatório, e adicionar e testar localmente o pipeline de CI/CD (GitHub Actions).

**Prompt Utilizado (Entrada do Usuário):**
> "Pode seguir com o plano"

**Padrão de Prompting:** Approval / Delegation
> O usuário ratificou o plano gerado autonomamente pela IA para configurar CI/CD e regras de proteção antes de prosseguirmos.

**Resultado e Ação (Saída da IA):**
- Criado `tools/pdf_reader.py` usando `pymupdf`.
- Criado `tools/job_reader.py` com suporte robusto a fallback de encoding (UTF-8 e CP1252).
- Criado `tools/report_writer.py` usando `pathlib`.
- Configurado o workflow de Actions em `.github/workflows/ci.yml`.
- Executado formatador `black` no código.
- Feita tentativa de configurar proteção de branch (`gh api`), recebendo aviso (403) de que a conta free para repo privado não suporta Proteção de Branch obrigatória via settings, no entanto, o Action funcionará.
- Feito o Push e aberto o PR #10 (com descrições rigorosas, obedecendo o feedback da iteração anterior) e Issue #2 fechada.

---

### Bugfix - Atualização de Versões do GitHub Actions
**Data:** 15 de Julho de 2026, 15:13

**Objetivo:**
Corrigir alertas de depreciação do Node.js 20 reportados pela pipeline de CI/CD.

**Prompt Utilizado (Entrada do Usuário):**
> "Annotations 1 warning Complete job Node.js 20 is deprecated. The following actions target Node.js 20 but are being forced to run on Node.js 24: actions/checkout@v3, actions/setup-python@v4. [...] A pipeline esta retornando esse aviso"

**Padrão de Prompting:** Troubleshooting / Error-driven
> O usuário forneceu a saída direta do console/pipeline de CI/CD contendo o aviso de depreciação. O padrão orienta a IA a diagnosticar o warning provido (ferramentas e ecossistema Github Actions) e resolver o aviso atualizando as dependências.

**Resultado e Ação (Saída da IA):**
- Modificou o arquivo `.github/workflows/ci.yml`.
- Atualizou `actions/checkout@v3` para `@v4`.
- Atualizou `actions/setup-python@v4` para `@v5`.
- Realizou o commit da correção (bugfix) na branch atual (`feature/02-tools`) e fez o push para o repositório remoto para atualização do PR e do workflow online.

---

### Implementação - Estado Compartilhado e Esquemas (Bloco 3)
**Data:** 15 de Julho de 2026, 15:17

**Objetivo:**
Executar as especificações do Bloco 3, implementando a memória compartilhada do agente (`AgentState`) e os esquemas Pydantic que serão usados para forçar uma saída estruturada da LLM.

**Prompt Utilizado (Entrada do Usuário):**
> "Podemos seguir para Issue #3 (Bloco 3: Estado Compartilhado e Esquemas Pydantic), porem a pipeline ainda esta retornando um aviso: Cleaning up orphan processes Warning: Node.js 20 is deprecated. The following actions target Node.js 20 but are being forced to run on Node.js 24: actions/checkout@v4, actions/setup-python@v5."

**Padrão de Prompting:** Delegation / Status Report
> O usuário relatou o warning (agora restrito à infraestrutura nativa do Actions V4/V5 e Node 24) e autorizou a progressão para a próxima etapa (Bloco 3). A IA interpretou a autorização e lidou com a execução do código de infraestrutura de dados da aplicação.

**Resultado e Ação (Saída da IA):**
- Criada a branch `feature/03-state` a partir de `develop`.
- Implementado o arquivo `graph/state.py` com o `AgentState` e as classes Pydantic (`CurriculumData`, `JobData`, `ExtractedInformation`) detalhadas com o atributo `Field` de `description` fundamental para as ferramentas/JSON mode das LLMs.
- Formatado e lintado sem erros via Black/Flake8.
- Realizado o commit seguindo estritamente as regras de documentação e aberto o Pull Request detalhado (#11) vinculado à Issue #3 (atualizando status no Kanban).

---

### Implementação - Criação dos Prompts (Bloco 4)
**Data:** 15 de Julho de 2026, 15:23

**Objetivo:**
Executar as especificações do Bloco 4 implementando a engenharia de prompts da aplicação usando `ChatPromptTemplate` do LangChain.

**Prompt Utilizado (Entrada do Usuário):**
> "Vamos iniciar o Bloco 4 (Criação dos Prompts)"

**Padrão de Prompting:** Delegation / Workflow progression
> O usuário ditou explicitamente o fluxo (avanço sequencial de blocos). A IA acata o comando e avança na ramificação (GitFlow) e Kanban aplicando os requisitos da especificação pré-planejada.

**Resultado e Ação (Saída da IA):**
- Criado e feito checkout na branch `feature/04-prompts`.
- Criado `prompts/extract_prompt.py` instruindo a IA a preencher todos os campos do schema JSON com base apenas no texto fornecido, evitando alucinações de parâmetros.
- Criado `prompts/analyze_prompt.py` instruindo a IA a cruzar os dados, gerar score de aderência, gaps e recomendações em Markdown padronizado.
- Ferramentas de CI locais (Black e Flake8) utilizadas para garantia de formato.
- Atualizado log, aberto PR detalhado (#12) para a branch `develop`, movida a Issue #4 para a coluna de finalizada (Closed).

---

### Implementação - Nós de Execução / Nodes (Bloco 5)
**Data:** 15 de Julho de 2026, 15:27

**Objetivo:**
Executar as especificações do Bloco 5, orquestrando as "ferramentas" criadas nos blocos 2, 3 e 4 dentro de funções Python robustas que serão usadas como os Nós (Nodes) da máquina de estados do LangGraph.

**Prompt Utilizado (Entrada do Usuário):**
> "Vamos para a proxima etapa: Bloco 5 (Nós de Execução - Nodes). validate_inputs, read_curriculum, read_job, extract_information, analyze_match, generate_report, save_report"

**Padrão de Prompting:** Task Execution / Delegation
> O usuário autorizou o avanço do Workflow citando nominalmente as responsabilidades estabelecidas nas Specs do projeto para a IA seguir.

**Resultado e Ação (Saída da IA):**
- Criada e feito checkout na branch `feature/05-nodes` a partir de `develop`.
- Implementado arquivo `graph/nodes.py`.
- Instanciado `ChatGroq` e integrado `with_structured_output(ExtractedInformation)`.
- Escritas 7 funções de processamento (`validate_inputs`, `read_curriculum_node`, `read_job_node`, `extract_information`, `analyze_match`, `generate_report`, `save_report_node`) gerenciando a leitura e salvamento do AgentState e tratamento estrito de exceções (try/except).
- Código formatado via Black/Flake8. PR #13 aberto e Issue #5 marcada como completa.

---

### Implementação - Orquestração / Workflow (Bloco 6)
**Data:** 15 de Julho de 2026, 15:36

**Objetivo:**
Implementar o grafo de estados do LangGraph (`StateGraph`) conectando todos os nós por arestas sequenciais e condicionais, garantindo um fluxo de execução robusto com tratamento de falhas em cada etapa.

**Prompt Utilizado (Entrada do Usuário):**
> "Vamos para o Bloco 6 (Orquestração - Workflow) compilar tudo isso usando as arestas (Edges) e regras condicionais do StateGraph"

**Padrão de Prompting:** Task Execution / Delegation
> O usuário autorizou o avanço para a etapa de orquestração, citando os componentes técnicos-chave (Edges, condicionais, StateGraph) presentes na especificação `06_workflow.md`.

**Resultado e Ação (Saída da IA):**
- Criada branch `feature/06-workflow` a partir de `develop`.
- Implementado `graph/workflow.py` com a função `build_graph()` instanciando o `StateGraph(AgentState)`.
- Registrados os 7 nós de execução no grafo.
- Adicionada aresta condicional `route_after_validation` com lógica de *fail-fast*: encerra o grafo em `END` imediatamente se `validate_inputs` detectar arquivos inválidos.
- Adicionadas arestas condicionais `route_after_read` após `read_curriculum` e `read_job` para prevenir que falhas silenciosas de I/O cheguem aos nós de LLM.
- Configurado fluxo sequencial: `extract_information → analyze_match → generate_report → save_report → END`.
- Grafo compilado e exportado como instância de módulo (`app = build_graph()`).
- Código formatado via Black/Flake8. PR #14 aberto com diagrama ASCII do fluxo. Issue #6 fechada.

---

### Workflow - Registro de Entrada e Saída Ausente (Bloco 6 - Correção)
**Data:** 15 de Julho de 2026, 15:38

**Objetivo:**
Corrigir a omissão do registro de interação do Bloco 6 no arquivo de log histórico `prompts_dev.md`.

**Prompt Utilizado (Entrada do Usuário):**
> "Faltou uma coisa, o registro de entrada e saida no /docs/prompts/prompts_dev.md"

**Padrão de Prompting:** Feedback / Constraint Enforcement
> O usuário identificou uma falha no processo de documentação e exigiu que o registro fosse retrospectivamente adicionado, reforçando que a atualização do log de interações é uma etapa obrigatória após cada bloco.

**Resultado e Ação (Saída da IA):**
- Verificado o arquivo `prompts_dev.md` e confirmada a ausência do registro do Bloco 6.
- Adicionados dois registros: a interação principal do Bloco 6 e esta correção.
- Commit atualizado na branch `feature/06-workflow` com o arquivo de log corrigido.

---

### Implementação - Ponto de Entrada / Entrypoint (Bloco 7)
**Data:** 15 de Julho de 2026, 15:40

**Objetivo:**
Criar o ponto de entrada central da aplicação (`main.py`) expondo uma CLI funcional, carregando as variáveis de ambiente com segurança e exibindo logs informativos ao longo do pipeline de execução.

**Prompt Utilizado (Entrada do Usuário):**
> "Podemos seguir para o Bloco 7 (main.py — Ponto de Entrada)"

**Padrão de Prompting:** Task Execution / Delegation
> O usuário autorizou o avanço sequencial para o Bloco 7 seguindo o roadmap do projeto.

**Resultado e Ação (Saída da IA):**
- Criada branch `feature/07-entrypoint` a partir de `develop` atualizado.
- Implementado `main.py` com `argparse` expondo `--curriculo` e `--vaga` com valores padrão para o Bloco 8.
- Carregamento de `.env` via `load_dotenv()` com verificação explícita de `GROQ_API_KEY` antes de qualquer outra operação.
- Importação tardia de `app` (após `.env` carregado) para evitar falha na instanciação do `ChatGroq`.
- Logs em 6 etapas com emojis para feedback visual do pipeline ao usuário.
- Verificação do estado final do grafo (`error_message`) com `sys.exit(1)` em caso de falha.
- Código formatado via Black/Flake8. PR #15 aberto e Issue #7 fechada.

---

### Qualidade - Auditoria Pré-Bloco 8 e Correções
**Data:** 15 de Julho de 2026, 15:45

**Objetivo:**
Realizar uma auditoria formal do projeto verificando a conformidade de todos os entregáveis com a documentação em `/docs` antes de iniciar os testes finais (Bloco 8).

**Prompt Utilizado (Entrada do Usuário):**
> "Antes de iniciarmos o Bloco 8 (Testes e Validação), quero uma auditoria do projeto, tudo esta registrado em /docs. Quero uma validação se esta tudo de acordo."
> *(Ação seguinte)*: "sim" (confirmação para corrigir os pontos de atenção identificados)

**Padrão de Prompting:** Quality Assurance / Validation-driven
> O usuário solicitou um processo formal de auditoria, pedindo à IA que comparasse o estado atual do código e do repositório com cada documento de referência em `/docs` antes de avançar para os testes.

**Resultado e Ação (Saída da IA):**
- Lidos e cruzados todos os documentos em `/docs`: `architecture.md`, `gitflow.md`, `task-completion.md`, `prompts.md`, `tasks.md`, `specs/*.md`.
- Verificados via `gh` os estados de todas as 7 issues e 7 PRs no GitHub.
- Auditoria completa gerada em `walkthrough.md` (artefato interno) cobrindo: estrutura de arquivos, conformidade arquitetural, GitFlow, Task Completion, log de prompts e CI/CD.
- **Resultado geral: ✅ APROVADO** com 3 pontos menores identificados.
- Correções aplicadas em `chore(audit)`: remoção de `pathlib` do `requirements.txt`, adição de `protection.json` e `pr_body.txt` ao `.gitignore`, remoção do `protection.json` do tracking do git e atualização do `docs/tasks.md` com os checks `[x]` dos blocos concluídos.

---

### Fase 8: Testes e Validação
**Data:** 15 de Julho de 2026, 16:03

**Objetivo:**
Executar o pipeline final passando um currículo real e uma vaga sintética para testar a integração de ponta a ponta e validar o relatório gerado pelo LLM.

**Prompt Utilizado (Entrada do Usuário):**
> "Vamos seguir para Bloco 8 (Testes e Validação), mas não quero que suba o PDF para o github. Crie o TXT da vaga."
> *(Ação seguinte)*: "Continue" (após sucesso da execução)

**Padrão de Prompting:** Execution & Security-focused
> O usuário ordenou a execução final mas com restrições explícitas de segurança (não vazar PII no repositório). Ele também delegou à IA a criação de massa de dados realista (`vaga.txt`).

**Resultado e Ação (Saída da IA):**
- Atualização do `.gitignore` protegendo `input/*.pdf` e `input/*.txt`.
- Criação de uma vaga sintética (`input/vaga.txt`) para a stack do projeto (Python, LangChain, etc.).
- Correção de encoding em `main.py` removendo emojis que quebravam o terminal Windows (cp1252) com `UnicodeEncodeError`.
- Execução bem-sucedida da aplicação (`python main.py ...`) com o `output/relatorio.md` devidamente populado.
- Commit `fix(main)` protegendo emojis e commit do `.gitignore`.
- Atualização de `docs/tasks.md` marcando todos os blocos como finalizados.

---

### Ajuste Fino - Generalização do Extrator
**Data:** 15 de Julho de 2026, 16:16

**Objetivo:**
Melhorar a abrangência da extração de habilidades. O LLM estava perdendo skills aninhadas em descrições de projetos e a correção anterior enviesou o prompt apenas para tecnologia (ex: Vite, Express). O objetivo foi forçar a leitura profunda de todo o documento sem amarrar a uma profissão específica.

**Prompt Utilizado (Entrada do Usuário):**
> "No PDF tem uma parte de P R O J E T O S R E A L I Z A D O S [...] Onde mensiona o Sequelize, e o relatorio diz que não"
> *(Ação seguinte)*: "Certo, mas ideia do projeto é a analise geral de curriculos, de diferentes areas, porem o extract_prompt.py parece estar focado em tecnologia com essa nova regra"
**Padrão de Prompting:** Refinement / Context Expansion
> O usuário iterou sobre a resposta da IA, primeiro apontando uma "alucinação/omissão" baseada na estrutura do documento e depois exigindo a abstração da regra para múltiplos domínios (marketing, engenharia, etc).

**Resultado e Ação (Saída da IA):**
- Modificação no schema Pydantic (`graph/state.py`): expandiu o conceito de `habilidades` para incluir hard skills, softwares, certificações e metodologias, forçando a leitura de experiências e projetos.
- Modificação no `prompts/extract_prompt.py`: remoção do viés de TI, adicionando exemplos genéricos de múltiplas áreas (`Excel, Lean Six Sigma, AutoCad, React, Google Analytics`) e obrigando o parser a ler "TODO O TEXTO".

---

### Resolução de Alucinação (Gaps Injustos)
**Data:** 15 de Julho de 2026, 16:20

**Objetivo:**
Corrigir o comportamento da LLM que gerava falsos negativos (apontava como falta/gap tecnologias que o candidato possuía, como Express.js e Sequelize) devido à limitação de extração e ausência de flexibilidade a sinônimos.

**Prompt Utilizado (Entrada do Usuário):**
> "Quero uma solução para isso, o projeto é para ser certeiro em qualuqer area, e com esse gaps, pode prejudicar o candidato"
> *(Ação seguinte)*: "Execute mais uma vez"

**Padrão de Prompting:** Troubleshooting / Feedback Loop
> O usuário relatou que a ferramenta penalizava o candidato de forma incorreta e exigiu que o projeto não gerasse esses "gaps" arbitrários para manter a confiabilidade.

**Resultado e Ação (Saída da IA):**
- Modificação na arquitetura de extração (`graph/state.py` e `prompts/extract_prompt.py`): o Pydantic Schema foi dividido, forçando a LLM a popular um array para "habilidades principais" e outro focado na "varredura de ferramentas dentro de experiências/projetos" para contornar a perda de tokens.
- Otimização do avaliador (`prompts/analyze_prompt.py`): inclusão de uma "REGRA DE OURO" proibindo o modelo de apontar gaps apenas por variação de nomenclatura e exigindo verificação profunda nas experiências antes de penalizar o candidato.
- Resultado: Execução detectou os requisitos corretamente sem alucinações de exclusão.

---

### Simplificação e Automação de Uso
**Data:** 15 de Julho de 2026, 16:25

**Objetivo:**
Simplificar o processo de execução do sistema para que não seja mais necessário digitar comandos CLI com os caminhos dos arquivos. Gerar documentação de onboarding para o repositório.

**Prompt Utilizado (Entrada do Usuário):**
> "Ok, agora eu quero uma forma simplificada de rodar o projeto"
> *(Ação seguinte)*: "Não, a inicialização ainta esta complicada, tendo que adicionar o nome dos arquivos pdf e txt"
> *(Ação seguinte)*: "Para uma pessoa que acabou de clonar o projeto, oq ela deve fazer?"

**Padrão de Prompting:** Usability / Developer Experience (DX) / Documentation
> O usuário focou em "Experiência de Uso", rejeitou a automação intermediária que exigia argumentos e solicitou a criação de um roteiro de onboard para recém-chegados.

**Resultado e Ação (Saída da IA):**
- Criação de `run.bat` (Windows) e `run.sh` (Linux/Mac) com lógica para escanear automaticamente a pasta `input/` pelo primeiro `.pdf` e `.txt`, dispensando completamente parâmetros manuais.
- Tratamento de erro interativo nos scripts para alertar sobre falta de VENV ou de arquivos base.
- Criação do `README.md` completo detalhando o setup desde o git clone até a obtenção da chave do Groq.
