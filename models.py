from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
import sqlalchemy as sa
from acl import init_acl

# สร้าง instance ของ SQLAlchemy
bcrypt = Bcrypt()


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def init_app(app):
    db.init_app(app)
    bcrypt.init_app(app)
    init_acl(app)
    with app.app_context():
        db.create_all()
        db.reflect()


# โมเดล Role
class Role(db.Model):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False, default="user")
    created_date = mapped_column(sa.DateTime(timezone=True), server_default=func.now())


# โมเดล User
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String)
    status = db.Column(db.String, default="active")
    _password_hash = db.Column(db.String)
    created_date = mapped_column(sa.DateTime(timezone=True), server_default=func.now())
    updated_date = mapped_column(sa.DateTime(timezone=True), server_default=func.now())

    roles: Mapped[list[Role]] = relationship("Role", secondary="user_roles")
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
    profile = db.relationship("Profile", backref="user", uselist=False)
    reviews = db.relationship("Review", backref="user", lazy=True)
    places = db.relationship("Place", backref="user", lazy=True)
    ratings = db.relationship(
        "Rating", backref="user", lazy=True
    )  # เพิ่มความสัมพันธ์กับ Rating

    # Password hash management
    @hybrid_property
    def password_hash(self):
        raise Exception("Password hashes may not be viewed.")

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode("utf-8"))
        self._password_hash = password_hash.decode("utf-8")

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode("utf-8"))

    def has_role(self, role_name):
        return any(role.name == role_name for role in self.roles)


# ตารางกลางสำหรับการเชื่อมโยงผู้ใช้และบทบาท
user_roles = db.Table(
    "user_roles",
    db.Model.metadata,
    sa.Column("user_id", sa.ForeignKey("users.id"), primary_key=True),
    sa.Column("role_id", sa.ForeignKey("roles.id"), primary_key=True),
)


class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String)
    data = db.Column(db.LargeBinary)
    created_date = mapped_column(sa.DateTime(timezone=True), server_default=func.now())
    updated_date = mapped_column(sa.DateTime(timezone=True), server_default=func.now())


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String)
    data = db.Column(db.LargeBinary)


class PlaceImage(db.Model):
    __tablename__ = "place_images"
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String)
    data = db.Column(db.LargeBinary)
    place_id = db.Column(db.Integer, db.ForeignKey("places.id"))


class Rating(db.Model):
    __tablename__ = "ratings"
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    place_id = db.Column(db.Integer, db.ForeignKey("places.id"))
    created_date = db.Column(db.DateTime, default=func.now())


class Place(db.Model):
    __tablename__ = "places"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    created_date = db.Column(db.DateTime, default=func.now())
    updated_date = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
    reviews = db.relationship("Review", backref="place", lazy=True)
    images = db.relationship("PlaceImage", backref="place", lazy=True)
    ratings = db.relationship("Rating", backref="place", lazy=True)
    average_rating = db.Column(db.Float, default=0.0)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def update_average_rating(self):
        if self.ratings:
            total_rating = sum(rating.rating for rating in self.ratings)
            self.average_rating = total_rating / len(self.ratings)
        else:
            self.average_rating = 0.0
        db.session.commit()


class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    place_id = db.Column(
        db.Integer, db.ForeignKey("places.id")
    )  # Foreign key ไปยัง places
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))  # Foreign key ไปยัง users
    created_date = db.Column(db.DateTime, default=func.now())
