from sqlmodel import SQLModel, Field, Relationship
from typing import List

class User(SQLModel, table=True):
  __tablename__ = 'users'
  
  id: int | None = Field(default=None, primary_key=True, index=True)
  name: str
  email: str
  password: str
  blogs: List["Blog"] = Relationship(back_populates="creator")
  

class Blog(SQLModel, table=True):
  __tablename__ = 'blogs'
  
  id: int | None = Field(default=None, primary_key=True, index=True)
  title: str
  body: str
  creator_id: int = Field(foreign_key="users.id", nullable=False)
  creator: "User" = Relationship(back_populates="blogs")
