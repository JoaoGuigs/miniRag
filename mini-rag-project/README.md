# Mini RAG Project

Projeto de estudo com RAG (Retrieval-Augmented Generation) usando FastAPI + Agno + Gemini + LanceDB.

## Visão geral

Este projeto permite:

- enviar PDFs para indexação semântica;
- consultar os documentos com perguntas em linguagem natural;
- manter memória curta de conversa por sessão.

O backend usa uma base vetorial para recuperar trechos relevantes dos PDFs e enviar contexto para o modelo antes de responder.

## Stack

- Python 3.13
- FastAPI + Uvicorn
- Agno (Agent, Knowledge, Reader)
- Gemini (modelo e embeddings)
- LanceDB (vetor DB local)
- SQLite (memória de sessões do agente)
- Frontend estático (`index.html` + `main.js`)

## Estrutura de pastas

```text
mini-rag-project/
├─ backend/
│  ├─ main.py            # rotas FastAPI e serving do frontend
│  ├─ config.py          # configuração de env, LanceDB e SQLite
│  ├─ agent_factory.py   # criação e configuração do Agent
│  └─ engine.py
├─ frontend/
│  ├─ index.html         # interface simples de upload/chat
│  └─ main.js            # chamadas para /upload e /chat
├─ storage/              # PDFs enviados (runtime)
├─ tmp/                  # LanceDB e sessões SQLite (runtime)
├─ requirements.txt
└─ .env
```

## Variáveis de ambiente

Crie um arquivo `.env` na raiz:

```env
GOOGLE_API_KEY=seu_token_aqui
```

Compatibilidade: o código também aceita `GEMINI_API_KEY`.

## Como rodar

No PowerShell:

```powershell
cd "C:\Users\joaog\OneDrive\Área de Trabalho\ProjRag"
.\.venv\Scripts\activate
cd mini-rag-project
pip install -r requirements.txt
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Abra no navegador:

- Frontend: `http://127.0.0.1:8000/`
- Docs da API: `http://127.0.0.1:8000/docs`

## Fluxo de uso

1. Envie um PDF na tela inicial.
2. O backend indexa o documento no LanceDB.
3. Faça perguntas no chat.
4. O agente recupera contexto da base vetorial e responde.

## Persistência de dados

Dados locais gerados em runtime:

- `tmp/lancedb`: embeddings/chunks dos documentos;
- `tmp/agno_sessions.db`: histórico de sessão para memória de conversa;
- `storage/`: arquivos PDF enviados.

## Notas de desenvolvimento

- O frontend envia `session_id` para separar memória entre sessões.
- A memória de conversa usa `add_history_to_context=True`.
- O RAG usa `search_knowledge=True` no Agent.

## Próximos passos sugeridos

- adicionar testes de API (`pytest`);
- mostrar fontes e páginas na resposta;
- melhorar tratamento de erros no frontend;
- criar endpoint para limpar sessão/conversa.
