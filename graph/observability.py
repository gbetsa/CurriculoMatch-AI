"""Configuracao de logs estruturados com structlog para observabilidade."""

import os
import sys
from datetime import datetime, timezone
from typing import Optional

import structlog


def setup_structlog():
    """Configura structlog para logs JSON estruturados."""
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    # Mapear nome do level para numero
    level_map = {
        "DEBUG": 10,
        "INFO": 20,
        "WARNING": 30,
        "ERROR": 40,
        "CRITICAL": 50,
    }
    level_number = level_map.get(log_level, 20)

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(level_number),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=True,
    )


def get_logger(correlation_id: Optional[str] = None):
    """
    Retorna um logger estruturado com correlation_id opcional.

    Args:
        correlation_id: ID de correlacao para rastrear execucoes.

    Returns:
        Logger configurado com structlog.
    """
    if correlation_id:
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(correlation_id=correlation_id)

    return structlog.get_logger()


def log_node_start(logger, node_name: str, input_summary: dict):
    """Loga o inicio de um node do grafo."""
    logger.info(
        "node_started",
        node=node_name,
        input_summary=input_summary,
    )


def log_node_complete(
    logger,
    node_name: str,
    status: str = "success",
    duration_ms: Optional[float] = None,
    extra_data: Optional[dict] = None,
):
    """Loga a conclusao de um node do grafo."""
    log_data = {
        "node": node_name,
        "status": status,
        "duration_ms": duration_ms,
    }
    if extra_data:
        log_data.update(extra_data)

    logger.info("node_completed", **log_data)


def log_error(logger, node_name: str, error: Exception, duration_ms: Optional[float] = None):
    """Loga um erro em um node do grafo."""
    logger.error(
        "node_error",
        node=node_name,
        error_type=type(error).__name__,
        error_message=str(error),
        duration_ms=duration_ms,
    )


def log_llm_call(
    logger,
    model: str,
    tokens_used: Optional[dict] = None,
    duration_ms: Optional[float] = None,
    status: str = "success",
):
    """Loga uma chamada ao LLM."""
    log_data = {
        "model": model,
        "status": status,
        "duration_ms": duration_ms,
    }
    if tokens_used:
        log_data["tokens_used"] = tokens_used

    logger.info("llm_call", **log_data)


# Configurar structlog ao importar o modulo
setup_structlog()
