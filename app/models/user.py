from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from .. import Base


class User(Base):
    """ The user class holds the user attributes (presumably name, an FK to addresses, FK to payment info, etc)
    and a list of all the user's rides. The last ride (self.rides[-1] is always either the current in-progress ride or
    the most recently completed ride.

    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    rides = relationship('Ride', backref='users')

    @classmethod
    def max_cost_user(cls, session):
        max_cost = (None, 0)
        users = session.query(cls).all()
        for user in users:
            cost_sum = sum([ride.cost for ride in user.rides])
            if cost_sum > max_cost[1]:
                max_cost = (user.id, cost_sum)

        return max_cost

