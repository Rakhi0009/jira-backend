from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import  UserCreate
from database import get_db
from curd import get_user_by_email, create_new_user, soft_delete_user, get_user_by_id

router = APIRouter()

@router.post("/users/")
def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    user_row = get_user_by_email(email_address=user.email_address, db=db)
    if user_row:
        raise HTTPException(status_code=400, detail="Email already registerd")
    return create_new_user(user=user, db=db)

@router.delete("/user/{user_id}")
def delete_user(user_id: int, db: AsyncSession =Depends(get_db)):
    user_row = get_user_by_id(user_id=user_id, db=db)
    if not user_row:
        raise HTTPException(status_code=404, detail="No user found")
    return soft_delete_user(user_id=user_id, db=db)

