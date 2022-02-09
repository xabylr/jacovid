from persistence.database import Session
from persistence.models.measures import Measures
from persistence.models.place import Place


def is_database_empty():
    session = Session()

    is_empty = session.query(Place).first() is None

    session.close()

    return is_empty


def retrieve_measures_from_date(date, session=None):
    if session is None:
        session = Session()

    return session.query(Measures).filter_by(date_reg=date).all()
