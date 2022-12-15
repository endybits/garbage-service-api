from sqlalchemy import Column, Float, String, Integer, DateTime, Enum, PickleType 
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.mutable import MutableList

from app.utils.base import StatusContainer, StatusRoute

Base = declarative_base()

class ContainerModel(Base):
    __tablename__ = 'container'

    container_id = Column(Integer, primary_key=True)
    address = Column(String(50), nullable=False)
    volume = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    status = Column(Enum(StatusContainer), nullable=False, default=StatusContainer.empty)

class RouteModel(Base):
    __tablename__ = 'routes'

    route_id = Column(Integer, primary_key=True)
    cumulative_vol = Column(Float, nullable=False, default=0)
    points = Column(MutableList.as_mutable(PickleType), default=[])
    status = Column(Enum(StatusRoute), nullable=False, default=StatusRoute.opened)