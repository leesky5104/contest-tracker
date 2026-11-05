from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# DB 파일 위치 (프로젝트 폴더에 contest.db 파일이 생겨요)
DATABASE_URL = "sqlite:///./contest.db"

# 엔진: DB와 실제로 연결해 주는 통로
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite 전용 설정
)

# 세션 공장: 요청이 올 때마다 DB와 대화할 "창구"를 만들어 줘요
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모든 테이블 모양(모델)이 물려받을 기본 클래스
Base = declarative_base()


# API 함수에서 DB 창구를 받아 쓰고, 끝나면 닫아주는 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()