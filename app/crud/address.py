from sqlalchemy.orm import Session
from typing import List
from app.models.address import Address
from app.schemas.address import AddressCreate, AddressUpdate
import math

EARTH_RADIUS_KM = 6371.0088

def create(db: Session, *, obj_in: AddressCreate) -> Address:
    db_obj = Address(
        name=obj_in.name.strip(),
        street=obj_in.street.strip(),
        city=obj_in.city.strip(),
        state=(obj_in.state.strip() if obj_in.state else None),
        country=(obj_in.country.strip() if obj_in.country else None),
        postal_code=(obj_in.postal_code.strip() if obj_in.postal_code else None),
        latitude=round(obj_in.latitude, 8),
        longitude=round(obj_in.longitude, 8),
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get(db: Session, id: int):
    return db.query(Address).filter(Address.id == id).first()

def list_all(db: Session, skip: int = 0, limit: int = 100) -> List[Address]:
    return db.query(Address).offset(skip).limit(limit).all()

def update(db: Session, db_obj: Address, obj_in: AddressUpdate) -> Address:
    data = obj_in.dict(exclude_unset=True)
    for field, value in data.items():
        if isinstance(value, str):
            value = value.strip()
        if field in ('latitude','longitude') and value is not None:
            value = round(value,8)
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, db_obj: Address):
    db.delete(db_obj)
    db.commit()

def _haversine(lat1, lon1, lat2, lon2):
    lat1_r = math.radians(lat1)
    lon1_r = math.radians(lon1)
    lat2_r = math.radians(lat2)
    lon2_r = math.radians(lon2)
    dlat = lat2_r - lat1_r
    dlon = lon2_r - lon1_r
    a = math.sin(dlat/2)**2 + math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return EARTH_RADIUS_KM * c

def nearby(db: Session, lat: float, lon: float, distance_km: float, limit: int = 100):
    # simple bounding box to reduce candidates
    lat_delta = distance_km / 111.32
    lon_delta = distance_km / (111.32 * abs(math.cos(math.radians(lat))) if abs(math.cos(math.radians(lat)))>1e-9 else 1e-9)
    min_lat, max_lat = max(lat - lat_delta, -90.0), min(lat + lat_delta, 90.0)
    min_lon, max_lon = max(lon - lon_delta, -180.0), min(lon + lon_delta, 180.0)

    candidates = db.query(Address).filter(
        Address.latitude >= min_lat,
        Address.latitude <= max_lat,
        Address.longitude >= min_lon,
        Address.longitude <= max_lon,
    ).all()

    results = []
    for c in candidates:
        d = _haversine(lat, lon, c.latitude, c.longitude)
        if d <= distance_km + 1e-9:
            results.append({"address": c, "distance_km": round(d,6)})
    results.sort(key=lambda x: x["distance_km"])
    return results[:limit]
