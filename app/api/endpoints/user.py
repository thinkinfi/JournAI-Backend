import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Depends, Form, Response
from app.models import User
from app.database import engine
from app.schemas import UserSignupSchema, UserLoginSchema, UserResponseSchema
from passlib.context import CryptContext
import jwt

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

router = APIRouter(prefix="/user")

pwd_context = CryptContext(schemes=["bcrypt"])

# Signup route
@router.post("/signup", response_model=UserResponseSchema)
async def create_user(user: UserSignupSchema):
    existing_user = await engine.find_one(User, User.email == user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(user.password)
    new_user = User(name=user.name, email=user.email, password_hash=hashed_password)
    await engine.save(new_user)

    token = jwt.encode({"id": str(new_user.id), "name": new_user.name, "email": new_user.email}, SECRET_KEY, algorithm="HS256")
    
    return UserResponseSchema(id=str(new_user.id), name=new_user.name, email=new_user.email, token=token)

# Login route
@router.post("/login", response_model=UserResponseSchema)
async def login_user(user: UserLoginSchema):
    existing_user = await engine.find_one(User, User.email == user.email)
    if not existing_user:
        raise HTTPException(status_code=400, detail="User not found")
    
    if not pwd_context.verify(user.password, existing_user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid password")
    
    token = jwt.encode({"id": str(existing_user.id), "name": existing_user.name, "email": existing_user.email}, SECRET_KEY, algorithm="HS256")

    return UserResponseSchema(id=str(existing_user.id), name=existing_user.name, email=existing_user.email, token=token)

