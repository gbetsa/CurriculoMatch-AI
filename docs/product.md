# Product.md

# CurriculoMatch AI

## Visão Geral

O **CurriculoMatch AI** é um agente de IA desenvolvido em Python utilizando **LangGraph** para automatizar a triagem inicial de currículos.

O agente recebe um currículo em PDF e uma descrição de vaga em formato de texto, analisa ambos os documentos e gera um relatório contendo o nível de compatibilidade entre o candidato e a vaga, além de sugestões de melhoria.

O projeto tem como objetivo demonstrar a construção de um agente utilizando LangGraph, empregando estado compartilhado, contexto, ferramentas e geração de respostas estruturadas.

---

# Problema

O processo de triagem de currículos costuma ser repetitivo e demorado.

Recrutadores precisam analisar diversas informações antes de decidir quais candidatos possuem maior aderência à vaga.

Este projeto automatiza essa primeira etapa, fornecendo uma análise inicial baseada nas informações presentes no currículo e na descrição da vaga.

---

# Objetivos

O agente deverá ser capaz de:

* Ler um currículo em PDF.
* Ler uma descrição de vaga.
* Extrair informações importantes de ambos os documentos.
* Comparar o perfil do candidato com os requisitos da vaga.
* Calcular um percentual de compatibilidade.
* Gerar um relatório estruturado.
* Salvar o relatório em arquivo.

---

# Público-alvo

* Recrutadores
* Empresas
* Gestores técnicos
* Profissionais de RH
* Estudantes que desejam avaliar seus currículos

---

# Fluxo da Aplicação

```text
Usuário

↓

Adiciona os arquivos na pasta input/

↓

Executa o projeto

↓

Agente valida os arquivos

↓

Ferramentas fazem a leitura

↓

Agente extrai informações

↓

Agente compara currículo e vaga

↓

Agente calcula compatibilidade

↓

Agente gera relatório

↓

Ferramenta salva relatório

↓

Usuário consulta o resultado
```

---

# Estrutura do Projeto

```text
curriculomatch-ai/

│

├── input/
│   ├── curriculo.pdf
│   └── vaga.txt
│
├── output/
│   └── relatorio.md
│
├── graph/
│   ├── state.py
│   ├── nodes.py
│   └── workflow.py
│
├── tools/
│   ├── pdf_reader.py
│   ├── job_reader.py
│   └── report_writer.py
│
├── prompts/
│   └── prompts.md
│
├── main.py
├── README.md
├── requirements.txt
└── .env.example
```

---

# Entrada

O usuário deverá adicionar dois arquivos na pasta `input`.

## Currículo

Arquivo PDF contendo o currículo do candidato.

Exemplo:

```text
input/curriculo.pdf
```

## Descrição da vaga

Arquivo de texto contendo os requisitos da vaga.

Exemplo:

```text
input/vaga.txt
```

Após isso basta executar:

```bash
python main.py
```

---

# Saída

O agente irá gerar um arquivo Markdown em:

```text
output/relatorio.md
```

O relatório conterá:

* Resumo do candidato
* Resumo da vaga
* Habilidades encontradas
* Requisitos identificados
* Compatibilidade (%)
* Pontos fortes
* Pontos de melhoria
* Sugestões
* Recomendação final

---

# Funcionalidades

## 1. Validação

O agente deverá validar:

* existência do currículo;
* existência da vaga;
* formato do currículo;
* conteúdo dos arquivos.

Caso algum arquivo seja inválido, a execução será interrompida.

---

## 2. Leitura dos arquivos

### Ferramenta PDF Reader

Responsável por:

* abrir o currículo;
* extrair o texto do PDF.

### Ferramenta Job Reader

Responsável por:

* abrir o arquivo da vaga;
* carregar sua descrição.

---

## 3. Extração de Informações

O agente deverá identificar, quando possível, no currículo:

* Nome
* E-mail
* Telefone
* Formação
* Experiências
* Habilidades técnicas
* Idiomas
* Certificações

Da descrição da vaga deverão ser extraídos:

* Cargo
* Tecnologias
* Requisitos obrigatórios
* Requisitos desejáveis
* Diferenciais

Todas essas informações serão armazenadas no estado do agente.

---

## 4. Comparação Currículo × Vaga

O agente deverá comparar:

* habilidades do candidato;
* requisitos da vaga;
* experiências profissionais;
* formação;
* tecnologias mencionadas.

Ao final será calculado um percentual de compatibilidade.

Exemplo:

* Compatibilidade: **84%**

A justificativa deverá explicar os principais fatores considerados.

---

## 5. Geração da Análise

O agente deverá produzir:

### Resumo do candidato

Breve descrição do perfil profissional.

### Pontos fortes

Exemplo:

* Boa experiência em Python.
* Conhecimento em Git.
* Projetos relevantes.

### Pontos de melhoria

Exemplo:

* Não informa nível de inglês.
* Pouca experiência com Docker.

### Sugestões

Exemplo:

* Adicionar projetos pessoais.
* Destacar resultados obtidos nas experiências.
* Inserir links para GitHub e LinkedIn.

---

## 6. Geração do Relatório

Ao final será criado um relatório em Markdown contendo todas as informações produzidas pelo agente.

---

# Ferramentas

O projeto utilizará três ferramentas.

## PDF Reader

Entrada:

* caminho do PDF

Saída:

* texto do currículo

---

## Job Reader

Entrada:

* caminho do arquivo da vaga

Saída:

* descrição da vaga

---

## Report Writer

Entrada:

* relatório final

Saída:

* arquivo Markdown

---

# Estado (Contexto)

Durante toda a execução, o agente compartilhará informações através do State do LangGraph.

Exemplo de informações armazenadas:

* caminho do currículo;
* caminho da vaga;
* texto do currículo;
* texto da vaga;
* dados extraídos;
* requisitos identificados;
* compatibilidade;
* análise final;
* relatório.

Cada etapa utilizará os dados produzidos anteriormente, evitando processamento duplicado.

---

# Fluxo do LangGraph

```text
START

↓

Validar arquivos

↓

Ler currículo

↓

Ler vaga

↓

Extrair informações

↓

Comparar currículo × vaga

↓

Calcular compatibilidade

↓

Gerar análise

↓

Salvar relatório

↓

END
```

---

# Requisitos Técnicos

* Python 3.12+
* LangGraph
* LangChain
* Leitura de PDF
* Estado compartilhado
* Ferramentas integradas
* Relatório em Markdown

---

# Critérios de Aceitação

O projeto será considerado concluído quando:

* O agente executar corretamente o fluxo do LangGraph.
* O currículo for lido automaticamente.
* A vaga for carregada automaticamente.
* A compatibilidade for calculada.
* O relatório for gerado.
* O relatório for salvo na pasta `output`.

---

# Possíveis Evoluções

* Interface Web com Streamlit.
* Upload de arquivos pelo navegador.
* Comparação entre vários candidatos.
* Ranking de candidatos.
* Histórico de análises.
* Exportação em PDF.
* Integração com APIs de recrutamento.
