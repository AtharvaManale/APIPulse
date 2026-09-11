from sqlalchemy.orm import Session
from app.models.apis_model import API

class ApiRepository:

    def get_api_by_id(db: Session, api_id: str):
        return (db.query(API).filter(API.id == api_id).first())

    def get_api_of_user(db:Session, user_id: str):
        return [db.query(API).filter(API.user_id == user_id).all()]

    def get_api_by_url(db: Session, api_url: str):
        return (db.query(API).filter(API.url == api_url).first())

    def get_api_by_url_url_method(db: Session, url: str, url_method: str):
        return (db.query(API).filter(API.url == url, API.url_method == url_method).first())

    def register_endpoint(db: Session, request: API):
        db.add(request)