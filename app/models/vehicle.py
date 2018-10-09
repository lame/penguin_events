from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from .common import EventType
from .location import Location
from .. import Base


class Vehicle(Base):
    """ The Vehicle class exists to store vehicle data. Properties are available for computed fields such as
    the total distance that a vehicle has covered.

    Args:
        id (str): The vehicle ID string, should be unique to the vehicle

    Attributes:
        id          (str):              The ID of the vehicle
        events      (:obj: [Event]):    A list of all the events the vehicle has had
        locations   (:obj: [Location]): A list of all the locations a vehicle has been

    Properties:
        drop_location   (:obj: Location): Location object of the instance's first drop event of the simulation
        start_location  (:obj: Location): Location object of the instance's most recent start location
        end_location    (:obj: Location): Location object of the instance's most recent end location, if a new start event has not yet begun
    """

    __tablename__ = 'vehicles'

    id = Column(String, primary_key=True)
    total_distance = Column(Float, default=0, nullable=False)

    # Events: 1:M each vehicle has many events
    events = relationship('Event', backref='vehicles')

    drop_location_id = Column(Integer, ForeignKey('locations.id'))
    drop_location = relationship('Location', foreign_keys=[drop_location_id])

    current_location_id = Column(Integer, ForeignKey('locations.id'))
    current_location = relationship('Location', foreign_keys=[current_location_id])

    def __repr__(self):
        return self.id

    def update_location(self, event_type, location):
        if event_type is EventType.DROP:
            self.drop_location = location
            self.current_location = location
        else:
            self.total_distance += Location.get_distance(self.current_location, location)
            self.current_location = location
        return self

    @property
    def distance_from_drop(self):
        return Location.get_distance(start=self.drop_location, end=self.current_location)

    @classmethod
    def max_distance_from_drop(cls, session):
        max_from_drop = (None, 0)
        for vehicle in session.query(cls).all():
            if vehicle.distance_from_drop > max_from_drop[1]:
                max_from_drop = (vehicle.id, vehicle.distance_from_drop)
        return max_from_drop

    @classmethod
    def max_distance_traveled(cls, session):
        max_distance = (None, 0)
        for vehicle in session.query(cls).all():
            if vehicle.total_distance > max_distance[1]:
                max_distance = (vehicle.id, vehicle.total_distance)
        return max_distance

    @classmethod
    def vehicles_count(cls, session):
        return session.query(cls).count()
