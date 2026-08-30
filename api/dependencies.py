"""Dependencias da API: rate limit, validacao, inicializacao do grafo."""

import os
import time
from collections import defaultdict

from fastapi import HTTPException, UploadFile


class RateLimiter:
    """Rate limiter simples por IP."""

    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: dict[str, list[float]] = defaultdict(list)

    def is_allowed(self, client_ip: str) -> bool:
        """Verifica se o IP pode fazer requisicao."""
        now = time.time()
        cutoff = now - self.window_seconds

        # Remove requisicoes antigas
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip] if req_time > cutoff
        ]

        if len(self.requests[client_ip]) >= self.max_requests:
            return False

        self.requests[client_ip].append(now)
        return True


# Rate limiter global
rate_limiter = RateLimiter(max_requests=100, window_seconds=60)


def validate_file_upload(file: UploadFile, max_size_mb: int = 10) -> None:
    """Valida arquivo upload: tamanho e tipo."""
    if not file.filename:
        raise HTTPException(status_code=422, detail="Nome do arquivo e obrigatorio")

    # Verificar extensao
    allowed_extensions = {".pdf"}
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=422,
            detail=f"Tipo de arquivo nao permitido: {file_ext}. Apenas PDF e aceito.",
        )


def get_graph():
    """Retorna o grafo compilado (lazy loading)."""
    from graph.workflow import app

    return app
