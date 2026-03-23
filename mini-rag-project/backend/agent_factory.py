from agno.agent import Agent
from agno.models.google import Gemini
from agno.knowledge.knowledge import Knowledge
from agno.db.sqlite import SqliteDb


def create_agent(knowledge: Knowledge, session_db: SqliteDb, google_api_key: str) -> Agent:
    """Cria e configura o Agent do Agno/Gemini usado pela API."""
    return Agent(
        model=Gemini(id="gemini-2.5-flash", api_key=google_api_key),
        knowledge=knowledge,
        search_knowledge=True,
        db=session_db,
        add_history_to_context=True,
        num_history_runs=2,
        instructions=[
    "Você é um assistente que SEMPRE cita fontes.",
    "Para cada resposta, identifique de qual arquivo e página a informação veio.",
    "Formato esperado: 'Sua resposta aqui. (Fonte: arquivo.pdf, pág. X)'.",
    "Se o documento não tiver a resposta, não invente nada."
        ],
        markdown=True,
    )

