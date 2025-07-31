# blog/schemas/user.py

from pydantic import BaseModel, EmailStr


# 1. OTP request schema
class OTPRequest(BaseModel):
    email: EmailStr


# 2. Register request (with OTP + password)
class RegisterRequest(BaseModel):
    email: EmailStr
    name: str
    otp: str
    password: str


# 3. Login with email and password
class LoginUser(BaseModel):
    email: EmailStr
    password: str


# 4. Optional: Login with OTP
class LoginOTPRequest(BaseModel):
    email: EmailStr

class LoginOTPVerify(BaseModel):
    email: EmailStr
    otp: str

class UserProfile(BaseModel):
    email: EmailStr
    name: str
    is_private: bool  

    class Config:
        from_attributes = True

class UpdatePrivacyRequest(BaseModel):
    is_private: bool

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str
