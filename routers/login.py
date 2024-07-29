from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from config import ACCESS_TOKEN_EXPIRE_SECONDS
from curd import get_user_by_email
from database import get_db
from utils import create_access_token, verfiy_password

router = APIRouter()

@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user_row = get_user_by_email(email_address=form_data.username, db=db)
    if not user_row:
        raise HTTPException(status_code=404, detail="User not registered")
    if not verfiy_password(form_data.password, user_row.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(
        data={"sub": user_row.email_address}
    )
    return {"access_token":access_token, "token_type":"bearer"}
