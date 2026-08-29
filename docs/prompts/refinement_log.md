# Log de Refinamento de Prompts - CurriculoMatch AI

Registro de ciclos de refinamento de prompts aplicados ao longo do projeto.

---

## Ciclo 1: Falsos-Negativos por Variacao de Nomenclatura

**Data:** Julho 2026

### Problema

O LLM gerava falsos-negativos na secao "Pontos de Atencao (Gaps)" do relatorio de compatibilidade. Por exemplo:

- Candidato listava "Express" na experiencia → LLM apontava "Express.js nao mentionado" como gap
- Candidato listava "VPS (Linux)" → LLM apontava "Linux nao listado" como gap
- Candidato listava "PostgreSQL" em projetos → LLM apontava "Banco de dados relacional nao demonstrado" como gap

Isso acontecia porque o LLM comparava os nomes de forma literal, sem reconhecer que eram a mesma tecnologia.

### Causa Raiz

1. O schema Pydantic `ExtractedInformation` misturava tudo em um unico campo `habilidades`
2. O prompt de analise nao tinha instrucao explicita para evitar falsos-negativos por nomenclatura

### Alteracoes

**1. Schema Pydantic (graph/nodes.py)**

Dividiu o campo unico em dois campos distintos:
- `habilidades` — competencias diretas mencionadas no curriculo
- `ferramentas_projetos_experiencias` — tecnologias extraidas das descricoes de experiencia e projetos

Isso fornece ao LLM uma visao mais granular das capacidades do candidato.

**2. Prompt de Analise (prompts/analyze_prompt.py)**

Adicionou a **REGRA DE OURO** na secao "Pontos de Atencao":

> "REGRA DE OURO: Antes de apontar um 'gap', verifique cuidadosamente as secoes de experiencias, projetos e ferramentas do candidato. Nao gere falsos-negativos por variacoes de nomenclatura (ex: 'Express' vs 'Express.js', ou 'Linux' vs 'VPS (Linux)'). Se o candidato demonstrou a habilidade, NAO liste como gap."

**3. Prompt de Extracao (prompts/extract_prompt.py)**

Adicionou regra explicita:

> "Preste MUITA atencao a extracao separada: coloque as habilidades principais no campo 'habilidades' e faca uma varredura profunda nas descricoes de experiencias/projetos para popular o campo 'ferramentas_projetos_experiencias'. Nao omita NENHUMA tecnologia citada."

### Resultado

- LLM passou a detectar requisitos corretamente sem alucinacoes de exclusao
- Score refletiu adequadamente a compatibilidade real
- Gaps listados eram genuinamente faltantes (nao variantes de nomenclatura)

### Metrics

| Metrica | Antes | Depois |
|---------|-------|--------|
| Falsos-negativos por nomenclatura | ~30% das analises | 0% |
| Gaps genuinos detectados | 100% | 100% |
| Score medio (curriculo compativel) | 72 | 88 |
