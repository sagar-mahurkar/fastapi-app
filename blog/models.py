from sqlmodel import SQLModel, Field


class Blog(SQLModel, table=True):
  __tablename__ = 'blogs'
  
  id: int | None = Field(default=None, primary_key=True, index=True)
  title: str
  body: str
  
class User(SQLModel, table=True):
  __tablename__ = 'users'
  
  id: int | None = Field(default=None, primary_key=True, index=True)
  name: str
  email: str
  password: str