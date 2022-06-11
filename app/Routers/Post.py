from typing import List
from urllib import response
from .. import models, Schemas
from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..Database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts'] 
)

@router.get("/", response_model=List[Schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
	posts = db.query(models.Post).all()
	return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Schemas.PostResponse)
def create_posts(post: Schemas.PostCreate, db: Session = Depends(get_db)):
	new_post = models.Post(**post.dict())
	db.add(new_post)
	db.commit()
	db.refresh(new_post)
	return new_post

@router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
	post = db.query(models.Post).filter(models.Post.id == id).first()
	if not post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} was not found.")
	return post
