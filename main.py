from fastapi import FastAPI, Response, Header
from database import engine, Base
from routers import auth, user, post
from models import user as user_model, post as post_model
from routers import auth, user
from fastapi.responses import JSONResponse
import models
from typing import Optional
from pydantic import BaseModel


Base.metadata.create_all(bind=engine)




app = FastAPI()





@app.get("/")
def Wlecome():
    return {"Greeting": "Wlecome to my blog"}


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
# app.include_router(auth.router)

    
@app.get("/cookie/")
def create_cookie():
    content = {"message": "Come to the dark side, we have cookies"}
    response = JSONResponse(content=content)
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return response


@app.get("/headers-and-object/")
def get_headers():
    content = {"message": "Hello World"}
    headers = {"X-Cat-Dog": "alone in the world", "Content-Language": "en-US"}
    return JSONResponse(content=content, headers=headers)


@app.get("/greet")
async def greet_name(name:Optional[str] = "User", age:int = 0) -> dict:
    return {"message":f"Hello {name}","age":age}

class BookCreateModel(BaseModel):
    title : Optional[str] = "sssss"
    author : Optional[str] = "nandha"


@app.post('/create_book')
async def create_book(book_data:BookCreateModel):
    return {
       "title": book_data.title,
       "author": book_data.author       
    }

@app.get("/get_headers",status_code = 201)
async def get_headers(
    accept:str = Header(None),
    content_type: str = Header(None),
    User_agent: str = Header(None),
    host :  str = Header(None)  
):
    request_headers = {}

    request_headers["Accept"] = accept

    request_headers["Content-type"] = content_type

    request_headers["User-Agent"] = User_agent

    request_headers["Host"] = host

    return request_headers




