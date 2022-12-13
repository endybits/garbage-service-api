import json
from typing import List, Any

from sqlalchemy.orm import Session
from fastapi import APIRouter
from fastapi import status, Depends
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
    path='/',
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
    container_id: int = Path(..., gt=0)
):
    with open('./app/containers.json', 'r', encoding='utf-8') as f:
        container_list = f.read()
        container_list = json.loads(container_list)
        for container in container_list:
            if container['container_id'] == container_id:
                return container
        f.close()
    # TODO Handle errors when element doesn't exists (Raise a status code 400)
    return {'Error': 'Element does not exists'}


### Update container
@router.put(
    path='/{container_id}',
    status_code=status.HTTP_200_OK,
    response_model=Container
)
async def update_container(
    container_id: int = Path(..., gt=0),
    container_payload: ContainerUpdate = Body(...)
):
    container_dict = container_payload.dict()
    updated = False
    with open('./app/containers.json', 'r+', encoding='utf-8') as f:
        container_list = f.read()
        container_list = json.loads(container_list)
        for container in container_list:
            if container['container_id'] == container_id:
                container['address'] = container_dict.get('address') if container_dict.get('address') else container['address']
                container['volume'] = container_dict.get('volume') if container_dict.get('volume') else container['volume']
                container['latitude'] = container_dict.get('latitude') if container_dict.get('latitude') else container['latitude']
                container['longitude'] = container_dict.get('longitude') if container_dict.get('longitude') else container['longitude']
                container['status'] = container_dict.get('status') if container_dict.get('status') else container['status']
                container_ok = container
                updated = True
        if updated:
            updated_container_list = json.dumps(container_list)
            f.seek(0)
            f.truncate(0) # Clear the file content.
            f.write(updated_container_list)
            f.close()
            return container_ok
        f.close()
    # TODO Handle errors when element doesn't exists (Raise a status code 400)
    return {'Error': 'Element does not exists'}

### Delete container
@router.delete(
    path='/{container_id}',
    status_code=status.HTTP_200_OK,
)
async def delete_container(
    container_id: int = Path(..., gt=0),
):
    delete = False
    with open('./app/containers.json', 'r+', encoding='utf-8') as f:
        container_list = f.read()
        container_list = json.loads(container_list)
        for i, container in enumerate(container_list):
            print('INDEX => '.format(i))
            print('CONTAINER: '.format(container))
            if container['container_id'] == container_id:
                index = i
                delete = True
        
        if delete:
            container_list.pop(index)
            container_new_list = json.dumps(container_list)
            f.seek(0)
            f.truncate(0) # Clear the file content.
            f.write(container_new_list)
            f.close()
            return {'message': f'The element with id: {container_id} was deleted'}
        
    # TODO Handle errors when element doesn't exists (Raise a status code 400)
    return {'Error': 'Element does not exists'}
