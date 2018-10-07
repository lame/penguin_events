import enum
from sqlalchemy import Column, ForeignKey, Integer, Enum
from sqlalchemy.orm import relationship, backref

from .. import Base
from .common import EventType


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    type = Column('value', Enum(EventType), nullable=False)
    timestamp = Column(Integer, nullable=False)

    # Location, 1:1 with no backref relationship
    location_id = Column(Integer, ForeignKey('locations.id'))
    location = relationship("Location", backref=backref("events", uselist=False))

    # Vehicle, 1:M with backref
    #   Every vehicle has many events
    #   Every event has one vehicle
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'))
    vehicle = relationship("Vehicle")

    # Vehicle, 1:M with backref
    #   Every user has many events
    #   Every event has one user
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User")

    def __repr__(self):
        return f'{self.type.name} Event\nID: {self.id}\nVehicle: {self.vehicle_id}'
