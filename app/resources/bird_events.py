import csv

from .events_facade import EventsFacade


class BirdEvents(object):

    def __init__(self, in_file, session):
        self.session = session
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
                    session = self.session
                ).create()
                if self.total_distance.get(ef.vehicle.id):
                    self.total_distance[ef.vehicle.id] += ef.vehicle.event_distance()
                else:
                    self.total_distance[ef.vehicle.id] = ef.vehicle.event_distance()
            breakpoint()
