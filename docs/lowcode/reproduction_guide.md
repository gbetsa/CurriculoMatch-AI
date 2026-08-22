# Guia de Reprodução - Automação Low-Code (n8n)

## 1. Pré-requisitos

- Docker instalado
- API CurriculoMatch rodando (porta 8000)
- Conta Slack com webhook configurado (opcional)

## 2. Instalação do n8n

### Opção 1: Docker Compose (Recomendado)

```bash
# Navegar até a pasta lowcode
cd lowcode

# Iniciar n8n
docker-compose -f docker-compose.n8n.yml up -d

# Verificar status
docker-compose -f docker-compose.n8n.yml ps
```

### Opção 2: Docker Run

```bash
docker run -it --rm \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  -v $(pwd)/input:/home/node/input \
  -v $(pwd)/output:/home/node/output \
  n8nio/n8n
```

## 3. Acessar Interface

1. Abrir http://localhost:5678
2. Login: `admin` / `curriculomatch`

## 4. Importar Workflow

1. Clicar no menu "..." (tres pontos) no canto superior direito
2. Selecionar "Import from File"
3. Selecionar o arquivo `lowcode/n8n_workflow.json`
4. O workflow sera importado com todos os nos configurados

## 5. Configurar Credenciais

### Slack (Opcional)
1. Ir em Credentials > Add Credential
2. Selecionar "Slack API"
3. Inserir Slack Bot Token
4. Salvar com nome "Slack Recrutamento"

### API CurriculoMatch
1. O workflow ja vem configurado para `http://host.docker.internal:8000`
2. Se a API estiver em outra porta, atualizar no node "Chama API CurriculoMatch"

## 6. Ativar Workflow

1. Clicar no toggle "Active" no canto superior direito
2. O workflow ficara verde indicando que esta ativo

## 7. Testar

### Via Webhook (curl)
```bash
curl -X POST http://localhost:5678/webhook/analyze \
  -F "job_title=Desenvolvedor Python" \
  -F "job_description=Vaga para dev Python com Django"
```

### Via Formulario
1. Acesse http://localhost:5678/form/analyze
2. Preencha os campos
3. Envie

## 8. Fluxo do Workflow

```
Webhook Trigger → Chama API → Verifica Score → Slack (Aprovado/Rejeitado) → Resposta
```

## 9. Logs e Monitoramento

- Logs do n8n: `docker-compose -f docker-compose.n8n.yml logs -f`
- Execucoes: Acesse http://localhost:5678/executions

## 10. Parar n8n

```bash
docker-compose -f docker-compose.n8n.yml down
```

## 11. Solucao de Problemas

| Problema | Solucao |
|----------|---------|
| n8n nao inicia | Verificar se a porta 5678 esta livre |
| API nao responde | Verificar se a API esta rodando na porta 8000 |
| Webhook nao funciona | Verificar se o workflow esta ativo |
| Slack nao envia | Verificar credenciais do Slack |
