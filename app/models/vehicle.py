from geopy.distance import geodesic
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .. import Base
from .common import EventType

LAT_FLOOR = -90.0
LAT_CEIL = 90.0
LONG_FLOOR = -180.0
LONG_CEIL = 180.0


class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(String, primary_key=True)

    # Events: 1:M 1 vehicle has many events
    events = relationship('Event', backref='vehicles')

    # Location, 1:M with no backref relationship, this
    #   will store in the order:
    #   [0]: drop_location
    #   [1]: start_location
    #   [2]: end_location
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
        return self.locations

    @property
    def start_location(self):
        return self.locations[1]

    @start_location.setter
    def start_location(self, value):
        self.locations.append(value)
        return self.locations

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
        return self.locations

    @end_location.deleter
    def end_location(self):
        if len(self.locations) > 2:
            del self.locations[2]

    def event_distance(self, start_at_drop=False):
        try:
            if start_at_drop:
                start = self.limit_lat_long(self.drop_location.lat, self.drop_location.long)
            else:
                start = self.limit_lat_long(self.start_location.lat, self.start_location.long)
            end = self.limit_lat_long(self.end_location.lat, self.end_location.long)
            return self.get_distance(start, end)
        except IndexError:
            return 0

    def limit_lat_long(self, lat, long):
        lat = self.limit(lat, LAT_FLOOR, LAT_CEIL)
        long = self.limit(long, LONG_FLOOR, LONG_CEIL)
        return lat, long

    @staticmethod
    def limit(n, minn, maxn):
        return max(min(maxn, n), minn)

    @staticmethod
    def get_distance(start, end):
        try:
            return geodesic(start, end).meters
        except ValueError:
            # Need to log the error
            breakpoint()
            return 0
