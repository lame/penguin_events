import unittest

from app import session_factory
from app.resources.penguin_events import PenguinEvents

class BaseUnitTest(unittest.TestCase):

    def setUp(self):
        self.session = session_factory()
        PenguinEvents('tests/fixtures/test_events.csv', self.session).read_file()

    def tearDown(self):
        self.session.close()
