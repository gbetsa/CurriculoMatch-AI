# Bloco 16: Low-Code / No-Code (n8n)

## Descricao
Implementar automacao low-code integrada a solucao principal utilizando n8n. A ferramenta visual atua como orquestrador/ integrador, enquanto a logica principal permanece no agente Python.

## Estrutura de Arquivos
- lowcode/n8n_workflow.json (workflow exportado do n8n)
- lowcode/docker-compose.n8n.yml (n8n standalone para testes locais)
- docs/lowcode/reproduction_guide.md (instrucoes de reproducao)

## Fluxo Principal: "Analise Automatica de Curriculo"

### Gatilho
Email com curriculo anexado (IMAP) OU webhook HTTP (formulario Typeform/Google Forms)

### Processamento
n8n salva PDF em pasta compartilhada + extrai metadados do email/formulario

### Acao
HTTP POST para http://localhost:8000/analyze (mesma API do CurriculoMatch)

### Saida
Mensagem no Slack #recrutamento com resumo do relatorio (score + veredito)

### Fluxo Visual
```
Gatilho Email/Webhook --> Salva PDF --> Chama API --> Formata --> Slack/Email
```

## Fluxo Alternativo: "Vaga Recebida"
```
Google Forms --> Webhook --> n8n --> Compara com curriculos da pasta --> Ranking --> Email RH
```

## Instrucoes de Reproducao
1. Instalar n8n: docker run -it --rm -p 5678:5678 -v n8n_data:/home/node/.n8n n8nio/n8n
2. Abrir http://localhost:5678
3. Importar lowcode/n8n_workflow.json
4. Configurar credenciais: SMTP (email), Slack (webhook URL), HTTP Request (API URL)
5. Ativar workflow
6. Enviar email com PDF para testar

## Criterios de Aceite
- [ ] Instalar n8n localmente (Docker) e confirmar que sobe
- [ ] Criar workflow com pelo menos 1 gatilho (email ou webhook)
- [ ] Workflow integra com a API POST /analyze
- [ ] Workflow produz saida observavel (mensagem Slack ou email)
- [ ] Exportar workflow como lowcode/n8n_workflow.json
- [ ] Criar docs/lowcode/reproduction_guide.md com instrucoes passo a passo
- [ ] Documentar no README.md (secao "Automacao Low-Code")
- [ ] Demonstracao no video: workflow recebendo trigger e chamando agente

## Dependencias
- Bloco 10 (API) — endpoint para o n8n chamar

## Branch Sugerida
feature/16-lowcode-n8n
