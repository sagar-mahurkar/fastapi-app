from pydantic import BaseModel



class Blog(BaseModel):
  tilte: str
  body: str
