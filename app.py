from flask import Flask,jsonify,render_template
from configure import configure
from models.base import db
from models import Teacher,Student,Session,Course,TempAttendance,Attendance
from routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(configure)

    db.init_app(app)

    with app.app_context():
        db.create_all()
        print("All tables were created sucessfully.")
    
    register_routes(app)
    return app

app = create_app()
if __name__ == '__main__':
    app.run(debug=True)