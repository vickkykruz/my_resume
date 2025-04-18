import eventlet

eventlet.monkey_patch()

import secrets
import os
from flask import Flask, render_template, send_from_directory, current_app
from jinja2 import FileSystemLoader
from website.database.database import db
from website.mailer.mail import mail
from website.clients.models.views import views
#from website.clients.models.users import shuffle_list
#from website.clients.models.auth import auth
#from website.admin.models.auth import adminAuth
#from website.admin.models.views import adminViews
import firebase_admin
from firebase_admin import credentials, firestore, storage
from os import path, environ
from datetime import timedelta
from flask_mail import Mail
from werkzeug.security import generate_password_hash
#from website.admin.models.models import Admin
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
import pyrebase
import requests


# Load environment variables once at startup
load_dotenv()

# Connect to database
DB_NAME = 'vickkyprogramming.db'
EVENT_FACE_RECONGITION_FIREBASE_CREDENTIALS = environ.get('EVENT_FACE_RECONGITION_FIREBASE_KEY_PATH')
TELEMEDICAL_FIREBASE_CREDENTIALS = environ.get('TELEMEDICAL_FIREBASE_KEY_PATH')
IPINFO_API_TOKEN = environ.get('IPINFO_API_TOKEN')

if not firebase_admin._apps:
    event_face_recognition_cred = credentials.Certificate(EVENT_FACE_RECONGITION_FIREBASE_CREDENTIALS)
    telemedical_cred = credentials.Certificate(TELEMEDICAL_FIREBASE_CREDENTIALS)

    event_app = firebase_admin.initialize_app(event_face_recognition_cred, name="event-face")
    telemedical_app = firebase_admin.initialize_app(telemedical_cred, {
        'storageBucket': 'telemedical-710dc.appspot.com'
    }, name="telemedical")


# Here to store the uploaded images
UPLOAD_FOLDER = "website/static/uploads"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def create_app():
    """ This is a function that issues the name of the app """
    app = Flask(__name__) # This represent the name of the file

    # Configure logging
    if not app.debug:
        file_handler = RotatingFileHandler('flask.log', maxBytes=10240, backupCount=1)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)

    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    # This is going to encrpt or secure D cookie
    app.config['SECRET_KEY'] = environ.get('SECRET_KEY', 'fallback_secret_key')
    # Set session timeout to 1 hour (for example)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
    app.config['SESSION_COOKIE_SECURE'] = True  # Ensures cookies are only sent over HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True  # Helps mitigate cross-site scripting (XSS)
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    # Firebase Pyrebase Config (Replace with your actual Firebase project details)
    firebase_config = {
            'apiKey': environ.get('FIREBASE_APIKEY'),
            'authDomain': environ.get('FIREBASE_AUTHDOMAIN'),
            'projectId': environ.get('FIREBASE_PROJECTID'),
            'storageBucket': environ.get('FIREBASE_STOREAGEBUCKET'),
            'messagingSenderId': environ.get('FIRBASE_MESSAGEINGSENDERID'),
            'appId': environ.get('FIREBASE_APPID'),
            'measurementId': environ.get('FIREBASE_MEASUREMENTID'),
            'databaseURL': environ.get('FIREBASE_DATABASEURL')
    }

    # Store firebase_config in app.config
    app.config['FIREBASE_CONFIG'] = firebase_config

    # Define template folders for clients and admin
    client_template_folder = path.join(app.root_path, 'clients', 'templates')
#    admin_template_folder = path.join(app.root_path, 'admin', 'templates')

    # Configure Jinja2 environment with multiple template folders
#    loader = FileSystemLoader([client_template_folder, admin_template_folder])
    loader = FileSystemLoader([client_template_folder])
    app.jinja_loader = loader  # Set the Jinja loader directly to the Flask app

    # Connect to our database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, DB_NAME)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    firebase = pyrebase.initialize_app(firebase_config)
    app.firebase_auth = firebase.auth()

    # Configure Flask-Mail
    app.config['MAIL_SERVER'] = 'mail.sacoeteccscdept.com.ng'  # Your email server (e.g., smtp.gmail.com)
    app.config['MAIL_PORT'] = 465  # Port for your email server (e.g., 587 for Gmail)
    app.config['MAIL_USE_SSL'] = True 
    app.config['MAIL_USE_TLS'] = False  # Enable TLS encryption
    app.config['MAIL_USERNAME'] = 'noreply@sacoeteccscdept.com.ng'  # Your email address
    app.config['MAIL_PASSWORD'] = 'Vicchi232312@'  # Your email password
    app.config['DEBUG'] = True

    db.init_app(app)
    mail.init_app(app)

    # Register the blueprint
    app.register_blueprint(views, url_prefix='/')
#    app.register_blueprint(auth, url_prefix='/auth')
#   app.register_blueprint(adminAuth, url_prefix='/admin')
#    app.register_blueprint(adminViews, url_prefix='/admin/page')

    # Custom error handler for 404 Not Found
    @app.errorhandler(404)
    def page_not_found(error):
        """ This is a function that handle the 404 error handlers """
        return render_template('404.html')


    @app.errorhandler(500)
    def internal_server_error(error):
        """ This is a function that handler the 500 error handlers """
        return render_template('500.html')


    @app.errorhandler(405)
    def method_not_found(error):
        """ This is a function that handler the 405 error handlers """
        return render_template('405.html')


    # Import the schemer of our database
    from website.clients.models.models import Testimonals
#    from website.admin.models.models import Admin
    create_database(app)

#    if create_database(app):
#        with app.app_context():

#           create_default_admin()

    # Return the app
    return app

def create_database(app):
    """This is a function that create the database"""

    # check if the path of our database doesn't exist then create it
    if not path.exists("website/" + DB_NAME):
        with app.app_context():
            db.create_all()
        print("Created Database")

# Explicitly expose event_app and telemedical_app for imports
__all__ = ["event_app", "telemedical_app"]
