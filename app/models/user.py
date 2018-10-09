from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from .. import Base


class User(Base):
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

