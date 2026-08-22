"""Testes E2E para a API REST do CurriculoMatch AI."""

import io
import pytest
from fastapi.testclient import TestClient

from api.main import app


@pytest.fixture
def client():
    """Cria cliente de teste para a API."""
    return TestClient(app)


class TestE2EHealthCheck:
    """Testes E2E para health check."""

    def test_health_check_returns_200(self, client):
        """Testa que health check retorna 200."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_returns_json(self, client):
        """Testa que health check retorna JSON com campos corretos."""
        response = client.get("/health")
        data = response.json()

        assert "status" in data
        assert "database" in data
        assert "llm" in data
        assert "version" in data


class TestE2EAnalyze:
    """Testes E2E para analise de curriculo."""

    def test_analyze_requires_curriculum(self, client):
        """Testa que /analyze requer arquivo PDF."""
        response = client.post(
            "/analyze",
            data={
                "job_title": "Desenvolvedor Python",
                "job_description": "Vaga para desenvolvedor Python com Django",
            },
        )
        assert response.status_code == 422

    def test_analyze_requires_job_title(self, client):
        """Testa que /analyze requer titulo da vaga."""
        pdf_content = b"%PDF-1.4 fake content"
        response = client.post(
            "/analyze",
            files={
                "curriculum": (
                    "curriculo.pdf",
                    io.BytesIO(pdf_content),
                    "application/pdf",
                )
            },
            data={"job_description": "Vaga para desenvolvedor Python"},
        )
        assert response.status_code == 422

    def test_analyze_requires_job_description(self, client):
        """Testa que /analyze requer descricao da vaga."""
        pdf_content = b"%PDF-1.4 fake content"
        response = client.post(
            "/analyze",
            files={
                "curriculum": (
                    "curriculo.pdf",
                    io.BytesIO(pdf_content),
                    "application/pdf",
                )
            },
            data={"job_title": "Desenvolvedor Python"},
        )
        assert response.status_code == 422

    def test_analyze_rejects_non_pdf(self, client):
        """Testa que /analyze rejeita arquivos nao-PDF."""
        txt_content = b"Este nao e um PDF"
        response = client.post(
            "/analyze",
            files={
                "curriculum": ("curriculo.txt", io.BytesIO(txt_content), "text/plain")
            },
            data={
                "job_title": "Desenvolvedor Python",
                "job_description": "Vaga para desenvolvedor Python com Django",
            },
        )
        assert response.status_code == 422


class TestE2EBatch:
    """Testes E2E para analise em lote."""

    def test_batch_requires_curriculos(self, client):
        """Testa que /analyze/batch requer curriculos."""
        response = client.post(
            "/analyze/batch",
            data={
                "job_title": "Desenvolvedor Python",
                "job_description": "Vaga para desenvolvedor Python com Django",
            },
        )
        assert response.status_code == 422


class TestE2EHistory:
    """Testes E2E para historico."""

    def test_history_returns_200(self, client):
        """Testa que /history retorna 200."""
        response = client.get("/history")
        assert response.status_code == 200

    def test_history_returns_paginated_response(self, client):
        """Testa que /history retorna resposta paginada."""
        response = client.get("/history")
        data = response.json()

        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "pages" in data

    def test_history_with_pagination_params(self, client):
        """Testa /history com parametros de paginacao."""
        response = client.get("/history?page=1&limit=5")
        data = response.json()

        assert data["page"] == 1
        assert data["items"] == [] or len(data["items"]) <= 5


class TestE2EHistoryDetail:
    """Testes E2E para detalhes de analise."""

    def test_history_detail_not_found(self, client):
        """Testa que /history/{id} retorna 404 para ID inexistente."""
        response = client.get("/history/nonexistent-id-123")
        assert response.status_code == 404
