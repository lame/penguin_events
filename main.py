import argparse

from app import session_factory
from app.resources.bird_events import BirdEvents

def main():
    parser = argparse.ArgumentParser(description='Process Bird Vehicle Events')
    parser.add_argument('in_file', type=str, help='Input file of comma separated events')
    args = parser.parse_args()

    response = ''

    if args.in_file:
        # Possible refactor: create a wrapper for main() so session will be created and closed implicitly
        session = session_factory()

        bird_events = BirdEvents(args.in_file, session).read_file()
        response += vehicle_drop_count(bird_events)
        response += farthest_from_drop_location(bird_events)
        response += longest_vehicle_distance(bird_events)

        session.close()

def vehicle_drop_count(ef):
    return f'\nNumber of Bird Vehicles Dropped in Simulation: {ef.num_scooters}'

def farthest_from_drop_location(ef):
    # Please note that distance measures are in meters and have decimals truncated for clarity
    vehicle_id, distance = ef.farthest_from_drop
    return f'\nVehicle {vehicle_id} was the farthest from the initial drop location at {distance:.0f} meters'

def longest_vehicle_distance(ef):
    # Please note that distance measures are in meters and have decimals truncated for clarity
    vehicle_id, distance = ef.max_distance
    return f'\nVehicle {vehicle_id} traveled the most distance today with {distance:.0f} meters'


if __name__ == '__main__':
    main()
