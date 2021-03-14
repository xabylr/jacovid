from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from persistence.models.user import User
from persistence.models.user_tracking import UserTracking
from persistence.models.place import Place
from persistence.models.measures import Measures