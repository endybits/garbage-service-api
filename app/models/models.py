from sqlalchemy import Column, Float, String, Integer, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ContainerModel(Base):
    __tablename__ = 'container'

    container_id = Column(Integer, primary_key=True)
    address = Column(String(50), nullable=False)
    volume = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)