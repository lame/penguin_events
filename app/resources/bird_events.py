import csv

from .events_facade import EventsFacade
from app.models.vehicle import Vehicle


class BirdEvents(object):
    """ This class will take care of how our information is ingested by the program.
    In this version there is only a read_file method, however with the EventsFacade
    class, it can easily be altered to accept an input stream like pub/sub, and can
    also be made Async to keep response times quick

    Args:
        in_file (str):              The file to use for bird events data
        session (:obj: Session):    SQLAlchemy database session object

    Attributes:
        total_distance (dict):      A dictionary with key scooter_id and value total distance covered (in meters)

    Properties:
        num_scooters   (int):                                   The integer value of the number of scooters dropped in the simulation
        max_distance   (:tuple: (scooter_id, distance)):        A tuple of scooter ID's and it's associated distance (in meters)
        farthest_from_drop   (:tuple: (scooter_id, distance)):  A tuple of scooter ID's and it's associated distance (in meters)
    """

    def __init__(self, in_file, session):
        self._session = session
        self.in_file = in_file
        self.total_distance = {}

    def read_file(self):
        with open(self.in_file, newline='') as csvfile:
            line_reader = csv.reader(csvfile, delimiter=',')
            for row in line_reader:
                ef = EventsFacade(
                    timestamp = row[0],
                    vehicle_id = row[1],
                    event_type = row[2],
                    lat = row[3],
                    long = row[4],
                    user_id = row[5],
                    session = self._session
                ).create()
                self._update_total_distance(ef)
        return self

    def _update_total_distance(self, ef):
        if self.total_distance.get(ef.vehicle.id):
            self.total_distance[ef.vehicle.id] += ef.vehicle.event_distance()
        else:
            self.total_distance[ef.vehicle.id] = ef.vehicle.event_distance()
        return self.total_distance

    # The following properties should logically be placed in Vehicle class,
    # however there is a performance benefit because the iterative event
    # creation can keep track of state we would otherwise have to search
    # again through the DB for. I have included those implementations as well
    # for the sake of completemess in the Vehicle class

    @property
    def vehicles_count(self):
        return len(set(self.total_distance.keys()))

    @property
    def max_distance_for_ride(self):
        max_distance = (None, 0)
        for key, value in self.total_distance.items():
            if value > max_distance[1]:
                max_distance = (key, value)
        return max_distance


