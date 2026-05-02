import os
from flask import Blueprint, redirect, url_for, session, request, jsonify
from models.base import db
from models.teacher import Teacher
from models.student import Student
from authlib.integrations.flask_client import OAuth


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
oauth = OAuth()

def init_oauth(app):
    oauth.init_app(app)
    oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'} 
        # -> these are the things that i need from the OAuth service, i.e the openid, the email and profile.
    )

@auth_bp.route('/login/teacher')
def teacher_login():
    session['oauth_role'] = 'Teacher'  # store role in session first
    redirect_uri = url_for('auth.callback', _external=True)  # clean URI, no role param
    print("EXACT REDIRECT URI:", redirect_uri)

    return oauth.google.authorize_redirect(redirect_uri)

@auth_bp.route('/login/student')
def student_login():
    session['oauth_role'] = 'Student'  # store role in session first
    # preserve the QR token so we can redirect back after OAuth
    qr_token = request.args.get('token')
    if qr_token:
        session['qr_token'] = qr_token
    redirect_uri = url_for('auth.callback', _external=True)  # clean URI, no role param
    return oauth.google.authorize_redirect(redirect_uri)


#callback is the route where google send the verfication details
#  after the request to sign in

@auth_bp.route('/callback')
def callback():
    token = oauth.google.authorize_access_token()
    user_info = token.get('userinfo')
    print("\n" + "="*50)
    print("GOOGLE RETURNED EMAIL:", user_info['email'])
    print("="*50 + "\n")
    if not user_info:
        return jsonify({'error': 'OAuth tokenization failed'}), 400

    Email = user_info['email']
    sub = user_info['sub']
    name = user_info.get('name', '-')
    role = session.pop('oauth_role', None)  # read role from session, then remove it

    if role == 'Teacher':
        user = Teacher.query.filter_by(email=Email).first()
        if not user:
            return jsonify({'error': 'You were not registered as a Teacher'}), 403
        if not user.google_sub:
            user.google_sub = sub
            db.session.commit()
        session['user_id']   = user.id
        session['user_role'] = 'Teacher'
        session['user_name'] = user.name
        return redirect(url_for('teacher.dashboard'))

    elif role == 'Student':
        user = Student.query.filter_by(email=Email).first()
        if not user:
            return jsonify({'error': 'You are not a registered student'}), 403
        if not user.google_sub:
            user.google_sub = sub
            db.session.commit()
        session['user_id']   = user.id
        session['user_role'] = 'Student'
        session['user_name'] = user.name
        # restore the QR token that was saved before OAuth redirect
        qr_token = session.pop('qr_token', None)
        if qr_token:
            return redirect(url_for('student.scan_page', token=qr_token))
        return redirect(url_for('student.scan_page'))
    
    return jsonify({'error': 'Invalid role'}), 400
    
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))