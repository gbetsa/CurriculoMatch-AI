import os
from typing import Optional
from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver


def create_checkpointer() -> Optional[PostgresSaver]:
    """
    Cria e retorna um PostgresSaver configurado via DATABASE_URL.

    O PostgresSaver gerencia automaticamente as tabelas:
    - checkpoints: snapshots de estado por thread_id
    - checkpoint_writes: mutacoes individuais por no
    - checkpoint_blobs: binarios serializados (texto CV, relatorio)

    Returns:
        PostgresSaver: Checkpointer configurado e pronto para uso.
        None: Se DATABASE_URL nao estiver configurada.
    """
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        return None

    # Usar ConnectionPool com autocommit para evitar problemas com CREATE INDEX CONCURRENTLY
    pool = ConnectionPool(
        database_url,
        min_size=1,
        max_size=10,
        kwargs={"autocommit": True},
    )

    checkpointer = PostgresSaver(pool)
    checkpointer.setup()

    return checkpointer
