from orm import Student, Teacher, session, Course

teacher = session.query(Teacher).filter_by(id=1).first()

print(teacher.student)

student = session.query(Student).filter_by(id=8).first()


print(student.teacher)
session.commit()
