"""Testes para o modulo de consulta de historico."""

from unittest.mock import MagicMock, patch

from graph.history_query import query_similar_analyses


class TestQuerySimilarAnalyses:
    """Testes para query_similar_analyses."""

    @patch("graph.history_query.psycopg.connect")
    @patch("graph.history_query.os.getenv")
    def test_returns_empty_when_no_database(self, mock_getenv, mock_connect):
        mock_getenv.return_value = None
        result = query_similar_analyses(candidate_name="Joao")
        assert result == []

    @patch("graph.history_query.psycopg.connect")
    @patch("graph.history_query.os.getenv")
    def test_returns_empty_on_connection_error(self, mock_getenv, mock_connect):
        mock_getenv.return_value = "postgresql://localhost/test"
        mock_connect.side_effect = Exception("Connection failed")
        result = query_similar_analyses(candidate_name="Joao")
        assert result == []

    @patch("graph.history_query.psycopg.connect")
    @patch("graph.history_query.os.getenv")
    def test_returns_matching_candidate(self, mock_getenv, mock_connect):
        mock_getenv.return_value = "postgresql://localhost/test"

        mock_cur = MagicMock()
        mock_cur.fetchall.return_value = [("thread-1",)]
        mock_cur.fetchone.return_value = (
            {
                "channel_values": {
                    "report": "# Analise de Compatibilidade: Joao Silva vs Dev Python",
                    "compatibility_score": 82,
                    "extracted_information": {"vaga": {"cargo": "Dev Python"}},
                },
                "ts": "2026-08-20T10:00:00",
            },
        )

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cur
        mock_connect.return_value = mock_conn

        result = query_similar_analyses(
            candidate_name="Joao Silva", job_title="", score=0
        )
        assert len(result) == 1
        assert result[0].candidate_name == "Joao Silva"
        assert result[0].score == 82

    @patch("graph.history_query.psycopg.connect")
    @patch("graph.history_query.os.getenv")
    def test_returns_empty_when_no_matches(self, mock_getenv, mock_connect):
        mock_getenv.return_value = "postgresql://localhost/test"

        mock_cur = MagicMock()
        mock_cur.fetchall.return_value = [("thread-1",)]
        mock_cur.fetchone.return_value = (
            {
                "channel_values": {
                    "report": "# Analise de Compatibilidade: Maria vs Designer",
                    "compatibility_score": 60,
                    "extracted_information": {"vaga": {"cargo": "Designer"}},
                },
                "ts": "2026-08-20T10:00:00",
            },
        )

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cur
        mock_connect.return_value = mock_conn

        result = query_similar_analyses(
            candidate_name="Pedro", job_title="Dev Python", score=80
        )
        assert result == []

    @patch("graph.history_query.psycopg.connect")
    @patch("graph.history_query.os.getenv")
    def test_returns_matching_job_title(self, mock_getenv, mock_connect):
        mock_getenv.return_value = "postgresql://localhost/test"

        mock_cur = MagicMock()
        mock_cur.fetchall.return_value = [("thread-2",)]
        mock_cur.fetchone.return_value = (
            {
                "channel_values": {
                    "report": "# Analise de Compatibilidade: Ana vs Dev Python",
                    "compatibility_score": 75,
                    "extracted_information": {"vaga": {"cargo": "Desenvolvedor Python"}},
                },
                "ts": "2026-08-19T10:00:00",
            },
        )

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cur
        mock_connect.return_value = mock_conn

        result = query_similar_analyses(
            candidate_name="Pedro", job_title="Python", score=0
        )
        assert len(result) == 1
        assert result[0].job_title == "Dev Python"

    @patch("graph.history_query.psycopg.connect")
    @patch("graph.history_query.os.getenv")
    def test_limit_results(self, mock_getenv, mock_connect):
        mock_getenv.return_value = "postgresql://localhost/test"

        mock_cur = MagicMock()
        # 3 threads
        mock_cur.fetchall.return_value = [
            ("t1",),
            ("t2",),
            ("t3",),
        ]

        # Retornar dados diferentes para cada thread
        results_data = [
            (
                {
                    "channel_values": {
                        "report": "# Analise de Compatibilidade: Joao vs Dev",
                        "compatibility_score": 80,
                        "extracted_information": {"vaga": {"cargo": "Dev"}},
                    },
                    "ts": "2026-08-20T10:00:00",
                },
            ),
            (
                {
                    "channel_values": {
                        "report": "# Analise de Compatibilidade: Joao vs Dev",
                        "compatibility_score": 75,
                        "extracted_information": {"vaga": {"cargo": "Dev"}},
                    },
                    "ts": "2026-08-19T10:00:00",
                },
            ),
            (
                {
                    "channel_values": {
                        "report": "# Analise de Compatibilidade: Joao vs Dev",
                        "compatibility_score": 70,
                        "extracted_information": {"vaga": {"cargo": "Dev"}},
                    },
                    "ts": "2026-08-18T10:00:00",
                },
            ),
        ]
        mock_cur.fetchone.side_effect = results_data

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cur
        mock_connect.return_value = mock_conn

        result = query_similar_analyses(
            candidate_name="Joao", job_title="Dev", score=80, limit=2
        )
        assert len(result) == 2
