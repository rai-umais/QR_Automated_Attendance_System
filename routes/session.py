from flask import Blueprint, request, jsonify, session
from datetime import datetime, UTC
from models.base import db
from models.attendance import TempAttendance, Attendance
from models.course import Course
from services.session_manager import get_active_session, close_session
from routes.decorators import teacher_required

session_bp = Blueprint('session', __name__, url_prefix='/session')

@session_bp.route('/finalize', methods=['POST'])
@teacher_required
def finalize():
    course_id = request.json.get('course_id')
    active = get_active_session(course_id)
    if not active:
        return jsonify({'error': 'No active session found'}), 404

    course = Course.query.get(course_id)
    enrolled_students = course.students
    temp_records = TempAttendance.query.filter_by(session_id=active.id).all()
    present_ids = {r.student_id for r in temp_records}

    for student in enrolled_students:
        status = 'P' if student.id in present_ids else 'A'
        record = Attendance(
            session_id=active.id,
            student_id=student.id,
            date=active.date,
            status=status,
            finalized_at=datetime.now(UTC)
        )
        db.session.add(record)

    TempAttendance.query.filter_by(session_id=active.id).delete()
    close_session(active.id)
    db.session.commit()
    return jsonify({'message': 'Attendance finalized successfully'})