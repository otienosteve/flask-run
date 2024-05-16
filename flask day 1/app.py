from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from model import db, Student
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///school.db'
db.init_app(app)

migrate = Migrate(app, db)

@app.route('/')
def home():
    data = 'In Class'
    return render_template('index.html', data=data)


@app.route('/student')
def view_student():
    students = Student.query.all()
    return render_template('view-student.html', students=students)


@app.route('/add_student', methods=['POST','GET'])
def  add_student():
    if request.method == 'POST':
        student = Student(first_name=request.form.get('first_name'), last_name =request.form.get('last_name'), email =request.form.get('email'))
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('view_student'))
    
    return render_template('add-student.html')
