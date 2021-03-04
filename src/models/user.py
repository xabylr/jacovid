from sqlalchemy import Column, Integer

from models import Base

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True) #Telegram user id
    # marca = Column(String)
    # modelo = Column(String)
