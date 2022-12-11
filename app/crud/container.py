
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.models.models import ContainerModel as Container
from app.schemas.container import ContainerCreate
from app.crud.base import CRUDBase

class CRUDContainer(CRUDBase[Container, ContainerCreate]):
    def create(self, db: Session, *, object_add: ContainerCreate) -> Container:
        object_add_data = jsonable_encoder(object_add)
        db_obj = self.model(**object_add_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj