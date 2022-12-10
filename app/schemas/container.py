from pydantic import BaseModel
from pydantic import Field


class Container(BaseModel):
    container_id: int = Field(
        ...,
        gt=1,
        example=23
    )
    address: str = Field(
        ...,
        min_length=4,
        max_length=40,
        example='Calle 3 No 2'
    )
    volume: float = Field(..., example=4000.45)
    latitude: float = Field(..., example=11.465376)
    longitude: float = Field(..., example=17.642488)