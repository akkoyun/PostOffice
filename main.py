from typing import Optional
from fastapi import FastAPI
#from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
	message: str
	rating: Optional[int] = None



@app.get("/")
def root():
	return {"message": "Get"}

@app.post("/")
def Post_Data(New_Post: Post):

	# Print Incomming Payload
	print(New_Post.message)

	return {"data": New_Post.rating}
