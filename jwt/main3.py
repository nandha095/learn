# from pydantic import BaseModel, Field, EmailStr,field_validator
# import re

# usernames = ['ybor222']

# class User(BaseModel):
#   name: str = Field(min_length=3)
#   age: int = Field(gt=18)
#   height: int = Field(gt=48, le=70)
#   email: EmailStr
#   username: str = Field(min_length=5)




#   @field_validator('username')
#   def validate_username(cls, value):

#     if not re.match(r'^[a-zA-Z0-9_]+$', value):
#       raise ValueError('Username must contain only alphanumeric characters and underscores.')
#     if value in usernames:
#       raise ValueError('Username already exists.')
    
#     usernames.append(value)
#     return value





# def main() -> None:
#   user = User(
#     name = "nandha",
#     age = 30,
#     height = 65,
#     email = "nandhap095@gmail.com",
#     username = "nandha123"
#     )
  
# if __name__ == "__main__":
#   main()

# Import required modules
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# Create a FastAPI app instance
app = FastAPI()


# Define a Pydantic model for Todo items
class TodoItem(BaseModel):
    title: str
    description: str
    completed: bool = False


# Initialize an in-memory database (list) to store Todo items
todo_db = []


# Endpoint to create a new Todo item
@app.post("/todos/", response_model=TodoItem)
def create_todo(todo: TodoItem):
    todo_db.append(todo)  # Add the new Todo item to the database
    return todo  # Return the created Todo item as a response


# Endpoint to retrieve all Todo items
@app.get("/todos/", response_model=List[TodoItem])
def read_todos():
    return todo_db  


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)
