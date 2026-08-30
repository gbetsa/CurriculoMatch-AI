# Matriz de Risco x Impacto

## CurriculoMatch AI - Analise de Riscos

| Cenario | Risco | Impacto | Prioridade | Justificativa |
|---------|-------|---------|------------|---------------|
| Analise completa falha | Alto | Alto | P0 | Teste E2E de analise completa e prioridade porque uma regressao nesse fluxo torna a aplicacao inutil para o usuario. |
| Score incorreto (falso positivo) | Medio | Alto | P1 | Um score incorreto pode levar a decisoes erradas de contratacao, mas e detectavel em testes de integracao. |
| Falha de leitura PDF | Baixo | Medio | P2 | Falha isolada que nao afeta outros fluxos; tratamento de erro ja implementado. |
| Timeout na API | Medio | Medio | P2 | Pode causar inconveniencia mas nao perda de dados; retry ja implementado. |
| Injection bypass (seguranca) | Alto | Alto | P0 | Se a sanitizacao falhar, o LLM pode ser manipulado; testes de seguranca cobrem. |
| Perda de dados (checkpointer) | Baixo | Alto | P1 | Dados ficam no PostgreSQL; fallback para modo sem historico disponivel. |
| Falha de conexao LLM | Medio | Alto | P1 | Tenacity retry + fallback Ollama mitigam; testes de resiliencia cobrem. |
| Memory leak em logs | Baixo | Baixo | P3 | Logs em JSONL sao leves; diretorio logs/ no .gitignore. |

## Legenda de Prioridade

- **P0**: Critico - Falha que torna a aplicacao inutil. Requer teste imediato.
- **P1**: Alto - Falha que afeta funcionalidade principal mas tem mitigacao.
- **P2**: Medio - Falha isolada com tratamento de erro existente.
- **P3**: Baixo - Falha menor sem impacto significativo.

## Distribuicao de Testes por Prioridade

| Prioridade | Testes | Arquivo |
|------------|--------|---------|
| P0 | 3 | test_e2e.py, test_integration.py |
| P1 | 4 | test_integration.py, test_security.py |
| P2 | 3 | test_integration.py, test_tools.py |
| P3 | 0 | - |
