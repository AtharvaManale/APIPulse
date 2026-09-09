from sqlalchemy.orm import Session
from app.models.users_model import Users
import email

class UsersRepository():

    def add_user(db:Session, user: Users):
        db.add(user)

    def get_user_by_id(db: Session, id: str):
        return (db.query(Users).filter(Users.id == id).first())

    def get_user_by_username(db: Session, username: str):
        return (db.query(Users).filter(Users.username == username).first())

    def get_user_by_email(db: Session, email_id: email):
            return (db.query(Users).filter(Users.email_id == email_id).first())