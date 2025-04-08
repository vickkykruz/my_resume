"""
This is a module that define views routes for the users to access...
"""

from flask import Blueprint, render_template, flash, request, redirect, url_for, make_response, current_app, session, jsonify

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

    return render_template("index.html")