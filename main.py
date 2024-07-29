from fastapi import FastAPI, Depends
from models import Base
from database import engine
from routers import users, jira_boards, tasks, comments, login
from auth import JWTBearer


app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(login.router)
app.include_router(users.router, dependencies=[Depends(JWTBearer())])
app.include_router(jira_boards.router, dependencies=[Depends(JWTBearer())])
app.include_router(tasks.router, dependencies=[Depends(JWTBearer())])
app.include_router(comments.router, dependencies=[Depends(JWTBearer())])
