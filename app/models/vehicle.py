from geopy.distance import geodesic
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from .common import EventType
from .. import Base

# Setting limits for Lat/Long because sample file
# has lat of -93, which freaks out geopy
LAT_FLOOR = -90.0
LAT_CEIL = 90.0
LONG_FLOOR = -180.0
LONG_CEIL = 180.0


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

    # Events: 1:M each vehicle has many events
    events = relationship('Event', backref='vehicles')

    # drop_location_id = Column(Integer, ForeignKey('location.id'))
    # drop_location = relationship('Location', backref=backref('vehicles.drop_location', uselist=False))
    #
    # current_location_id = Column(Integer, ForeignKey('location.id'))
    # current_location = relationship('Location', backref=backref('vehicles.current_location', uselist=False))

    # Location, 1:M with no backref relationship, this
    #   will store in the order:
    #       locations[0]: drop_location
    #       locations[1]: start_location
    #       locations[2]: end_location
    locations = relationship('Location', backref='vehicles')

    def __init__(self, id):
        self.id = id

    def update_location(self, event_type, location):
        if event_type is EventType.DROP:
            del self.start_location
            del self.end_location
            self.drop_location = location
        if event_type is EventType.START_RIDE or event_type is EventType.DROP:
            del self.end_location
            self.start_location = location
        else:
            self.end_location = location
        return self

    @property
    def drop_location(self):
        return self.locations[0]

    @drop_location.setter
    def drop_location(self, value):
        self.locations.append(value)

    @property
    def start_location(self):
        return self.locations[1]

    @start_location.setter
    def start_location(self, value):
        self.locations.append(value)

    @start_location.deleter
    def start_location(self):
        if len(self.locations) > 1:
            del self.locations[1]

    @property
    def end_location(self):
        return self.locations[2]

    @end_location.setter
    def end_location(self, value):
        self.locations.append(value)

    @end_location.deleter
    def end_location(self):
        if len(self.locations) > 2:
            del self.locations[2]

    def event_distance(self, start_at_drop=False):
        try:
            if start_at_drop:
                start = self._limit_lat_long(self.drop_location.lat, self.drop_location.long)
            else:
                start = self._limit_lat_long(self.start_location.lat, self.start_location.long)
            end = self._limit_lat_long(self.end_location.lat, self.end_location.long)
            return self._get_distance(start, end)
        except IndexError:
            return 0

    def _limit_lat_long(self, lat, long):
        lat = self._limit(lat, LAT_FLOOR, LAT_CEIL)
        long = self._limit(long, LONG_FLOOR, LONG_CEIL)
        return lat, long

    @staticmethod
    def _limit(n, minn, maxn):
        return max(min(maxn, n), minn)

    @staticmethod
    def _get_distance(start, end):
        return geodesic(start, end).meters

    @classmethod
    def max_distance_from_drop(cls, session):
        max_from_drop = (None, 0)
        for vehicle in session.query(cls).all():
            distance = vehicle.event_distance(start_at_drop=True)
            if distance > max_from_drop[1]:
                max_from_drop = (vehicle.id, distance)

        return max_from_drop

    @classmethod
    def vehicles_count(cls, session):
        return session.query(cls).count()
