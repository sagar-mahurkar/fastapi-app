from sqlmodel import SQLModel, Field


class Blog(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True, index=True)
  title: str
  body: str