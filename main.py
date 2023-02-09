from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from todo.core.database import create_db_and_tables
from todo.todoData import get_todo_manager, TodoDataService
from todo.core.schemas.todoItem import TodoItem

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup():
    # create db tables
    await create_db_and_tables()


# @app.get(path="/", status_code=status.HTTP_200_OK)
# def home_page(request: Request):
#     return templates.TemplateResponse("homePage.html", context={"request": request})


@app.get(path="/items", status_code=status.HTTP_200_OK)
async def show_todo_items(request: Request, todoService: TodoDataService = Depends(get_todo_manager)):
    items = await todoService.getItems()
    return items
    # return templates.TemplateResponse("showTodoItems.html", context={"request": request, "items": items})


@app.post(path="/items/add-update", status_code=status.HTTP_201_CREATED, response_model=TodoItem)
async def add_todo_items(item: TodoItem, todoService: TodoDataService = Depends(get_todo_manager)):
    await todoService.addItem(TodoItem(title=item.title, description=item.description, deadLine=item.deadLine))


# @app.get(path="/items/add-update", status_code=status.HTTP_200_OK)
# def add_todo_items(request: Request):
    # return templates.TemplateResponse("addTodoItem.html", context={"request": request, "todoItem": None})


@app.get(path="/items/add-update/{todoId}", status_code=status.HTTP_200_OK)
async def add_todo_items(request: Request, todoId: int, todoService: TodoDataService = Depends(get_todo_manager)):
    item = await todoService.getItem(todoId)
    return item
    # return templates.TemplateResponse("addTodoItem.html", context={"request": request, "todoItem": item})


@app.get(path="/items/{todoId}", status_code=status.HTTP_200_OK)
async def getItem(request: Request, todoId: int, todoService: TodoDataService = Depends(get_todo_manager)):
    item = await todoService.getItem(todoId)
    return item
    # return templates.TemplateResponse("todoItem.html", context={"request": request, "todoItem": item})


@app.delete(path="/items/{todoId}", status_code=status.HTTP_202_ACCEPTED)
async def deleteItem(todoId: int, todoService: TodoDataService = Depends(get_todo_manager)):
    await todoService.removeItem(todoId)


@app.patch(path="/items/{todoId}", response_model=TodoItem)
async def updateItem(todoId: int, item: TodoItem, todoService: TodoDataService = Depends(get_todo_manager)):
    await todoService.updateItem(todoId, item)
