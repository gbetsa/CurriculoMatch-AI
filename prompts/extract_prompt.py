from langchain_core.prompts import ChatPromptTemplate

EXTRACT_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Você é um especialista em extração de dados estruturados focado em recrutamento e seleção.
Sua missão é extrair rigorosamente as informações do currículo e da descrição da vaga fornecidos pelo usuário.

Regras de Extração:
1. Respeite fielmente os dados originais do texto base.
2. Preencha TODOS os campos do modelo de dados solicitado.
3. Não invente ou presuma informações que não estão explicitamente no texto.
4. Caso uma informação falte, retorne uma string vazia ("") ou array vazio ([]).""",
        ),
        (
            "user",
            """--- Currículo ---
{curriculum_text}

--- Vaga ---
{job_description}

Extraia as informações rigorosamente e forneça-as conforme o formato estruturado JSON exigido.""",
        ),
    ]
)
