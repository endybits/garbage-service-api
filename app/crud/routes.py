from typing import List, Dict, Any, Union, Optional
from fastapi.encoders import jsonable_encoder
from  sqlalchemy.orm import Session

from app.models.models import RouteModel
from app.schemas.route import RouteCreate, RouteUpdate
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

    def get_last_row(self, db: Session, *, skip: int = 0, limit: int = 100) -> Optional[RouteModel]:
        return db.query(RouteModel).order_by(RouteModel.route_id.desc()).offset(skip).limit(limit).first()

    def get(self, db: Session, id: int) -> Optional[RouteModel]:
        return db.query(RouteModel).filter(RouteModel.route_id == id).first()

    def update(self, db: Session, *, db_obj: RouteModel, object_in: Union[RouteUpdate, Dict[str, Any]]) -> RouteModel:
        object_data = jsonable_encoder(db_obj)
        if isinstance(object_in, Dict):
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


    def remove(self, db: Session, *, id: int) -> RouteModel:
        return super().remove(db, id=id)