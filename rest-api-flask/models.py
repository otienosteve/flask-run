from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
    }
)

db = SQLAlchemy(metadata=metadata)

student_course = db.Table('student_course', db.Model.metadata,
    db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'))
)

class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)

class User(db.Model,SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String())
    password = db.Column(db.String())
    role = db.Column(db.String())
    student= db.relationship('Student', back_populates = 'user', uselist=False)

class Student(db.Model,SerializerMixin):
    serialize_rules =('-biodata.student','-id')
    __tablename__ = 'student'
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String())
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    courses  = db.relationship('Course', secondary=student_course, back_populates='students')
    biodata = db.relationship('BioData', back_populates = 'student', uselist=False)
    user = db.relationship('User', back_populates = 'student', uselist=False)
    
    def __repr__(self) -> str:
        return f'<Student: {self.first_name}>'
    
class BioData(db.Model,SerializerMixin):
    serialize_rules =('-biodata.student',)
    __tablename__ = 'biodata'
    id = db.Column(db.Integer(), primary_key=True)
    hometown = db.Column(db.String())
    contact = db.Column(db.String())
    student_id = db.Column(db.Integer(), db.ForeignKey('student.id'))
    student = db.relationship('Student', back_populates = 'biodata', uselist=False)



class Course(db.Model):
    __tablename__ ='course'
    id =  db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    students  = db.relationship('Student', secondary=student_course, back_populates='courses')


