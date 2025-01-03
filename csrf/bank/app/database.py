from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./bank.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_test_users():
    db = SessionLocal()
    from .models import User

    # 기존 테스트 데이터 삭제
    db.query(User).delete()

    # 테스트 유저 생성
    test_users = [
        User(username="alice", balance=10000),
        User(username="bob", balance=5000),
        User(username="charlie", balance=3000),
    ]

    for user in test_users:
        db.add(user)

    db.commit()
    db.close()
