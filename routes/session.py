from flask import Blueprint, request, jsonify, session
from datetime import datetime, UTC
from models.base import db
from models.attendance import TempAttendance, Attendance
from models.course import Course
from models.session import Session
from services.session_manager import get_active_session
from routes.decorators import teacher_required

session_bp = Blueprint('session', __name__, url_prefix='/session')

@session_bp.route('/finalize', methods=['POST'])
@teacher_required
def finalize():
    course_id = request.json.get('course_id')

    if not course_id:
        return jsonify({'error': 'course_id is required'}), 400

    # get active session
    active = get_active_session(course_id)
    if not active:
        return jsonify({'error': 'No active session found'}), 404

    try:
        # get all enrolled students
        course = db.session.get(Course, course_id)
        if not course:
            return jsonify({'error': 'Course not found'}), 404

        enrolled_students = course.students
        temp_records      = TempAttendance.query.filter_by(
                                session_id=active.id).all()
        present_ids       = {r.student_id for r in temp_records}

        # write permanent attendance for every enrolled student
        for student in enrolled_students:
            status = 'P' if student.id in present_ids else 'A'
            record = Attendance(
                session_id   = active.id,
                student_id   = student.id,
                date         = active.date,
                status       = status,
                finalized_at = datetime.now(UTC)
            )
            db.session.add(record)

        # delete temp records
        TempAttendance.query.filter_by(session_id=active.id).delete()

        # close the ongoing session
        active.status       = 'closed'
        active.finalized_at = datetime.now(UTC)

        # single commit for everything
        db.session.commit()

        return jsonify({
            'message': f'Attendance finalized. '
                       f'{len(present_ids)} present, '
                       f'{len(enrolled_students) - len(present_ids)} absent.'
        })

    except Exception as e:
        db.session.rollback()
        print(f"Finalize error: {e}")
        return jsonify({'error': f'Finalization failed: {str(e)}'}), 500