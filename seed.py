from app import app
from models.base import db
from models import Teacher, Student, Course

with app.app_context():
    t1 = Teacher(name='Dr. Umais', email='raiumaiskharal@gmail.com')
    t2 = Teacher(name='Dr. Rai', email='gokboruhan2@gmail.com')

    db.session.add(t1)
    db.session.add(t2)

    db.session.flush()

    c = Course(code='CS-301', name='Data Structures', teacher_id=t1.id)
    db.session.add(c)
    db.session.flush()

    students = [
        Student(roll_number='2022-CS-004', name='Umais',    email='l243032@lhr.nu.edu.pk'),
        Student(roll_number='2022-CS-005', name='Muazzam',   email='l243063@lhr.nu.edu.pk'),
        Student(roll_number='2022-CS-006', name='Husnain', email='l243007@lhr.nu.edu.pk'),
    ]
    for s in students:
        db.session.add(s)
        c.students.append(s)

    db.session.commit()
    print("Seed data inserted.")