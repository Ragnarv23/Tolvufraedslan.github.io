from flask import Flask, render_template
from models.models import db, Course
import os
from routes.course_routes import course_routes 

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Ragnar:1234@34.147.250.192:5432/classes_and_registration'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

db.init_app(app)

app.register_blueprint(course_routes)

@app.route('/')
def index():
    courses = Course.query.all()
    return render_template('course_list/index.html', courses=courses)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get('PORT', 5000)) 
    app.run(debug=True, host='0.0.0.0', port=port)

