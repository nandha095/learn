from typing import Generic, Optional, TypeVar
from pydantic.generics import GenericModel
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
import datetime
from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar('T')

#LOGIN
class Login(BaseModel):
    username: str = Field(..., alias="username")
    password: str = Field(..., alias="password")

    class Config:
        allow_population_by_field_name = True

#register
# class Register(BaseModel):
#     username : str 
#     password : str
#     email : str
#     Phone_number : str

#     first_name : str
#     last_name : str

class Register(BaseModel):
    username: str = Field(..., alias="username")
    password: str = Field(..., alias="password")
    email: str = Field(..., alias="email")
    Phone_number: str = Field(..., alias="phoneNumber")  
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")

    class Config:
        allow_population_by_field_name = True 

#response model   
class ResponseSchema(BaseModel):
      code: str
      status: str
      message: str
      results: Optional[T] = None

# token
class TokenResponse(BaseModel):
    access_token: str 
    token_type: str

