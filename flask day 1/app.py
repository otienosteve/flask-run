from flask import Flask
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import render_template
from flask_bcrypt import Bcrypt
from functools import wraps
from model import db, Student, Course,BioData, User
from flask_migrate import Migrate
from forms import BioDataForm, RegisterForm, LoginForm
from flask_login import LoginManager, login_user, current_user
app = Flask(__name__,static_folder='/static')
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///school.db'
app.config['SECRET_KEY'] ='You"ll never walk alone'
login_manager = LoginManager()
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager.init_app(app)
migrate = Migrate(app, db)

def allow(*role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if current_user.role == role[0]:
                return fn(*args,**kwargs)
            else:
                return render_template('forbidden.html')
        return decorator
    return wrapper



@app.route('/')
def home():
    students = Student.query.all()
    courses = Course.query.all()
    return render_template('main.html', students=students, courses=courses)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if request.method== 'POST':
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.data.get('password'))
            user = User(email= form.data.get('email'), password=hashed_password)
            db.session.add(user)
            db.session.commit()
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Error in field "{getattr(form, field).label.text}": {error}', 'error')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.data.get('email')).first()
            if not user:
                flash('User Does not exist on Our site')
                return render_template('login.html', form=form)
            if not bcrypt.check_password_hash(user.password, form.data.get('password')):
                return render_template('login.html', form=form)
            login_user(user)
            return redirect(url_for('student_details',id=user.student.id ))
    return render_template('login.html', form=form)


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
@allow('student')
def student_details(id):
    student = Student.query.filter_by(id=id).first()
    return render_template('student-details.html',student=student)

import re
@app.route('/update_bio_data/<int:id>', methods=['GET','POST'])
def update_bio_data(id):
    biodata = BioData.query.filter_by(id=id).first()
    form = BioDataForm()
    user = current_user
    if request.method == 'POST':
        if re.findall(r'\D',form.data.get('contact')):
            flash('Only digits are allowed for contact')
            return render_template('bio-data.html',biodata=biodata, form=form,user=user) 
        if form.validate_on_submit():
            for key,value in form.data.items():
                setattr(biodata, key,value)
            db.session.add(biodata)
            db.session.commit()
        return redirect(url_for('student_details',id=biodata.student_id))
            
    return render_template('bio-data.html',biodata=biodata, form=form,user=user)