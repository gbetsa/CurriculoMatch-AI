import os
from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver


def create_checkpointer() -> PostgresSaver:
    """
    Cria e retorna um PostgresSaver configurado via DATABASE_URL.

    O PostgresSaver gerencia automaticamente as tabelas:
    - checkpoints: snapshots de estado por thread_id
    - checkpoint_writes: mutacoes individuais por no
    - checkpoint_blobs: binarios serializados (texto CV, relatorio)

    Returns:
        PostgresSaver: Checkpointer configurado e pronto para uso.
    """
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/curriculomatch",
    )

    pool = ConnectionPool(
        database_url,
        min_size=1,
        max_size=10,
    )

    return PostgresSaver(pool)
