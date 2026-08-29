# Decisoes de Design e Trade-offs - CurriculoMatch AI

Registro consolidado das decisoes de arquitetura e justificativas tecnicas.

---

## 1. LLM: Groq + qwen/qwen3.8-27b

**Decisao:** Utilizar Groq como provedor de LLM com modelo `qwen/qwen3.8-27b`.

**Alternativas consideradas:**
- OpenAI GPT-4o: Mais caro, latencia maior
- Ollama local: Sem custo, mas requer GPU e tem latencia variavel
- Groq Llama-3.3-70b: Modelo maior, mas atingiu rate limit rapido (200k TPD)

**Justificativa:**
- Latencia ultrabaixa (respostas em 1-3s)
- Tier gratuito generoso para desenvolvimento
- Suporte a structured output via LangChain
- Facil troca via variavel de ambiente (GROQ_MODEL)

**Trade-off:** Dependencia de servico externo. Mitigado com fallback para Ollama local.

---

## 2. Arquitetura: Workflow Deterministico + Agente LLM

**Decisao:** Sistema hibrido com LangGraph orquestrando nos deterministico + LLM.

**Por que nao 100% agente?**
- Extração de dados e mais deterministica com structured output
- Sanitizacao via regex e mais rapida e previsivel que LLM
- Validacao de entrada nao precisa de LLM
- Reducao de custo (menos chamadas LLM)

**Por que nao 100% deterministico?**
- Analise de compatibilidade exige raciocinio semantico
- Geracao de relatorio em linguagem natural
- Comparacao com historico exige inferencia

---

## 3. Memoria: Checkpointer PostgreSQL vs RAG

**Decisao:** PostgresSaver (checkpointer persistente) em vez de RAG.

**Justificativa:**
- O dominio de recrutamento nao requer busca semantica em base de conhecimento externa
- O necessario e lembrar analises anteriores do mesmo candidato/vaga
- Tarefa de persistencia relacional, nao de vetores
- Checkpointer e mais simples, eficiente e testavel

**Trade-off:** Nao busca contexto externo (ex: benchmarks de mercado). Mitigado com buscas na web quando necessario.

---

## 4. Schema Pydantic: Extracao Dividida

**Decisao:** Dividir o schema em `habilidades` + `ferramentas_projetos_experiencias`.

**Problema original:** Campo unico causava perda de tokens e LLM "esquecia" ferramentas citadas em experiencias.

**Resultado:** Extração 100% das tecnologias mencionadas, sem omissao.

**Trade-off:** Schema mais complexo. Mitigado com documentacao clara e validacao Pydantic.

---

## 5. Prompt: REGRA DE OURO (Anti-Alucinação)

**Decisao:** Adicionar instrucao explicita para nao gerar falsos-negativos por variacao de nomenclatura.

**Problema original:** LLM apontava gaps como "Express.js falta" quando candidato tinha "Express".

**Resultado:** 0% de falsos-negativos por nomenclatura.

**Trade-off:** LLM pode ser excessivamente complacente. Mitigado com validacao humana (human-in-the-loop).

---

## 6. Seguranca: Multi-Camada

**Decisao:** 3 camadas de protecao contra prompt injection:

1. **n8n AI Agent:** Detecta injection no titulo/descricao da vaga
2. **API regex:** Valida texto da vaga com 29 padroes (PT+EN)
3. **LangGraph:** sanitize_inputs sanitiza curriculo e vaga

**Trade-off:** Triple-check pode bloquear textos legitimos. Mitigado com fail-open no analyze_injection (LLM) e sanitizacao suave no regex.

---

## 7. API: FastAPI com Endpoints REST

**Decisao:** FastAPI para a API REST.

**Alternativas consideradas:**
- Flask: Mais simples, mas menos features
- Django REST: Muito pesado para o escopo
- Direct invocation (sem API): Impossivel integrar com n8n e Streamlit

**Justificativa:**
- Async nativo (importante para chamadas LLM)
- OpenAPI automatico (/docs)
- Validacao via Pydantic nativa
- CORS configurado para Streamlit

---

## 8. UI: Streamlit

**Decisao:** Streamlit para interface web.

**Alternativas consideradas:**
- Gradio: Mais simples, menos customizavel
- React/Next.js: Muito complexo para o escopo
- Terminal: Sem interface visual

**Justificativa:**
- Rapido de prototipar
- Componentes nativos (upload, tabelas, botoes)
- Renderizacao de Markdown nativa
- Integracao direta com Python

**Trade-off:** Limitacoes de customizacao visual. Aceitavel para prototipo academico.

---

## 9. Low-Code: n8n como Guardrails

**Decisao:** n8n como camada intermediaria entre Streamlit e API.

**Justificativa:**
- Validacao de dados antes de chegar a API
- Deteccao de injection via IA (Groq) sem sobrecarregar a API
- Workflow visual para debugging
- Separacao de responsabilidades

**Trade-off:** Mais um servico para manter. Mitigado com Docker Compose.

---

## 10. CI/CD: GitHub Actions

**Decisao:** Pipeline com 7 jobs paralelos (lint, typecheck, test-unit, test-integration, test-api, test-e2e, docker-build).

**Justificativa:**
- Feedback rapido ao desenvolvedor
- Paralelismo reduz tempo total
- Docker build so roda apos todos os testes
- Ruff + Black para padronizacao de codigo

---

## 11. Observabilidade: structlog + LangSmith

**Decisao:** Logs JSON estruturados (structlog) + traces opcionais (LangSmith).

**Justificativa:**
- Logs JSON sao parseaveis e indexaveis
- Correlation ID permite rastrear execucoes
- LangSmith opcional (nao obriga chave de API)
- Script de investigacao para debugging

---

## 12. Testes: Estrategia em Piramide

**Decisao:** Piramide de testes com 85+ testes.

- **Unitarios (60+):** Funcoes isoladas, tools, security
- **Integracao (12):** Fluxo completo com LLM mockada
- **E2E (11):** API via TestClient

**Justificativa:**
- Unitarios rapidos e baratos
- Integracao valida o fluxo sem gastar tokens
- E2E valida a API real
- Code review com IA complementa
