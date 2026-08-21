import os
import pytest
import psycopg
from graph.checkpointer import create_checkpointer


def is_postgres_available():
    """Check if PostgreSQL is available."""
    try:
        conn = psycopg.connect(
            "postgresql://postgres:postgres@localhost:5432/curriculomatch",
            connect_timeout=3,
        )
        conn.close()
        return True
    except (psycopg.OperationalError, psycopg.DatabaseError):
        return False


requires_postgres = pytest.mark.skipif(
    not is_postgres_available(),
    reason="PostgreSQL not available",
)


@requires_postgres
def test_checkpointer_creation():
    """Test that checkpointer can be created when DATABASE_URL is set."""
    os.environ["DATABASE_URL"] = (
        "postgresql://postgres:postgres@localhost:5432/curriculomatch"
    )
    checkpointer = create_checkpointer()
    assert checkpointer is not None


def test_checkpointer_none_without_database_url():
    """Test that checkpointer returns None when DATABASE_URL is not set."""
    # Save original value
    original_value = os.environ.get("DATABASE_URL")

    # Remove DATABASE_URL if it exists
    if "DATABASE_URL" in os.environ:
        del os.environ["DATABASE_URL"]

    checkpointer = create_checkpointer()
    assert checkpointer is None

    # Restore original value
    if original_value:
        os.environ["DATABASE_URL"] = original_value


@requires_postgres
def test_checkpointer_tables_created():
    """Test that checkpointer creates required tables."""
    os.environ["DATABASE_URL"] = (
        "postgresql://postgres:postgres@localhost:5432/curriculomatch"
    )
    checkpointer = create_checkpointer()

    conn = psycopg.connect(
        "postgresql://postgres:postgres@localhost:5432/curriculomatch"
    )
    cur = conn.cursor()

    # Check if tables exist
    cur.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_name IN ('checkpoints', 'checkpoint_writes', 'checkpoint_blobs')
    """)
    tables = [row[0] for row in cur.fetchall()]

    assert "checkpoints" in tables
    assert "checkpoint_writes" in tables
    assert "checkpoint_blobs" in tables

    cur.close()
    conn.close()


@requires_postgres
def test_checkpointer_config_structure():
    """Test that checkpointer has the expected configuration structure."""
    os.environ["DATABASE_URL"] = (
        "postgresql://postgres:postgres@localhost:5432/curriculomatch"
    )
    checkpointer = create_checkpointer()

    # Verify checkpointer has the expected attributes
    assert hasattr(checkpointer, "put")
    assert hasattr(checkpointer, "get")
    assert hasattr(checkpointer, "get_tuple")
    assert hasattr(checkpointer, "list")
    assert hasattr(checkpointer, "setup")
