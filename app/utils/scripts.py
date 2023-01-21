from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi.encoders import jsonable_encoder

from app.api.deps import get_db
from app.models.models import RouteModel, ContainerModel
from app.schemas.route import Route
from app.crud.routes import CRUDRoutes
from app.crud.container import CRUDContainer
from app.utils.base import StatusRoute
from app.utils.vehicle_routing_problem import sort_vehicle_routing_problem

def get_last_route(db: Session = Depends(get_db)) -> Optional[RouteModel]:
    last_route = CRUDRoutes(RouteModel).get_last_row(db=db)
    return last_route

def get_container(db: Session = Depends(get_db), container_id: int=0) -> Optional[ContainerModel]:
    container_obj = CRUDContainer(ContainerModel).get(db=db, id=container_id)
    return container_obj


def add_point_to_route(
    container_id: int = 0,
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
        json_route = jsonable_encoder(route_obj)
        print(json_route['status'] is not StatusRoute.closed)
        if json_route['status'] is not StatusRoute.closed:
            route_schema = Route(
                route_id = json_route['route_id'],
                cumulative_vol = json_route['cumulative_vol'],
                points = [point for point in json_route['points'] ],
                status=StatusRoute(json_route['status'])
            )
            
            locations = route_schema.points
            print(locations)
            is_duplicated = False
            for location in  locations:
                if location['container_id'] == container_id:
                    #TODO Could be necessary to raise an Exception.
                    is_duplicated = True
                    print(f"Duplicate asignation container_id = {container_id}")
            if not is_duplicated:
                container =  get_container(db=db, container_id=container_id)
                if isinstance(container, ContainerModel):
                    ## Update route
                    json_route['cumulative_vol'] += container.volume
                    container_point = {
                        "container_id": container.container_id,
                        "latitude": container.latitude,
                        "longitude": container.longitude
                    }
                    locations.append(container_point)
                    obj_in = {
                        "points": locations,
                        "cumulative_vol": round(json_route['cumulative_vol'], 2)
                    }
                    if json_route['cumulative_vol'] >= 10000:
                        #TODO cuando funcione bien, descomentar la linea de abajo
                        #obj_in['status'] = StatusRoute.closed
                        updated_route = CRUDRoutes(RouteModel).update(db=db, db_obj=route_obj, object_in=obj_in)
                        print(updated_route)
                        print('Launching Routing Service.')
                        
                        ### Tansform Status to closed
                        
                        
                        ### Calculate Optimal Route
                        route_json = jsonable_encoder(updated_route)
                        points_list = route_json['points']
                        locations_to_sort = []

                        for point in points_list:
                            point_tuple = (
                                point['latitude'],
                                point['longitude'],
                                point['container_id']
                            )
                            locations_to_sort.append(point_tuple)
                        print(locations_to_sort)
                        sorted_locations = sort_vehicle_routing_problem(locations_to_sort)
                        if isinstance(sorted_locations, list):
                            print(sorted_locations)
                            obj_in_sorted_route = {
                                "points": sorted_locations,
                                "status": StatusRoute.closed
                            }
                            sorted_route = CRUDRoutes(RouteModel).update(db=db, db_obj=route_obj, object_in=obj_in_sorted_route)
                            print(jsonable_encoder(sorted_route))
                        
                        ### Generate the service trip. 
                        ### Entre las acciones dentro del service trip se debe crear una ruta nueva
                        ### Y buscar una forma de vaciar todos los containers de la route list relacionada al service trip.

                    else:
                        updated_route = CRUDRoutes(RouteModel).update(db=db, db_obj=route_obj, object_in=obj_in)
                        print(updated_route)

#        else:
#            print('You need create a new route and recall the add_point_to_route function')