from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
session = None

from models.user import User
from models.municipality import Municipality
from models.municipality_tracking import MunicipalityTracking


def get_session():
    return session

def _populate_database(): #TODO web scrapping
    session.add(Municipality(code= '29067', name= 'Málaga (capital)'))

    session.commit()

def init_db(db_url, debug=False):
    engine = create_engine(db_url, echo=debug)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    global session
    session = Session()
    result = session.query(Municipality).first()
    if result is None:
        _populate_database()