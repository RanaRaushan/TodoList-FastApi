import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Date

from todo.core.database import Base


class TodoListTable(Base):
    __tablename__ = "todolist"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True, unique=True, nullable=False)
    description = Column(String, nullable=False)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    modified = Column(DateTime, default=datetime.datetime.utcnow)
    deadLine = Column(Date)
    active = Column(Boolean)
