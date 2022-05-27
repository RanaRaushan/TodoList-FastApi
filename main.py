from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from starlette import status
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
    return templates.TemplateResponse("showTodoItems.html", context={"request": request, "items": todo_data.getItems()})


@app.post(path="/items/add-update", status_code=status.HTTP_201_CREATED, response_model=TodoItem)
async def add_todo_items(item: TodoItem):
    todo_data.addItem(TodoItem(title=item.title, description=item.description, deadLine=item.deadLine))


@app.get(path="/items/add-update", status_code=status.HTTP_200_OK)
def add_todo_items(request: Request):
    return templates.TemplateResponse("addTodoItem.html", context={"request": request, "todoItem": None})


@app.get(path="/items/add-update/{todoId}", status_code=status.HTTP_200_OK)
def add_todo_items(request: Request, todoId: int):
    item = todo_data.getItem(todoId)
    return templates.TemplateResponse("addTodoItem.html", context={"request": request, "todoItem": item})


@app.get(path="/items/{todoId}", status_code=status.HTTP_200_OK)
def getItem(request: Request, todoId: int):
    item = todo_data.getItem(todoId)
    return templates.TemplateResponse("todoItem.html", context={"request": request, "todoItem": item})


@app.delete(path="/items/{todoId}", status_code=status.HTTP_202_ACCEPTED)
def deleteItem(todoId: int):
    todo_data.removeItem(todoId)


@app.patch(path="/items/{todoId}", response_model=TodoItem)
def updateItem(todoId: int, item: TodoItem):
    todo_data.updateItem(todoId, item)

