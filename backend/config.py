import os
from pathlib import Path
from typing import Tuple

from agno.knowledge.embedder.google import GeminiEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb
from agno.db.sqlite import SqliteDb
from dotenv import load_dotenv


def load_settings() -> str:
    """Carrega variáveis de ambiente e retorna a API key do Google/Gemini."""
    load_dotenv()
    google_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not google_api_key:
        raise RuntimeError("GOOGLE_API_KEY ou GEMINI_API_KEY não configurada no .env")
    return google_api_key


def create_vector_db(google_api_key: str) -> LanceDb:
    """Cria o banco vetorial LanceDb usado pelo Knowledge."""
    tmp_dir = Path("tmp")
    tmp_dir.mkdir(parents=True, exist_ok=True)

    return LanceDb(
        table_name="pdf_documents",
        uri=str(tmp_dir / "lancedb"),
        embedder=GeminiEmbedder(api_key=google_api_key),
    )


def create_session_db() -> SqliteDb:
    """Cria o banco SQLite usado para armazenar sessões/histórico do agente."""
    tmp_dir = Path("tmp")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    db_file = tmp_dir / "agno_sessions.db"
    return SqliteDb(db_file=str(db_file))


def create_knowledge(google_api_key: str) -> Tuple[Knowledge, SqliteDb]:
    """Convenience: retorna a Knowledge (LanceDb) e o banco de sessões."""
    vector_db = create_vector_db(google_api_key)
    session_db = create_session_db()
    knowledge = Knowledge(vector_db=vector_db)
    return knowledge, session_db

