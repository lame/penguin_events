from sqlalchemy.orm.session import Session

from app.models.common import EventType, DBOperations
from app.models.event import Event
from app.models.location import Location
from app.models.vehicle import Vehicle
from app.models.user import User
from app.models.ride import Ride


class EventsFacade(object):
    """ The EventsFacade class takes the args listed below as strings, performs all necessary
    type conversions and returns an EventsFacade instance that has a Location, Vehicle, Event
    and User on it to perform any necessary post-processing.

    Args:
        timestamp   (int):              The time, in seconds, from the beginning of the events stream
        vehicle_id: (str):              String Id of the bird vehicle (scooter... for now!)
        event_type: (str):              Events include 'DROP', 'START_RIDE' and 'END_RIDE'
        lat:        (float):            Latitude of the current location, between [-90.0, +90.0]
        long:       (float):            Longitude of the current location, between [-180.0, +180.0]
        user_id:    (int):              The integer ID of a user
        session:    (:obj: Session):    The SQLAlchemy database session object

    Attributes:
        location (:obj: Location)       The Lat/Long location
        vehicle  (:obj: Vehicle)        The Vehicle object with id, vehicle_location, etc.
        event    (:obj: Event)          The Event object that has a user, a vehicle, timestamp, etc.
        user     (:obj: User)           The User object with id, many events
        ride     (:obj: Ride)           The Ride object that contains a user and 2 events, plus the cost of rides and such

    """

    def __init__(self,
                 timestamp: int,
                 vehicle_id: str,
                 event_type: str,
                 lat: float,
                 long: float,
                 user_id: int,
                 session: Session
                 ):

        # Format input vars
        self._timestamp = int(timestamp)
        self._event_type = EventType[event_type]
        self._lat = float(lat)
        self._long = float(long)
        self._user_id = (None if user_id == 'NULL' else int(user_id))
        self._session = session

        # Set User
        self.user = DBOperations.find_or_initialize_by(self._session, User, **{'id': self._user_id})

        # Set Location
        self.location = Location(lat=self._lat, long=self._long)

        # Set Vehicle
        self.vehicle = DBOperations.find_or_initialize_by(self._session, Vehicle, **{'id': vehicle_id})
        self.vehicle.update_location(self._event_type, self.location)

        # Set Event
        self.event = Event(
            type=self._event_type,
            timestamp=self._timestamp,
            location=self.location,
            vehicle=self.vehicle,
        )

        # Set Ride
        self.ride = None
        if self.event.type is EventType.START_RIDE:
            self.ride = Ride(self.user, self.vehicle, self.event)
        elif self.event.type is EventType.END_RIDE:
            self.ride = self.user.rides[-1]
            self.ride.end_ride(self.event)

    def create(self):
        """ Persist location, vehicle, event, and user instances to database
        :return: EventsFacade instsance
        """
        to_commit = [self.location, self.vehicle, self.event, self.user]
        if self.ride:
            to_commit.append(self.ride)

        DBOperations.session_add_and_commit(
            self._session,
            to_commit
        )
        return self
