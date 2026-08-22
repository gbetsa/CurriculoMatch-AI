"""Wrapper de resiliencia para chamadas LLM com retry, timeout e fallback."""

import os
from typing import Optional

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from graph.observability import get_logger, log_llm_call


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((ConnectionError, TimeoutError)),
)
def call_llm_with_retry(llm, prompt, model_name: str = "unknown"):
    """
    Chama o LLM com retry automatico em caso de falhas de conexao.

    Args:
        llm: Instancia do modelo LLM (ChatGroq, etc.)
        prompt: Prompt a ser enviado
        model_name: Nome do modelo para logs

    Returns:
        Resposta do LLM

    Raises:
        Exception: Se todas as tentativas falharem
    """
    logger = get_logger()

    try:
        result = llm.invoke(prompt)

        # Log de sucesso
        log_llm_call(
            logger,
            model=model_name,
            status="success",
        )

        return result

    except Exception as e:
        # Log de erro
        log_llm_call(
            logger,
            model=model_name,
            status="error",
        )
        raise


def call_llm_with_fallback(
    primary_llm,
    fallback_llm,
    prompt,
    primary_model: str = "primary",
    fallback_model: str = "fallback",
):
    """
    Chama o LLM primario com fallback para secundario em caso de falha.

    Args:
        primary_llm: LLM primario (ex: Groq)
        fallback_llm: LLM fallback (ex: Ollama local)
        prompt: Prompt a ser enviado
        primary_model: Nome do LLM primario para logs
        fallback_model: Nome do LLM fallback para logs

    Returns:
        Resposta do LLM (primario ou fallback)
    """
    logger = get_logger()

    try:
        result = call_llm_with_retry(primary_llm, prompt, primary_model)
        return result
    except Exception as e:
        logger.warning(
            "llm_fallback_triggered",
            primary_model=primary_model,
            fallback_model=fallback_model,
            error=str(e),
        )

        # Tentar fallback
        try:
            result = fallback_llm.invoke(prompt)
            log_llm_call(
                logger,
                model=fallback_model,
                status="fallback_success",
            )
            return result
        except Exception as fallback_error:
            log_llm_call(
                logger,
                model=fallback_model,
                status="fallback_error",
            )
            raise fallback_error
