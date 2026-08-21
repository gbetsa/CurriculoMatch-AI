# Bloco 9: Memória e Checkpointer PostgreSQL

## Descrição
Implementar persistência de estado entre execuções do agente LangGraph utilizando PostgreSQL como checkpointer. O agente deve ser capaz de recuperar análises anteriores de candidatos/vagas e utilizar esse histórico no contexto de novas análises. Estratégia de memória escolhida: **checkpointer persistente** (não RAG), justificada pela natureza transacional do domínio (histórico de triagens, não busca semântica em documentos).

## Justificativa (não-RAG)
O domínio de recrutamento não requer busca semântica em base de conhecimento externa. O que se necessita é lembrar análises anteriores do mesmo candidato ou vaga — tarefa de persistência relacional, não de vetores.

## Dependências Novas
```txt
psycopg[pool]==3.1.18
langgraph-checkpoint-postgres==1.2.9
```

## Estrutura de Arquivos
```
graph/
  checkpointer.py      # Configuração do PostgresSaver + pool de conexões
graph/state.py          # Atualização: campos history, correlation_id, metadata
```

## Esquema de Banco
Tabelas gerenciadas automaticamente pelo `PostgresSaver`:
- `checkpoints` — snapshots de estado por thread_id
- `checkpoint_writes` — mutações individuais por nó
- `checkpoint_blobs` — binários serializados (texto do CV, relatório)

## Critérios de Aceite
- [ ] Criar `graph/checkpointer.py` com `PostgresSaver` configurado via `DATABASE_URL` do `.env`.
- [ ] Atualizar `graph/state.py` com novos campos: `history: List[AnalysisRecord]`, `correlation_id: str`, `metadata: Dict[str, Any]`.
- [ ] Criar nó `load_history` em `graph/nodes.py` que recupera análises anteriores do mesmo candidato (pelo nome extraído) via checkpointer.
- [ ] Atualizar `graph/workflow.py` para compilar o grafo com `checkpointer` e incluir nó `load_history` entre `validate_inputs` e `read_curriculum`.
- [ ] Adicionar `DATABASE_URL` ao `.env.example` com valor placeholder.
- [ ] Testar que segunda execução com mesmo candidato recupera histórico.
- [ ] Documentar decisão de não-RAG em `README.md` (seção "Contexto e Memória").

## Dependências
- Bloco 3 (Estado Compartilhado) — AgentState existente
- Bloco 6 (Workflow) — Grafo compilado existente
- PostgreSQL instalado localmente

## Branch Sugerida
`feature/09-memory-checkpoint`
