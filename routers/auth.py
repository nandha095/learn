# blog/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from blog.database import get_db
from blog.services import otp as otp_service
from blog.services import email as email_service
from blog.utils.jwt import create_token
from blog.utils.hash import get_password_hash, verify_password
from blog.models.user import User
from blog.schemas.user import (
    OTPRequest,
    RegisterRequest,
    LoginUser,
    LoginOTPRequest,
    LoginOTPVerify,
    ResetPasswordRequest
)
from blog.utils.hash import get_password_hash

router = APIRouter(prefix="/auth", tags=["Auth"])

# 1. Request OTP for registration
@router.post("/request-otp")
def request_otp(payload: OTPRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    otp = otp_service.generate_otp(payload.email)
    email_service.send_otp_email(payload.email, otp)
    return {"message": "OTP sent to email"}

# 2. Register new user using OTP
@router.post("/register")
def register_user(payload: RegisterRequest, db: Session = Depends(get_db)):
    # print("Received registration request:", payload.dict()) 

    if not otp_service.verify_otp(payload.email, payload.otp):
        # print("OTP verification failed")
        raise HTTPException(status_code=400, detail="Invalid OTP")

    existing_user = db.query(User).filter_by(email=payload.email).first()
    if existing_user:
        # print("User already registered")
        raise HTTPException(status_code=400, detail="User already registered")

    hashed_pw = get_password_hash(payload.password)
    # print("Password hashed")

    new_user = User(
        email=payload.email,
        name=payload.name,
        password=hashed_pw,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # print("User created")

    return {"message": "User registered successfully"}


# blog/routers/auth.py
from blog.schemas.user import LoginUser

# @router.post("/login")
# def login_user(payload: LoginUser, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.email == payload.email).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     if not verify_password(payload.password, user.password):
#         raise HTTPException(status_code=401, detail="Invalid password")

#     if not user.is_active or user.is_blocked:
#         raise HTTPException(status_code=403, detail="User not allowed")

#     token = create_token({"sub": user.email})
#     return {"access_token": token, "token_type": "bearer"}


# 3. Login user using email + password
@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=form_data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid password")
    if not user.is_active or user.is_blocked:
        raise HTTPException(status_code=403, detail="User not allowed")

    token = create_token(user)
    return {"access_token": token, "token_type": "bearer"}

# 4. Request OTP for login (optional flow)
# @router.post("/login-request-otp")
# def login_request_otp(payload: OTPRequest, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.email == payload.email).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not registered")

#     otp = otp_service.generate_otp(payload.email)
#     email_service.send_otp_email(payload.email, otp)
#     return {"message": "OTP sent for login"}

# # 5. Verify OTP for login (optional flow)
# @router.post("/login-verify-otp")
# def login_verify_otp(payload: LoginOTPVerify, db: Session = Depends(get_db)):
#     if not otp_service.verify_otp(payload.email, payload.otp):
#         raise HTTPException(status_code=400, detail="Invalid OTP")

#     user = db.query(User).filter(User.email == payload.email).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     token = create_token({"sub": user.email})
#     return {"token": token}


@router.post("/forgot-password")
def forgot_password(payload: OTPRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    otp = otp_service.generate_otp(payload.email)
    email_service.send_otp_email(payload.email, otp, purpose="Password Reset")
    return {"message": "OTP for password reset sent to your email"}


@router.post("/reset-password")
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    if not otp_service.verify_otp(payload.email, payload.otp):
        raise HTTPException(status_code=400, detail="Invalid OTP")
    


    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    
    user.password = get_password_hash(payload.new_password)
    db.commit()
    return {"message": "Password reset successful"}



