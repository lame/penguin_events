import enum


class EventType(enum.Enum):
    DROP = 0
    START_RIDE = 1
    END_RIDE = 2


def find_or_initialize_by(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance

def session_add_and_commit(session, itr):
    for instance in itr:
        session.add(instance)
    session.commit()
