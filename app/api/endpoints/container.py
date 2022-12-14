import json
from typing import List, Dict, Any, Union

from sqlalchemy.orm import Session
from fastapi import APIRouter
from fastapi import status, Depends, HTTPException
from fastapi import Path, Body

from app.schemas.container import Container, ContainerCreate, ContainerUpdate
from app.api.deps import get_db
from app.crud.container import CRUDContainer
from app.models.models import ContainerModel


router = APIRouter()


### Create container
@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=Container
)
async def create_container(
    *,
    db: Session = Depends(get_db),
    container_add: ContainerCreate = Body(...)
) -> Any:
    """
        Create a new container    
    """
    container = CRUDContainer(ContainerModel).create(db=db, object_add=container_add)
    if not container:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail= f'Object not was created'
        )
    resp_container = Container(
        container_id=container.container_id,
        address = container.address,
        volume = container.volume,
        latitude = container.latitude,
        longitude = container.longitude,
        status=container.status
    )    
    return resp_container


### Get container list
@router.get(
    path='/list',
    status_code=status.HTTP_200_OK,
    response_model=List[Container]
)
async def container_list(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    containers = CRUDContainer(ContainerModel).get_container_list(db=db, skip=skip, limit=limit)
    resp_container_list = []
    for container in containers:
        container_item = Container(
            container_id=container.container_id,
            address = container.address,
            volume = container.volume,
            latitude = container.latitude,
            longitude = container.longitude,
            status=container.status
        )
        resp_container_list.append(container_item)
    return resp_container_list    


### Get container detail
@router.get(
    path='/{container_id}',
    status_code=status.HTTP_200_OK,
    response_model=Container
)
async def container_detail(
    db: Session = Depends(get_db),
    container_id: int = Path(..., gt=0)
):
    container = CRUDContainer(ContainerModel).get(db=db, id=container_id)
    if not container:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= f'Container with id= {container_id} doesn\'t exists'
        )

    resp_container = Container(
        container_id=container.container_id,
        address = container.address,
        volume = container.volume,
        latitude = container.latitude,
        longitude = container.longitude,
        status=container.status
    )    
    return resp_container


### Update container
@router.put(
    path='/{container_id}',
    status_code=status.HTTP_200_OK,
    response_model=Container
)
async def update_container(
    db: Session = Depends(get_db),
    container_id: int = Path(..., gt=0),
    container: Union[ContainerUpdate, Dict[str, Any]] = Body(...)
):
    container_obj = CRUDContainer(ContainerModel).get(db=db, id=container_id)
    if not container_obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= f'Container with id= {container_id} doesn\'t exists'
        )
    container_updated = CRUDContainer(ContainerModel).update(db=db, db_obj=container_obj, object_in=container)
    if not container_updated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= f'Error updating Container with id= {container_id}'
        )
    resp_container = Container(
            container_id=container_updated.container_id,
            address = container_updated.address,
            volume = container_updated.volume,
            latitude = container_updated.latitude,
            longitude = container_updated.longitude,
            status=container_updated.status
        )    
    return resp_container


### Delete container
@router.delete(
    path='/{container_id}',
    status_code=status.HTTP_200_OK,
)
async def delete_container(
    db: Session = Depends(get_db),
    container_id: int = Path(..., gt=0)
):
    container_obj = CRUDContainer(ContainerModel).get(db=db, id=container_id)
    if not container_obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= f'Container with id= {container_id} doesn\'t exists'
        )
    removed_container = CRUDContainer(ContainerModel).remove(db=db, id=container_id)
    return {'message': f'Container with id= {container_id} was removed successfully'}
