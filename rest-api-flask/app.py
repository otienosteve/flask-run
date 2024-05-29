from flask import Flask, request, redirect, url_for
from flask_migrate import Migrate 
from models import db, Student
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
import json
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///school.db'
db.init_app(app)
migrate = Migrate(app, db)
cors = CORS(app, resources={r"*": {"origins": "*"}})

api = Api(app)
def former():

# @app.route('/')
# def home():

#     return {"msg":"Welcome to Flask"}


# @app.route('/students', methods=['POST','GET'])
# def students():
#     if request.method =='POST':
#         new_student = Student(**request.json)
#         db.session.add(new_student)
#         db.session.commit()
#         return request.json
    
#     students = Student.query.all()
#     students_array = []
#     for student in students:
#         # convert student to JSON
#         student_json = {"id":student.id,
#                         "first_name":student.first_name,
#                         "last_name":student.last_name,
#                         "email":student.email,
#                         "user_id":student.user_id}
#         # append to students_array
#         students_array.append(student_json)

#     return students_array

    
# @app.route('/students/<int:id>', methods=['GET','PATCH','DELETE'])
# def student_by_id(id):

#     student = Student.query.filter_by(id=id).first()
#     if not student:
#         return {'msg': f'Student with id {id} not found on the server'}
    
#     if request.method == 'DELETE':
#         db.session.delete(student)
#         db.session.commit()
#         return {'msg':f'student with {id=} has been deleted successfully'}
    
#     if request.method == 'PATCH':
#         for key, value in request.json.items():
#             setattr(student,key,value)
        
#         db.session.add(student)
#         db.session.commit()
#         return redirect(url_for('student_by_id', id=id))
    
#     student_json ={"id":student.id,
#                         "first_name":student.first_name,
#                         "last_name":student.last_name,
#                         "email":student.email,
#                         "user_id":student.user_id}
#     return student_json


# flask restful
    pass

post_payload = reqparse.RequestParser()
post_payload.add_argument('first_name',type=str, help='add First Name', required=True)
post_payload.add_argument('last_name',type=str, help='add Last Name ', required=True)
post_payload.add_argument('email',type=str, help='add Email', required=True)
post_payload.add_argument('user_id',type=int, help='add user id ', required=True)

patch_payload = reqparse.RequestParser()
patch_payload.add_argument('first_name',type=str, help='add First Name')
patch_payload.add_argument('last_name',type=str, help='add Last Name ')
patch_payload.add_argument('email',type=str, help='add Email')
patch_payload.add_argument('user_id',type=int, help='add user id ')



class Students(Resource):
    
    def get(self):
        students = Student.query.all()
        students_json = [student.to_dict() for student in students]
        return students_json
    
    def post(self):
        data = post_payload.parse_args()
        new_student = Student(**data)
        db.session.add(new_student)
        db.session.commit()
        return data
    

class StudentByID(Resource):

    def get(self, id):
        student = Student.query.filter_by(id=id).first()
        return student.to_dict()
    
    def patch(self,id):
        student = Student.query.filter_by(id=id).first()
        data = patch_payload.parse_args()
        for key,value in data.items():
            if value is not None:
                setattr(student,key,value)
        db.session.add(student)
        db.session.commit()
        return student.to_dict()

    def delete(self,id):
        student = Student.query.filter_by(id=id).first()
        db.session.delete(student)
        db.session.commit()
        return f'Student with id {id=} has been deleted successfully'


api.add_resource(Students,'/students')
api.add_resource(StudentByID,'/students/<int:id>')




