"""
This is a module that define views routes for the users to access...
"""

from flask import Blueprint, render_template, flash, request, redirect, url_for, make_response, current_app, session, jsonify, abort
from website.mailer.mail import mail
from flask_mail import Message
from website.clients.models.utils import send_alert_email

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

    return render_template("index.html", navRoute=navRoute)


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

    pass
