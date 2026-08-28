"""Consulta compartilhada de historico de analises no PostgreSQL."""

import os
import re

import psycopg
from dotenv import load_dotenv

load_dotenv()

from graph.state import AnalysisRecord


def query_similar_analyses(
    candidate_name: str = "",
    job_title: str = "",
    score: int = 0,
    limit: int = 5,
) -> list[AnalysisRecord]:
    """Busca analises anteriores similares no PostgreSQL.

    Extrai candidato e cargo do report (que esta em channel_values).
    Prioriza:
    1. Mesmo candidato (nome exato ou parcial)
    2. Mesmo cargo/titulo da vaga
    3. Mesmo cargo com score proximo (±10)

    Retorna no maximo `limit` registros, deduplicados.
    """
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        return []

    conn = None
    try:
        conn = psycopg.connect(database_url)
        cur = conn.cursor()

        cur.execute(
            """
            SELECT DISTINCT thread_id
            FROM checkpoints
            WHERE thread_id NOT LIKE 'test-%'
            ORDER BY thread_id
        """
        )
        thread_ids = [row[0] for row in cur.fetchall()]

        records: list[tuple[int, AnalysisRecord]] = []

        for tid in thread_ids:
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
            state = cp.get("channel_values", {})

            report = state.get("report", "")
            score_val = state.get("compatibility_score", 0)
            created = cp.get("ts", "")

            # Extrair candidato e cargo do report
            cand = ""
            job = ""
            if report:
                match = re.search(
                    r"Compatibilidade:\s*(.+?)\s+vs\s+(.+?)(?:\n|$)", report
                )
                if match:
                    cand = match.group(1).strip().strip("*")
                    job = match.group(2).strip().strip("*")

            record = AnalysisRecord(
                analysis_id=tid,
                candidate_name=cand,
                job_title=job,
                score=score_val,
                report=report[:500],
                created_at=created,
                correlation_id=state.get("correlation_id", ""),
            )

            priority = 0
            if candidate_name and cand and (
                candidate_name.lower() in cand.lower()
                or cand.lower() in candidate_name.lower()
            ):
                priority += 100
            if job_title and job and (
                job_title.lower() in job.lower()
                or job.lower() in job_title.lower()
            ):
                priority += 50
            if score and score_val and abs(score - score_val) <= 10:
                priority += 25

            if priority > 0:
                records.append((priority, record))

        cur.close()
        conn.close()

        records.sort(key=lambda x: x[0], reverse=True)
        return [r for _, r in records[:limit]]

    except Exception:
        if conn:
            conn.close()
        return []
