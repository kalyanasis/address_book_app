from pydantic import BaseModel, Field, validator
from typing import Optional

class AddressBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    street: str = Field(..., min_length=1, max_length=300)
    city: str = Field(..., min_length=1, max_length=200)
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: float = Field(..., example=12.9716)
    longitude: float = Field(..., example=77.5946)

    @validator('latitude')
    def check_lat(cls, v):
        if v < -90 or v > 90:
            raise ValueError('latitude must be between -90 and 90')
        return v

    @validator('longitude')
    def check_lon(cls, v):
        if v < -180 or v > 180:
            raise ValueError('longitude must be between -180 and 180')
        return v

class AddressCreate(AddressBase):
    pass

class AddressUpdate(BaseModel):
    name: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    @validator('latitude')
    def check_lat_opt(cls, v):
        if v is None:
            return v
        if v < -90 or v > 90:
            raise ValueError('latitude must be between -90 and 90')
        return v

    @validator('longitude')
    def check_lon_opt(cls, v):
        if v is None:
            return v
        if v < -180 or v > 180:
            raise ValueError('longitude must be between -180 and 180')
        return v

class AddressOut(AddressBase):
    id: int

    class Config:
        # orm_mode = True
        from_attributes = True

