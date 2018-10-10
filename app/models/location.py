from geopy.distance import geodesic
from sqlalchemy import Column, Integer, Float

from .. import Base

# Setting limits for Lat/Long because sample file
# has lat of -93, which freaks out geopy
LAT_FLOOR = -90.0
LAT_CEIL = 90.0
LONG_FLOOR = -180.0
LONG_CEIL = 180.0


"""
Location is being used at a child with no backref relation
to the parent so that an Event can have a Location, but 
also a Vehicle can have a Location that would be updated
every time the Vehicle phones home or is polled
"""
class Location(Base):
    """
    TODO: Fill in the doc string
    """
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    lat = Column(Float, nullable=False)
    long = Column(Float, nullable=False)

    def __init__(self, lat, long):
        self.lat = self._limit(lat, LAT_FLOOR, LAT_CEIL)
        self.long = self._limit(long, LONG_FLOOR, LONG_CEIL)

    def __repr__(self):
        return f'lat: {self.lat:.2f}\nlong: {self.long:.2f}'

    @staticmethod
    def _limit(n, minn, maxn):
        return max(min(maxn, n), minn)

    @staticmethod
    def get_distance(start, end):
        return geodesic((start.lat, start.long), (end.lat, end.long)).meters


