import argparse

from app import session_factory
from app.resources.bird_events import BirdEvents

def main():
    parser = argparse.ArgumentParser(description='Process Bird Vehicle Events')
    parser.add_argument('in_file', type=str, help='Input file of comma separated events')
    args = parser.parse_args()

    if args.in_file:
        session = session_factory()
        BirdEvents(args.in_file, session).read_file()
        breakpoint()

        session.close()

def vehicle_drop_count(session):
    # return drop_count
    pass

def farthest_from_drop_location(session):
    # return vehicle.id, distance
    pass

def longest_vehicle_distance(session):
    # return vehicle.id, distance
    pass



if __name__ == '__main__':
    main()
