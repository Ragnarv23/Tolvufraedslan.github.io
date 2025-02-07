from flask import Flask, render_template
from flask_migrate import Migrate
from models.models import db, Course
import os
from routes.course_routes import course_routes 

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Ragnar:1234@34.147.250.192:5432/classes_and_registration'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ue5928nnlbv4sh:p2165940681a26f666f22ead415e129d7c7ee09054c86767ac9b37e64bd832f77@c7u1tn6bvvsodf.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com:5432/d1l6ff90kdtfug'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

#DATABASE_URL = os.getenv('DATABASE_URL', 'postgres://fallback_url_if_needed')
#app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL.replace("postgres://", "postgresql://", 1)



db.init_app(app)
migrate = Migrate(app, db)

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

