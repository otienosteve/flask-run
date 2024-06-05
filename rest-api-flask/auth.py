from datetime import datetime
from datetime import timezone
from datetime import timedelta
from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from models import User, db, TokenBlocklist
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token,create_refresh_token, current_user, jwt_required,JWTManager, get_jwt,get_jwt_identity
auth_bp = Blueprint('auth_bp',__name__)
api = Api(auth_bp)
jwt = JWTManager()

user_payload = reqparse.RequestParser()

user_payload.add_argument('email', help='Add Email', required=True)
user_payload.add_argument('password', help='Add Password', required=True)
user_payload.add_argument('role', help='Add Role', required=True)

login_parser = reqparse.RequestParser()
login_parser.add_argument('email',help='Add Email', required=True)
login_parser.add_argument('password',help='Add Password', required=True)

# Callback function to check if a JWT exists in the database blocklist
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()

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
        addidtional_claims = {"email":user.email, "role":user.role}
        token = create_access_token(identity=user.id, additional_claims=addidtional_claims)
        refresh_token = create_refresh_token(identity=user.id)

        return {"token": token, "refresh":refresh_token}
    
    @jwt_required()
    def get(self):
        print(current_user)

        return current_user.email
    

class UserLogout(Resource):

    @jwt_required()
    def get(self):
        token = get_jwt()
        jti =token.get('jti')
        now = datetime.now(timezone.utc)
        db.session.add(TokenBlocklist(jti=jti, created_at=now))
        db.session.commit()
        return 'logging out user'

class RefreshToken(Resource):
    
    @jwt_required(refresh=True)
    def get(self):
        identity = get_jwt_identity()
        token = create_access_token(identity=identity)
        return {"token":token}


api.add_resource(UserRegister,'/register')
api.add_resource(UserLogin,'/login')
api.add_resource(UserLogout,'/logout')
api.add_resource(RefreshToken, '/refresh')
