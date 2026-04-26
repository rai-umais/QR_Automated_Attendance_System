from functools import wraps
from flask import session, redirect, url_for, jsonify

def teacher_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.teacher_login'))
        if session.get('user_role') != 'Teacher':
            return jsonify({'error': 'Teachers only'}), 403
        return f(*args, **kwargs)
    return decorated

def student_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.student_login'))
        if session.get('user_role') != 'Student':
            return jsonify({'error': 'Students only'}), 403
        return f(*args, **kwargs)
    return decorated

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.teacher_login'))
        return f(*args, **kwargs)
    return decorated