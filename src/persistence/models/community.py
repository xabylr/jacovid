from sqlalchemy import Column, Integer, String

from persistence.models import Base


class Community(Base):
    __tablename__ = 'community'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String, unique=True)
    name = Column(String)
