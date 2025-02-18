from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from extensions import mail  
from datetime import datetime
from models.models import db, Course, RegisteredStudent

course_routes = Blueprint('course_routes', __name__)

@course_routes.route('/create-course', methods=['GET', 'POST'])
def create_course():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        short_description = request.form['short_description']
        startdate = datetime.strptime(request.form['startdate'], '%Y-%m-%d')
        price = request.form['price']
        location = request.form['location']
        image_url = request.form.get('image_url', None)

        new_course = Course(
            name=name,
            description=description,
            short_description=short_description,
            startdate=startdate,
            price=price,
            location=location,
            image_url=image_url
        )
        db.session.add(new_course)
        db.session.commit()

        return redirect(url_for('course_routes.course_detail', courseid=new_course.courseid))

    return render_template('create_course/create_course.html')

@course_routes.route('/course/<int:courseid>', methods=['GET'])
def course_detail(courseid):
    course = Course.query.get(courseid)
    if course:
        return render_template('course_details/index.html', course=course)
    else:
        return "Course not found", 404
    
@course_routes.route('/register/<int:courseid>', methods=['GET', 'POST'])
def register(courseid):
    course = Course.query.get(courseid)

    if course:
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            kennitala = request.form.get('kennitala')
            gender = request.form.get('gender')
            differentpayer = request.form.get('differentpayer') == 'on'  
            payerkennitala = request.form.get('payerkennitala') if differentpayer else None
            payername = request.form.get('payername') if differentpayer else None
            payerphone = request.form.get('payerphone') if differentpayer else None
            payment_method=request.form.get('paymentMethod')

            if not name or not email or not kennitala:
                flash('Please fill in all required fields.', 'error')
                return redirect(url_for('course_routes.register', courseid=courseid))

            new_registration = RegisteredStudent(
                courseid=courseid,
                name=name,
                email=email,
                phone=phone,
                kennitala=kennitala,
                gender=gender,
                differentpayer=differentpayer,
                payerkennitala=payerkennitala,
                payername=payername,
                payerphone=payerphone,
                payment_method=payment_method
            )
            
            db.session.add(new_registration)
            db.session.commit()

            msg = Message("Takk fyrir að skrá þig á námskeiðið okkar!",
                          recipients=[email])  
            msg.body = f"""
                    Takk fyrir að skrá þig á námskeiðið {course.name}

                    Við munum á næstu dögum senda þér greiðsluseðil fyrir námskeiðinu.

                    Einnig er hægt að millifæra á okkur og spara þannig seðilgjald:

                    kt. 681288-1399  
                    banki 0302  
                    höfuðbók 26  
                    reikningur 27080  

                    Upphæð: {course.price} 

                    Hlökkum til að sjá þig.

                    Starfsfólk Tölvufræðslunnar  
                    www.tf.s  
                    tf@tf.is  
                    462-7899
                    """
            try:
                mail.send(msg)
            except Exception as e:
                flash(f"Error sending email: {e}", 'error')

            company_email = "tf@tf.is"  
            company_msg = Message("New Course Registration",
                                  recipients=[company_email])  
            company_msg.body = f"A new student has registered for the course: {course.name} \n price: {course.price}.\n\nName: {name}\nKennitala: {kennitala}\nEmail: {email}\nPhone: {phone}\nPayment Method: {payment_method}"
            try:
                mail.send(company_msg)
            except Exception as e:
                flash(f"Error sending email to company: {e}", 'error')

            flash('Skráning tókst!', 'success')
            return redirect(url_for('course_routes.index'))

        return render_template('sign_up_form/index.html', course=course)

    return "Course not found", 404


@course_routes.route('/')
def index():
    courses = Course.query.all() 
    return render_template('course_list/index.html', courses=courses)

@course_routes.route('/edit-course/<int:courseid>', methods=['GET', 'POST'])
def edit_course(courseid):
    course = Course.query.get_or_404(courseid)

    if request.method == 'POST':
        course.name = request.form['name']
        course.short_description = request.form['short_description']
        course.description = request.form['description']
        course.price = request.form['price']
        course.image_url = request.form.get('image_url', course.image_url)

        db.session.commit()
        flash('Course updated successfully!', 'success')
        return redirect(url_for('course_routes.course_detail', courseid=courseid))

    return render_template('course_edit/index.html', course=course)
