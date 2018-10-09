import argparse

from app import session_factory
from app.resources.bird_events import BirdEvents
from app.models.vehicle import Vehicle
from app.models.user import User

def main():
    parser = argparse.ArgumentParser(description='Process Bird Vehicle Events')
    parser.add_argument('in_file', type=str, help='Input file of comma separated events')
    args = parser.parse_args()

    response = ''

    if not args.in_file:
        raise ValueError('Expected infile argument')
    else:
        # Possible refactor: create a wrapper for main() so session will be created and closed implicitly
        session = session_factory()

        BirdEvents(args.in_file, session).read_file()
        response += vehicle_drop_count(session)
        response += farthest_from_drop_location(session)
        response += longest_vehicle_distance(session)
        response += highest_cost_user(session)

        session.close()
        print(response)

def vehicle_drop_count(session):
    count = Vehicle.vehicles_count(session)
    return f'\nNumber of Bird Vehicles Dropped in Simulation: {count}'

def farthest_from_drop_location(session):
    # Please note that distance measures are in meters and have decimals truncated for clarity
    vehicle_id, distance = Vehicle.max_distance_from_drop(session)
    return f'\nVehicle {vehicle_id} was the farthest from the initial drop location at {distance:.0f} meters'

def longest_vehicle_distance(session):
    # Please note that distance measures are in meters and have decimals truncated for clarity
    vehicle_id, distance = Vehicle.max_distance_traveled(session)
    return f'\nVehicle {vehicle_id} traveled the most distance today with {distance:.0f} meters'

def highest_cost_user(session):
    user_id, cost = User.max_cost_user(session)
    return f'\nUser {user_id} racked up the biggest bill of ${cost:.2f}'


if __name__ == '__main__':
    main()
