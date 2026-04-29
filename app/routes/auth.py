from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordRequestForm

from app.db import get_session
from app.schemas.user import User, UserCreate
from app.auth.utils import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", status_code=201)
def signup(user: UserCreate, session: Session = Depends(get_session)):

    existing_user = session.exec(
        select(User).where(User.email == user.email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        email=user.email,
        password_hash=hash_password(user.password),
        name=user.name
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"user_id": new_user.user_id}


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(),
          session: Session = Depends(get_session)):

    user = session.exec(
        select(User).where(User.email == form_data.username)
    ).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.user_id})

    return {"access_token": token, "token_type": "bearer"}
