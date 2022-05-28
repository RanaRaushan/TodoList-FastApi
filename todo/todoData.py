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


async def get_todo_manager(session: AsyncSession = Depends(get_async_session)):
    yield TodoDataService(session)
