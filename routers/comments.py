from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import  CommentCreate, CommentUpdateDescription
from database import get_db
from curd import create_new_comment, update_comment_description, get_comment_by_id, soft_delete_comment

router = APIRouter()

@router.post("/comment/")
def create_task(comment: CommentCreate, db: AsyncSession= Depends(get_db)):
    return create_new_comment(comment=comment, db= db)

@router.put("/comment/update_description/{comment_id}")
def update_description(comment_id: int, update: CommentUpdateDescription, db: AsyncSession= Depends(get_db)):
    comment_row = update_comment_description(update= update, comment_id= comment_id, db= db)
    if not comment_row:
        raise HTTPException(status_code=404, detail="Task not found")
    return comment_row

@router.delete("/comment/{comment_id}")
def delete_comment(comment_id: int, db: AsyncSession =Depends(get_db)):
    task_row = get_comment_by_id(comment_id=comment_id, db=db)
    if not task_row:
        raise HTTPException(status_code=404, detail="No comment found")
    return soft_delete_comment(comment_id=comment_id, db=db)