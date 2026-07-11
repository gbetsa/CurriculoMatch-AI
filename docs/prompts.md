# Instruções de Registro de Prompts (prompts.md)

**Atenção Assistente de IA:** Este documento contém as regras estritas e arquiteturais que você deve seguir para registrar TODAS as interações significativas feitas pelo usuário durante o desenvolvimento do projeto **CurriculoMatch AI**. Como a arquitetura orienta o comportamento do sistema, este arquivo orienta o **seu** comportamento de documentação.

---

## 1. Regra de Registro Obrigatório

Para atender aos critérios avaliativos da disciplina (IA para DEVs [T2]), é **mandatório** que você (a IA) registre e versione as interações do usuário (prompts) e o resultado gerado (saída) em arquivos de log dedicados.

Sempre que o usuário realizar uma solicitação que envolva:
- **Planejamento** arquitetural ou de sistema.
- **Implementação** de código-fonte (nós do LangGraph, ferramentas, estado).
- **Melhoria** ou refatoração do código existente.
- **Correção** de erros e *debugging*.

**Ação Exigida da IA:** Você deve registrar essa interação no respectivo arquivo de log.

---

## 2. Onde Registrar (Caminhos de Arquivo)

- Todos os logs das interações do ciclo de desenvolvimento devem ser adicionados (em anexo/append) ao arquivo: `docs/prompts/prompts_dev.md`
- Caso o usuário inicie uma fase de *Testes* ou defina outro foco, você pode ser instruído a criar ou usar arquivos como `docs/prompts/prompts_tests.md`.

---

## 3. Padrão Exato de Registro (Template Obrigatório)

Ao atualizar o log com uma nova interação, você **DEVE** utilizar estritamente o formato Markdown abaixo:

```markdown
### [Fase/Etapa] - [Título Resumido da Tarefa]
**Data:** [Data e hora da interação]

**Objetivo:**
[Descreva objetivamente o problema ou a funcionalidade que o usuário exigiu. Ex: "Implementar a ferramenta pdf_reader.py utilizando pymupdf".]

**Prompt Utilizado (Entrada do Usuário):**
> [Registre aqui o prompt exato (ou um resumo fiel) que o usuário enviou para iniciar ou corrigir a tarefa.]

**Padrão de Prompting:** [Nome do Padrão, ex: Role-based, Zero-shot, Few-shot]
> [Descreva brevemente o padrão aplicado no prompt acima e como ele orientou a IA. Ex: "Define o papel da IA como geradora de especificações técnicas para um projeto de software, estabelecendo o contexto do ciclo de desenvolvimento."]

**Resultado e Ação (Saída da IA):**
[Descreva o que você gerou, construiu ou corrigiu na base de código. Ex: "Criado o arquivo tools/pdf_reader.py implementando tratamento de erros. Arquivo salvo com sucesso."]
```

---

## 4. Gatilhos de Ação (Para a IA)

1. **Pró-atividade:** Ao terminar de escrever ou modificar um bloco crítico de código (ex: `graph/state.py` ou `tools/job_reader.py`), utilize suas ferramentas de escrita de arquivo para adicionar imediatamente o registro daquela tarefa no `prompts_dev.md` sem precisar que o usuário peça.
2. **Transparência:** O professor e os avaliadores do projeto precisam ler os arquivos em `docs/prompts/` e entender perfeitamente como o aluno instruiu a IA e o que a IA devolveu. Não omita os prompts do usuário.
