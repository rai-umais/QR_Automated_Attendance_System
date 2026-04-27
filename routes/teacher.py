from flask import Blueprint, render_template, session, request, jsonify
from models.base import db
from models.course import Course
from models.attendance import TempAttendance
from services.session_manager import start_session, get_active_session
from services.qr_generator import generate_qr_token, generate_qr_image
from routes.decorators import teacher_required

teacher_bp = Blueprint('teacher', __name__, url_prefix='/teacher')

@teacher_bp.route('/dashboard')
@teacher_required
def dashboard():
    courses = Course.query.filter_by(teacher_id=session['user_id']).all()
    return render_template('dashboard.html',
                           name=session.get('user_name'),
                           courses=courses)

@teacher_bp.route('/start-session', methods=['POST'])
@teacher_required
def start_attendance_session():
    course_id = request.json.get('course_id')
    if not course_id:
        return jsonify({'error': 'course_id is required'}), 400
    active = start_session(course_id, session['user_id'])
    return jsonify({
        'session_id': active.id,
        'status': active.status,
        'message': 'Session started'
    })

@teacher_bp.route('/get-qr')
@teacher_required
def get_qr():
    course_id = request.args.get('course_id')
    if not course_id:
        return jsonify({'error': 'course_id required'}), 400
    active = get_active_session(course_id)
    if not active:
        return jsonify({'error': 'No active session'}), 404
    token = generate_qr_token(active.id)
    img_base64 = generate_qr_image(token)  # ← no base_url argument anymore
    return jsonify({'qr_image': img_base64, 'session_id': active.id})

@teacher_bp.route('/live-students')
@teacher_required
def live_students():
    course_id = request.args.get('course_id')
    active = get_active_session(course_id)
    if not active:
        return jsonify({'students': []})
    records = TempAttendance.query.filter_by(session_id=active.id).all()
    students = [{
        'id': r.id,
        'student_id': r.student_id,
        'name': r.student.name,
        'roll_number': r.student.roll_number,
        'scanned_at': r.scanned_at.strftime('%H:%M:%S')
    } for r in records]
    return jsonify({'students': students})

@teacher_bp.route('/remove-student', methods=['POST'])
@teacher_required
def remove_student():
    record_id = request.json.get('record_id')
    record = TempAttendance.query.get(record_id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Student removed'})