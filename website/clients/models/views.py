"""
This is a module that define views routes for the users to access...
"""

from flask import Blueprint, render_template, flash, request, redirect, url_for, make_response, current_app, session, jsonify, abort
from website.mailer.mail import mail
from flask_mail import Message
from website.clients.models.utils import send_alert_email, list_pending_testimonials, get_testimonial_info, get_all_publish_testimonial
from website.clients.models.models import Testimonals
from website import db
from werkzeug.utils import secure_filename
import os
import base64


# Define the BluePrint
views = Blueprint(
    "views",
    __name__,
    static_folder="website/clients/static",
    template_folder="website/clients/templates",
)


# Define the home route
@views.route("/")
def home():
    """This is a function that return the home page"""
    navRoute = "home"

    # Get all Publish Testimonials

    publish_testimonials = get_all_publish_testimonial()

    return render_template("index.html", navRoute=navRoute, publish_testimonials=publish_testimonials)


@views.route("/service-page")
def service_page():
    """ This is a route that display the service page """

    key = request.args.get("key")  # Get key from URL query parameter
    navRoute = "service"

    services = {
            "service1": [
                {
                    "title": "Software Development",
                    "heading": "Building End-to-End Digital Solutions",
                    "description": (
                        "I offer complete software development services, covering everything from planning to deployment. "
                        "Whether it's a dynamic web app, a business automation system, or a digital product, I craft tailored "
                        "solutions that solve real-world problems. My approach is focused on user experience, performance, and "
                        "long-term scalability."
                    ),
                    "highlights": [
                        "Full-cycle development — from concept to launch",
                        "Scalable, maintainable codebases",
                        "Solutions tailored to your business goals"
                    ],
                }
            ],
            "service2": [
                {
                    "title": "Frontend Design",
                    "heading": "Crafting User-Centric Interfaces",
                    "description": (
                        "I design and build intuitive, accessible, and responsive interfaces that offer seamless user experiences. "
                        "Every layout and interaction is carefully crafted to reflect brand identity and meet user needs."
                    ),
                    "highlights": [
                        "Responsive layouts for all devices",
                        "Clean, accessible UI patterns",
                        "Focus on UX and design consistency"
                    ],
                }
            ],
            "service3": [
                {
                    "title": "Authentication Systems",
                    "heading": "Securing Access and Identity",
                    "description": (
                        "I implement secure and reliable authentication systems to ensure users can safely log in and access their "
                        "personalized dashboards and data."
                    ),
                    "highlights": [
                        "User login and registration flows",
                        "Role-based access control",
                        "Secure session management"
                    ],
                }
            ],
            "service4": [
                {
                    "title": "Dashboard & Admin Panels",
                    "heading": "Managing Data and Insights",
                    "description": (
                        "I develop custom dashboards and admin panels that give users and administrators control, visibility, and "
                        "insights into their systems or business logic."
                    ),
                    "highlights": [
                        "Dynamic data presentation",
                        "Custom widgets and charts",
                        "Admin controls and permissions"
                    ],
                }
            ],
            "service5": [
                {
                    "title": "Payment Integration",
                    "heading": "Connecting Secure Payment Gateways",
                    "description": (
                        "I integrate seamless and secure payment solutions that help you monetize your platform or enable easy "
                        "transactions without disrupting the user experience."
                    ),
                    "highlights": [
                        "Real-time transaction tracking",
                        "Multiple payment methods",
                        "Secure and reliable API communication"
                    ],
                }
            ],
            "service6": [
                {
                    "title": "Mentorship & Training",
                    "heading": "Empowering Others Through Knowledge",
                    "description": (
                        "I guide and train developers and teams through code reviews, workshops, and hands-on mentorship, helping them "
                        "level up their skills and best practices in real-world scenarios."
                    ),
                    "highlights": [
                        "1-on-1 and group mentorship",
                        "Project-based learning",
                        "Code reviews and feedback"
                    ],
                }
            ],
            
    }

    if not key or key not in services:
        return abort(404)

    service_data = services[key][0]
    return render_template("service-details.html", navRoute=navRoute, service=service_data)

@views.route("/share-your-experenice", methods=["GET"])
def share_your_experenice():
    """ This is a function that allows the employee to write about me work """

    navRoute = "submit_testimonial_form"

    return render_template("testimony_form_fill.html", navRoute=navRoute)


@views.route("/process_testimonials_requests", methods=["GET"])
def view_all_testimonal_request():
    """ This is a function that list all this testimonals """

    navRoute = "list_testimonals"

    pending_testimonials = list_pending_testimonials()

    return render_template("testimonials.html", navRoute=navRoute, pending_testimonials=pending_testimonials)


@views.route("/testimonial-details/<bind_id>", methods=["GET", "POST"])
def testimonial_details(bind_id):
    """ This is a function that handle the update and display of the testimonial details """

    navRoute = "view_testimonals"

    testimonial_details = get_testimonial_info(bind_id)

    if request.method == "POST":

        status = request.form.get("status")

        if not status:
            flash("Error: Mising inputs", "danger")
            return redirect(url_for('views.testimonial_details', bind_id=bind_id))

        testimonial_details.status = status
        db.session.commit()

        flash("Update Successfully", "success")
        return redirect(url_for('views.view_all_testimonal_request'))

    return render_template("testimonials.html", navRoute=navRoute, testimonial_details=testimonial_details, bind_id=bind_id)


###################### HELPERS  FUNCTIONS ##########################
@views.route("/send-mail", methods=["POST"])
def send_contact_mail():
    """ This is a function that process the contact us functionalities """

    name = request.form.get("name")
    email = request.form.get("email")
    subject = request.form.get("subject")
    message = request.form.get("message")
    action = "View new job alert"

    if not all([name, email, subject, message]):
        return jsonify({"error": "All fields are required."}), 400

    try:
        send_alert_email(subject, name, message, message, email)

        return jsonify({"success": "Message sent successfully."}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": f"Failed to send message: {str(e)}"}), 500


@views.route("/submit-testimonial-form", methods=["POST"])
def submit_testimonial_form():
    """ This is a function that process the submittion of the testimonial form """

    from website.celery.tasks import upload_file_to_firebase_task

    try:
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        role = request.form.get("role")
        profile_photo = request.files.get("profile_pic")

        if not all([name, email, message, role, profile_photo]):
            return jsonify({"error": "All fields are required."}), 400

        add_testimonial = Testimonals(
                name=name,
                email=email,
                role=role,
                message=message
        )

        db.session.add(add_testimonial)
        db.session.commit()

        bind_id = add_testimonial.bind_id

        # Upload profile picture using Celery
        face_image_filename = secure_filename(f"{bind_id}.png")
        face_image_dir = "Victor_Chukwuemeka_Tesitmonal/faces/"
        face_image_path = os.path.join(face_image_dir, face_image_filename)
        image_bytes = profile_photo.read()

        upload_file_to_firebase_task.delay(
                file_data=base64.b64encode(image_bytes).decode('utf-8'),
                file_key="photo_url",
                content_type="image/png",
                file_path=face_image_path,
                task_role="testimonals",
                task_key=bind_id
        )

        return jsonify({"success": "Message sent successfully."}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": f"Failed to send message: {str(e)}"}), 500
