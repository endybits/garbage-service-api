from typing import Any

from sqlalchemy.orm import Session
from fastapi import APIRouter
from fastapi import status, Depends
from fastapi import Body

from app.api.deps import get_db
from app.models.models import RouteModel
from app.schemas.route import Route, RouteCreate, RouteUpdate
from app.crud.routes import CRUDRoutes

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
    object_route = Route(
        route_id=route_created_model.route_id,
        cumulative_vol=route_created_model.cumulative_vol,
        points=route_created_model.points,
        status=route_created_model.status
    )
    return object_route