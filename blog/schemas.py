from pydantic import BaseModel



class Blog(BaseModel):
  title: str
  body: str


class ShowBlog(BaseModel):
  title: str