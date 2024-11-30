from typing import Any, Dict, List
from pydantic import BaseModel


class UserSignupSchema(BaseModel):
    name: str
    email: str
    password: str

class UserLoginSchema(BaseModel):
    email: str
    password: str

class UserResponseSchema(BaseModel):
    id: str
    name: str
    email: str
    token: str = None

class TripRequestSchema(BaseModel):
    user_id: str
    destination: list[str]
    budget: float
    start_date: str
    duration: int
    interests: list[str]

class TripResponseSchema(BaseModel):
    id: str
    user_id: str
    destination: list[str]
    budget: float
    duration: int
    start_date: str
    interests: list[str]
    itineraries: List[Dict[str, Any]]
    favorite: bool = False