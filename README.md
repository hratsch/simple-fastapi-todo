# Todo App – FastAPI + SvelteKit

A **full-stack Todo app** with:
- **FastAPI** backend (Python + `uv`)
- **SvelteKit** frontend (Vite, HMR)
- **JSON persistence** (`todos.json`)
- **CRUD + Edit mode**
- **Dark theme**, responsive, production-ready

---

## Features

- Add, toggle, edit, delete todos
- Inline edit with **Enter to save**, **Esc to cancel**
- Persistence via `todos.json`
- Clean, responsive UI with Flexbox
- Dark mode by default
- Deployable to Vercel (frontend) + any Python host (backend)

---

## Tech Stack

| Layer     | Tech                     |
|---------|--------------------------|
| Backend | FastAPI, `uv`, Python 3.11+ |
| Frontend| SvelteKit, Vite, Node ≥20.19 |
| Storage | `todos.json` (or upgrade to SQLite) |

---

## Project Structure

```
todo-api-uv/
├── backend/
│   ├── main.py         # FastAPI server
│   └── todos.json      # Persistent storage
├── frontend/
│   ├── src/
│   │   └── routes/+page.svelte  # Main UI
│   └── svelte.config.js
├── README.md
└── .gitignore
```

---

## Setup & Run Locally

### 1. Backend (FastAPI)

```bash
cd backend
uv sync
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
→ Runs on `http://localhost:8000`

### 2. Frontend (SvelteKit)

```bash
cd frontend
npm install
npm run dev
```
→ Runs on `http://localhost:5173` (HMR enabled)

Open [http://localhost:5173](http://localhost:5173)

---

## API Endpoints

| Method | URL            | Action              |
|-------|----------------|---------------------|
| GET   | `/todos`       | List all todos      |
| POST  | `/todos`       | Create todo         |
| PUT   | `/todos/{id}`  | Update (title/completed) |
| DELETE| `/todos/{id}`  | Delete todo         |

---

## Build & Deploy

### Frontend (Vercel)

```bash
cd frontend
npm run build
```

### Backend

Deploy `backend/` to:
- run locally with `uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000`

> Tip: Use `gunicorn` or `uvicorn` in production:
> ```bash
> uvicorn main:app --host 0.0.0.0 --port $PORT
> ```

---

## Persistence

Todos are saved to `backend/todos.json`.  
- Simple, transparent, reloads on restart
- Perfect for demos and learning
- For scale: replace with SQLite or PostgreSQL

---

## Development

```bash
# Start both (in separate terminals)
cd backend && uuv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
cd frontend && npm run dev
```

---

## License

MIT © Hugh Ratsch — Feel free to fork and improve!

---

## Made With

- [FastAPI](https://fastapi.tiangolo.com)
- [SvelteKit](https://kit.svelte.dev)
- [Vite](https://vitejs.dev)
- [uv](https://docs.astral.sh/uv/) for Python dependency management

---