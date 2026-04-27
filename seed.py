from app import app
from models.base import db
from models import Teacher, Student, Course

with app.app_context():
    t2 = Teacher.query.filter_by(name='Dr. Rai',email='gokboruhan2@gmail.com').first()
    c2 = Course(code='MT-1004', name='Data Structures', teacher_id=t2.id)
    c3 = Course(code='SE-1301', name='Data Structures', teacher_id=t2.id)

    db.session.add(c2)
    db.session.add(c3)

    db.session.flush()

    students = [
        Student(roll_number='2022-CS-014', name='Rai',    email='gokboruhan2@gmail.com'),
        Student(roll_number='2022-CS-024', name='Muhammad',    email='l243012@lhr.nu.edu.pk'),
        Student(roll_number='2022-CS-034', name='Umais',    email='l243056@lhr.nu.edu.pk'),
    ]
    for s in students:
        db.session.add(s)
        c2.students.append(s)

    db.session.commit()
    print("Seed data inserted.")