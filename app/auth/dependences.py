from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlmodel import Session

from app.db import get_session
from app.schemas.user import User
from app.auth.utils import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
