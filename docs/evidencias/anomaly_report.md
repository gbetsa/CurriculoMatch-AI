# Relatorio de Deteccao de Anomalias

**Data:** 2026-08-22 18:08:16
**Total de execucoes analisadas:** 20
**Anomalias encontradas:** 3

## Estatisticas

- **Latencia media:** 2944.51ms
- **Desvio padrao:** 302.00ms
- **Latencia minima:** 2329.57ms
- **Latencia maxima:** 3485.71ms
- **Taxa de erro media:** 3.86%

## Anomalias Detectadas

| Execucao | Timestamp | Latencia | Erro | Motivo |
|----------|-----------|----------|------|--------|
| exec-017 | 2026-08-21T02:08 | 3178ms | 26.1% | Taxa de erro alta: 26.1% |
| exec-018 | 2026-08-21T10:08 | 3371ms | 26.5% | Taxa de erro alta: 26.5% |
| exec-019 | 2026-08-21T18:08 | 3486ms | 15.6% | Taxa de erro alta: 15.6% |

## Analise de Tendencia

- **Direcao:** aumento
- **Inclinacao:** 49.8775ms/execucao
- **Latencia atual:** 2944.51ms
- **Latencia estimada (7 dias):** 4515.65ms
- **Chance de falha (7 dias):** 38.8%

**Interpretacao:** Tendencia: aumento gradual. BAIXO risco de falha em 7 dias (38.8%).

## Recomendacoes

- Monitorar latencia nas proximas execucoes
- Verificar se o aumento e significativo