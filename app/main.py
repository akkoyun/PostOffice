from importlib.resources import contents
from fastapi import FastAPI, Response, status, HTTPException, Depends
from . import models
from .Database import engine, get_db
from .Routers import Post


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(Post.router)

@app.get("/", status_code=status.HTTP_202_ACCEPTED)
def root():
	return {"message": "Hello World"}

