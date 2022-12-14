from typing import List, Dict, Union, Any, Optional
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.models.models import ContainerModel
from app.schemas.container import ContainerCreate, ContainerUpdate
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

    def get(self, db: Session, id: Any) -> Optional[ContainerModel]:
        return db.query(ContainerModel).filter(ContainerModel.container_id==id).first()


    def update(
        self, db: Session, db_obj: ContainerModel, object_in: Union[ContainerUpdate, Dict[str, Any]]
    ) -> ContainerModel:
        object_data = jsonable_encoder(db_obj)
        if isinstance(object_in, dict):
            update_data = object_in
        else:
            update_data = object_in.dict(exclude_unset=True)
        #for field in object_data:
        #    if field in update_data:
        #        setattr(db_obj, field, update_data[field])
        return super().update(db=db, db_obj=db_obj, object_in=update_data)


    def delete(self, db: Session, id: Any) -> ContainerModel:
        container_model_obj = db.query(ContainerModel).get(id)
        db.delete(container_model_obj)
        db.commit()
        return container_model_obj