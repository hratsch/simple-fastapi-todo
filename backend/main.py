from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Svelte dev port 
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class Todo(BaseModel):
    title: str
    completed: bool = False

TODOS_FILE = "todos.json"

# Load todos from file if it exists
def load_todos():
    if os.path.exists(TODOS_FILE):
        with open(TODOS_FILE, "r") as f:
            return json.load(f)
    return [{"id": 1, "title": "Learn FastAPI", "completed": False}]

# Save todos to file
def save_todos(todos):
    with open(TODOS_FILE, "w") as f:
        json.dump(todos, f, indent=2)

# Load todos at startup
todos = load_todos()

@app.get("/")
def read_root():
    return {"message": "Hello from Todo API! We are now persistent."}

@app.get("/todos")
def get_todos():
    return todos

@app.post("/todos")
def create_todo(todo: Todo):
    global todos
    new_todo = {
        "id": len(todos) + 1,
        "title": todo.title,
        "completed": todo.completed
    }
    todos.append(new_todo)
    save_todos(todos)
    return new_todo

@app.delete("/todos/{id}")
def delete_todo(id: int):
    global todos
    for i, todo in enumerate(todos):
        if todo["id"] == id:
            deleted = todos.pop(i)
            save_todos(todos)
            return {"message": f"Todo '{deleted['title']}' deleted!"}
    raise HTTPException(status_code=404, detail="Todo not found")
    
@app.put("/todos/{id}")
def update_todo(id: int, updated_todo: Todo):
    global todos
    for i, todo in enumerate(todos):
        if todo["id"] == id:
            todos[i] = {
                "id": id,
                "title": updated_todo.title,
                "completed": updated_todo.completed
            }
            save_todos (todos)
            return todos[i]
    raise HTTPException(status_code=404, detail="Todo not found")