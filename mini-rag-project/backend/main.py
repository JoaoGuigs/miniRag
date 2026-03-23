from pathlib import Path

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from agno.knowledge.reader.pdf_reader import PDFReader

from .config import load_settings, create_knowledge
from .agent_factory import create_agent
import os
app = FastAPI()
PROJECT_ROOT = Path(__file__).resolve().parents[1]
FRONTEND_DIR = PROJECT_ROOT / "frontend"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Configuração de chaves e componentes de infraestrutura
google_api_key = load_settings()
knowledge, session_db = create_knowledge(google_api_key)

# 2. Agente com base de conhecimento + memória de conversa
agent = create_agent(knowledge=knowledge, session_db=session_db, google_api_key=google_api_key)

app.mount("/frontend", StaticFiles(directory=str(FRONTEND_DIR)), name="frontend")


@app.get("/")
async def index():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/main.js")
async def frontend_main_js():
    return FileResponse(FRONTEND_DIR / "main.js")

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    os.makedirs("storage", exist_ok=True)
    file_path = f"storage/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    custom_reader = PDFReader(chunk=True, chunk_size=500, chunk_overlap=50)
    # 4. Inserir o conteúdo do PDF usando o PDFReader oficial
    knowledge.insert(
        path=file_path,
        reader=custom_reader,
    )
    
    return {"message": f"PDF {file.filename} processado com sucesso!"}

@app.post("/chat")
async def chat(pergunta: str, session_id: str):
    # O agent.run cuida de buscar no banco e formular a resposta
    response = agent.run(pergunta, search_knowledge=True, session_id=session_id)
    return {"response": response.content}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)