from sqlalchemy import BigInteger, Column, Date, Integer, String

from app.database import Base


class ContestModel(Base):
    __tablename__ = "contests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    organizer = Column(String, nullable=False)
    category = Column(String, nullable=False)
    deadline = Column(Date, nullable=False)
    prize = Column(BigInteger, nullable=True)
    url = Column(String, nullable=True)