from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import  JiraBoardCreate, JiraBoardUpdateTitle, JiraBoardUpdateStatus
from database import get_db
from curd import create_new_board, update_board_title, update_board_status, get_jira_board_task, get_board_info, get_jira_boards, soft_delete_jira_board, get_board_by_id

router = APIRouter()

@router.post("/jira_board/")
def create_jira_board(board: JiraBoardCreate, db: AsyncSession = Depends(get_db)):
    return create_new_board(board= board, db= db)

@router.get("/jira_board/")
def get_all_jira_boards(db: AsyncSession = Depends(get_db)):
    return get_jira_boards(db=db)

@router.put("/jira_board/title/{jira_board_id: int}")
def update_jira_board_title(board_id: int, update:JiraBoardUpdateTitle, db: AsyncSession = Depends(get_db)):
    board_row = update_board_title(update= update, board_id= board_id, db= db)
    if not board_row:
        raise HTTPException(status_code=404, detail="Jira board not found")
    return board_row

@router.put("/jira_board/status/{jira_board_id: int}")
def update_jira_board_status(board_id: int, update:JiraBoardUpdateStatus, db: AsyncSession = Depends(get_db)):
    board_row = update_board_status(update= update, board_id= board_id, db= db)
    if not board_row:
        raise HTTPException(status_code=404, detail="Jira board not found")
    return board_row

@router.get("/jira_board/tasks/{board_id}")
def get_tasks(board_id: int, db: AsyncSession= Depends(get_db)):
    task_rows = get_jira_board_task(board_id=board_id, db=db)
    if not task_rows:
        raise HTTPException(status_code=404, detail="No tasks found")
    return task_rows 

@router.get("/jira_board/info/{board_id}")
def get_jira_board_info(board_id: int, db:AsyncSession = Depends(get_db)):
    board_row = get_board_info(board_id=board_id, db=db)
    if not board_row:
        raise HTTPException(status_code=404, detail="No board Found")
    return board_row

@router.delete("/jira_board/{board_id}")
def delete_board(board_id: int, db: AsyncSession =Depends(get_db)):
    board_row = get_board_by_id(board_id=board_id, db=db)
    if not board_row:
        raise HTTPException(status_code=404, detail="No board found")
    return soft_delete_jira_board(board_id=board_id, db=db)
