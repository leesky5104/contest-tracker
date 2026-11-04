from datetime import datetime
from typing import List

from fastapi import FastAPI, HTTPException

from app.schemas import Contest, ContestCreate

app = FastAPI(
    title="Contest Tracker API",
    description="공모전·해커톤 트래커 백엔드",
    version="0.2.0",
)

# 메모리 저장소 (서버를 끄면 사라져요. 3일차에 DB로 바꿀 거예요)
contests: List[Contest] = []
next_id = 1


@app.get("/")
def root():
    return {"message": "Contest Tracker API에 오신 걸 환영합니다"}


@app.get("/health")
def health_check():
    return {"status": "ok", "time": datetime.now().isoformat()}


@app.post("/contests", response_model=Contest, status_code=201)
def create_contest(data: ContestCreate):
    global next_id
    contest = Contest(id=next_id, **data.model_dump())
    contests.append(contest)
    next_id += 1
    return contest


@app.get("/contests", response_model=List[Contest])
def list_contests():
    return contests


@app.get("/contests/{contest_id}", response_model=Contest)
def get_contest(contest_id: int):
    for contest in contests:
        if contest.id == contest_id:
            return contest
    raise HTTPException(status_code=404, detail="공모전을 찾을 수 없습니다")


@app.put("/contests/{contest_id}", response_model=Contest)
def update_contest(contest_id: int, data: ContestCreate):
    for index, contest in enumerate(contests):
        if contest.id == contest_id:
            updated = Contest(id=contest_id, **data.model_dump())
            contests[index] = updated
            return updated
    raise HTTPException(status_code=404, detail="공모전을 찾을 수 없습니다")


@app.delete("/contests/{contest_id}", status_code=204)
def delete_contest(contest_id: int):
    for index, contest in enumerate(contests):
        if contest.id == contest_id:
            contests.pop(index)
            return
    raise HTTPException(status_code=404, detail="공모전을 찾을 수 없습니다")