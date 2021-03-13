from sqlalchemy import Table, Column, Integer, Boolean, ForeignKey

from persistence.models import Base

UserTracking = Table('user_tracking',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('province_id', Integer, ForeignKey('province.id'), primary_key=True),
    Column('district_id', Integer, ForeignKey('district.id'), primary_key=True),
    Column('municipality_id', Integer, ForeignKey('municipality.id'), primary_key=True),

    Column('notification', Boolean)
)

