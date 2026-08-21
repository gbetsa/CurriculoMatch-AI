# Bloco 17: Prompts, Modelos e Refinamento

## Descricao
Documentar todos os system prompts utilizados, configurar modelo via variavel de ambiente e documentar pelo menos 1 ciclo de refinamento de prompt com problema, alteracao e resultado.

## Estrutura de Arquivos
- docs/prompts/system_prompts.md (todos os prompts consolidados)
- docs/prompts/refinement_log.md (ciclos de refinamento documentados)
- .env.example (atualizacao com novas variaveis)

## Componentes

### 1. System Prompts Consolidados (docs/prompts/system_prompts.md)
Consolidar em 1 arquivo:
- Prompt de Extracao (extract_prompt.py) — regras, objetivo, restricoes
- Prompt de Analise (analyze_prompt.py) — regras, REGRA DE OURO, formato saida
- Prompt de Sanitizacao (se aplicavel) — regras de deteccao de injection

### 2. Ciclo de Refinamento (docs/prompts/refinement_log.md)
Documentar o ciclo ja existente no projeto:

**Problema:** LLM gerava falsos-negativos (apontava gaps injustos como "Express.js falta" quando candidato tinha "Express")

**Alteracao:** 
- Dividiu schema Pydantic em habilidades + ferramentas_projetos_experiencias
- Adicionou REGRA DE OURO no prompt de analise proibindo falsos-negativos por variacao de nomenclatura

**Resultado:**
- Execucao detectou requisitos corretamente sem alucinacoes de exclusao
- Score refletiu adequadamente a compatibilidade real

### 3. Variaveis de Ambiente Atualizadas (.env.example)
Adicionar:
- LLM_PROVIDER=groq
- LLM_MODEL=llama-3.3-70b-versatile
- LLM_TEMPERATURE=0
- DATABASE_URL=postgresql://user:pass@localhost:5432/curriculomatch
- LANGCHAIN_TRACING_V2=true
- LANGCHAIN_API_KEY=your_langsmith_key_here

## Criterios de Aceite
- [ ] Criar docs/prompts/system_prompts.md com todos os prompts consolidados e anotados
- [ ] Criar docs/prompts/refinement_log.md com pelo menos 1 ciclo completo (problema-alteracao-resultado)
- [ ] Atualizar .env.example com todas as variaveis de ambiente novas
- [ ] Verificar que nenhum valor real de chave aparece no .env.example
- [ ] Documentar no README.md (secao "Prompts, Modelos e Refinamento")
- [ ] Modelo configurado via variavel de ambiente (LLM_MODEL), hardcoded no codigo

## Dependencias
- Bloco 4 (Prompts existentes) — prompts ja implementados
- Bloco 12 (Seguranca) — prompt de sanitizacao, se aplicavel

## Branch Sugerida
feature/17-prompts-refinement
