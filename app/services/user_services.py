from typing import Optional

from app.core.unit_of_work import UnitOfWork
from app.core.security import get_password_hash, verify_password
from app.services.base import BaseServices
from app.constants.role import Role
from pydantic.types import UUID4
from app import models, schemas, services


class UserServices(BaseServices[models.User, schemas.UserCreate, schemas.UserUpdate]):
    def get_by_email(self, uow: UnitOfWork, *, email: str) -> Optional[models.User]:
        return uow.query(self.model).filter(self.model.email == email).first()

    def register(self, uow: UnitOfWork, *, obj_in: schemas.UserRegister) -> models.User:
        user_role = services.role.get_by_name(uow, name=Role.USER["name"])
        db_obj = self.model(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            role_id=user_role.id,
            is_active=True,
        )
        uow.add(db_obj)
        return db_obj

    def create(
        self,
        uow: UnitOfWork,
        *,
        obj_in: schemas.UserCreate,
    ) -> models.User:
        user_db_obj = self.model(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            phone_number=obj_in.phone_number,
            is_active=obj_in.is_active,
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            role_id=obj_in.role_id,
        )
        uow.add(user_db_obj)
        return user_db_obj

    def authenticate(
        self, uow: UnitOfWork, *, email: str, password: str
    ) -> Optional[models.User]:
        current_user = self.get_by_email(uow, email=email)
        if not current_user:
            return None
        if not verify_password(password, current_user.hashed_password):
            return None
        return current_user

    def is_active(self, current_user) -> bool:
        return current_user.is_active

    def get(self, uow: UnitOfWork, id: UUID4) -> Optional[models.User]:
        return uow.query(self.model).filter(self.model.id == id).first()


user = UserServices(models.User)
