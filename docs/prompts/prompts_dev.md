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
