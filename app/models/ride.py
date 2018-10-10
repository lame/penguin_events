from math import ceil
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .location import Location
from .. import Base

FREE_RIDE_MAX_LENGTH = 60


class Ride(Base):
    """
    TODO: Finish docstring

    Properties:
        duration        (int):              Integer representation of the ride duration in seconds.
        is_free_ride    (bool):             Boolean value of if the ride should be charged to the user
        ride_minutes    (int):              The ceiling whole number of the ride minutes
        cost            (int):              The total cost to the user for the ride (start event and end event pair)
        start_location  (:obj: Location):   The location object of the START_RIDE event
        end_location    (:obj: Location):   the location object of the END_RIDE event

    """
    __tablename__ = 'rides'

    id = Column(Integer, primary_key=True)
    events = relationship("Event", backref='users')

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User")

    def __init__(self, user, vehicle, start_event):
        self.user = user
        self.vehicle = vehicle
        self.events.append(start_event)

    def end_ride(self, end_event):
        self.events.append(end_event)

    def distance(self):
        start = Location(self.start_location.lat, self.start_location.long)
        end = Location(self.end_location.lat, self.end_location.long)
        if start and end:
            return Location.get_distance(start, end)
        else:
            return 0

    # Business Logic
    # The cost of a ride is:
    #   $1 to start
    #   $0.15 for every started minute.
    # Edge Case:
    #   If the ride lasts less than 1 minute, the cost is $0. For example:

    @property
    def duration(self):
        return self.events[1].timestamp - self.events[0].timestamp

    @property
    def is_free_ride(self):
        return self.duration < FREE_RIDE_MAX_LENGTH

    @property
    def ride_minutes(self):
        return ceil(self.duration / 60)

    @property
    def cost(self):
        if not self.is_free_ride:
            cost =  1 + 0.15 * self.ride_minutes
            return round(cost, 2)
        else:
            return 0

    @property
    def start_location(self):
        if len(self.events) > 0:
            return self.events[0].location
        else:
            return None

    @property
    def end_location(self):
        if len(self.events) > 1:
            return self.events[1].location
        else:
            return None
