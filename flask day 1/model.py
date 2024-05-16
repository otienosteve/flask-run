from flask_sqlalchemy import SQLAlchemy 


db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String())


    def __repr__(self) -> str:
        return f'<Student: {self.first_name}>'

