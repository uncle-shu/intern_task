from sqlmodel import Session

from app.utils import utils
from app.models import UserCreate
from app.tests.utils.utils import random_email, random_lower_string


def test_create_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = utils.create_user(session=db, user_create=user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")


def test_authenticate_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = utils.create_user(session=db, user_create=user_in)
    authenticated_user = utils.authenticate(session=db, email=email, password=password)
    assert authenticated_user
    assert user.email == authenticated_user.email
