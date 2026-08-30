"""API REST principal para o CurriculoMatch AI."""

import os
import re
import uuid
from datetime import datetime

import psycopg
from dotenv import load_dotenv

load_dotenv()

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
    HistoryItem,
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
    temp_curr_path = f"temp_curriculum_{analysis_id}.pdf"
    temp_job_path = f"temp_job_{analysis_id}.txt"

    try:
        content = await curriculum.read()
        with open(temp_curr_path, "wb") as f:
            f.write(content)

        with open(temp_job_path, "w", encoding="utf-8") as f:
            f.write(job_description)

        # Executar grafo
        graph = get_graph()
        initial_state = {
            "curriculum_path": temp_curr_path,
            "job_path": temp_job_path,
            "job_title": job_title,
            "job_description": job_description,
            "is_valid": True,
        }

        config = {"configurable": {"thread_id": analysis_id}}
        result = graph.invoke(initial_state, config=config)

        # Verificar se o grafo bloqueou a analise (injection detectado)
        if not result.get("is_valid") and result.get("error_message"):
            return JSONResponse(
                status_code=200,
                content={
                    "_blocked": True,
                    "_stage": "api_injection",
                    "detail": result["error_message"],
                },
            )

        # Extrair nome do candidato
        candidate_name = "Candidato"
        if result.get("candidate_name"):
            candidate_name = result["candidate_name"]
        elif result.get("extracted_information"):
            extracted = result["extracted_information"]
            candidate_name = extracted.get("candidato", {}).get("nome", "Candidato")

        return AnalysisResult(
            analysis_id=analysis_id,
            candidate_name=candidate_name,
            job_title=job_title,
            score=result.get("compatibility_score", 0),
            report=result.get("report", ""),
            status="completed",
            created_at=datetime.now(),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar analise: {e!s}")
    finally:
        # Limpar arquivos temporarios
        for p in (temp_curr_path, temp_job_path):
            if os.path.exists(p):
                os.remove(p)


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

    try:
        for curriculum in curriculos:
            analysis_id = str(uuid.uuid4())
            temp_curr_path = f"temp_curriculum_{analysis_id}.pdf"
            temp_job_path = f"temp_job_{analysis_id}.txt"

            try:
                validate_file_upload(curriculum)

                content = await curriculum.read()
                with open(temp_curr_path, "wb") as f:
                    f.write(content)

                with open(temp_job_path, "w", encoding="utf-8") as f:
                    f.write(job_description)

                graph = get_graph()
                initial_state = {
                    "curriculum_path": temp_curr_path,
                    "job_path": temp_job_path,
                    "job_title": job_title,
                    "job_description": job_description,
                    "is_valid": True,
                }

                config = {"configurable": {"thread_id": analysis_id}}
                result = graph.invoke(initial_state, config=config)

                # Verificar se o grafo bloqueou a analise (injection detectado)
                if not result.get("is_valid") and result.get("error_message"):
                    continue

                candidate_name = "Candidato"
                if result.get("candidate_name"):
                    candidate_name = result["candidate_name"]
                elif result.get("extracted_information"):
                    extracted = result["extracted_information"]
                    candidate_name = extracted.get("candidato", {}).get(
                        "nome", "Candidato"
                    )

                results.append(
                    AnalysisResult(
                        analysis_id=analysis_id,
                        candidate_name=candidate_name,
                        job_title=job_title,
                        score=result.get("compatibility_score", 0),
                        report=result.get("report", ""),
                        status="completed",
                        created_at=datetime.now(),
                    )
                )

            except Exception as e:
                import structlog

                logger = structlog.get_logger()
                logger.error(
                    "batch_analysis_error", curriculum=curriculum.filename, error=str(e)
                )
                continue
            finally:
                for p in (temp_curr_path, temp_job_path):
                    if os.path.exists(p):
                        os.remove(p)

    except Exception as e:
        import structlog

        logger = structlog.get_logger()
        logger.error("batch_processing_error", error=str(e))
        raise HTTPException(
            status_code=500, detail=f"Erro no processamento em lote: {e!s}"
        )

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
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        return HistoryResponse(items=[], total=0, page=page, pages=0)

    try:
        conn = psycopg.connect(database_url)
        cur = conn.cursor()

        # Buscar checkpoints unicos (cada thread_id = 1 analise)
        query = """
            SELECT DISTINCT thread_id
            FROM checkpoints
            WHERE thread_id NOT LIKE 'test-%'
            ORDER BY thread_id
        """
        cur.execute(query)
        thread_ids = [row[0] for row in cur.fetchall()]

        items = []
        for tid in thread_ids:
            # Buscar ultimo checkpoint da thread
            cur.execute(
                """
                SELECT checkpoint FROM checkpoints
                WHERE thread_id = %s
                ORDER BY checkpoint_id DESC LIMIT 1
                """,
                (tid,),
            )
            row = cur.fetchone()
            if not row:
                continue

            cp = row[0]
            # O checkpoint contem o estado final do grafo
            state = cp.get("channel_values", {})

            score = state.get("compatibility_score", 0)
            report = state.get("report", "")
            created = cp.get("ts", "")

            candidate = state.get("candidate_name", "")
            if not candidate:
                # Extrair do report: "# Análise de Compatibilidade: <Nome> vs"
                match = re.search(r"Compatibilidade:\s*(.+?)\s+vs", report)
                if match:
                    candidate = match.group(1).strip().strip("*")
                else:
                    candidate = "Candidato"
            job = state.get("job_description", "")[:50]
            # Tentar pegar titulo estruturado
            ei = state.get("extracted_information")
            if ei and isinstance(ei, dict):
                vaga = ei.get("vaga", {})
                if isinstance(vaga, dict) and vaga.get("cargo"):
                    job = vaga["cargo"]

            # Filtrar se necessario
            if candidate_name and candidate_name.lower() not in candidate.lower():
                continue
            if job_title and job_title.lower() not in job.lower():
                continue

            items.append(
                HistoryItem(
                    analysis_id=tid,
                    candidate_name=candidate,
                    job_title=job,
                    score=score,
                    created_at=created,
                )
            )

        cur.close()
        conn.close()

        # Paginacao
        total = len(items)
        pages = max(1, (total + limit - 1) // limit)
        start = (page - 1) * limit
        end = start + limit
        paginated = items[start:end]

        return HistoryResponse(items=paginated, total=total, page=page, pages=pages)

    except Exception:
        return HistoryResponse(items=[], total=0, page=page, pages=0)


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
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise HTTPException(status_code=404, detail="Analise nao encontrada")

    try:
        conn = psycopg.connect(database_url)
        cur = conn.cursor()

        cur.execute(
            """
            SELECT checkpoint FROM checkpoints
            WHERE thread_id = %s
            ORDER BY checkpoint_id DESC LIMIT 1
            """,
            (analysis_id,),
        )
        row = cur.fetchone()

        cur.close()
        conn.close()

        if not row:
            raise HTTPException(status_code=404, detail="Analise nao encontrada")

        cp = row[0]
        state = cp.get("channel_values", {})

        return AnalysisResult(
            analysis_id=analysis_id,
            candidate_name=state.get("candidate_name", "Candidato"),
            job_title=state.get("job_title", ""),
            score=state.get("compatibility_score", 0),
            report=state.get("report", ""),
            status="completed" if state.get("is_valid", True) else "failed",
            created_at=cp.get("ts", ""),
        )

    except HTTPException:
        raise
    except Exception:
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
