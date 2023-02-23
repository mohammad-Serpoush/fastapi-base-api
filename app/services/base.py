from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from app.core.unit_of_work import UnitOfWork
from app.db.base import Base
from fastapi.encoders import jsonable_encoder
from pydantic import UUID4, BaseModel

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseServices(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_multi(
        self, uow: UnitOfWork, *, skip: int = 0, limit: int = 20
    ) -> List[ModelType]:
        return uow.query(self.model).offset(skip).limit(limit).all()

    def get(self, uow: UnitOfWork, id: UUID4) -> Optional[ModelType]:
        return uow.query(self.model).filter(self.model.id == id).first()

    def create(self, uow: UnitOfWork, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        uow.add(db_obj)
        return db_obj

    def update(
        self,
        uow: UnitOfWork,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        uow.add(db_obj)
        return db_obj

    def remove(self, uow: UnitOfWork, *, obj: ModelType) -> None:
        uow.delete(obj)
