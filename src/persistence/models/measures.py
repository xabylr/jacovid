from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, ForeignKey, UniqueConstraint, func

from persistence.models import Base

class Measures(Base):
    __tablename__ = 'measures'

    id = Column(Integer, primary_key=True, autoincrement=True)
    community_code = Column(String, ForeignKey('community.code'))
    province_code = Column(String, ForeignKey('province.code'))
    district_code = Column(String, ForeignKey('district.code'))
    municipality_code = Column(String, ForeignKey('municipality.code'))

    # Register time from database
    date_reg = Column(Date(), server_default=func.now())
    dt_reg = Column(DateTime(), server_default=func.now())
    dt_mod = Column(DateTime(timezone=False), onupdate=func.now())

    pdia_14d_rate = Column(Numeric)

    __table_args__ = (
        UniqueConstraint('community_code', 'date_reg'),
        UniqueConstraint('province_code', 'date_reg'),
        UniqueConstraint('district_code', 'date_reg'),
        UniqueConstraint('municipality_code', 'date_reg')
        )

class MeasuresCodeComparator:
    def __init__(self, measures):
        self.measures = measures
    def __eq__(self, other):
        return (
            self.measures.community_code == other.measures.community_code and
            self.measures.province_code == other.measures.province_code and
            self.measures.district_code == other.measures.district_code and
            self.measures.municipality_code == other.measures.municipality_code)

    def __hash__(self):
        return (hash(self.measures.community_code)
            +hash(self.measures.province_code)
            +hash(self.measures.district_code)
            +hash(self.measures.municipality_code))