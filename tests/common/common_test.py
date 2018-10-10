import unittest

from app import session_factory
from app.resources.bird_events import BirdEvents

class BaseUnitTest(unittest.TestCase):

    def setUp(self):
        self.session = session_factory()
        BirdEvents('tests/fixtures/test_events.csv', self.session).read_file()

    def tearDown(self):
        self.session.close()
