from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Text
from sqlalchemy.orm import relationship


Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email_address = Column(String, unique=True)
    password = Column(String)
    deleted_at = Column(DateTime, nullable=True)

    jira_board = relationship("JiraBoard", back_populates="user")
    task_reported = relationship("Task", foreign_keys="[Task.task_reporter]", back_populates="reporter")
    task_assigned = relationship("Task", foreign_keys="[Task.task_assignee]", back_populates="assignee")
    comment = relationship("Comment", back_populates="user")


class JiraBoard(Base):
    __tablename__ = "jira_boards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    title = Column(String, unique=True)
    created_time = Column(DateTime)
    board_status = Column(String)
    deleted_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="jira_board")
    tasks = relationship("Task", back_populates="jira_board")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    jira_board_id = Column(Integer, ForeignKey("jira_boards.id"))
    task_description = Column(Text)
    task_reporter = Column(Integer, ForeignKey("users.id"))
    task_assignee = Column(Integer, ForeignKey("users.id"), nullable=True)
    task_status = Column(String)
    deleted_at = Column(DateTime, nullable=True)

    jira_board = relationship("JiraBoard", back_populates="tasks")
    comment = relationship("Comment", back_populates="task")
    reporter = relationship("User", foreign_keys="[Task.task_reporter]", back_populates= "task_reported")
    assignee = relationship("User", foreign_keys="[Task.task_assignee]", back_populates="task_assigned")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    description = Column(Text)
    commented_by = Column(Integer, ForeignKey("users.id") )
    created_time = Column(DateTime)
    deleted_at = Column(DateTime, nullable=True)
    
    task = relationship("Task", back_populates="comment")
    user = relationship("User", back_populates="comment")

