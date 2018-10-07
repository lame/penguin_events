from dataclasses import dataclass
from sqlalchemy.orm.session import Session

from app.models.common import EventType, find_or_initialize_by, session_add_and_commit
from app.models.event import Event
from app.models.location import Location
from app.models.vehicle import Vehicle
from app.models.user import User


class EventsFacade(object):
    # FIXME: Add proper class docstring
    """Exceptions are documented in the same way as classes.

    The __init__ method may be documented in either the class level
    docstring, or as a docstring on the __init__ method itself.

    Either form is acceptable, but the two should not be mixed. Choose one
    convention to document the __init__ method and be consistent with it.

    Note:
        Do not include the `self` parameter in the ``Args`` section.

    Args:
        msg (str): Human readable string describing the exception.
        code (:obj:`int`, optional): Error code.

    Attributes:
        msg (str): Human readable string describing the exception.
        code (int): Exception error code.

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

        # Set Location
        self.location = Location(lat=self._lat, long=self._long)

        # Set Vehicle
        self.vehicle = find_or_initialize_by(self._session, Vehicle, **{'id': vehicle_id})
        self.vehicle.update_location(self._event_type, self.location)

        # Set Event
        self.event = Event(
            type=self._event_type,
            timestamp=self._timestamp,
            location=self.location,
            vehicle=self.vehicle
        )

        # Set User
        self.user = find_or_initialize_by(self._session, User, **{'id': self._user_id})
        self.user.events.append(self.event)

    def create(self):
        session_add_and_commit(self._session, [self.location, self.vehicle, self.event, self.user])
        return self
