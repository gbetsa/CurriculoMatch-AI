# Plano de Testes - CurriculoMatch AI

## 1. Estrategia de Testes

### 1.1. Niveis de Teste
- **Unitarios**: Testes isolados de funcoes e componentes (ja implementados)
- **Integracao**: Testes do grafo completo com LLM mockada
- **E2E**: Testes de ponta a ponta via API

### 1.2. Ferramentas
- **pytest**: Framework de testes
- **pytest-mock**: Mocking de dependencias
- **FastAPI TestClient**: Testes de API
- **coverage**: Medicao de cobertura

## 2. Priorizacao por Risco

### P0 - Critico
- **Analise completa**: Fluxo principal da aplicacao. Se falhar, o sistema e inutil.
- **Injection bypass**: Seguranca do sistema. Se falhar, o LLM pode ser manipulado.

### P1 - Alto
- **Score incorreto**: Afeta decisoes de contratacao.
- **Falha de conexao LLM**: Disponibilidade do servico.
- **Perda de dados**: Integridade das informacoes.

### P2 - Medio
- **Falha de leitura PDF**: Falha isolada com tratamento.
- **Timeout na API**: Inconveniencia sem perda de dados.

### P3 - Baixo
- **Memory leak em logs**: Impacto minimo.

## 3. Cenarios de Teste

### 3.1. Testes de Integracao (test_integration.py)
1. **Happy Path**: PDF + vaga validos → relatorio gerado
2. **Falha de Validacao**: PDF inexistente → END sem gastar tokens
3. **Falha de Leitura**: PDF corrompido → error_message no estado

### 3.2. Testes E2E (test_e2e.py)
1. **POST /analyze**: PDF + vaga → 200 + relatorio
2. **POST /analyze sem PDF**: 422
3. **GET /health**: 200

### 3.3. Testes de Seguranca (test_security.py)
1. **Injection Detection**: Padrões de injection detectados
2. **Sanitization**: Textos sanitizados corretamente
3. **Adversarial Scenario**: Injection nao altera score

## 4. Justificativa P0

O teste E2E de analise completa e P0 porque:

1. **Fluxo Principal**: E a funcionalidade core da aplicacao
2. **Impacto Total**: Se falhar, o sistema e inutil para o usuario
3. **Deteccao Precoce**: Regressoes nesse fluxo devem ser detectadas antes de qualquer deploy
4. **Cobertura**: Testa todas as camadas (API → Grafo → LLM → Banco → Resposta)

## 5. Execucao

```bash
# Todos os testes
pytest tests/ -v

# Apenas integracao
pytest tests/test_integration.py -v

# Apenas E2E
pytest tests/test_e2e.py -v

# Com cobertura
pytest tests/ --cov=graph --cov=api --cov-report=html
```
