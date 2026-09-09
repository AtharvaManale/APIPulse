from sqlalchemy.orm import session
from app.models.users_model import Users

class UsersRepository():

    def get_user_by_id(db: session, id: str):
        return (db.query(Users).filter(Users.id == id).first())

    