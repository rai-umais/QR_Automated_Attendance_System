import uuid
from models.base import db

course_students = db.Table('course_students',
    db.Column('course_id',  db.String(50), db.ForeignKey('courses.id'),  primary_key=True),
    db.Column('student_id', db.String(50), db.ForeignKey('students.id'), primary_key=True)
)

class Course(db.Model):
    __tablename__ = 'courses'

    id         = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    code       = db.Column(db.String(50), nullable=False)
    name       = db.Column(db.String(150), nullable=False)
    teacher_id = db.Column(db.String(50), db.ForeignKey('teachers.id'), nullable=False)

    students = db.relationship('Student', secondary=course_students, backref='courses', lazy=True)
    sessions = db.relationship('Session', backref='course', lazy=True)

    def __repr__(self):
        return f'<Course {self.code}>'