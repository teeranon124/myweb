from wtforms_sqlalchemy.orm import model_form
from flask_wtf import FlaskForm
from wtforms import Field, widgets, validators, fields
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    TextAreaField,
    FloatField,
    SubmitField,
    MultipleFileField,
)
from wtforms.validators import DataRequired, NumberRange
import models


# ฟอร์มการลงทะเบียนและเข้าสู่ระบบ
BaseUserForm = model_form(
    models.User,
    base_class=FlaskForm,
    exclude=["created_date", "updated_date", "status", "_password_hash"],
    db_session=models.db.session,
)


class LoginForm(FlaskForm):
    username = fields.StringField("Username", [validators.DataRequired()])
    password = fields.PasswordField("Password", [validators.DataRequired()])


class RegisterForm(BaseUserForm):
    username = fields.StringField(
        "Username", [validators.DataRequired(), validators.Length(min=6)]
    )
    password = fields.PasswordField(
        "Password", [validators.DataRequired(), validators.Length(min=6)]
    )
    name = fields.StringField(
        "Name", [validators.DataRequired(), validators.Length(min=6)]
    )


BaseUploadForm = model_form(
    models.Upload,
    base_class=FlaskForm,
    db_session=models.db.session,
    exclude=["created_date", "updated_date", "status", "filename"],
)


class UploadForm(BaseUploadForm):
    file = fields.FileField(
        "Upload team image (png or jpg) , Recommended image size:250(px) x 230(px)",
        validators=[
            FileAllowed(["png", "jpg", "jpeg"], "You can use onlyjpg , png"),
        ],
    )


# ฟอร์มสำหรับอัปโหลดโปรไฟล์
BaseUploadProfileForm = model_form(
    models.Profile,
    base_class=FlaskForm,
    db_session=models.db.session,
    exclude=["created_date", "updated_date", "filename"],
)


class ProfileForm(BaseUploadProfileForm):
    file = FileField(
        "Upload profile image (png or jpg)",
        validators=[
            FileAllowed(["png", "jpg", "jpeg"], "Only jpg and png are allowed"),
        ],
    )


class PlaceForm(FlaskForm):
    name = StringField("ชื่อสถานที่", validators=[DataRequired()])
    description = TextAreaField("คำอธิบาย")
    images = MultipleFileField(
        "อัปโหลดรูปภาพ",
        validators=[
            FileAllowed(["jpg", "png", "jpeg"], "Only jpg and png are allowed")
        ],
    )
    submit = SubmitField("บันทึก")


class ReviewForm(FlaskForm):
    content = TextAreaField("รีวิว", validators=[DataRequired()])
    rating = FloatField(
        "คะแนนดาว",
        validators=[
            DataRequired(),
            NumberRange(min=0, max=5, message="คะแนนต้องอยู่ระหว่าง 0 ถึง 5"),
        ],
    )
    submit = SubmitField("ส่งรีวิว")
