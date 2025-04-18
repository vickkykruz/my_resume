import uuid
from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

class Testimonals(db.Model, UserMixin):
    """This is a class that contains the information of the testimonls."""

    __tablename__ = 'testimonals'

    id = db.Column(db.Integer, primary_key=True)
    bind_id = db.Column(
        db.String(36),
        unique=True,
        default=lambda: str(uuid.uuid4())
    )
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(100))
    message = db.Column(db.Text)
    photo_url = db.Column(db.String(150))
    status = db.Column(db.Enum("Publish", "Unpublish", name="status_enum"), default="Unpublish", nullable=True)
    create_date = db.Column(db.DateTime(timezone=True), default=func.now())
    update_date = db.Column(db.DateTime(timezone=True), onupdate=func.now())
