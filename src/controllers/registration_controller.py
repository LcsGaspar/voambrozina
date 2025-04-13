from flask import Blueprint, render_template, request, redirect, url_for
from models.registration import Registration

registration = Blueprint('registration', __name__)

@registration.route('/submit_course_registration', methods=['POST'])
def submit_course_registration():
    try:
        Registration.create(request.form)
        return '', 204
    
    except Exception as e:
        print(f"Error: {e}")
        return '', 500
    