from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn

app = FastAPI()


class Blog(BaseModel):
  title: str
  body: str
  published: Optional[bool]



@app.get('/blog')
def index(limit, published: bool, sort: Optional[str] = None):
  # only get 10 published blogs
	if published:
		return {'data': f'{limit} published blogs from db'}
	else:
		return {'data': f'{limit} blogs from db'}



@app.get('/blog/unpublished')
def unpublished():
  return {'data': 'All unpublished blogs'}



@app.get('/blog/{blog_id}')
def show(blog_id: int):
  # fetch blog with id = blog_id
  return {'data': blog_id}



@app.get('/blog/{blog_id}/comments')
def comments(blog_id, limit=10):
  # fetch comments with id = blog_id
  return limit
  return {'data': {'1', '2'}}



@app.post('/blog')
def create_blog(blog: Blog):
  return {'data': f'The blog is created with title as {blog.title}'}


# if __name__ == "__main__":
#   uvicorn.run(app, host="127.0.0.1", port=9000)