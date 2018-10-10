from app.models.location import Location
from ..common.common_test import BaseUnitTest


class RideTest(BaseUnitTest):

    def test_limit(self):
        start_location = Location(-100, 190)
        self.assertEqual(start_location.lat, -90)
        self.assertEqual(start_location.long, 180)

    def test_get_distance(self):
        start_location = Location(33, -87)
        end_location = Location(7,91)
        distance = Location.get_distance(start_location, end_location)
        self.assertEqual(distance, 15572131.792956578)
