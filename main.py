import datetime
from typing import Any

from fastapi import FastAPI, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from starlette import status
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from todo.todoData import TodoData
from todo.todoItem import TodoItem

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
todo_data = TodoData()


@app.get(path="/", status_code=status.HTTP_200_OK)
def home_page(request: Request):
    return templates.TemplateResponse("homePage.html", context={"request": request})


@app.get(path="/items", status_code=status.HTTP_200_OK)
def show_todo_items(request: Request):
    return templates.TemplateResponse("showTodoItems.html", context={"request": request, "items": todo_data.items})


@app.post(path="/items/add", status_code=status.HTTP_201_CREATED, response_model=TodoItem)
async def add_todo_items(request: Request, item: TodoItem):
    print(item)
    todo_data.addItem(TodoItem(title=item.title, description=item.description,
                               deadLine=item.deadLine))


@app.get(path="/items/add", status_code=status.HTTP_200_OK)
def add_todo_items(request: Request):
    return templates.TemplateResponse("addTodoItem.html", context={"request": request, "id": id(id)})


@app.get(path="/items/{todoId}", status_code=status.HTTP_200_OK)
def getItem(request: Request):
    return templates.TemplateResponse("todoItem.html", context={"request": request, "id": id(id)})


@app.delete(path="/items/{todoId}", status_code=status.HTTP_202_ACCEPTED)
def deleteItem(request: Request, todoId: int):
    todo_data.removeItem(todoId)


@app.patch(path="/items/{todoId}")
def updateItem(request: Request, item: TodoItem):# word: str = Form(...),
    todo_data.updateItem(item)
