import datetime

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from todo.core.database import get_async_session
from todo.core.models.model import TodoListTable
from todo.core.schemas.todoItem import TodoItemList, TodoItem


class TodoDataService:
    items: TodoItemList = TodoItemList()

    def __init__(self, session: AsyncSession):
        self.session = session

    async def getItems(self):
        todo_table = select(TodoListTable).where(TodoListTable.active == True)
        results = await self.session.execute(todo_table)
        results = list(map(lambda res: res[0], results.all()))
        self.items.from_orm_list(results)
        return tuple(self.items)

    async def addItem(self, item: TodoItem):
        todo_table = TodoListTable(**item.dict())
        self.session.add(todo_table)
        await self.session.commit()

    async def removeItem(self, itemId: int):
        item: TodoListTable = await self.session.get(TodoListTable, itemId)
        if not item:
            raise ValueError("Item doesn't exist")
        item.active = False
        self.session.add(item)
        await self.session.commit()

    async def updateItem(self, todoId: int, updatedItem: TodoItem):
        updatedItem.id = todoId
        item: TodoListTable = await self.session.get(TodoListTable, todoId)
        for k, v in updatedItem:
            setattr(item, k, v)
        item.modified = datetime.datetime.utcnow()
        self.session.add(item)
        await self.session.commit()

    async def getItem(self, itemId: int):
        if not self.items:
            await self.getItems()
        for item in self.items:
            if item.id == itemId:
                return item

        return None


class TodoData:
    id_: int = 1
    items: TodoItemList = TodoItemList()

    def __init__(self):
        self.addItem(TodoItem(title="first", description="first desc", deadLine=datetime.date.today()))
        self.addItem(TodoItem(title="second", description="second desc", deadLine=datetime.date.today()))
        self.addItem(TodoItem(title="3rd", description="3rd desc", deadLine=datetime.date.today()))
        self.addItem(TodoItem(title="4th", description="4th desc", deadLine=datetime.date.today()))
        self.addItem(TodoItem(title="5th", description="5th desc", deadLine=datetime.date.today()))

    def getItems(self):
        return tuple(self.items)

    def addItem(self, item: TodoItem):
        item.id = self.id_
        self.items.append(item)
        self.id_ += 1

    def removeItem(self, itemId: int):
        item = self.getItem(itemId)
        if item:
            self.items.remove(item)
        else:
            raise ValueError("Item doesn't exist")

    def updateItem(self, todoId: int, updatedItem: TodoItem):
        for index in range(len(self.items)):
            if self.items[index].id == todoId:
                updatedItem.id = todoId
                self.items[index] = updatedItem
                break
        return None

    def getItem(self, itemId: int):
        for item in self.items:
            if item.id == itemId:
                return item
        return None


async def get_todo_manager(session: AsyncSession = Depends(get_async_session)):
    yield TodoDataService(session)
