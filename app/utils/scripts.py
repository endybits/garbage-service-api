from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import Depends

from app.api.deps import get_db
from app.models.models import RouteModel, ContainerModel
from app.schemas.route import Route
from app.crud.routes import CRUDRoutes
from app.crud.container import CRUDContainer
from app.utils.base import StatusRoute

def get_last_route(db: Session = Depends(get_db)) -> Optional[RouteModel]:
    last_route = CRUDRoutes(RouteModel).get_last_row(db=db)
    return last_route

def get_container(db: Session = Depends(get_db), container_id: int=0) -> Optional[ContainerModel]:
    container_obj = CRUDContainer(ContainerModel).get(db=db, id=container_id)
    return container_obj


def add_point_to_route(
    container_id: int = 0,
    volume: float = 0,
    db: Session = Depends(get_db),
):
    ## Get last route_id (OK)
    ## Validate if container_id not already exists in route point's list (OK)
    ## Get container object (Ok)
    ## Add container volume (Ok)
    ## Verify if cumulative value is >= truck capacity
    ## - If True: Launch routing service.

    route_obj = get_last_route(db=db)
    if isinstance(route_obj, RouteModel):
        ID = route_obj.route_id
        CUMULIATIVE_VOL = route_obj.cumulative_vol
        STATUS = route_obj.status
        LOCATIONS = [point for point in route_obj.points]
        route_schema = Route(
            route_id=int(str(ID)),
            cumulative_vol=float(str(CUMULIATIVE_VOL)),
            points=LOCATIONS,
            status=StatusRoute(STATUS)
        )
        
        locations = route_schema.points
        print(locations)
        container_id = 2
        is_duplicated = False
        for location in  locations:
            if location['container_id'] == container_id:
                #TODO Could be necessary to raise an Exeption.
                is_duplicated = True
                print(f"Duplicate asignation container_id = {container_id}")
        if not is_duplicated:
            container =  get_container(db=db, container_id=container_id)
            if isinstance(container, ContainerModel):
                ## Update route
                CUMULIATIVE_VOL += container.volume
                container_point = {
                    "container_id": container.container_id,
                    "latitude": container.latitude,
                    "longitude": container.longitude
                }
                locations.append(container_point)
                obj_in = {
                    "points": locations,
                    "cumulative_vol": CUMULIATIVE_VOL
                }
                print(obj_in)
                updated_route = CRUDRoutes(RouteModel).update(db=db, db_obj=route_obj, object_in=obj_in)
                print(updated_route)
                if updated_route >= 10000:
                    print('Launching Routing Service.')
                    
                    ### Tansform Status to closed
                    ### Calculate Optimal Route
                    ### Create a new field called optimar_route
                    ### Generate an Alert to generate the service trip. 
                    ### Create a new route. 