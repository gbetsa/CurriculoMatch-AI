# Guia de Reprodução - Automação Low-Code (n8n)

## Fluxo Principal

```
Streamlit (Web) → n8n Webhook → API CurriculoMatch → n8n → Streamlit (Web) → Slack
```

1. **Streamlit** envia PDF + dados da vaga para n8n webhook
2. **n8n** recebe e encaminha para a API via HTTP
3. **API** processa com LangGraph e retorna resultado
4. **n8n** retorna resultado ao Streamlit E notifica Slack

## 1. Pré-requisitos

- Docker instalado
- API CurriculoMatch rodando (porta 8001)
- n8n rodando (porta 5678)
- Conta Slack com bot token (opcional)

## 2. Instalar e Iniciar n8n

```bash
# Iniciar n8n com acesso a API via host.docker.internal
docker run -d --name curriculomatch-n8n ^
  -p 5678:5678 ^
  -e N8N_BASIC_AUTH_ACTIVE=true ^
  -e N8N_BASIC_AUTH_USER=admin ^
  -e N8N_BASIC_AUTH_PASSWORD=curriculomatch ^
  n8nio/n8n
```

## 3. Importar Workflow

1. Acesse http://localhost:5678
2. Login: `admin` / `curriculomatch`
3. Clique no menu "..." → "Import from File"
4. Selecione `lowcode/n8n_workflow.json`
5. O workflow sera importado com 4 nos:
   - **Recebe Dados** (Webhook POST /analyze)
   - **Chama API** (Code node - envia para API)
   - **Responde Webhook** (retorna JSON ao Streamlit)
   - **Notifica Slack** (envia para #recrutamento)

## 4. Configurar Slack (Opcional)

1. No n8n, va em Credentials → Add Credential
2. Busque "Slack API"
3. Insira seu Slack Bot Token
4. Salve com nome "CurriculoMatch Slack"
5. No node "Notifica Slack", selecione a credencial criada

## 5. Ativar o Workflow

1. Abra o workflow importado
2. Clique no toggle "Active" (canto superior direito)
3. O webhook estara disponivel em: `http://localhost:5678/webhook/analyze`

## 6. Configurar Streamlit

Configure as variaveis de ambiente antes de iniciar o Streamlit:

```bash
set N8N_WEBHOOK_URL=http://localhost:5678/webhook/analyze
set API_URL=http://localhost:8001
streamlit run streamlit_app.py
```

## 7. Testar o Fluxo Completo

### Teste 1: Via curl (simula Streamlit)
```bash
curl -X POST http://localhost:5678/webhook/analyze ^
  -F "data=@input/Curriculo_Guilherme_Betsa.pdf" ^
  -F "job_title=Desenvolvedor Python" ^
  -F "job_description=Vaga para dev Python com Django e FastAPI"
```

### Teste 2: Via Streamlit
1. Acesse http://localhost:8501
2. Faca upload de um curriculo PDF
3. Preencha titulo e descricao da vaga
4. Clique em "Analisar"
5. Resultado aparece na tela + notificacao no Slack

## 8. Como Funciona o Code Node

O node "Chama API" usa JavaScript para:
1. Ler o PDF enviado como binario
2. Montar multipart/form-data com o campo "curriculum"
3. Enviar para `http://host.docker.internal:8001/analyze`
4. Retornar o resultado JSON

## 9. Solucao de Problemas

| Problema | Solucao |
|----------|---------|
| n8n nao inicia | Verificar se porta 5678 esta livre |
| API nao responde | Verificar se API esta rodando na porta 8001 |
| Webhook 404 | Verificar se workflow esta ativo (toggle verde) |
| Erro "form-data" | Verificar se Code node esta configurado corretamente |
| Slack nao envia | Configurar credenciais do Slack no n8n |
| Streamlit fallback | Se n8n cair, Streamlit chama API diretamente |

## 10. Parar Servicos

```bash
# Parar n8n
docker stop curriculomatch-n8n
docker rm curriculomatch-n8n

# Parar API (matar processo uvicorn)
taskkill /F /IM python.exe
```
