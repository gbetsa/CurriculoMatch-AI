# Bloco 11: Interface Web com Streamlit

## Descrição
Criar interface web para que o recrutador interaja com o agente de forma visual, sem necessidade de CLI. Interface com 3 abas: Nova Análise, Histórico e Comparar Candidatos.

## Dependências Novas
```txt
streamlit==1.45.1
requests==2.32.3
```

## Estrutura de Arquivos
```
streamlit_app.py       # Interface principal (3 abas)
```

## Layout e Funcionalidades

### Aba 1 — Nova Análise
- `st.file_uploader("Currículo (PDF)", type=["pdf"])`
- `st.text_area("Título da Vaga")`
- `st.text_area("Descrição da Vaga")`
- `st.button("Analisar")`
- Exibe relatório renderizado em Markdown com score e barra de progresso

### Aba 2 — Histórico
- Tabela paginada com: Data, Candidato, Vaga, Score, Status
- Filtros por nome do candidato e título da vaga
- Clique em uma linha → detalhe completo do relatório

### Aba 3 — Comparar
- Seleciona 1 vaga (text_area)
- Upload de múltiplos PDFs (st.file_uploader com accept_multiple_files)
- Botão "Comparar" → chama `/analyze/batch`
- Exibe ranking lado a lado com scores e gaps

## Critérios de Aceite
- [ ] Criar `streamlit_app.py` com layout de 3 abas.
- [ ] Aba 1: upload PDF + campos de vaga → chama `POST /analyze` → exibe relatório Markdown.
- [ ] Aba 2: tabela com histórico → chama `GET /history` → paginação funcional.
- [ ] Aba 3: múltiplos PDFs + vaga → chama `POST /analyze/batch` → ranking comparativo.
- [ ] Tratar erros de conexão com API (mensagem amigável se backend estiver offline).
- [ ] Exibir barra de progresso durante análise (simulada ou real via polling).
- [ ] Renderizar relatório Markdown com `st.markdown()`.
- [ ] Executar com `streamlit run streamlit_app.py` sem erros.
- [ ] Endereço padrão: `http://localhost:8501`.

## Dependências
- Bloco 10 (API) — endpoints para consumo
- Bloco 9 (Memória) — histórico para aba de histórico

## Branch Sugerida
`feature/11-streamlit-ui`
