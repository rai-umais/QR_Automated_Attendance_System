from app import app
from models.base import db
from models import Teacher, Student, Course

with app.app_context():
    t2 = Teacher.query.filter_by(name='Dr.VORTX',email='muazzamm024@gmail.com').first()
    if not t2:
        t2 = Teacher(name='Dr.VORTX', email='muazzamm024@gmail.com')
        db.session.add(t2)
        db.session.commit()
        
    c3 = Course.query.filter_by(code='SE-2001', name='Software Requirement Engineering').first()
    if not c3:
        c3 = Course(code='SE-2001', name='Software Requirement Engineering', teacher_id=t2.id)
        db.session.add(c3)
        db.session.commit()

    students = [
        Student(roll_number='l243063', name='Muhammad Muazzam Mahmood',    email='l243063@lhr.nu.edu.pk'),
        Student(roll_number='l240001', name='Muhammad Anas',    email='l240001@lhr.nu.edu.pk'),
        Student(roll_number='l243095', name='Arqam Hafeez',    email='l243095@lhr.nu.edu.pk'),
        Student(roll_number='l227998', name='Laiba Nadeem',    email='l227998@lhr.nu.edu.pk'),
        Student(roll_number='l243029', name='Abdul Ahad Shams', email='l243029@lhr.nu.edu.pk'),
        Student(roll_number='l243059', name='Abdul Rehman', email='l243059@lhr.nu.edu.pk'),
        Student(roll_number='l243058', name='Adnan Ali Khan', email='l243058@lhr.nu.edu.pk'),
        Student(roll_number='l243024', name='Aliza Nadeem', email='l243024@lhr.nu.edu.pk'),
        Student(roll_number='l243033', name='Aliza Vahidy',    email='l243033@lhr.nu.edu.pk'),
        Student(roll_number='l243017', name='Aqsa Ehtesham',    email='l243017@lhr.nu.edu.pk'),
        Student(roll_number='l243075', name='Fatima Asif',    email='l243075@lhr.nu.edu.pk'),
        Student(roll_number='l243086', name='Hamza Abbas',    email='l243086@lhr.nu.edu.pk'),
        Student(roll_number='l243065', name='Hania Zahra',    email='l243065@lhr.nu.edu.pk'),
        Student(roll_number='l243022', name='Hassan Butt',    email='l243022@lhr.nu.edu.pk'),
        Student(roll_number='l240707', name='Iman Abid',    email='l240707@lhr.nu.edu.pk'),
        Student(roll_number='l243088', name='Kabeer Ahmad Shahzeb',    email='l243088@lhr.nu.edu.pk'),
        Student(roll_number='l243084', name='Kainat Afzal',    email='l243084@lhr.nu.edu.pk'),
        Student(roll_number='l243082', name='Minahil Basalat',    email='l243082@lhr.nu.edu.pk'),
        Student(roll_number='l243071', name='Muhammad Abdullah',    email='l243071@lhr.nu.edu.pk'),
        Student(roll_number='l243002', name='Muhammad Abdullah Rasheed',    email='l243002@lhr.nu.edu.pk'),
        Student(roll_number='l243004', name='Muhammad Anas',    email='l243004@lhr.nu.edu.pk'),
        Student(roll_number='l243076', name='Muhammad Ayub Butt',    email='l243076@lhr.nu.edu.pk'),
        Student(roll_number='l243047', name='Muhammad Babar Shehzad',    email='l243047@lhr.nu.edu.pk'),
        Student(roll_number='l243006', name='Muhammad Haider Mughal',    email='l243006@lhr.nu.edu.pk'),
        Student(roll_number='l243073', name='Muhammad Hassan Ashraf',    email='l243073@lhr.nu.edu.pk'),
        Student(roll_number='l243019', name='Muhammad Huzaifa',    email='l243019@lhr.nu.edu.pk'),
        Student(roll_number='l243023', name='Muhammad Shehryar Waheed',    email='l243023@lhr.nu.edu.pk'),
        Student(roll_number='l243001', name='Romesha Afzaal',    email='l243001@lhr.nu.edu.pk'),
        Student(roll_number='l242549', name='Syed Saad Ali',    email='l242549@lhr.nu.edu.pk'),
        Student(roll_number='l243055', name='Sharjeel Shahid',    email='l243055@lhr.nu.edu.pk'),
        Student(roll_number='l243038', name='Zunaira Tahir',    email='l243038@lhr.nu.edu.pk'),
        Student(roll_number='l243032', name='Rai Muhammad Umais Kharal',  email='l243032@lhr.nu.edu.pk'),
        Student(roll_number='l243007', name='Muhammad Husnain Khan',   email='l243007@lhr.nu.edu.pk'),
    ]
    for s in students:
        existing = Student.query.filter_by(roll_number=s.roll_number).first()
        if not existing:
            db.session.add(s)
            c3.students.append(s)
        else:
            if existing not in c3.students:
                c3.students.append(existing)

    db.session.commit()
    print("Seed data inserted.")