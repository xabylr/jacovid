from sqlalchemy import Column, ForeignKeyConstraint, UniqueConstraint, Integer, String

from persistence.models import Base


class Place(Base):
    __tablename__ = 'place'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String)
    """
        C -> Community
        P -> Province
        D -> District
        Z -> ZBS
        M -> Municipality
    """
    type = Column(String(length=1))
    
    parent = Column(String)
    parent_type = Column(String(length=1))


    __table_args__ = (
        UniqueConstraint('code', 'type'),
        #ForeignKeyConstraint(['parent', 'parent_type'], ['place.code', 'place.type'])
    )


    name = Column(String)
