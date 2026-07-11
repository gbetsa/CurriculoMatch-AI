# Task Completion Steering

## Objetivo

Padronizar o fluxo de conclusão de tarefas, garantindo que o Kanban do GitHub Projects reflita corretamente o estado do desenvolvimento.

---

## Fluxo Obrigatório ao Concluir uma Tarefa

Ao finalizar qualquer tarefa do tasks.md, a IA DEVE executar os seguintes passos:

### 1. Commit e Push

- Fazer commit seguindo Conventional Commits
- Push para a branch da feature

### 2. Pull Request

- Criar PR de `feature/nome` para `develop`
- Body do PR deve conter `Closes #N` referenciando a issue correspondente
- **NUNCA usar `--delete-branch`** no merge

### 3. Atualizar a Issue (Card do Kanban)

Após merge do PR, a issue correspondente DEVE ser atualizada com:

- **Assignee**: `gbetsa`
- **Descrição original**: NÃO editar o body da issue — manter a descrição da tarefa intacta
- **Comentário de conclusão**: Adicionar um NOVO COMENTÁRIO (`gh issue comment`) com o que foi feito
- **Status**: Fechar a issue (move automaticamente para Done)

### 4. Formato do Comentário de Conclusão

Usar `gh issue comment N --body "..."` para adicionar o seguinte:

```markdown
## ✅ Tarefa concluída

### O que foi feito
- [Lista de entregáveis concretos]

### Verificação
- [Como foi validado: testes, build, etc.]

### Branch
feature/nome-da-branch

### PR
#N (mergeado em develop)
```

---

## Regras

- SEMPRE adicionar assignee `gbetsa` ao card
- SEMPRE adicionar comentário de conclusão ANTES de fechar a issue
- NUNCA editar o body original da issue — usar comentário
- NUNCA fechar uma issue sem comentário do que foi feito
- NUNCA deletar branches após merge
- O comentário deve refletir exatamente o que foi implementado, não o que foi planejado
