from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import environment

engine = create_engine(environment.DATABASE_URL, echo=environment.DEBUG)
Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)

if __name__ == '__main__':
    Base.metadata.create_all(engine)  # Database schema generation for missing tables
