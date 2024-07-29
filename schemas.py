from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email_address: str
    password: str

class UserCreate(UserBase):
    pass

class UserLogin(BaseModel):
    email_address: str
    password: str

class JiraBoardBase(BaseModel):
    created_by: int
    title: str
    created_time: datetime
    board_status: str

class JiraBoardCreate(JiraBoardBase):
    pass

class JiraBoardUpdateTitle(BaseModel):
    title: str

class JiraBoardUpdateStatus(BaseModel):
    board_status: str

class TaskBase(BaseModel):
    jira_board_id: int
    task_description: str
    task_reporter: int
    task_assignee: Optional[int] = None
    task_status: Optional[str] 

class TaskCreate(TaskBase):
    pass

class TaskUpdateAssignee(BaseModel):
    task_assignee: str

class TaskUpdateDescription(BaseModel):
    task_description: str

class TaskUpdateStatus(BaseModel):
    task_status: str

class CommentBase(BaseModel):
    task_id: int
    description: str
    commented_by: int
    created_time: datetime

class CommentCreate(CommentBase):
    pass

class CommentUpdateDescription(BaseModel):
    description: str