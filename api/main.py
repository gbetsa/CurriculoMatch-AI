"""API REST principal para o CurriculoMatch AI."""

import os
import uuid
from datetime import datetime

from fastapi import FastAPI, File, Form, HTTPException, Query, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from api.dependencies import get_graph, validate_file_upload
from api.schemas import (
    AnalysisResult,
    BatchResult,
    ErrorResponse,
    HealthResponse,
    HistoryResponse,
)

app = FastAPI(
    title="CurriculoMatch AI API",
    description="API para analise de compatibilidade entre curriculos e vagas",
    version="1.0.0",
)

# CORS para permitir Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Tratador de erros padronizado."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": str(exc.detail)},
    )


@app.post(
    "/analyze",
    response_model=AnalysisResult,
    responses={422: {"model": ErrorResponse}},
    summary="Analise individual de curriculo x vaga",
)
async def analyze_curriculum(
    curriculum: UploadFile = File(..., description="Arquivo PDF do curriculo"),
    job_title: str = Form(
        ..., min_length=1, max_length=200, description="Titulo da vaga"
    ),
    job_description: str = Form(..., min_length=10, description="Descricao da vaga"),
):
    """
    Analisa a compatibilidade entre um curriculo (PDF) e uma descricao de vaga.

    - **curriculum**: Arquivo PDF do curriculo (max 10MB)
    - **job_title**: Titulo da vaga
    - **job_description**: Descricao detalhada da vaga
    """
    # Rate limit
    # Em producao, usar request.client.host

    # Validar arquivo
    validate_file_upload(curriculum)

    # Salvar curriculo temporariamente
    analysis_id = str(uuid.uuid4())
    temp_path = f"temp_{analysis_id}.pdf"

    try:
        content = await curriculum.read()
        with open(temp_path, "wb") as f:
            f.write(content)

        # Executar grafo
        graph = get_graph()
        initial_state = {
            "curriculum_path": temp_path,
            "job_path": None,
            "job_title": job_title,
            "job_description": job_description,
            "is_valid": True,
        }

        result = graph.invoke(initial_state)

        # Extrair nome do candidato
        candidate_name = "Candidato"
        if result.get("extracted_curriculum"):
            candidate_name = (
                result["extracted_curriculum"].get("name", "Candidato") or "Candidato"
            )

        return AnalysisResult(
            analysis_id=analysis_id,
            candidate_name=candidate_name,
            job_title=job_title,
            score=result.get("match_analysis", {}).get("score", 0),
            report=result.get("report", ""),
            status="completed",
            created_at=datetime.now(),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar analise: {e!s}")
    finally:
        # Limpar arquivo temporario
        if os.path.exists(temp_path):
            os.remove(temp_path)


@app.post(
    "/analyze/batch",
    response_model=BatchResult,
    summary="Analise em lote de multiplas vagas",
)
async def analyze_batch(
    curriculos: list[UploadFile] = File(..., description="Lista de curriculos PDF"),
    job_title: str = Form(
        ..., min_length=1, max_length=200, description="Titulo da vaga"
    ),
    job_description: str = Form(..., min_length=10, description="Descricao da vaga"),
):
    """
    Analisa multiplos curriculos em relacao a uma mesma vaga.

    Retorna ranking dos candidatos por score de aderencia.
    """
    batch_id = str(uuid.uuid4())
    results = []

    for curriculum in curriculos:
        validate_file_upload(curriculum)

        analysis_id = str(uuid.uuid4())
        temp_path = f"temp_{analysis_id}.pdf"

        try:
            content = await curriculum.read()
            with open(temp_path, "wb") as f:
                f.write(content)

            graph = get_graph()
            initial_state = {
                "curriculum_path": temp_path,
                "job_path": None,
                "job_title": job_title,
                "job_description": job_description,
                "is_valid": True,
            }

            result = graph.invoke(initial_state)

            candidate_name = "Candidato"
            if result.get("extracted_curriculum"):
                candidate_name = (
                    result["extracted_curriculum"].get("name", "Candidato")
                    or "Candidato"
                )

            results.append(
                AnalysisResult(
                    analysis_id=analysis_id,
                    candidate_name=candidate_name,
                    job_title=job_title,
                    score=result.get("match_analysis", {}).get("score", 0),
                    report=result.get("report", ""),
                    status="completed",
                    created_at=datetime.now(),
                )
            )

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    # Ordenar por score (decrescente)
    results.sort(key=lambda x: x.score, reverse=True)
    ranking = [r.candidate_name for r in results]

    return BatchResult(
        batch_id=batch_id,
        results=results,
        ranking=ranking,
    )


@app.get(
    "/history",
    response_model=HistoryResponse,
    summary="Lista historico de analises",
)
async def list_history(
    page: int = Query(1, ge=1, description="Pagina"),
    limit: int = Query(10, ge=1, le=100, description="Itens por pagina"),
    candidate_name: str | None = Query(None, description="Filtrar por nome"),
    job_title: str | None = Query(None, description="Filtrar por titulo da vaga"),
):
    """
    Lista analises anteriores com paginacao e filtros.

    - **page**: Pagina actual (default: 1)
    - **limit**: Itens por pagina (1-100, default: 10)
    - **candidate_name**: Filtrar por nome do candidato
    - **job_title**: Filtrar por titulo da vaga
    """
    # Em producao, buscar do checkpointer/PostgreSQL
    # Por agora, retornar lista vazia
    return HistoryResponse(
        items=[],
        total=0,
        page=page,
        pages=0,
    )


@app.get(
    "/history/{analysis_id}",
    response_model=AnalysisResult,
    responses={404: {"model": ErrorResponse}},
    summary="Detalhes de uma analise",
)
async def get_analysis(analysis_id: str):
    """
    Retorna detalhes de uma analise especifica pelo ID.

    - **analysis_id**: ID da analise
    """
    # Em producao, buscar do checkpointer/PostgreSQL
    raise HTTPException(status_code=404, detail="Analise nao encontrada")


class ApprovalRequest(BaseModel):
    """Request para aprovacao de analise."""

    approved: bool = Field(..., description="Se a analise foi aprovada")


@app.post(
    "/approve/{analysis_id}",
    response_model=AnalysisResult,
    responses={404: {"model": ErrorResponse}},
    summary="Aprova ou rejeita uma analise pendente",
)
async def approve_analysis(analysis_id: str, request: ApprovalRequest):
    """
    Endpoint para aprovacao humana de analises.

    - **analysis_id**: ID da analise a ser aprovada
    - **approved**: True para aprovar, False para rejeitar
    """
    # Em producao, buscar do checkpointer/PostgreSQL
    # Por agora, retornar erro 404 (analise nao encontrada)
    if not request.approved:
        raise HTTPException(status_code=400, detail="Analise rejeitada pelo usuario")

    # Se aprovada, retornar status atualizado
    return AnalysisResult(
        analysis_id=analysis_id,
        candidate_name="Candidato",
        job_title="Vaga",
        score=0,
        report="",
        status="approved",
        created_at=datetime.now(),
    )


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check da API",
)
async def health_check():
    """
    Verifica saude da API, banco de dados e LLM.

    Retorna status de cada componente.
    """
    database_status = "connected"
    llm_status = "available"

    # Verificar banco
    try:
        from graph.checkpointer import create_checkpointer

        checkpointer = create_checkpointer()
        if checkpointer is None:
            database_status = "not_configured"
    except Exception:
        database_status = "disconnected"

    # Verificar LLM
    try:
        from dotenv import load_dotenv

        load_dotenv()
        if not os.getenv("GROQ_API_KEY"):
            llm_status = "not_configured"
    except Exception:
        llm_status = "unavailable"

    return HealthResponse(
        status="healthy",
        database=database_status,
        llm=llm_status,
        version="1.0.0",
    )
