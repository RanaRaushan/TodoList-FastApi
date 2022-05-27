import datetime

from todo.todoItem import TodoItemList, TodoItem


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
        return tuple(self.items.dataList)

    def addItem(self, item: TodoItem):
        item.id_ = self.id_
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
            if self.items[index].id_ == todoId:
                updatedItem.id_ = todoId
                self.items[index] = updatedItem
                break
        return None

    def getItem(self, itemId: int):
        for item in self.items:
            if item.id_ == itemId:
                return item
        return None
