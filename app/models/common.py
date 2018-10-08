import enum


class EventType(enum.Enum):
    DROP = 0
    START_RIDE = 1
    END_RIDE = 2


class DBOperations(object):
    """ DBOperations is used for common database related tasks such as

    find_or_initialize_by:
        which will search the user provided model for a match with the
        requisite args, or create the object, and

    session_add_and_commit:
        A shortcut to add an interator of instances to the session and
        commit all of them. Saves a few lines of code here and there
    """

    @staticmethod
    def find_or_initialize_by(session, model, **kwargs):
        instance = session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            session.add(instance)
            session.commit()
            return instance

    @staticmethod
    def session_add_and_commit(session, itr):
        for instance in itr:
            session.add(instance)
        session.commit()
