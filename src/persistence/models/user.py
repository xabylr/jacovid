from sqlalchemy import Column, Integer

from persistence.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)  # Telegram user id
