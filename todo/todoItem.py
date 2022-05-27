import datetime
from typing import List, Optional, Any

from pydantic import BaseModel


class TodoItem(BaseModel):
    id_: Optional[int]
    title: str
    description: str
    deadLine: datetime.date


class TodoItemList:
    dataList: List[TodoItem]

    def __init__(self):
        self.dataList = []

    def __len__(self):
        return self.dataList.__len__()

    def __add__(self, other):
        return self.dataList.__add__(other)

    def __getitem__(self, item):
        return self.dataList.__getitem__(item)

    def __setitem__(self, key, value):
        return self.dataList.__setitem__(key, value)

    def insert(self, i, v):
        self.dataList.insert(i, v)

    def append(self, v):
        self.dataList.append(v)

    def remove(self, v):
        self.dataList.remove(v)
