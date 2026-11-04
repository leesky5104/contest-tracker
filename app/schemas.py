from datetime import date
from typing import Optional

from pydantic import BaseModel


class ContestCreate(BaseModel):
    title: str
    organizer: str
    category: str
    deadline: date
    prize: Optional[int] = None
    url: Optional[str] = None


class Contest(ContestCreate):
    id: int