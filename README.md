# CurriculoMatch AI 🚀

CurriculoMatch AI é um agente autônomo baseado em grafos (LangGraph) que cruza as habilidades de um currículo (PDF) com a descrição de uma vaga (TXT) utilizando Inteligência Artificial (Groq/Llama3), gerando um relatório estruturado de compatibilidade.

---

## 🛠️ Como Usar (Para quem acabou de clonar)

Siga os passos abaixo para rodar o projeto localmente:

### 1. Configurar o Ambiente Virtual
É altamente recomendado o uso de um ambiente virtual para isolar as dependências:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar Dependências
Com o ambiente ativado, instale as bibliotecas necessárias:
```bash
pip install -r requirements.txt
```

### 3. Configurar as Chaves de API (LLM)
O sistema utiliza a API da Groq por padrão por ser ultrarrápida.
1. Renomeie o arquivo `.env.example` para `.env`
2. Edite o arquivo `.env` inserindo a sua chave da Groq:
```env
GROQ_API_KEY=sua_chave_aqui
```

### 4. Preparar os Arquivos de Entrada
Para o sistema funcionar, ele precisa de **exatamente** 1 currículo e 1 vaga:
1. Coloque o **Currículo em PDF** dentro da pasta `input/`
2. Coloque a **Descrição da Vaga em TXT** dentro da pasta `input/`

> **Nota:** Seus dados estão seguros! O arquivo `.gitignore` bloqueia o envio de arquivos PDF e TXT presentes na pasta `input/` para o GitHub.

### 5. Rodar a Análise
Com os arquivos na pasta, basta executar o script simplificado:

**No Windows:**
Dê um duplo-clique no arquivo `run.bat` ou rode no terminal:
```bash
.\run.bat
```

**No Linux/macOS:**
```bash
chmod +x run.sh
./run.sh
```

### 6. Ver o Resultado
Após a execução (que leva cerca de 15 segundos), o relatório final contendo o Score, Pontos Fortes, Gaps e o Veredito estará disponível em:
👉 `output/relatorio.md`

---

## 🏗️ Arquitetura
O sistema utiliza um **StateGraph** para orquestrar os nós:
1. **Validação:** Checa os arquivos de entrada.
2. **Leitura:** Usa `PyMuPDF` para ler o PDF.
3. **Extração (LLM):** Extrai habilidades rigorosamente separando "stacks" e "tecnologias descritas em projetos".
4. **Análise (LLM):** Cruza os dados extraídos, evitando falsos-negativos (alucinações).
5. **Relatório:** Salva o output final em Markdown.
