from fastapi import APIRouter, Depends, HTTPException, status
from models.users import ResponseSchema, Login, Register, TokenResponse
from sqlalchemy.orm import Session
from authentication.config import get_db
from passlib.context import CryptContext
from repository.users import UserRepo, JWTRepo
from tabel.users import User


router = APIRouter(
    tags={"Authentication"}
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


#register user
@router.post("/signup", response_model=ResponseSchema)
async def signup(request: Register, db: Session = Depends(get_db),):
    try:
        _user = User(
            username=request.username,
            password=pwd_context.hash(request.password),
            email=request.email,
            Phone_number=request.Phone_number,
            first_name=request.first_name,
            last_name=request.last_name
        )
        
        UserRepo.insert(db, _user)

        return ResponseSchema(
            code="201",
            status="success",
            message="User created successfully"
        ).dict(exclude_none=True)

    except Exception as e:
        return ResponseSchema(
            code="500",
            status="error",
            message=f"An error occurred: {str(e)}"
        ).dict(exclude_none=True)
    
#login user
@router.post("/login")
async def login(request: Login, db: Session = Depends(get_db),):
    try:
        _user = UserRepo.find_by_username(db, User, request.username)
        if not pwd_context.verify(request.password, _user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        token = JWTRepo.generate_token(
            data={"sub": _user.username}
        )
        return ResponseSchema(
            code="200",
            status="success",
            message="Login successful",
            results=TokenResponse(
                access_token=token,
                token_type="bearer"
            )
        ).dict(exclude_none=True)
    except Exception as error:
        error_message = str(error)
        print(error_message)
        return ResponseSchema(
            code="500",
            status="error",
            message=f"An error occurred: {error_message}"
        ).dict(exclude_none=True)

           
    
    
     