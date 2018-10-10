from app.models.vehicle import Vehicle
from ..common.common_test import BaseUnitTest


class UserTest(BaseUnitTest):

    def test_distance_from_drop(self):
        vehicle = self.session.query(Vehicle).filter_by(id='VEHICLE1').first()
        self.assertEqual(vehicle.distance_from_drop, 15572131.792956578)

    def test_max_distance_from_drop(self):
        vehicle_id, distance = Vehicle.max_distance_from_drop(self.session)
        self.assertEqual(vehicle_id, 'VEHICLE1')
        self.assertEqual(distance, 15572131.792956578)

    def test_max_distance_traveled(self):
        vehicle_id, distance = Vehicle.max_distance_traveled(self.session)
        self.assertEqual(vehicle_id, 'VEHICLE1')
        self.assertEqual(distance, 46716395.378869735)

    def test_vehicles_count(self):
        self.assertEqual(Vehicle.vehicles_count(self.session), 1)
