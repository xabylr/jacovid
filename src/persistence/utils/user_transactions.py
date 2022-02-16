from typing import Tuple
from persistence.database import Session
from persistence.models import User, UserTracking, Place

def update_user_registration(user: User):
    with Session() as session:
        session.merge(user)
        session.commit()

def track_place(user_id, place_id):
    entity = UserTracking(user_id=user_id, place_id=place_id)
    with Session() as session:
        session.add(entity)
        session.commit()

# def user_places(user_id) -> Tuple[UserTracking, Place] :
#     with Session() as session:
#         return session.query(UserTracking).\
#             join(UserTracking.place_id)
    
def user_places(user_id) -> Tuple[Place, UserTracking] :
    with Session() as session:
        return session.query(Place, UserTracking).\
            join(UserTracking, Place.id == UserTracking.place_id).\
            filter(UserTracking.user_id == user_id)