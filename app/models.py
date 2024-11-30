from typing import Any, Dict, List
from odmantic import Model


class User(Model):
    name: str
    email: str
    password_hash: str

class Trip(Model):
    user_id: str
    destination: list[str]
    budget: float
    duration: int
    interests: list[str]
    itineraries: List[Dict[str, Any]]
    start_date: str
    favorite: bool = False