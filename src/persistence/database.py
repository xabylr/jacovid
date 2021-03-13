from persistence.models import Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = None
Session = None

def get_session():
    # Create a new session using the constructor
    return Session()


def connect(db_url, debug=False):
    global engine, Session

    # Create the engine
    conn_args = {}
    # if debug:
    #     conn_args["sslmode"] = "disable"

    engine = create_engine(db_url, echo=debug, connect_args=conn_args)

    # Database schema generation for missing tables
    Base.metadata.create_all(engine)

    # Create a session constructor
    Session = sessionmaker(bind=engine)
