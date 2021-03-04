from sqlalchemy import Column, Integer, Table, ForeignKey

from models import Base

MunicipalityTracking = Table('municipality_tracking',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('municipality_id', Integer, ForeignKey('municipality.id'), primary_key=True)
)

