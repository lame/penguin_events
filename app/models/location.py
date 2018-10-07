from sqlalchemy import Column, Integer, Float, ForeignKey

from .. import Base

"""
Location is being used at a child with no backref relation
to the parent so that an Event can have a Location, but 
also a Vehicle can have a Location that would be updated
every time the Vehicle phones home or is polled
"""
class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    lat = Column(Float, nullable=False)
    long = Column(Float, nullable=False)

    vehicle_id = Column(Integer, ForeignKey('vehicles.id'))

    def __repr__(self):
        return f'lat: {self.lat:.2f}\nlong: {self.long:.2f}'


