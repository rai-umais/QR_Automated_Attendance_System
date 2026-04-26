import uuid
from models.base import db

# Association table between Course and Student

# One student has many courses and
# One course has many students
# so we can not ad them in single table,

course_student = db.Table('Course_Student',
                          db.Column('course_id',db.String(50) ,db.ForeignKey('courses.id'), primary_key = True),
                        db.Column('student_id', db.String(50), db.ForeignKey('students.id') , primary_key = True))


class Course(db.Model):
    __tablename__ = 'Courses'

    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    code = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    teacher_id = db.Column(db.String(36), db.ForeignKey('teachers.id'), nullable = False)

    # to get a student record, go and check the course_student table; this is what secondary tells
    students   = db.relationship('Student', secondary=course_student, backref='courses', lazy=True)
    sessions   = db.relationship('Session', backref='course', lazy=True)

    def __repr__(self):
        return f'<Course {self.code}>'