import json
from typing import Any, Union, Any, Dict, List

from sqlalchemy.orm import Session
from fastapi import APIRouter
from fastapi import status, Depends
from fastapi import Body, Path
from fastapi.encoders import jsonable_encoder

from app.api.deps import get_db
from app.utils.base import StatusRoute
from app.models.models import RouteModel, ContainerModel
from app.schemas.route import Route, RouteCreate, RouteUpdate
from app.crud.routes import CRUDRoutes
from app.crud.container import CRUDContainer

router = APIRouter()

## Get Route Service List
@router.get(
    path='/',
    status_code=status.HTTP_200_OK
)
async def routes_list(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    rep_route_list = CRUDRoutes(RouteModel).get_list(db=db, skip=skip, limit=limit)
    for route in rep_route_list:
        points = route.points
        print(points)
        for point in points:
            print(type(point))
    
    return rep_route_list


## Create Route Service
@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED
)
async def create_route(
    db: Session = Depends(get_db),
    route_add: RouteCreate = Body(...)
) -> Any:
    route_created_model = CRUDRoutes(model=RouteModel).create(db=db, object_add=route_add)
    ROUTE_ID = int(str(route_created_model.route_id))
    CUMULATIVE_VOL = float(str(route_created_model.cumulative_vol))
    LOCATIONS = [point for point in route_created_model.points]
    STATUS = StatusRoute(route_created_model.status)
    print(LOCATIONS)
    object_route = Route(
        route_id=ROUTE_ID,
        cumulative_vol=CUMULATIVE_VOL,
        points=LOCATIONS,
        status=STATUS
    )
    return object_route


## Update Route
@router.put(
    path='/{route_id}',
    status_code=status.HTTP_200_OK
)
async def update_route(
    db: Session = Depends(get_db),
    route_id: int = Path(..., gt=0),
    route: Union[RouteUpdate, Dict[str, Any]] = Body(...)
):
    
    route_obj = CRUDRoutes(RouteModel).get(db=db, id=route_id)
    updated_route = CRUDRoutes(RouteModel).update(db=db, db_obj=route_obj, object_in=route)
    return updated_route

## Update Route
@router.put(
    path='/{route_id}/{container_id}',
    status_code=status.HTTP_200_OK
)
async def eject_container_from_route(
    db: Session = Depends(get_db),
    route_id: int = Path(..., gt=0),
    container_id: int = Path(..., gt=0),
):
    
    route_obj = CRUDRoutes(RouteModel).get(db=db, id=route_id)
    route = jsonable_encoder(route_obj)
    container_points = route["points"]
    print(route)
    print('\n')
    container_exists = False
    for point in container_points:
        if point['container_id'] == container_id:
            container_exists = True
            container_points.remove(point)
    if container_exists:
        container_obj = CRUDContainer(ContainerModel).get(db=db, id=container_id)
        container_obj = jsonable_encoder(container_obj)
        result_cum_vol = route['cumulative_vol'] - container_obj['volume']
        route['cumulative_vol'] = result_cum_vol if result_cum_vol > 0 else 0
        print(route)
        updated_route = CRUDRoutes(RouteModel).update(db=db, db_obj=route_obj, object_in=route)
        return {"action":f"The container {container_id} was ejected from the list point in route {route_id}", "object": updated_route} #TODO include 200 status code
    return {"response":f"Container {container_id} does not exists in route {route_id}"} #TODO include 400 status code



## Remove Route
@router.delete(
    path='/{route_id}',
    status_code=status.HTTP_200_OK
)
async def delete_route(
    db: Session = Depends(get_db),
    route_id: int = Path(..., gt=0)
):
    route_obj = CRUDRoutes(RouteModel).remove(db=db, id=route_id)
    return {'message': f'The route with id = {route_id} was removed successfully'}