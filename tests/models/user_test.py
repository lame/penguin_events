from app.models.user import User
from ..common.common_test import BaseUnitTest


class UserTest(BaseUnitTest):

    def test_user(self):
        user = self.session.query(User).filter_by(id=1).first()
        self.assertTrue(user.id, 1)

    def test_cost(self):
        self.assertEqual(User.max_cost_user(self.session), (1, 1.45))
