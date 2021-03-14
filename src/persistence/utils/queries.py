from persistence.models.measures import Measures
from persistence.models.place import Place


import persistence.database as database

def is_database_empty():
    session = database.get_session()

    is_empty = session.query(Place).first() == None

    session.close()

    return is_empty

def retrieve_measures_from_date(date, session=None):
    if session is None:
        session = database.get_session()
    
    return session.query(Measures).filter_by(date_reg = date).all()