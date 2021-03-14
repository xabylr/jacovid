from persistence.models import Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config.environment as env

engine = None
Session = None


def get_session():
    # Create a new session using the constructor
    return Session(bind=engine)


def connect(db_url, debug=False):
    global engine

    # Create the engine
    conn_args = {}
    # if debug:
    #     conn_args["sslmode"] = "disable"
    execution_options = {
    "schema_translate_map": {None: env.PG_SCHEMA} }

    engine = create_engine(db_url, echo=debug, connect_args=conn_args,
         execution_options=execution_options)

    # Database schema generation for missing tables
    Base.metadata.create_all(engine)
