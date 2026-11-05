from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ContestCreate(BaseModel):
    title: str
    organizer: str
    category: str
    deadline: date
    prize: Optional[int] = None
    url: Optional[str] = None


class Contest(ContestCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int