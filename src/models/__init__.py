from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
session = None


def get_session():
    return session


def init_db(db_url):
    global session
    engine = create_engine(db_url)
    # Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
