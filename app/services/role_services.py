from typing import Optional

from app.core.unit_of_work import UnitOfWork
from app.services.base import BaseServices
from app import models, schemas


class RoleServices(BaseServices[models.Role, schemas.RoleCreate, schemas.RoleUpdate]):
    def get_by_name(self, uow: UnitOfWork, *, name: str) -> Optional[models.Role]:
        return uow.query(self.model).filter(self.model.name == name).first()


role = RoleServices(models.Role)
