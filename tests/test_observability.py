"""Testes de observabilidade e resiliencia."""

import tempfile
from unittest.mock import MagicMock

import pytest

from graph.observability import (
    get_logger,
    log_error,
    log_llm_call,
    log_node_complete,
    log_node_start,
    setup_structlog,
)


class TestStructlogSetup:
    """Testes para configuracao do structlog."""

    def test_setup_structlog_no_error(self):
        """Testa que setup_structlog nao levanta erros."""
        setup_structlog()

    def test_get_logger_returns_logger(self):
        """Testa que get_logger retorna um logger."""
        logger = get_logger()
        assert logger is not None

    def test_get_logger_with_correlation_id(self):
        """Testa que get_logger aceita correlation_id."""
        logger = get_logger(correlation_id="test-123")
        assert logger is not None


class TestLogNodeStart:
    """Testes para funcao log_node_start."""

    def test_log_node_start_no_error(self):
        """Testa que log_node_start nao levanta erros."""
        logger = get_logger()
        log_node_start(logger, "test_node", {"key": "value"})

    def test_log_node_start_with_empty_summary(self):
        """Testa que log_node_start aceita resumo vazio."""
        logger = get_logger()
        log_node_start(logger, "test_node", {})


class TestLogNodeComplete:
    """Testes para funcao log_node_complete."""

    def test_log_node_complete_success(self):
        """Testa log de conclusao com sucesso."""
        logger = get_logger()
        log_node_complete(logger, "test_node", "success", 100.5)

    def test_log_node_complete_with_extra_data(self):
        """Testa log de conclusao com dados extras."""
        logger = get_logger()
        log_node_complete(logger, "test_node", "success", 100.5, {"score": 85})

    def test_log_node_complete_error_status(self):
        """Testa log de conclusao com status de erro."""
        logger = get_logger()
        log_node_complete(logger, "test_node", "error", 50.0)


class TestLogError:
    """Testes para funcao log_error."""

    def test_log_error_no_exception(self):
        """Testa que log_error nao levanta erros."""
        logger = get_logger()
        error = Exception("Test error")
        log_error(logger, "test_node", error, 100.0)

    def test_log_error_with_custom_exception(self):
        """Testa log_error com excecao customizada."""
        logger = get_logger()
        error = ValueError("Invalid value")
        log_error(logger, "test_node", error, 50.0)


class TestLogLlmCall:
    """Testes para funcao log_llm_call."""

    def test_log_llm_call_success(self):
        """Testa log de chamada LLM com sucesso."""
        logger = get_logger()
        log_llm_call(logger, "llama-3.3-70b-versatile", status="success")

    def test_log_llm_call_with_tokens(self):
        """Testa log de chamada LLM com informacoes de tokens."""
        logger = get_logger()
        tokens = {"prompt": 100, "completion": 50}
        log_llm_call(
            logger, "llama-3.3-70b-versatile", tokens_used=tokens, duration_ms=250.0
        )

    def test_log_llm_call_error(self):
        """Testa log de chamada LLM com erro."""
        logger = get_logger()
        log_llm_call(logger, "llama-3.3-70b-versatile", status="error")


class TestResilienceModule:
    """Testes para o modulo de resiliencia."""

    def test_import_resilience(self):
        """Testa que o modulo resilience pode ser importado."""
        from graph.resilience import call_llm_with_fallback, call_llm_with_retry

        assert call_llm_with_retry is not None
        assert call_llm_with_fallback is not None

    def test_call_llm_with_retry_success(self):
        """Testa call_llm_with_retry com LLM mockado que retorna sucesso."""
        from graph.resilience import call_llm_with_retry

        mock_llm = MagicMock()
        mock_llm.invoke.return_value = MagicMock(content="Test response")

        result = call_llm_with_retry(mock_llm, "test prompt", "test-model")
        assert result is not None
        mock_llm.invoke.assert_called_once()

    def test_call_llm_with_retry_failure_then_success(self):
        """Testa call_llm_with_retry com falha na primeira tentativa."""
        from graph.resilience import call_llm_with_retry

        mock_llm = MagicMock()
        mock_llm.invoke.side_effect = [
            ConnectionError("Connection failed"),
            MagicMock(content="Test response"),
        ]

        result = call_llm_with_retry(mock_llm, "test prompt", "test-model")
        assert result is not None
        assert mock_llm.invoke.call_count == 2

    def test_call_llm_with_retry_all_failures(self):
        """Testa call_llm_with_retry com todas as tentativas falhando."""
        from tenacity import RetryError

        from graph.resilience import call_llm_with_retry

        mock_llm = MagicMock()
        mock_llm.invoke.side_effect = ConnectionError("Connection failed")

        with pytest.raises(RetryError):
            call_llm_with_retry(mock_llm, "test prompt", "test-model")

    def test_call_llm_with_fallback_primary_success(self):
        """Testa call_llm_with_fallback com LLM primario funcionando."""
        from graph.resilience import call_llm_with_fallback

        mock_primary = MagicMock()
        mock_primary.invoke.return_value = MagicMock(content="Primary response")

        mock_fallback = MagicMock()

        result = call_llm_with_fallback(
            mock_primary, mock_fallback, "test prompt", "primary", "fallback"
        )
        assert result is not None
        mock_primary.invoke.assert_called_once()
        mock_fallback.invoke.assert_not_called()

    def test_call_llm_with_fallback_primary_fails(self):
        """Testa call_llm_with_fallback com LLM primario falhando."""
        from graph.resilience import call_llm_with_fallback

        mock_primary = MagicMock()
        mock_primary.invoke.side_effect = ConnectionError("Connection failed")

        mock_fallback = MagicMock()
        mock_fallback.invoke.return_value = MagicMock(content="Fallback response")

        result = call_llm_with_fallback(
            mock_primary, mock_fallback, "test prompt", "primary", "fallback"
        )
        assert result is not None
        mock_fallback.invoke.assert_called_once()


class TestAnalyzeExecutionScript:
    """Testes para o script de investigacao."""

    def test_import_script(self):
        """Testa que o script pode ser importado."""
        from scripts.analyze_execution import (
            analyze_execution,
            filter_by_correlation_id,
            generate_report,
            load_logs,
        )

        assert load_logs is not None
        assert filter_by_correlation_id is not None
        assert analyze_execution is not None
        assert generate_report is not None

    def test_load_logs_empty_dir(self):
        """Testa load_logs com diretorio vazio."""
        from scripts.analyze_execution import load_logs

        with tempfile.TemporaryDirectory() as tmpdir:
            logs = load_logs(tmpdir)
            assert logs == []

    def test_load_logs_nonexistent_dir(self):
        """Testa load_logs com diretorio inexistente."""
        from scripts.analyze_execution import load_logs

        logs = load_logs("/nonexistent/path")
        assert logs == []

    def test_filter_by_correlation_id(self):
        """Testa filter_by_correlation_id com logs de exemplo."""
        from scripts.analyze_execution import filter_by_correlation_id

        logs = [
            {"correlation_id": "abc-123", "event": "node_started"},
            {"correlation_id": "def-456", "event": "node_started"},
            {"correlation_id": "abc-123", "event": "node_completed"},
        ]

        filtered = filter_by_correlation_id(logs, "abc-123")
        assert len(filtered) == 2
        assert all(log["correlation_id"] == "abc-123" for log in filtered)

    def test_analyze_execution_empty_logs(self):
        """Testa analyze_execution com logs vazios."""
        from scripts.analyze_execution import analyze_execution

        result = analyze_execution([])
        assert "error" in result

    def test_analyze_execution_with_logs(self):
        """Testa analyze_execution com logs de exemplo."""
        from scripts.analyze_execution import analyze_execution

        logs = [
            {
                "timestamp": "2026-08-22T14:30:00.000Z",
                "correlation_id": "test-123",
                "event": "node_started",
                "node": "validate_inputs",
            },
            {
                "timestamp": "2026-08-22T14:30:00.100Z",
                "correlation_id": "test-123",
                "event": "node_completed",
                "node": "validate_inputs",
                "status": "success",
                "duration_ms": 100,
            },
        ]

        result = analyze_execution(logs)
        assert result["correlation_id"] == "test-123"
        assert len(result["nodes"]) == 1
        assert result["nodes"][0]["name"] == "validate_inputs"
        assert result["total_duration_ms"] == 100

    def test_generate_report(self):
        """Testa generate_report com analise de exemplo."""
        from scripts.analyze_execution import generate_report

        analysis = {
            "correlation_id": "test-123",
            "started_at": "2026-08-22T14:30:00.000Z",
            "ended_at": "2026-08-22T14:30:01.000Z",
            "total_duration_ms": 1000,
            "nodes": [
                {
                    "name": "validate_inputs",
                    "status": "success",
                    "duration_ms": 100,
                }
            ],
            "errors": [],
        }

        report = generate_report(analysis)
        assert "test-123" in report
        assert "validate_inputs" in report
        assert "success" in report
