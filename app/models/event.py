from sqlalchemy import Column, ForeignKey, Integer, Enum
from sqlalchemy.orm import relationship, backref

from .. import Base
from .common import EventType


class Event(Base):
    """
    # TODO: Fill in the class docstring
    """
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    type = Column('value', Enum(EventType), nullable=False)
    timestamp = Column(Integer, nullable=False)

    # Location, 1:1 with no backref relationship
    location_id = Column(Integer, ForeignKey('locations.id'))
    location = relationship("Location", backref=backref("events", uselist=False))

    # Vehicle, 1:M with backref
    #   Every vehicle has many events
    #   Every event belongs to a vehicle
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'))
    vehicle = relationship("Vehicle")

    # Ride, 1:M with backref
    #   Every ride has 2 events
    #   Every event belongs to a ride
    ride_id = Column(Integer, ForeignKey('rides.id'))
    ride = relationship("Ride")

    def __repr__(self):
        return f'{self.type.name} Event\nID: {self.id}\nVehicle: {self.vehicle_id}'
