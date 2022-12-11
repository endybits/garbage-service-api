from typing import List
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.models.models import ContainerModel
from app.schemas.container import ContainerCreate
from app.crud.base import CRUDBase

class CRUDContainer(CRUDBase[ContainerModel, ContainerCreate]):
    
    def create(
        self, db: Session, *, object_add: ContainerCreate
    ) -> ContainerModel:
        object_add_data = jsonable_encoder(object_add)
        db_obj = self.model(**object_add_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_container_list(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ContainerModel]:
        return db.query(self.model).offset(skip).limit(limit).all()