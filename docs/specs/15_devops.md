# Bloco 15: DevOps Inteligente e Deteccao de Falhas

## Descricao
Aprimorar pipeline CI/CD, utilizar IA para analisar logs do pipeline (2+ etapas), detectar anomalias e produzir estimativa simples de tendencia/risco de falha. Deploy nao e obrigatorio.

## Estrutura de Arquivos
- .github/workflows/ci.yml (atualizacao)
- scripts/analyze_ci_logs.py (IA analisa logs do CI)
- scripts/detect_anomaly.py (deteccao de anomalias + tendencia)
- docs/evidencias/ci_log_analysis.md (evidencia da analise IA)
- docs/evidencias/anomaly_report.md (relatorio de anomalia + tendencia)

## Componentes

### 1. Pipeline Aprimorado (.github/workflows/ci.yml)
Etapas: lint (ruff/flake8), typecheck (mypy), testes unit, testes integracao, testes e2e, docker build (sem push).

### 2. Analise de Logs com IA (scripts/analyze_ci_logs.py)
- Captura logs de 2+ stages do CI (ex: lint + testes, ou testes + build)
- Passa para LLM: "Analise estes logs, identifique falhas e explique cada uma"
- Salva resultado em docs/evidencias/ci_log_analysis.md

### 3. Deteccao de Anomalias (scripts/detect_anomaly.py)
- Simula 10-20 execucoes passadas com metricas (latencia, taxa de erro)
- Analise simples: media movel ou regra de threshold
- Exemplo: "Latencia do no extract aumentou 40% nas ultimas 10 execucoes -> risco de timeout"
- Gera relatorio em docs/evidencias/anomaly_report.md

### 4. Estimativa de Tendencia
- Dados simulados (documentados como tal) ou reais do checkpointer
- Regressao linear simples ou calculo de taxa de crescimento
- Output: "Se a tendencia persistir, chance de falha em 7 dias: 65%"

## Criterios de Aceite
- [ ] Atualizar .github/workflows/ci.yml com typecheck + testes e2e + docker build
- [ ] Criar scripts/analyze_ci_logs.py que le logs do CI e gera analise com IA
- [ ] Criar scripts/detect_anomaly.py com simulacao de dados + deteccao
- [ ] Gerar docs/evidencias/ci_log_analysis.md com analise real de 2+ stages
- [ ] Gerar docs/evidencias/anomaly_report.md com anomalia identificada + tendencia
- [ ] Documentar no README.md (secao QA, Observabilidade e DevOps)
- [ ] Evidencias: pipeline funcional + analise de logs + anomalia + estimativa documentadas

## Dependencias
- Bloco 13 (Observabilidade) — logs estruturados para entrada da analise
- Bloco 14 (QA) — testes que rodam no pipeline

## Branch Sugerida
feature/15-devops-anomaly
