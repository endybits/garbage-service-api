from typing import List

from pydantic import BaseModel
from pydantic import Field

from app.utils.base import StatusRoute

class RouteBase(BaseModel):
    cumulative_vol: float = Field(..., example=0)
    points: List = Field(..., example=[])
    status: StatusRoute = Field(..., example=StatusRoute.opened)


class Route(RouteBase):
    route_id: int = Field(..., gt=0, example=12)


class RouteCreate(RouteBase):
    pass


class RouteUpdate(RouteBase):
    ### Verify if this class heritage of RouteBase (without route_id)
    pass
