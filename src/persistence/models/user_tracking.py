from sqlalchemy import Table, Column, Integer, Boolean, ForeignKey

from persistence.models import Base

class UserTracking(Base):
    __tablename__ = 'user_tracking'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    place_id = Column(Integer, ForeignKey('place.id'), primary_key=True)

    notification = Column(Boolean)


