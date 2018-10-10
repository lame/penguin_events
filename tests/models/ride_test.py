from app.models.ride import Ride
from app.models.location import Location
from ..common.common_test import BaseUnitTest


class RideTest(BaseUnitTest):

    def test_user(self):
        ride = self.session.query(Ride).all()[0]
        self.assertTrue(ride.user.id, 1)

    def test_distance(self):
        ride = self.session.query(Ride).all()[0]
        distance = ride.distance()
        self.assertEqual(distance, 15572131.792956578)

    def test_duration(self):
        ride = self.session.query(Ride).all()[0]
        duration = ride.duration
        self.assertEqual(duration, 121)

    def test_is_free_ride(self):
        ride = self.session.query(Ride).all()[0]
        self.assertFalse(ride.is_free_ride)

    def test_ride_minutes(self):
        ride = self.session.query(Ride).all()[0]
        self.assertEqual(ride.ride_minutes, 3)

    def test_cost(self):
        ride = self.session.query(Ride).all()[0]
        self.assertEqual(ride.cost, 1.45)

    def test_start_location(self):
        test_start_location = Location(33, -87)
        ride = self.session.query(Ride).all()[0]
        self.assertEqual(ride.start_location.lat, test_start_location.lat)
        self.assertEqual(ride.start_location.long, test_start_location.long)

    def test_end_location(self):
        test_end_location = Location(7, 91)
        ride = self.session.query(Ride).all()[0]
        self.assertEqual(ride.end_location.lat, test_end_location.lat)
        self.assertEqual(ride.end_location.long, test_end_location.long)
