from flask_sqlalchemy import SQLAlchemy 


db = SQLAlchemy()

student_course = db.Table('student_course', db.Model.metadata,
    db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'))
)

class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String())
    courses  = db.relationship('Course', secondary=student_course, back_populates='students')
    biodata = db.relationship('BioData', back_populates = 'student', uselist=False)

    def __repr__(self) -> str:
        return f'<Student: {self.first_name}>'
    
class BioData(db.Model):
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


