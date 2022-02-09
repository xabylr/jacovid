from sqlalchemy import Column, Date, DateTime, ForeignKeyConstraint, Integer, Numeric, String, UniqueConstraint, func

from persistence.database import Base


class Measures(Base):
    __tablename__ = 'measures'

    id = Column(Integer, primary_key=True, autoincrement=True)
    place_code = Column(String)
    place_type = Column(String(length=1))

    # Register time from database
    date_reg = Column(Date(), server_default=func.now())
    dt_reg = Column(DateTime(), server_default=func.now())
    dt_mod = Column(DateTime(), onupdate=func.now())

    population = Column(Numeric)
    pdia_confirmed = Column(Numeric)
    pdia_14d_confirmed = Column(Numeric)
    pdia_14d_rate = Column(Numeric)
    pdia_7d_confirmed = Column(Numeric)
    total_confirmed = Column(Numeric)
    cured = Column(Numeric)
    deceased = Column(Numeric)

    __table_args__ = (
        UniqueConstraint('place_code', 'place_type', 'date_reg'),
        ForeignKeyConstraint(('place_code', 'place_type'), ('place.code', 'place.type'))
    )


class MeasuresCodeComparator:
    def __init__(self, measures):
        self.measures = measures

    def __eq__(self, other):
        return (self.measures.place_code == other.measures.place_code and
                self.measures.place_type == other.measures.place_type)

    def __hash__(self):
        return hash(self.measures.place_code) + hash(self.measures.place_type)
