import uuid
from datetime import datetime,UTC
from models.base import db


class Teacher(db.Model):
    __tablename__ = 'Teachers'

    id = db.Column(db.String(36), primary_key = True, default = lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable = False)
    email  = db.Column(db.String(100) , nullable = False , unique = True)
    google_sub = db.Column(db.String(120), unique = True, nullable = True)  # google sub => google subject; it is a token like value that is given to each google account when a user sign in to the  system using the "Sign in with Google" option. Unique for each account and can be null for those who sign in using email and password.
    created_at = db.Column(db.DateTime , default = datetime.now(UTC))

    courses = db.relationship('Courses', backref = 'teacher', lazy = True)     #  backref='teacher' -> teacher is not the table name here, it is a python object that is created itself, here it is created on the 'Course' object that point backs to the teacher.
    sessions = db.relationship('Session', backref = 'teacher' , lazy = True)        #lazy means that when to load all the dt=ata; when said to do so or when the code runs!

    def __repr__(self):
        return f'<Teacher  {self.email}>'