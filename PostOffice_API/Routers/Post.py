from typing import List
from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, Request
from ..Database import Get_DataBase
from .. import DataBase_Models, Schemas

router = APIRouter(
    prefix="/posts",
    tags=['Posts'] 
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[Schemas.PostResponse])
def get_posts(request: Request, db: Session = Depends(Get_DataBase)):
    
    # Query Table
    posts = db.query(DataBase_Models.Post_Table).all()

    # Get Remote IP
    IP = request.client.host

    # Print Remote IP
    print("------------------------")
    print("Client IP :", IP)
    print("------------------------")

    # Send Response
    return posts

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=Schemas.PostResponse)
def get_post(id: int, db: Session = Depends(Get_DataBase)):

	get_post = db.query(DataBase_Models.Post_Table).filter(DataBase_Models.Post_Table.id == id).first()

	if not get_post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} was not found.")
	return get_post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Schemas.PostResponse)
def create_posts(Post_Schema: Schemas.PostCreate, db: Session = Depends(Get_DataBase)):
    
    # Set Inputs
    new_post = DataBase_Models.Post_Table(**Post_Schema.dict())
    
    # Add Post To Table
    db.add(new_post)
    
    # Commit Database
    db.commit()

    # Refresh Data
    db.refresh(new_post)
    
    # Send Response
    return new_post

