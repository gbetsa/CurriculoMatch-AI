import os
import re
import json
import uuid
from datetime import datetime, timezone
from langchain_groq import ChatGroq
from graph.state import AgentState, ExtractedInformation
from tools.pdf_reader import read_curriculum
from tools.job_reader import read_job
from tools.report_writer import save_report
from prompts.extract_prompt import EXTRACT_PROMPT
from prompts.analyze_prompt import ANALYZE_PROMPT


def get_llm() -> ChatGroq:
    """Inicializa e retorna o modelo LLM do Groq configurado."""
    model_name = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    return ChatGroq(model=model_name, temperature=0)


def validate_inputs(state: AgentState) -> AgentState:
    """Valida se os arquivos de entrada existem e têm extensões corretas."""
    curr_path = state.get("curriculum_path", "")
    job_path = state.get("job_path", "")

    if not os.path.exists(curr_path) or not curr_path.endswith(".pdf"):
        return {
            "is_valid": False,
            "error_message": f"Currículo inválido ou não encontrado: {curr_path}",
        }

    if not os.path.exists(job_path) or not job_path.endswith(".txt"):
        return {
            "is_valid": False,
            "error_message": f"Vaga inválida ou não encontrada: {job_path}",
        }

    return {"is_valid": True, "error_message": None}


def load_history(state: AgentState) -> AgentState:
    """
    Recupera historico de analises anteriores via checkpointer.

    Gera um correlation_id unico para observabilidade e inicializa
    metadata basica da execucao.
    """
    correlation_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()

    return {
        "correlation_id": correlation_id,
        "history": state.get("history", []),
        "metadata": {
            "started_at": now,
            "correlation_id": correlation_id,
            "model": os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        },
    }


def read_curriculum_node(state: AgentState) -> AgentState:
    """Lê o currículo em PDF usando a tool apropriada."""
    try:
        text = read_curriculum(state["curriculum_path"])
        return {"curriculum_text": text}
    except Exception as e:
        return {"is_valid": False, "error_message": str(e)}


def read_job_node(state: AgentState) -> AgentState:
    """Lê a descrição da vaga usando a tool apropriada."""
    try:
        text = read_job(state["job_path"])
        return {"job_description": text}
    except Exception as e:
        return {"is_valid": False, "error_message": str(e)}


def extract_information(state: AgentState) -> AgentState:
    """Extrai informações do texto bruto para o formato estruturado (ExtractedInformation)."""
    llm = get_llm().with_structured_output(ExtractedInformation)
    chain = EXTRACT_PROMPT | llm

    try:
        result = chain.invoke(
            {
                "curriculum_text": state.get("curriculum_text", ""),
                "job_description": state.get("job_description", ""),
            }
        )
        # Compatibilidade com Pydantic v1 (dict) e v2 (model_dump)
        extracted_dict = (
            result.model_dump() if hasattr(result, "model_dump") else result.dict()
        )
        return {"extracted_information": extracted_dict}
    except Exception as e:
        return {
            "is_valid": False,
            "error_message": f"Falha na extração de dados: {str(e)}",
        }


def analyze_match(state: AgentState) -> AgentState:
    """Cruza as informações estruturadas para gerar a análise de compatibilidade."""
    llm = get_llm()
    chain = ANALYZE_PROMPT | llm

    candidato_json = json.dumps(
        state["extracted_information"].get("candidato", {}),
        ensure_ascii=False,
        indent=2,
    )
    vaga_json = json.dumps(
        state["extracted_information"].get("vaga", {}), ensure_ascii=False, indent=2
    )

    try:
        result = chain.invoke(
            {"candidato_data": candidato_json, "vaga_data": vaga_json}
        )
        analysis_text = result.content

        # Extrai o score numérico do texto Markdown gerado pela LLM.
        # Suporta formatos como: "85/100", "Score: 85", "pontuação: 85", "85 de 100".
        score_match = re.search(
            r"(\d{1,3})\s*(?:/|de)\s*100|score[^\d]*(\d{1,3})|pontua[çc][aã]o[^\d]*(\d{1,3})",
            analysis_text,
            re.IGNORECASE,
        )
        score = 0
        if score_match:
            raw = score_match.group(1) or score_match.group(2) or score_match.group(3)
            score = min(int(raw), 100)  # garante que não ultrapasse 100

        return {"analysis": analysis_text, "compatibility_score": score}
    except Exception as e:
        return {"is_valid": False, "error_message": f"Falha na análise: {str(e)}"}


def generate_report(state: AgentState) -> AgentState:
    """Gera o relatório final. Como a análise já está em Markdown, apenas repassa."""
    # Adicionamos um cabeçalho padrão ou repassamos diretamente
    return {"report": state.get("analysis", "")}


def save_report_node(state: AgentState) -> AgentState:
    """Salva o relatório em disco usando a tool de gravação."""
    success = save_report(state.get("report", ""))
    if not success:
        return {
            "is_valid": False,
            "error_message": "Falha ao salvar relatório no disco.",
        }
    return {}
