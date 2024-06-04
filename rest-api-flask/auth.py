from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
auth_bp = Blueprint('auth_bp',__name__)
api = Api(auth_bp)

user_payload = reqparse.RequestParser()

user_payload.add_argument('email', help='Add Email', required=True)
user_payload.add_argument('password', help='Add Password', required=True)
user_payload.add_argument('role', help='Add Role', required=True)

login_parser = reqparse.RequestParser()
login_parser.add_argument('email',help='Add Email', required=True)
login_parser.add_argument('password',help='Add Password', required=True)



class UserRegister(Resource):

    def post(self):
        data = user_payload.parse_args()
        hashed_password = generate_password_hash(data.password)
        user = User(email= data.email, password = hashed_password, role = data.get('role'))
        db.session.add(user)
        db.session.commit()
        return f"User {user.email} has been added succesfully"

 



class UserLogin(Resource):

    def post(self):
        data = login_parser.parse_args()
        user = User.query.filter_by(email=data.get('email')).first()
        if not user:
            return f'User with {data.email=} not found on server'
        if not check_password_hash(user.password, data.get('password')):
            return f"You have entered the wrong passord"
        
        token = create_access_token(identity=user.id)
        return token



api.add_resource(UserRegister,'/register')
api.add_resource(UserLogin,'/login')
