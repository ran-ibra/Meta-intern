from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.auth import RegisterIn, LoginIn, TokenOut
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.core.rate_limit import check_rate_limit
from app.services.logging import add_log

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=TokenOut)
def register(payload: RegisterIn, request: Request, db: Session = Depends(get_db)):
    ip_key = f"ip:{request.client.host}"
    check_rate_limit(ip_key)

    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(email=payload.email, hashed_password=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(subject=user.email)
    add_log(db, user, "REGISTER")
    return TokenOut(access_token=token)

@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn, request: Request, db: Session = Depends(get_db)):
    ip_key = f"ip:{request.client.host}"
    check_rate_limit(ip_key)

    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(subject=user.email)
    add_log(db, user, "LOGIN")
    return TokenOut(access_token=token)
