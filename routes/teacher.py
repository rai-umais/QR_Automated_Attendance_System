from flask import Blueprint, render_template, session, request, jsonify
from sqlalchemy import func
from models.base import db
from models.course import Course
from models.student import Student
from models.attendance import TempAttendance
from services.session_manager import start_session, get_active_session, get_teacher_active_session
from services.qr_generator import generate_qr_token, generate_qr_image
from services.xlsx_import import parse_students_from_xlsx
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
    mode = request.json.get('mode', 'normal')
    
    if not course_id:
        return jsonify({'error': 'course_id is required'}), 400

    # Block if teacher already has an open session (any course)
    existing = get_teacher_active_session(session['user_id'])
    if existing and str(existing.course_id) != str(course_id):
        return jsonify({
            'error': 'You already have an active session. '
                     'Please finalize it before starting a new one.'
        }), 409

    active = start_session(course_id, session['user_id'], mode=mode)
    return jsonify({
        'session_id': active.id,
        'status': active.status,
        'message': 'Session started'
    })

@teacher_bp.route('/check-active-session')
@teacher_required
def check_active_session():
    """Returns info about any currently open session for this teacher."""
    existing = get_teacher_active_session(session['user_id'])
    if existing:
        return jsonify({
            'active': True,
            'course_id': existing.course_id,
            'session_id': existing.id,
            'mode': existing.mode
        })
    return jsonify({'active': False})

@teacher_bp.route('/get-qr')
@teacher_required
def get_qr():
    course_id = request.args.get('course_id')
    if not course_id:
        return jsonify({'error': 'course_id required'}), 400
    active = get_active_session(course_id)
    if not active:
        return jsonify({'error': 'No active session'}), 404
    
    # Determine expiry time based on mode
    seconds = 50 if active.mode == 'normal' else 30
    
    token = generate_qr_token(active.id, seconds=seconds)
    img_base64 = generate_qr_image(token)
    return jsonify({
        'qr_image': img_base64, 
        'session_id': active.id,
        'seconds': seconds
    })

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


@teacher_bp.route('/import-students', methods=['POST'])
@teacher_required
def import_students():
    course_id = request.form.get('course_id')
    file = request.files.get('excel_file')

    if not course_id:
        return jsonify({'error': 'course_id is required'}), 400
    if not file:
        return jsonify({'error': 'Excel file is required'}), 400
    if not file.filename.lower().endswith('.xlsx'):
        return jsonify({'error': 'Only .xlsx files are supported'}), 400

    course = Course.query.filter_by(id=course_id, teacher_id=session['user_id']).first()
    if not course:
        return jsonify({'error': 'Course not found'}), 404

    try:
        parsed_students = parse_students_from_xlsx(file.read())
    except Exception as exc:
        return jsonify({'error': f'Failed to read Excel: {exc}'}), 400

    created = 0
    skipped_existing = 0
    enrolled_now = 0

    for parsed in parsed_students:
        normalized_roll = parsed.roll_number.replace('-', '')
        existing = Student.query.filter(
            func.replace(Student.roll_number, '-', '') == normalized_roll,
            func.lower(Student.name) == parsed.name.lower()
        ).first()

        if existing:
            student = existing
            skipped_existing += 1
        else:
            student = Student(
                roll_number=parsed.roll_number,
                name=parsed.name,
                email=parsed.email
            )
            db.session.add(student)
            created += 1

        if student not in course.students:
            course.students.append(student)
            enrolled_now += 1

    db.session.commit()

    return jsonify({
        'message': 'Excel import completed.',
        'rows_read': len(parsed_students),
        'created': created,
        'skipped_existing': skipped_existing,
        'enrolled_in_course': enrolled_now
    })