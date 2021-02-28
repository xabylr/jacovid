from sqlalchemy import Column, Integer

from models import Base


class Moto(Base):
    __tablename__ = 'motos'

    id = Column(Integer, primary_key=True)
    # marca = Column(String)
    # modelo = Column(String)
