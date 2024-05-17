from model import Student, db,Course

from app import app 

with app.app_context():
    courses = [{
  "name": "Computer Science",
  "id": 6
}, {
  "name": "Electrical Engineering",
  "id": 7
}, {
  "name": "Mechanical Engineering",
  "id": 8
}, {
  "name": "Biology",
  "id": 9
}, {
  "name": "Chemistry",
  "id": 10
}, {
  "name": "Physics",
  "id": 11
}, {
  "name": "Mathematics",
  "id": 12
}]

    new_courses = [Course(**course) for course in courses]
    db.session.add_all(new_courses)
    db.session.commit()

