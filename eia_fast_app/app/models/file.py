from pydantic import BaseModel, Field, PrivateAttr, conlist, confloat
from typing import List, Dict, Any, Tuple 
from shapely.geometry import Polygon


class GeoJSONFeature(BaseModel):
    type: str
    properties: Dict[str, str]
    geometry: Dict[str, List[List[float]]]

class GeoJSONData(BaseModel):
    type: str
    features: List[GeoJSONFeature]

# validate polygons
 
class Latitude(BaseModel):
    value: confloat(ge=-90, le=90)

class Longitude(BaseModel):
    value: confloat(ge=-180, le=180)
 

class RawPolygon(BaseModel):
    __root__: conlist(conlist(Tuple[Longitude, Latitude], min_items=3), min_items=1)
    _polygon: Polygon = PrivateAttr()
 
    def __init__(self, **data: Any):
        super().__init__(**data)
        self._polygon = Polygon(data["__root__"][0], data["__root__"][1:])
 
    @property
    def polygon(self) -> Polygon:
        return self._polygon
 
class MyModel(BaseModel):
 
    raw_polygon: RawPolygon = Field(..., alias="polygon")
 
    @property
    def polygon(self) -> Polygon:
        return self.raw_polygon.polygon