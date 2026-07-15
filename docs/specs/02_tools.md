# Bloco 2: Implementação das Ferramentas (Tools)

## Descrição
Criação dos módulos utilitários de I/O que serão consumidos pelo agente para leitura e escrita de arquivos.

## Critérios de Aceite
- [ ] `tools/pdf_reader.py` implementado com a biblioteca `pymupdf` (fitz) para ler e extrair texto de PDFs de forma resiliente.
- [ ] `tools/job_reader.py` implementado para ler texto simples com tratamento adequado de fallback de encoding (`utf-8`).
- [ ] `tools/report_writer.py` implementado utilizando `pathlib` para criar a pasta `output` (se não existir) e salvar relatórios em `.md`.
