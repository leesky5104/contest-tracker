from datetime import datetime
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import ContestModel
from app.schemas import Contest, ContestCreate

# 서버가 시작될 때 테이블이 없으면 만들어요 (contest.db 파일도 이때 생겨요)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Contest Tracker API",
    description="공모전·해커톤 트래커 백엔드",
    version="0.3.0",
)


@app.get("/")
def root():
    return {"message": "Contest Tracker API에 오신 걸 환영합니다"}


@app.get("/health")
def health_check():
    return {"status": "ok", "time": datetime.now().isoformat()}


@app.post("/contests", response_model=Contest, status_code=201)
def create_contest(data: ContestCreate, db: Session = Depends(get_db)):
    contest = ContestModel(**data.model_dump())
    db.add(contest)
    db.commit()
    db.refresh(contest)
    return contest


@app.get("/contests", response_model=List[Contest])
def list_contests(db: Session = Depends(get_db)):
    return db.query(ContestModel).all()


@app.get("/contests/{contest_id}", response_model=Contest)
def get_contest(contest_id: int, db: Session = Depends(get_db)):
    contest = db.query(ContestModel).filter(ContestModel.id == contest_id).first()
    if contest is None:
        raise HTTPException(status_code=404, detail="공모전을 찾을 수 없습니다")
    return contest


@app.put("/contests/{contest_id}", response_model=Contest)
def update_contest(contest_id: int, data: ContestCreate, db: Session = Depends(get_db)):
    contest = db.query(ContestModel).filter(ContestModel.id == contest_id).first()
    if contest is None:
        raise HTTPException(status_code=404, detail="공모전을 찾을 수 없습니다")
    for key, value in data.model_dump().items():
        setattr(contest, key, value)
    db.commit()
    db.refresh(contest)
    return contest


@app.delete("/contests/{contest_id}", status_code=204)
def delete_contest(contest_id: int, db: Session = Depends(get_db)):
    contest = db.query(ContestModel).filter(ContestModel.id == contest_id).first()
    if contest is None:
        raise HTTPException(status_code=404, detail="공모전을 찾을 수 없습니다")
    db.delete(contest)
    db.commit()