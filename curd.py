from datetime import datetime
from passlib.context import CryptContext
from sqlalchemy.orm import Session, joinedload
from models import User, JiraBoard, Task, Comment
from schemas import UserCreate, JiraBoardCreate, TaskCreate, CommentCreate, JiraBoardUpdateTitle, JiraBoardUpdateStatus, TaskUpdateAssignee, TaskUpdateDescription, TaskUpdateStatus, CommentUpdateDescription

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(email_address: str, db: Session):
    return db.query(User).filter(User.email_address==email_address, User.deleted_at.is_(None)).first()

def get_user_by_id(user_id: str, db: Session):
    return db.query(User).filter(User.id==user_id, User.deleted_at.is_(None)).first()

def create_new_user(user:UserCreate, db:Session):
    new_user = User(name= user.name, email_address= user.email_address, password= pwd_context.hash(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def soft_delete_user(user_id: int, db:Session):
    user_row = db.query(User).filter(User.id == user_id).first()
    if not user_row:
        return None
    user_row.deleted_at = datetime.now()
    db.add(user_row)
    db.commit()
    db.refresh(user_row)
    return user_row

def create_new_board(board:JiraBoardCreate, db:Session):
    new_board = JiraBoard(**board.model_dump())
    db.add(new_board)
    db.commit()
    db.refresh(new_board)
    return new_board

def create_new_task(task:TaskCreate, db:Session):
    new_task = Task(**task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def create_new_comment(comment:CommentCreate, db:Session):
    new_comment = Comment(**comment.model_dump())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def update_board_title(update: JiraBoardUpdateTitle, board_id: int, db:Session):
    board_row = db.query(JiraBoard).filter(JiraBoard.id==board_id).first()
    if not board_row:
        return None
    board_row.title = update.title
    db.add(board_row)
    db.commit()
    db.refresh(board_row)
    return board_row

def update_board_status(update: JiraBoardUpdateStatus, board_id: int, db:Session):
    board_row = db.query(JiraBoard).filter(JiraBoard.id==board_id).first()
    if not board_row:
        return None
    board_row.board_status = update.board_status
    db.add(board_row)
    db.commit()
    db.refresh(board_row)
    return board_row

def update_task_status(update: TaskUpdateStatus, task_id: int, db:Session):
    task_row = db.query(Task).filter(Task.id==task_id).first()
    if not task_row:
        return None
    task_row.task_status = update.task_status
    db.add(task_row)
    db.commit()
    db.refresh(task_row)
    return task_row

def update_task_assignee(update: TaskUpdateAssignee, task_id: int, db:Session):
    task_row = db.query(Task).filter(Task.id==task_id).first()
    if not task_row:
        return None
    task_row.task_assignee = update.task_assignee
    db.add(task_row)
    db.commit()
    db.refresh(task_row)
    return task_row

def update_task_description(update: TaskUpdateDescription, task_id: int, db:Session):
    task_row = db.query(Task).filter(Task.id==task_id).first()
    if not task_row:
        return None
    task_row.task_description = update.task_description
    db.add(task_row)
    db.commit()
    db.refresh(task_row)
    return task_row

def update_comment_description(update: CommentUpdateDescription, comment_id: int, db:Session):
    comment_row = db.query(Comment).filter(Comment.id==comment_id).first()
    if not comment_row:
        return None
    comment_row.description = update.description
    db.add(comment_row)
    db.commit()
    db.refresh(comment_row)
    return comment_row

def get_jira_board_task(board_id: int, db:Session):
    return db.query(Task).filter(Task.jira_board_id == board_id).all()

def get_task_comment(task_id:int, db:Session):
    return db.query(Comment).filter(Comment.task_id==task_id).all()

def get_board_info(board_id:int, db:Session):
    return db.query(JiraBoard).options(joinedload(JiraBoard.tasks).joinedload(Task.comment), joinedload(JiraBoard.user)).filter(JiraBoard.id == board_id).first()

def get_jira_boards(db:Session):
    return db.query(JiraBoard).all()

def get_board_by_id(board_id: str, db: Session):
    return db.query(JiraBoard).filter(JiraBoard.id==board_id, JiraBoard.deleted_at.is_(None)).first()

def soft_delete_jira_board(board_id: int, db:Session):
    board_row = db.query(JiraBoard).filter(JiraBoard.id == board_id).first()
    if not board_row:
        return None
    board_row.deleted_at = datetime.now()
    db.add(board_row)
    db.commit()
    db.refresh(board_row)
    return board_row

def get_task_by_id(task_id: str, db: Session):
    return db.query(Task).filter(Task.id==task_id, Task.deleted_at.is_(None)).first()

def soft_delete_task(task_id: int, db:Session):
    task_row = db.query(Task).filter(Task.id == task_id).first()
    if not task_row:
        return None
    task_row.deleted_at = datetime.now()
    db.add(task_row)
    db.commit()
    db.refresh(task_row)
    return task_row

def get_comment_by_id(comment_id: str, db: Session):
    return db.query(Comment).filter(Comment.id==comment_id, Comment.deleted_at.is_(None)).first()

def soft_delete_comment(comment_id: int, db:Session):
    comment_row = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment_row:
        return None
    comment_row.deleted_at = datetime.now()
    db.add(comment_row)
    db.commit()
    db.refresh(comment_row)
    return comment_row


