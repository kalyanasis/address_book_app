from sqlalchemy import Column, Integer, String, Float
from app.db.base import Base

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    street = Column(String(300), nullable=False)
    city = Column(String(200), nullable=False)
    state = Column(String(200), nullable=True)
    country = Column(String(200), nullable=True)
    postal_code = Column(String(50), nullable=True)
    latitude = Column(Float, nullable=False, index=True)
    longitude = Column(Float, nullable=False, index=True)
