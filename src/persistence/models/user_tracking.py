from sqlalchemy import Boolean, Column, ForeignKey, Integer

from persistence.database import Base


class UserTracking(Base):
    __tablename__ = 'user_tracking'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    place_id = Column(Integer, ForeignKey('place.id'), primary_key=True)

    notification = Column(Boolean)
