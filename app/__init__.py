from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


"""
Create an in-memory SQLite3 database
Used in this case because the code 
is in a non-production version and
other software cannot be installed.

Otherwise we could switch the engine to
read a PostgreSQL URI from a config file
"""

engine = create_engine('sqlite:///:memory:', echo=True)
_SessionFactory = sessionmaker(bind=engine)
Base = declarative_base()

def session_factory():
    Base.metadata.create_all(engine)
    return _SessionFactory()
