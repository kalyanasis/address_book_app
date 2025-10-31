from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from sqlalchemy.orm import Session
from app.schemas.address import AddressCreate, AddressOut, AddressUpdate
from app.crud import address as crud
from app.api.deps import get_db

router = APIRouter()

@router.post("/", response_model=AddressOut, status_code=201)
def create_address(payload: AddressCreate, db: Session = Depends(get_db)):
    return crud.create(db, obj_in=payload)

@router.get("/", response_model=List[AddressOut])
def list_addresses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_all(db, skip, limit)

@router.get("/{address_id}", response_model=AddressOut)
def get_address(address_id: int, db: Session = Depends(get_db)):
    obj = crud.get(db, address_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Address not found")
    return obj

@router.put("/{address_id}", response_model=AddressOut)
def update_address(address_id: int, payload: AddressUpdate, db: Session = Depends(get_db)):
    obj = crud.get(db, address_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Address not found")
    return crud.update(db, obj, payload)

@router.delete("/{address_id}", status_code=204)
def delete_address(address_id: int, db: Session = Depends(get_db)):
    obj = crud.get(db, address_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Address not found")
    crud.delete(db, obj)
    return None

@router.get("/nearby", response_model=List[AddressOut])
def nearby(lat: float = Query(...), lon: float = Query(...), distance_km: float = Query(..., gt=0.0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    if lat < -90 or lat > 90:
        raise HTTPException(status_code=400, detail="lat must be between -90 and 90")
    if lon < -180 or lon > 180:
        raise HTTPException(status_code=400, detail="lon must be between -180 and 180")
    results = crud.nearby(db, lat, lon, distance_km, limit)
    return [r["address"] for r in results]
