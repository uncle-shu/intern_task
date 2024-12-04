from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.deps import dbDep
from app.utils import utils
from app.utils.config import settings
from app.models import Token, UserPublic, UserCreate

router = APIRouter(tags=["auth"])


@router.post(
    "/", response_model=UserPublic
)
def create_user(*, session: dbDep, user_in: UserCreate) -> Any:
    """
    Create new user.
    """
    user = utils.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    user = utils.create_user(session=session, user_create=user_in)
    return user


@router.post("/login")
def login_access_token(
        session: dbDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = utils.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=utils.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )
