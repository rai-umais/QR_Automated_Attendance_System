from routes.main import main_bp
from routes.auth import init_oauth,auth_bp
from routes.student import student_bp
from routes.teacher import teacher_bp
from routes.session import session_bp


# Now we need to register the blueprint that we created in main, and plug it in our system.

def register_routes(app):
    init_oauth(app)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(session_bp)
    