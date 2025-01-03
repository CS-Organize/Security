from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
import urllib.parse

router = APIRouter(
    prefix="/bank",
    tags=["bank"],
)


@router.post("/transfer")
async def transfer_money(request: Request, db: Session = Depends(get_db)):
    # form 데이터 파싱
    body = (await request.body()).decode()
    form_data = dict(urllib.parse.parse_qsl(body))

    # 파라미터 추출
    from_user = form_data.get("from_user")
    to_user = form_data.get("to_user")
    try:
        amount = int(form_data.get("amount", 0))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid amount")

    # 송금 처리
    sender = db.query(User).filter(User.username == from_user).first()
    receiver = db.query(User).filter(User.username == to_user).first()

    if not sender or not receiver:
        raise HTTPException(status_code=404, detail="User not found")

    if sender.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    sender.balance -= amount
    receiver.balance += amount

    db.commit()

    return {
        "message": "Transfer successful",
        "from": from_user,
        "to": to_user,
        "amount": amount,
    }


@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get("/")
def bank():
    return {"message": "bank"}
