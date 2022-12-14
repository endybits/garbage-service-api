from typing import Generic, TypeVar, Type, List, Dict, Union, Any, Optional

from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder


from app.models.models import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
            CRUD object with default CRUD methods
            **Parameters**
            - model: A SQLAlchemy model class
            - schema: A Pydantic model (schema) class
        """
        self.model = model


    def create(
        self, db: Session, *, object_add: CreateSchemaType
    ) -> ModelType:
        object_add_data = jsonable_encoder(object_add)
        db_obj = self.model(**object_add_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


    def get_list(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()


    def get(
        self, db: Session, id: Any
    ) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()


    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        object_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        object_data = jsonable_encoder(db_obj)
        if isinstance(object_in, dict):
            update_data = object_in
        else:
            update_data = object_in.dict(exclude_unset=True)
        for field in object_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


    def remove(self, db: Session, *, id: int) -> ModelType:
        object = db.query(self.model).get(id)
        db.delete(object)
        db.commit()
        return object