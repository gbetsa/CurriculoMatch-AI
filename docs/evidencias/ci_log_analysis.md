# Analise de Logs do CI

**Data:** 2026-08-22 18:08:10
**Total de etapas:** 5
**Sucesso:** 3
**Falhas:** 1
**Warnings:** 1
**Duracao total:** 70.35s

## Problemas Encontrados

### typecheck
- **Problema:** Found 5 errors in 3 files (run with --check for details)
  - `graph/nodes.py:45` - Incompatible types in assignment
  - `api/main.py:23` - Missing return type annotation

### test-integration
- **Problema:** FAILED tests/test_integration.py::test_extract_information_success
  - `tests/test_integration.py:78` - AssertionError: assert 'extracted_information' in {}

## Recomendacoes

- Corrija os erros de teste antes de fazer merge na branch principal.
- Considere corrigir os warnings de typecheck para melhorar a qualidade do codigo.
- Pipeline lenta (>60s). Considere paralelizar etapas ou otimizar dependencias.