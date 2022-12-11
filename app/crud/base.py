from typing import Generic, TypeVar, Type, List

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
