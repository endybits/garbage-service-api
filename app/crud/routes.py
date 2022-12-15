from typing import List
from fastapi.encoders import jsonable_encoder
from  sqlalchemy.orm import Session

from app.models.models import RouteModel
from app.schemas.route import RouteCreate
from app.crud.base import CRUDBase


class CRUDRoutes(CRUDBase):
    def create(self, db: Session, *, object_add: RouteCreate) -> RouteModel:
        object_add_data = jsonable_encoder(object_add)
        db_obj = self.model(**object_add_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_list(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[RouteModel]:
        return super().get_list(db, skip=skip, limit=limit)