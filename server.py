import pydantic

from flask import Flask, jsonify
from flask import request
from flask.views import MethodView
from flask_bcrypt import Bcrypt 
from sqlalchemy.exc import IntegrityError


from models import User, Advertisement, Session
from schema import CreateUser, UpdateUser, CreateAdvertisement, UpdateAdvertisement

app = Flask("flask_hw")
bcrypt =  Bcrypt(app)

def hash_password(password: str):
    password = password.encode()
    return bcrypt.generate_password_hash(password).decode()

def check_password(password: str, hashed_password: str):
    password = password.encode()
    hashed_password = hashed_password.encode()
    return bcrypt.check_password_hash(password, hashed_password)


def validate(schema_class, json_data):
    try:
        return schema_class(**json_data).dict(exclude_unset=True)
    except pydantic.ValidationError as er:
        error = er.errors()[0]
        error.pop("ctx", None)
        raise HttpError(400, error)

class HttpError(Exception):
    def __init__(self, status_code: int, description: str):
        self.status_code = status_code
        self.description = description

@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({"error": error.description})
    response.status_code = error.status_code
    return response

@app.before_request
def before_request():
    session = Session()
    request.session = session

@app.after_request
def after_request(response):
    request.session.close()
    return response

def get_obj_by_id(Obj_class, obj_id: int):
    obj = request.session.get(Obj_class, obj_id)
    if obj is None:
        raise HttpError(status_code=404, description="not found")
    return obj

def add_obj(obj):
    try:
        request.session.add(obj)
        request.session.commit()
    except IntegrityError as err:
        raise HttpError(status_code=409, description="already exists")
    return obj

def delete_obj_by_id(Obj_class, obj_id: int):
    obj = get_obj_by_id(Obj_class, obj_id)
    request.session.delete(obj)
    request.session.commit()
    return obj

def patch_add_obj(obj, json_data):
    for field, value in json_data.items():
        setattr(obj, field, value)
    add_obj(obj)
    return obj
    

class UserView(MethodView):
    def get(self, user_id: int = None):
        if user_id is None:
            users = request.session.query(User).all()
            return jsonify([user.json for user in users])        
        user = get_obj_by_id(User, user_id)
        return jsonify(user.json)
    
    def post(self):
        json_data = validate(CreateUser, request.json)
        json_data["password"] = hash_password(json_data["password"])
        user = User(**json_data)
        add_obj(user)
        response = jsonify(user.json)
        response.status_code = 201
        return response
    
    def patch(self, user_id: int):
        json_data = validate(UpdateUser, request.json)
        if "password" in json_data:
            json_data["password"] = hash_password(json_data["password"])
        user = get_obj_by_id(User, user_id)
        patch_add_obj(user, json_data)
        return jsonify(user.json)

    def delete(self, user_id: int):
        delete_obj_by_id(User, user_id)
        return jsonify({'status': 'ok'})
    
class AdvertisementView(MethodView):
    def get(self, advertisement_id: int):
        advertisement = get_obj_by_id(Advertisement, advertisement_id)
        return jsonify(advertisement.json)
    
    def post(self):
        json_data = validate(CreateAdvertisement, request.json)
        advertisement = Advertisement(**json_data)
        add_obj(advertisement)
        response = jsonify(advertisement.json)
        response.status_code = 201
        return response
    
    def patch(self, advertisement_id: int):
        json_data = validate(UpdateAdvertisement, request.json)
        advertisement = get_obj_by_id(Advertisement, advertisement_id)
        patch_add_obj(advertisement, json_data)
        return jsonify(advertisement.json)

    def delete(self, advertisement_id: int):
        delete_obj_by_id(Advertisement, advertisement_id)
        return jsonify({'status': 'ok'})

user_view = UserView.as_view("user_view")
app.add_url_rule("/user", view_func=user_view, methods=["POST", "GET"])
app.add_url_rule("/user/<int:user_id>", view_func=user_view, methods=["GET", "PATCH", "DELETE"])
advertisement_view = AdvertisementView.as_view("advertisement_view")
app.add_url_rule("/advertisement", view_func=advertisement_view, methods=["POST"])
app.add_url_rule("/advertisement/<int:advertisement_id>", view_func=advertisement_view, methods=["GET", "PATCH", "DELETE"])

app.run()