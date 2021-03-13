from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from persistence.models.user import User
from persistence.models.user_tracking import UserTracking
from persistence.models.community import Community
from persistence.models.province import Province
from persistence.models.district import District
from persistence.models.municipality import Municipality
from persistence.models.measures import Measures