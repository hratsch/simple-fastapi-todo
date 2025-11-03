from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Todo(BaseModel):
    title: str
    completed: bool = False

todos = []

# Create a new todo item
todos.append({"id": 1, "title": "Learn FastAPI", "completed": False})

@app.get("/")
def read_root():
    return {"message": "Hello from Todo API!"}

@app.get("/todos")
def get_todos():
    return todos

@app.post("/todos")
def create_todo(todo: Todo):
    new_todo = {
        "id": len(todos) + 1,
        "title": todo.title,
        "completed": todo.completed
    }
    todos.append(new_todo)
    return new_todo

@app.delete("/todos/{id}")
def delete_todo(id: int):
    for i, todo in enumerate(todos):
        if todo["id"] == id:
            deleted = todos.pop(i)
            return {"message": f"Todo '{deleted['title']}' deleted!"}
    raise HTTPException(status_code=404, detail="Todo not found")
    
@app.put("/todos/{id}")
def update_todo(id: int, updated_todo: Todo):
    for i, todo in enumerate(todos):
        if todo["id"] == id:
            todos[i] = {
                "id": id,
                "title": updated_todo.title,
                "completed": updated_todo.completed
            }
            return todos[i]
    raise HTTPException(status_code=404, detail="Todo not found")