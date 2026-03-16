import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from agno.agent import Agent
from agno.models.google import Gemini
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.knowledge.embedder.google import GeminiEmbedder
from agno.vectordb.lancedb import LanceDb
from agno.db.sqlite import SqliteDb
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Configuração de chaves e banco vetorial
google_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

vector_db = LanceDb(
    table_name="pdf_documents",
    uri="tmp/lancedb",
    # evita usar o OpenAIEmbedder padrão e usa Gemini para embeddings
    embedder=GeminiEmbedder(api_key=google_api_key),
)

# 2. Banco de sessões para memória de conversa (SQLite local)
session_db = SqliteDb(db_file="tmp/agno_sessions.db")

# 3. Criar a base de conhecimento (PDFs no LanceDb)
knowledge = Knowledge(vector_db=vector_db)

# 4. Agente com base de conhecimento + memória de conversa
agent = Agent(
    model=Gemini(id="gemini-2.5-flash", api_key=google_api_key),
    knowledge=knowledge,
    search_knowledge=True,  # consulta o banco vetorial automaticamente
    db=session_db,  # salva histórico de mensagens
    add_history_to_context=True,  # injeta histórico no contexto
    num_history_runs=2,  # quantas interações anteriores entram no contexto
    instructions=[
        "Você é um assistente especializado nos documentos do usuário.",
        "Sempre consulte a base de conhecimento antes de responder.",
        "Responda em Português Brasileiro.",
    ],
    markdown=True,
)

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    os.makedirs("storage", exist_ok=True)
    file_path = f"storage/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 4. Inserir o conteúdo do PDF usando o PDFReader oficial
    knowledge.insert(
        path=file_path,
        reader=PDFReader(),
    )
    
    return {"message": f"PDF {file.filename} processado com sucesso!"}

@app.post("/chat")
async def chat(pergunta: str):
    # O agent.run cuida de buscar no banco e formular a resposta
    response = agent.run(pergunta)
    return {"response": response.content}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)