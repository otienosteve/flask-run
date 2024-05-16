from sqlalchemy import Column, Integer, String, Date, create_engine, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# many to many -> association table, 
# Association Object 
student_teacher = Table(
    'student_teacher', Base.metadata,
    Column('student_id',ForeignKey('student.id')),
    Column('teacher_id',ForeignKey('teacher.id'))
)




class Student(Base):
    __tablename__ ='student'

    id = Column(Integer, primary_key=True)
    firstname = Column(String(30))
    lastname = Column(String(30))
    dob = Column(String)
    grade = Column(String(2))
    course = relationship('Course', back_populates='student') # one to many 
    teacher = relationship('Teacher', back_populates='student',secondary=student_teacher)
    biodata = relationship('BioData',backref='student', uselist=False ) # one to one
    
    def __repr__(self):
        return f'<Student: {self.firstname}>'



class Teacher(Base):
    __tablename__ ='teacher'

    id = Column(Integer, primary_key=True)
    firstname = Column(String(30))
    lastname = Column(String(30))
    student = relationship('Student', back_populates='teacher',secondary=student_teacher)

    def __repr__(self):
        return f'<Teacher: {self.firstname}>'



class BioData(Base):
    __tablename__ ='biodata'
    id = Column(Integer, primary_key=True)
    homewtown = Column(String(30))
    guardianContact = Column(String(30))
    student_id = Column(Integer, ForeignKey('student.id'))
     
    def __repr__(self):
        return f'<BioData: {self.homewtown}>'
    

class Course(Base):
    __tablename__ = 'course'
    id= Column(Integer, primary_key=True)
    name = Column(String(30))
    student_id = Column(Integer, ForeignKey('student.id'))
    student = relationship('Student', back_populates='course')

import datetime


# if __name__ == '__main__':
engine = create_engine('sqlite:///students.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
# student1 = Student(id=3,firstname='Steve',lastname='Otieno', dob=datetime.date(year=2002, day=1, month=4), grade='B+')
# student = Student(id=4,firstname='Michael',lastname='Limisi', dob=datetime.date(year=2002, day=1, month=4), grade='B+')
session = Session()
# use 'Session' class to create 'session' object
# session.add(student)
# student = session.query(Student).filter_by(id=2).first()
# course = Course(name='CS')
# course.student=student
# session.add(course)
# biodata = BioData(homewtown='kisumu',guardianContact='0781398340')
# biodata.student = student1
# session.add_all([student1, student, biodata])
