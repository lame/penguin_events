import csv

from .events_facade import EventsFacade


class PenguinEvents(object):
    """ This class will take care of how our information is ingested by the program.
    In this version there is only a read_file method, however with the EventsFacade
    class, it can easily be altered to accept an input stream like pub/sub, and can
    also be made Async to keep response times quick

    Args:
        in_file (str):              The file to use for penguin events data
        session (:obj: Session):    SQLAlchemy database session object
    """

    def __init__(self, in_file, session):
        self._session = session
        self.in_file = in_file

    def read_file(self):
        try:
            with open(self.in_file, newline='') as csvfile:
                line_reader = csv.reader(csvfile, delimiter=',')
                for row in line_reader:
                    EventsFacade(
                        timestamp = row[0],
                        vehicle_id = row[1],
                        event_type = row[2],
                        lat = row[3],
                        long = row[4],
                        user_id = row[5],
                        session = self._session
                    ).create()
        except Exception:
            raise ValueError('infile expected to be comma separated values')
