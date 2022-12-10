import json
from typing import List


from fastapi import FastAPI
from fastapi import Body, Path
from fastapi import status

from app.schemas.container import Container

app = FastAPI()

@app.get(path='/', status_code=status.HTTP_200_OK)
async def home():
    return {'message': 'Hi, this is the incredible service project\'s home page'}



### Create container
@app.post(
    path='/containers',
    status_code=status.HTTP_201_CREATED,
    response_model=Container
)
async def create_container(
    container: Container = Body(...)
):
    container_dict = container.dict()
    with open('./app/containers.json', 'r+', encoding='utf-8') as f:
        container_list = f.read()
        container_list = json.loads(container_list)
        container_list.append(container_dict)
        container_json = json.dumps(container_list)
        f.seek(0)
        f.write(container_json)
    return container

### Get container list
@app.get(
    path='/containers',
    status_code=status.HTTP_200_OK,
    response_model=List[Container]
)
async def container_list(
):
    with open('./app/containers.json', 'r', encoding='utf-8') as f:

        container_list = f.read()
        container_list = json.loads(container_list)
        f.close()
    return container_list

### Get container detail
@app.get(
    path='/containers/{container_id}',
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