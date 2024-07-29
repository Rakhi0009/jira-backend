from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import  TaskCreate, TaskUpdateAssignee, TaskUpdateDescription, TaskUpdateStatus
from database import get_db
from curd import create_new_task, update_task_assignee, update_task_description, update_task_status, get_task_comment, get_task_by_id, soft_delete_task

router = APIRouter()

@router.post("/task/")
def create_task(task: TaskCreate, db: AsyncSession= Depends(get_db)):
    return create_new_task(task=task, db= db)

@router.put("/task/update_assignee/{task_id}")
def update_assignee(task_id: int, update: TaskUpdateAssignee, db: AsyncSession= Depends(get_db)):
    task_row = update_task_assignee(update= update, task_id= task_id, db= db)
    if not task_row:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_row

@router.put("/task/update_description/{task_id}")
def update_description(task_id: int, update: TaskUpdateDescription, db: AsyncSession= Depends(get_db)):
    task_row = update_task_description(update= update, task_id= task_id, db= db)
    if not task_row:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_row

@router.put("/task/update_status/{task_id}")
def update_status(task_id: int, update: TaskUpdateStatus, db: AsyncSession= Depends(get_db)):
    task_row = update_task_status(update= update, task_id= task_id, db= db)
    if not task_row:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_row

@router.get("/task/comment/{task_id}")
def get_comments(task_id: int, db: AsyncSession = Depends(get_db)):
    comment_rows = get_task_comment(task_id= task_id, db= db)
    if not comment_rows:
        raise HTTPException(status_code=404, detail="No comments found")
    return comment_rows

@router.delete("/task/{task_id}")
def delete_task(task_id: int, db: AsyncSession =Depends(get_db)):
    task_row = get_task_by_id(task_id=task_id, db=db)
    if not task_row:
        raise HTTPException(status_code=404, detail="No task found")
    return soft_delete_task(task_id=task_id, db=db)