from datetime import datetime
from fastapi import FastAPI

app = FastAPI(
    title="Contest Tracker API",
    description="공모전·해커톤 트래커 백엔드",
    version="0.1.0",
)


@app.get("/")
def root():
    return {"message": "Contest Tracker API에 오신 걸 환영합니다"}


@app.get("/health")
def health_check():
    return {"status": "good", "time": datetime.now().isoformat()}