"""Schemas Pydantic para request/response da API."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    """Request para analise individual de curriculo x vaga."""

    job_title: str = Field(
        ..., min_length=1, max_length=200, description="Titulo da vaga"
    )
    job_description: str = Field(..., min_length=10, description="Descricao da vaga")


class AnalysisResult(BaseModel):
    """Resultado de uma analise individual."""

    analysis_id: str = Field(..., description="ID unico da analise")
    candidate_name: str = Field(..., description="Nome do candidato")
    job_title: str = Field(..., description="Titulo da vaga")
    score: int = Field(..., ge=0, le=100, description="Score de aderencia (0-100)")
    report: str = Field(..., description="Relatorio completo em Markdown")
    status: str = Field(default="completed", description="Status da analise")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Data/hora da analise"
    )


class BatchResult(BaseModel):
    """Resultado de analise em lote."""

    batch_id: str = Field(..., description="ID unico do lote")
    results: List[AnalysisResult] = Field(
        default_factory=list, description="Resultados individuais"
    )
    ranking: List[str] = Field(
        default_factory=list, description="Ranking dos candidatos por score"
    )


class HistoryItem(BaseModel):
    """Item de historico de analises."""

    analysis_id: str = Field(..., description="ID da analise")
    candidate_name: str = Field(..., description="Nome do candidato")
    job_title: str = Field(..., description="Titulo da vaga")
    score: int = Field(..., ge=0, le=100, description="Score de aderencia")
    created_at: datetime = Field(..., description="Data/hora da analise")


class HistoryResponse(BaseModel):
    """Response paginada do historico."""

    items: List[HistoryItem] = Field(
        default_factory=list, description="Itens da pagina"
    )
    total: int = Field(..., description="Total de itens")
    page: int = Field(..., description="Pagina atual")
    pages: int = Field(..., description="Total de paginas")


class HealthResponse(BaseModel):
    """Response do health check."""

    status: str = Field(default="healthy", description="Status da API")
    database: str = Field(default="connected", description="Status do banco")
    llm: str = Field(default="available", description="Status do LLM")
    version: str = Field(default="1.0.0", description="Versao da API")


class ErrorResponse(BaseModel):
    """Response de erro padronizada."""

    detail: str = Field(..., description="Mensagem de erro")
