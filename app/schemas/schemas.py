from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, Json
from flask_openapi3 import FileStorage

class UploadFileForm(BaseModel):
    file: FileStorage

class Pagination(BaseModel):
    limit: int = 100
    offset: int = 0

class ById(BaseModel):
    id: int = Field(..., description='id')

class Task(BaseModel):
    id: Optional[int]
    task_is: str
    data: Json
    date:datetime

    class Config:
        orm_mode = True

class TaskList(BaseModel):
    task_list: List[Task]

    class Config:
        orm_mode = True

class Transaction(BaseModel):
    
    id: Optional[int]
    name: str
    graph1: float
    graph2: float
    graph3: float
    date:datetime

    class Config:
        orm_mode = True

class TransactionList(BaseModel):
    transaction_list: List[Transaction]

    class Config:
        orm_mode = True

