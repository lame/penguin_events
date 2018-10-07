from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from .. import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)

    # Relations
    events = relationship("Event", backref='users')


