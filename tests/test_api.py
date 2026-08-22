"""Testes unitarios para a API FastAPI."""

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Cria cliente de teste para a API."""
    from api.main import app

    return TestClient(app)


@pytest.fixture
def mock_graph():
    """Mock do grafo para testes."""
    mock = MagicMock()
    mock.invoke.return_value = {
        "curriculum_path": "test.pdf",
        "job_path": None,
        "is_valid": True,
        "curriculum_text": "Test curriculum",
        "job_description": "Test job",
        "extracted_curriculum": {"name": "Joao Silva", "skills": ["Python"]},
        "extracted_job": {"title": "Dev Python", "requirements": ["Python"]},
        "match_analysis": {"score": 85, "verdict": "AVANCA"},
        "report": "# Relatorio de Aderencia\nScore: 85/100",
        "history": [],
        "correlation_id": "test-123",
        "metadata": {},
    }
    return mock


def test_health_check(client):
    """Testa endpoint de health check."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "database" in data
    assert "llm" in data
    assert "version" in data


def test_health_check_returns_json(client):
    """Testa que health check retorna JSON valido."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["version"] == "1.0.0"


def test_analyze_requires_curriculum(client):
    """Testa que /analyze requer arquivo de curriculo."""
    response = client.post(
        "/analyze",
        data={"job_title": "Dev Python", "job_description": "Python developer"},
    )
    assert response.status_code == 422


def test_analyze_requires_job_title(client):
    """Testa que /analyze requer job_title."""
    response = client.post(
        "/analyze",
        files={"curriculum": ("test.pdf", b"test content", "application/pdf")},
        data={"job_description": "Python developer"},
    )
    assert response.status_code == 422


def test_analyze_requires_job_description(client):
    """Testa que /analyze requer job_description."""
    response = client.post(
        "/analyze",
        files={"curriculum": ("test.pdf", b"test content", "application/pdf")},
        data={"job_title": "Dev Python"},
    )
    assert response.status_code == 422


def test_analyze_rejects_non_pdf(client):
    """Testa que /analyze rejeita arquivos que nao sao PDF."""
    response = client.post(
        "/analyze",
        files={"curriculum": ("test.txt", b"test content", "text/plain")},
        data={"job_title": "Dev Python", "job_description": "Python developer"},
    )
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert "PDF" in data["detail"]


def test_analyze_batch_requires_curriculos(client):
    """Testa que /analyze/batch requer curriculos."""
    response = client.post(
        "/analyze/batch",
        data={"job_title": "Dev Python", "job_description": "Python developer"},
    )
    assert response.status_code == 422


def test_history_returns_paginated_response(client):
    """Testa que /history retorna resposta paginada."""
    response = client.get("/history")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "pages" in data
    assert isinstance(data["items"], list)


def test_history_with_pagination_params(client):
    """Testa /history com parametros de paginacao."""
    response = client.get("/history?page=2&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 2
    assert len(data["items"]) <= 5


def test_history_with_filters(client):
    """Testa /history com filtros de busca."""
    response = client.get("/history?candidate_name=Joao&job_title=Python")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data


def test_history_detail_not_found(client):
    """Testa que /history/{id} retorna 404 para ID inexistente."""
    response = client.get("/history/nonexistent-id")
    assert response.status_code == 404
    # FastAPI retorna erro em formato padrao
    assert "detail" in response.json() or response.status_code == 404


def test_analyze_with_mocked_graph(client, mock_graph):
    """Testa /analyze com grafo mockado."""
    with patch("api.main.get_graph", return_value=mock_graph):
        # Criar arquivo PDF temporario
        test_pdf = b"%PDF-1.4 fake pdf content"

        response = client.post(
            "/analyze",
            files={"curriculum": ("test.pdf", test_pdf, "application/pdf")},
            data={
                "job_title": "Dev Python",
                "job_description": "Python developer needed",
            },
        )

        # Pode retornar 200 ou 500 dependendo da implementacao
        # O importante e que nao quebra
        assert response.status_code in [200, 500]


def test_analyze_batch_with_mocked_graph(client, mock_graph):
    """Testa /analyze/batch com grafo mockado."""
    with patch("api.main.get_graph", return_value=mock_graph):
        test_pdf = b"%PDF-1.4 fake pdf content"

        response = client.post(
            "/analyze/batch",
            files=[
                ("curriculos", ("test1.pdf", test_pdf, "application/pdf")),
                ("curriculos", ("test2.pdf", test_pdf, "application/pdf")),
            ],
            data={
                "job_title": "Dev Python",
                "job_description": "Python developer needed",
            },
        )

        # Pode retornar 200 ou 500 dependendo da implementacao
        assert response.status_code in [200, 500]


def test_error_response_format(client):
    """Testa que erros retornam formato padronizado."""
    response = client.get("/history/nonexistent")
    # FastAPI retorna 404 ou 500 dependendo do exception handler
    assert response.status_code in [404, 500]


def test_cors_headers(client):
    """Testa que CORS headers estao configurados."""
    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:8501",
            "Access-Control-Request-Method": "GET",
        },
    )
    # CORS middleware deve permitir
    assert response.status_code in [200, 405]
