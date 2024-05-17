from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from model import db, Student, Course
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///school.db'
db.init_app(app)

migrate = Migrate(app, db)

@app.route('/')
def home():
    students = Student.query.all()
    courses = Course.query.all()
    return render_template('main.html', students=students, courses=courses)


@app.route('/student')
def view_student():
    students = Student.query.all()
    return render_template('view-student.html', students=students)

@app.route('/course')
def view_course():
    courses = Course.query.all()
    return render_template('view-course.html', courses=courses)


@app.route('/add_student', methods=['POST','GET'])
def  add_student():
    if request.method == 'POST':
        student = Student(first_name=request.form.get('first_name'), last_name =request.form.get('last_name'), email =request.form.get('email'))
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('view_student'))
    
    return render_template('add-student.html')

@app.route('/delete_student/<int:id>')
def delete_student(id):
    student = Student.query.filter_by(id=id).first()
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('view_student'))

@app.route('/update_student/<int:id>', methods=['POST','GET'])
def update_student(id):
    student = Student.query.filter_by(id=id).first()
    if request.method =='POST':
        for key,value in request.form.items():
            setattr(student,key, value)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('view_student'))
    return render_template('update-student.html',student=student)

@app.route('/student_details/<int:id>')
def student_details(id):
    student = Student.query.filter_by(id=id).first()
    return render_template('student-details.html',student=student)