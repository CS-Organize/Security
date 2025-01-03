from fastapi import FastAPI
from .routers import bank
from .database import engine, get_db, create_test_users
from .models import Base

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Create test users
create_test_users()

app.include_router(bank.router)

@app.get("/")
async def root():
    return {"message": "Bank API"}
