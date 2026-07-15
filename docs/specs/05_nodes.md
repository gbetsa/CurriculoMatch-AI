# Bloco 5: Nós de Execução (Nodes)

## Descrição
Implementação das funções essenciais de cada etapa funcional (Nó) do LangGraph.

## Critérios de Aceite
- [ ] Nó de validação (`validate_inputs`) implementado para checar existência e extensão dos arquivos de entrada.
- [ ] Nós de leitura (`read_curriculum`, `read_job`) consumindo as *tools* implementadas no Bloco 2.
- [ ] Nó de extração (`extract_information`) consumindo a LLM (Groq) via *Structured Output* com o schema unificado.
- [ ] Nó de análise (`analyze_match`) gerando o score de compatibilidade via LLM.
- [ ] Nós de relatório (`generate_report`, `save_report`) para compilar o markdown final e persistir no sistema.
