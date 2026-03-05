from pydantic import BaseModel, computed_field, ConfigDict,Field
from geoalchemy2.shape import to_shape
from shapely.geometry import Point
from typing import Optional, Any

class Cafe(BaseModel):
    id: int
    name: str
    address: str
    phone: Optional[str] = None

class SpecificCafe(Cafe):
    location: Any = Field(exclude=True) 
    # Instead, we create computed fields:
    
    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def latitude(self) -> float:
        # 'self.location' is the SQLAlchemy Geography object
        # to_shape converts it to a Shapely Point(x, y)
        # 2. Type cast to 'Point' so the IDE knows .y exists
        shape = to_shape(self.location)
        if isinstance(shape, Point):
            return float(shape.y)
        return 0.0
    
    @computed_field
    @property
    def longitude(self) -> float:
        shape = to_shape(self.location)
        if isinstance(shape, Point):
            return float(shape.x)
        return 0.0