import json
import os
import re
import time
import uuid
from datetime import UTC, datetime

from langchain_groq import ChatGroq

from graph.observability import get_logger, log_error, log_node_complete, log_node_start
from graph.security import sanitize_text
from graph.state import AgentState, ExtractedInformation
from prompts.analyze_prompt import ANALYZE_PROMPT
from prompts.extract_prompt import EXTRACT_PROMPT
from tools.job_reader import read_job
from tools.pdf_reader import read_curriculum
from tools.report_writer import save_report


def get_llm() -> ChatGroq:
    """Inicializa e retorna o modelo LLM do Groq configurado."""
    model_name = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
    return ChatGroq(model=model_name, temperature=0)


def validate_inputs(state: AgentState) -> AgentState:
    """Valida se os arquivos de entrada existem e têm extensões corretas."""
    logger = get_logger(state.get("correlation_id"))
    start_time = time.time()

    log_node_start(
        logger,
        "validate_inputs",
        {
            "curriculum_path": state.get("curriculum_path", ""),
            "job_path": state.get("job_path", ""),
        },
    )

    curr_path = state.get("curriculum_path", "")
    job_path = state.get("job_path", "")

    if not os.path.exists(curr_path) or not curr_path.endswith(".pdf"):
        duration_ms = (time.time() - start_time) * 1000
        log_node_complete(logger, "validate_inputs", "error", duration_ms)
        return {
            "is_valid": False,
            "error_message": f"Currículo inválido ou não encontrado: {curr_path}",
        }

    if not os.path.exists(job_path) or not job_path.endswith(".txt"):
        duration_ms = (time.time() - start_time) * 1000
        log_node_complete(logger, "validate_inputs", "error", duration_ms)
        return {
            "is_valid": False,
            "error_message": f"Vaga inválida ou não encontrada: {job_path}",
        }

    duration_ms = (time.time() - start_time) * 1000
    log_node_complete(logger, "validate_inputs", "success", duration_ms)
    return {"is_valid": True, "error_message": None}


def sanitize_inputs(state: AgentState) -> AgentState:
    """Sanitiza textos de entrada contra prompt injection."""
    logger = get_logger(state.get("correlation_id"))
    start_time = time.time()

    log_node_start(
        logger,
        "sanitize_inputs",
        {
            "curriculum_length": len(state.get("curriculum_text", "")),
            "job_length": len(state.get("job_description", "")),
        },
    )

    injection_detected = []

    # Sanitizar curriculo se existir
    curriculum_text = state.get("curriculum_text", "")
    if curriculum_text:
        sanitized_curriculum, detected = sanitize_text(curriculum_text)
        if detected:
            injection_detected.extend([f"curriculum: {d}" for d in detected])
        state["curriculum_text"] = sanitized_curriculum

    # Sanitizar descricao da vaga se existir
    job_description = state.get("job_description", "")
    if job_description:
        sanitized_job, detected = sanitize_text(job_description)
        if detected:
            injection_detected.extend([f"job: {d}" for d in detected])
        state["job_description"] = sanitized_job

    # Atualizar metadata com injecoes detectadas
    metadata = state.get("metadata", {})
    if injection_detected:
        metadata["injection_detected"] = injection_detected
        metadata["sanitized"] = True
    state["metadata"] = metadata

    duration_ms = (time.time() - start_time) * 1000
    log_node_complete(
        logger,
        "sanitize_inputs",
        "success",
        duration_ms,
        {
            "injection_detected": len(injection_detected),
        },
    )

    return state


def request_approval(state: AgentState) -> AgentState:
    """Define que a analise requer aprovacao humana antes de salvar."""
    logger = get_logger(state.get("correlation_id"))
    log_node_start(logger, "request_approval", {})
    log_node_complete(logger, "request_approval", "success", 0)
    return {"approval_required": True}


def load_history(state: AgentState) -> AgentState:
    """
    Recupera historico de analises anteriores via checkpointer.

    Gera um correlation_id unico para observabilidade e inicializa
    metadata basica da execucao.
    """
    correlation_id = str(uuid.uuid4())
    now = datetime.now(UTC).isoformat()

    logger = get_logger(correlation_id)
    log_node_start(logger, "load_history", {})

    result = {
        "correlation_id": correlation_id,
        "history": state.get("history", []),
        "metadata": {
            "started_at": now,
            "correlation_id": correlation_id,
            "model": os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        },
    }

    log_node_complete(logger, "load_history", "success", 0)
    return result


def read_curriculum_node(state: AgentState) -> AgentState:
    """Lê o currículo em PDF usando a tool apropriada."""
    logger = get_logger(state.get("correlation_id"))
    start_time = time.time()

    log_node_start(
        logger,
        "read_curriculum",
        {
            "curriculum_path": state.get("curriculum_path", ""),
        },
    )

    try:
        text = read_curriculum(state["curriculum_path"])
        duration_ms = (time.time() - start_time) * 1000
        log_node_complete(
            logger,
            "read_curriculum",
            "success",
            duration_ms,
            {
                "text_length": len(text),
            },
        )
        return {"curriculum_text": text}
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        log_error(logger, "read_curriculum", e, duration_ms)
        return {"is_valid": False, "error_message": str(e)}


def read_job_node(state: AgentState) -> AgentState:
    """Lê a descrição da vaga usando a tool apropriada."""
    logger = get_logger(state.get("correlation_id"))
    start_time = time.time()

    log_node_start(
        logger,
        "read_job",
        {
            "job_path": state.get("job_path", ""),
        },
    )

    try:
        text = read_job(state["job_path"])
        duration_ms = (time.time() - start_time) * 1000
        log_node_complete(
            logger,
            "read_job",
            "success",
            duration_ms,
            {
                "text_length": len(text),
            },
        )
        return {"job_description": text}
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        log_error(logger, "read_job", e, duration_ms)
        return {"is_valid": False, "error_message": str(e)}


def extract_information(state: AgentState) -> AgentState:
    """Extrai informações do texto bruto para o formato estruturado (ExtractedInformation)."""
    logger = get_logger(state.get("correlation_id"))
    start_time = time.time()

    log_node_start(
        logger,
        "extract_information",
        {
            "curriculum_length": len(state.get("curriculum_text", "")),
            "job_length": len(state.get("job_description", "")),
        },
    )

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

        duration_ms = (time.time() - start_time) * 1000
        log_node_complete(
            logger,
            "extract_information",
            "success",
            duration_ms,
            {
                "model": os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            },
        )

        return {"extracted_information": extracted_dict}
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        log_error(logger, "extract_information", e, duration_ms)
        return {
            "is_valid": False,
            "error_message": f"Falha na extração de dados: {e!s}",
        }


def analyze_match(state: AgentState) -> AgentState:
    """Cruza as informações estruturadas para gerar a análise de compatibilidade."""
    logger = get_logger(state.get("correlation_id"))
    start_time = time.time()

    if not state.get("extracted_information"):
        duration_ms = (time.time() - start_time) * 1000
        log_node_complete(logger, "analyze_match", "error", duration_ms)
        return {
            "is_valid": False,
            "error_message": "Dados nao extraidos: extracted_information ausente",
        }

    log_node_start(
        logger,
        "analyze_match",
        {
            "model": os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        },
    )

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

        duration_ms = (time.time() - start_time) * 1000
        log_node_complete(
            logger,
            "analyze_match",
            "success",
            duration_ms,
            {
                "score": score,
            },
        )

        return {"analysis": analysis_text, "compatibility_score": score}
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        log_error(logger, "analyze_match", e, duration_ms)
        return {"is_valid": False, "error_message": f"Falha na análise: {e!s}"}


def generate_report(state: AgentState) -> AgentState:
    """Gera o relatório final. Como a análise já está em Markdown, apenas repassa."""
    logger = get_logger(state.get("correlation_id"))
    log_node_start(logger, "generate_report", {})
    log_node_complete(logger, "generate_report", "success", 0)
    return {"report": state.get("analysis", "")}


def save_report_node(state: AgentState) -> AgentState:
    """Salva o relatório em disco usando a tool de gravação."""
    logger = get_logger(state.get("correlation_id"))
    start_time = time.time()

    log_node_start(
        logger,
        "save_report",
        {
            "report_length": len(state.get("report", "")),
        },
    )

    success = save_report(state.get("report", ""))
    if not success:
        duration_ms = (time.time() - start_time) * 1000
        log_error(
            logger, "save_report", Exception("Falha ao salvar relatório"), duration_ms
        )
        return {
            "is_valid": False,
            "error_message": "Falha ao salvar relatório no disco.",
        }

    duration_ms = (time.time() - start_time) * 1000
    log_node_complete(logger, "save_report", "success", duration_ms)
    return {}
