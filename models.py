from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
import sqlalchemy as sa
from acl import init_acl

bcrypt = Bcrypt()


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def init_app(app):
    db.init_app(app)
    bcrypt.init_app(app)
    init_acl(app)
    with app.app_context():
        db.create_all()  # ✅ ลบ db.reflect() ออก


# ตารางกลางสำหรับ Many-to-Many ระหว่าง Note และ Tag
note_tag_m2m = db.Table(
    "note_tag",
    db.Column("note_id", db.ForeignKey("notes.id"), primary_key=True),
    db.Column("tag_id", db.ForeignKey("tags.id"), primary_key=True),
)


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
    updated_date = mapped_column(
        sa.DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    roles: Mapped[list[Role]] = relationship("Role", secondary="user_roles")

    @hybrid_property
    def password_hash(self):
        raise Exception("Password hashes may not be viewed.")

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(
            password.encode("utf-8")
        ).decode("utf-8")

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode("utf-8"))

    def has_role(self, role_name):
        return any(role.name == role_name for role in self.roles)


# โมเดล Tag
class Tag(db.Model):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False)
    created_date = mapped_column(sa.DateTime(timezone=True), server_default=func.now())


# โมเดล Note
class Note(db.Model):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(sa.String, nullable=False)
    description: Mapped[str] = mapped_column(sa.Text)
    tags: Mapped[list[Tag]] = relationship(secondary=note_tag_m2m)
    created_date = mapped_column(sa.DateTime(timezone=True), server_default=func.now())
    updated_date = mapped_column(
        sa.DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


# โมเดล UploadProfile (แก้ชื่อจาก Uploadproflie)
class UploadProfile(db.Model):
    __tablename__ = "uploadprofile"  # ✅ กำหนดชื่อ Table
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String, nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)
    created_date = mapped_column(sa.DateTime(timezone=True), server_default=func.now())
    updated_date = mapped_column(
        sa.DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


#  User and Role
user_roles = db.Table(
    "user_roles",
    db.Column("user_id", db.ForeignKey("users.id"), primary_key=True),
    db.Column("role_id", db.ForeignKey("roles.id"), primary_key=True),
)

# User and Profile
user_profile = db.Table(
    "user_profile",
    db.Column("user_id", db.ForeignKey("users.id"), primary_key=True),
    db.Column("profile_id", db.ForeignKey("uploadprofile.id"), primary_key=True),
)


# โมเดล Upload (อัปโหลดไฟล์)
class Upload(db.Model):
    __tablename__ = "uploads"
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String, nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)
    created_date = mapped_column(sa.DateTime(timezone=True), server_default=func.now())
    updated_date = mapped_column(
        sa.DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
