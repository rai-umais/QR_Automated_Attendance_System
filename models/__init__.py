# load everything here so that we can use this directly

from models.base import db
from models.teacher import Teacher
from models.student import Student
from models.course import Course, course_students
from models.session import Session
from models.attendance import TempAttendance, Attendance