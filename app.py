from flask import Flask,jsonify,render_template
from configure import configure
from models.base import db
from models import Teacher,Student,Session,Course,TempAttendance,Attendance
from routes import register_routes
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(configure)

    db.init_app(app)

    with app.app_context():
        db.create_all()
        print("All tables were created sucessfully.")
    
    register_routes(app)

    @app.after_request
    def add_ngrok_header(response):
        response.headers['ngrok-skip-browser-warning'] = 'true'
        return response
    return app

app = create_app()


if __name__ == '__main__':
    #port = int(os.environ.get('PORT',5000))
    app.run(debug=True, host='0.0.0.0', port=5000)