from typing import Any
from app import services, models, schemas
from app.api import deps
from app.core.exception import raise_http_exception
from app.core.unit_of_work import UnitOfWork
from app.constants.role import Role
from app.constants.errors import Error
from fastapi import APIRouter, Depends, Security, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserRegister,
) -> Any:
    """
    register user
    """
    with UnitOfWork(db) as uow:
        user = services.user.get_by_email(uow, email=user_in.email)
        if user:
            raise_http_exception(Error.USER_EXIST_ERROR)
        services.user.register(uow, obj_in=user_in)
    return


def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserUpdate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[
            Role.ADMIN["name"],
            Role.USER["name"],
        ],
    ),
) -> Any:
    with UnitOfWork(db) as uow:
        db_user = services.user.get(uow, id=current_user.id)
        user = services.user.update(uow, db_obj=db_user, obj_in=user_in)

    return user


@router.get("/me", response_model=schemas.User)
def get_user_me(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[
            Role.ADMIN["name"],
            Role.USER["name"],
        ],
    ),
) -> Any:
    with UnitOfWork(db) as uow:
        user = services.user.get(uow, id=current_user.id)
    return user
