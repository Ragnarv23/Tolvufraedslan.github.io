from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Course(db.Model):
    __tablename__ = 'courses'
    
    courseid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    short_description = db.Column(db.String(255), nullable=True)  
    startdate = db.Column(db.Date, nullable=False)
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(255), nullable=True)
    visibility = db.Column(db.Boolean, default=True, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)  

    students = db.relationship('RegisteredStudent', backref='course', lazy=True)

    def __repr__(self):
        return f'<Course {self.name}>'

class RegisteredStudent(db.Model):
    __tablename__ = 'registeredstudent'
    
    studentid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(50), nullable=True)
    kennitala = db.Column(db.String(10), nullable=False)
    gender = db.Column(db.String(10), nullable=True)
    differentpayer = db.Column(db.Boolean, default=False)
    payerkennitala = db.Column(db.String(10), nullable=True)
    payername = db.Column(db.String(255), nullable=True)
    payerphone = db.Column(db.String(50), nullable=True)
    payment_method = db.Column(db.String(50), nullable=False)
    
    courseid = db.Column(db.Integer, db.ForeignKey('courses.courseid'), nullable=False)
    
    def __repr__(self):
        return f'<RegisteredStudent {self.name}>'
