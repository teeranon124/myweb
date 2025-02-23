import flask
import models
import forms
from flask_login import login_required, login_user, logout_user, LoginManager
from flask import render_template, redirect, url_for
import acl
from flask import Response, send_file, abort
import io
from flask import request, redirect, url_for, render_template, Response, abort
from flask_login import current_user


app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "This is secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
models.init_app(app)


@app.route("/")
@login_required
def index():
    page = request.args.get("page", 1, type=int)  # รับค่าหน้าปัจจุบันจาก URL
    per_page = 6  # จำนวนสถานที่ต่อหน้า
    places = models.Place.query.paginate(
        page=page, per_page=per_page
    )  # ดึงข้อมูลสถานที่แบบแบ่งหน้า
    reviews = models.Review.query.all()  # ดึงข้อมูลรีวิวทั้งหมด รวมถึง user ที่รีวิว

    return render_template(
        "index.html", places=places, reviews=reviews, user=current_user
    )


@app.route("/profile")
@login_required
def profile():
    user = current_user
    return render_template("profile.html", user=current_user)


@app.route("/profile_picture")
@login_required
def profile_picture():
    if current_user.profile and current_user.profile.data:
        return send_file(
            io.BytesIO(current_user.profile.data), mimetype="image/jpeg"
        )  # เปลี่ยน mimetype ถ้าจำเป็น
    return "ไม่มีรูปโปรไฟล์", 404


@app.route("/profile_review/<int:user_id>")
@login_required
def profile_review(user_id):
    user = models.User.query.get(user_id)
    if user and user.profile and user.profile.data:
        return send_file(
            io.BytesIO(user.profile.data), mimetype="image/jpeg"
        )  # เปลี่ยน mimetype ถ้าจำเป็น
    return "ไม่มีรูปโปรไฟล์", 404


@app.route("/profile_post/<int:user_id>")
@login_required
def profile_post(user_id):
    user = models.User.query.get(user_id)
    if user and user.profile and user.profile.data:
        return send_file(
            io.BytesIO(user.profile.data), mimetype="image/jpeg"
        )  # เปลี่ยน mimetype ถ้าจำเป็น
    return "ไม่มีรูปโปรไฟล์", 404


# หน้าเข้าสู่ระบบ
@app.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginForm()
    if not form.validate_on_submit():

        return render_template("login.html", form=form)

    user = models.User.query.filter_by(username=form.username.data).first()
    if user and user.authenticate(form.password.data):
        login_user(user)
        return redirect(url_for("index"))

    return redirect(url_for("login", error="Invalid username or password"))


# หน้าออกจากระบบ
@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# หน้าเปิดใช้งานการลงทะเบียนผู้ใช้ใหม่
@app.route("/register", methods=["GET", "POST"])
def register():
    form = forms.RegisterForm()
    if not form.validate_on_submit():
        return render_template("register.html", form=form)

    user = models.User()  # Initialize the user here
    form.populate_obj(user)  # Populate the user object with form data

    # สร้าง role user ถ้ายังไม่มี
    role = models.Role.query.filter_by(name="user").first()
    if not role:
        role = models.Role(name="user")
        models.db.session.add(role)

    user.roles.append(role)
    user.password_hash = form.password.data
    models.db.session.add(user)
    models.db.session.commit()

    return redirect(url_for("index"))


# @app.route("/tags/<tag_name>")
# def tags_view(tag_name):
#     db = models.db
#     tag = (
#         db.session.execute(db.select(models.Tag).where(models.Tag.name == tag_name))
#         .scalars()
#         .first()
#     )
#     notes = db.session.execute(
#         db.select(models.Note).where(models.Note.tags.any(id=tag.id))
#     ).scalars()
#     return flask.render_template(
#         "tags_view.html",
#         tag_name=tag_name,
#         notes=notes,
#     )


# @app.route("/tags/<tag_id>/update_tags", methods=["GET", "POST"])
# def update_tags(tag_id):  # แก้ไข Tags ได้
#     db = models.db
#     tag = (
#         db.session.execute(db.select(models.Tag).where(models.Tag.id == tag_id))
#         .scalars()
#         .first()
#     )
#     form = forms.TagsForm()
#     form_name = tag.name
#     if not form.validate_on_submit():
#         print(form.errors)
#         return flask.render_template("update_tags.html", form=form, form_name=form_name)
#     note = models.Note(id=tag_id)
#     form.populate_obj(note)
#     tag.name = form.name.data
#     db.session.commit()
#     return flask.redirect(flask.url_for("index"))


# @app.route("/tags/<tag_id>/delete_tags", methods=["GET", "POST"])
# def delete_tags(tag_id):  # ลบ Tags ได้อย่างเดียว
#     db = models.db
#     tag = (
#         db.session.execute(db.select(models.Tag).where(models.Tag.id == tag_id))
#         .scalars()
#         .first()
#     )
#     tag.name = ""
#     db.session.commit()
#     return flask.redirect(flask.url_for("index"))


# @app.route("/notes/create_note", methods=["GET", "POST"])
# def create_note():
#     form = forms.NoteForm()
#     if not form.validate_on_submit():
#         print("error", form.errors)
#         return flask.render_template(
#             "create_note.html",
#             form=form,
#         )
#     note = models.Note()
#     form.populate_obj(note)
#     note.tags = []
#     db = models.db
#     for tag_name in form.tags.data:
#         tag = (
#             db.session.execute(db.select(models.Tag).where(models.Tag.name == tag_name))
#             .scalars()
#             .first()
#         )
#         if not tag:
#             tag = models.Tag(name=tag_name)
#             db.session.add(tag)
#         note.tags.append(tag)
#     db.session.add(note)
#     db.session.commit()
#     return flask.redirect(flask.url_for("index"))


# @app.route("/tags/<tag_id>/update_note", methods=["GET", "POST"])
# def update_note(tag_id):  # แก้ไข Note และสามารถเปลี่ยนชื่อ Title ได้
#     db = models.db
#     notes = (
#         db.session.execute(
#             db.select(models.Note).where(models.Note.tags.any(id=tag_id))
#         )
#         .scalars()
#         .first()
#     )
#     form = forms.NoteForm()
#     form_title = notes.title
#     form_description = notes.description
#     if not form.validate_on_submit():
#         print(form.errors)
#         return flask.render_template(
#             "update_note.html",
#             form=form,
#             form_title=form_title,
#             form_description=form_description,
#         )
#     note = models.Note(id=tag_id)
#     form.populate_obj(note)
#     notes.description = form.description.data
#     notes.title = form.title.data
#     db.session.commit()
#     return flask.redirect(flask.url_for("index"))


# @app.route("/tags/<tag_id>/delete_note", methods=["GET", "POST"])
# def delete_note(tag_id):  # ลบ Note เพียงอย่างเดียวไม่ได้ลบ Title
#     db = models.db
#     notes = (
#         db.session.execute(
#             db.select(models.Note).where(models.Note.tags.any(id=tag_id))
#         )
#         .scalars()
#         .first()
#     )
#     notes.description = ""
#     db.session.commit()
#     return flask.redirect(flask.url_for("index"))


# @app.route("/tags/<tag_id>/delete", methods=["GET", "POST"])
# def delete(tag_id):  # ลบทั้งหมดที่เกี่ยวกับ Tags
#     db = models.db
#     notes = (
#         db.session.execute(
#             db.select(models.Note).where(models.Note.tags.any(id=tag_id))
#         )
#         .scalars()
#         .first()
#     )
#     db.session.delete(notes)
#     db.session.commit()
#     return flask.redirect(flask.url_for("index"))


@app.route("/images")
def images():
    db = models.db
    images = db.session.execute(
        db.select(models.Upload).order_by(models.Upload.filename)
    ).scalars()
    return flask.render_template(
        "images.html",
        images=images,
    )


@app.route("/profileimage")
def imageprofile():
    db = models.db
    images = db.session.execute(
        db.select(models.Profile).order_by(models.Profile.filename)
    ).scalars()

    return flask.render_template(
        "images.html",
        images=images,
    )


@app.route("/upload", methods=["GET", "POST"])
def upload():
    form = forms.UploadForm()
    db = models.db
    file_ = models.Upload()
    if not form.validate_on_submit():
        return flask.render_template(
            "upload.html",
            form=form,
        )
    if form.file.data:
        file_ = models.Upload(
            filename=form.file.data.filename,
            data=form.file.data.read(),  # Read binary data
        )
    db.session.add(file_)
    db.session.commit()
    return flask.redirect(flask.url_for("index"))


@app.route("/uploadprofile", methods=["GET", "POST"])
def uploadprofile():
    db = models.db
    if not current_user.is_authenticated:
        return redirect(url_for("login"))

    form = forms.ProfileForm()
    if form.validate_on_submit():
        if form.file.data:
            profile = current_user.profile

            if profile:
                # อัปเดตโปรไฟล์ที่มีอยู่
                profile.filename = form.file.data.filename
                profile.data = form.file.data.read()
            else:
                # สร้างโปรไฟล์ใหม่
                profile = models.Profile(
                    filename=form.file.data.filename,
                    data=form.file.data.read(),
                )
                db.session.add(profile)
                current_user.profile = profile  # เชื่อมโยงโปรไฟล์กับผู้ใช้

            # บันทึกการเปลี่ยนแปลงลงฐานข้อมูล
            db.session.commit()

            # รีเฟรชข้อมูล current_user หลังจาก commit เพื่อให้ข้อมูลถูกต้อง
            db.session.refresh(current_user)

            return redirect(url_for("index"))

    return render_template("upload.html", form=form)


@app.route("/upload/<int:file_id>", methods=["GET"])
def get_upload_image(file_id):
    # Query the database for the file with the given file_id
    file_ = models.Upload.query.get(file_id)
    if not file_ or not file_.data:
        # Return 404 if file is not found
        abort(404, description="File not found")
    # Serve the binary data as a file
    return Response(
        file_.data,
        headers={
            "Content-Disposition": f'inline;filename="{file_.filename}"',
            "Content-Type": "application/octet-stream",
        },
    )


@app.route("/uploadprofile/<int:file_id>", methods=["GET"])
def get_profile_image(file_id):
    # Query the database for the file with the given file_id
    file_ = models.Profile.query.get(file_id)
    if not file_ or not file_.data:
        # Return 404 if file is not found
        abort(404, description="File not found")
    # Serve the binary data as a file
    return Response(
        file_.data,
        headers={
            "Content-Disposition": f'inline;filename="{file_.filename}"',
            "Content-Type": "application/octet-stream",
        },
    )


# เส้นทางสำหรับดึงรูปภาพของสถานที่
@app.route("/get_image/<int:file_id>", methods=["GET"])
def get_place_image(file_id):
    file_ = models.PlaceImage.query.get(file_id)
    if not file_ or not file_.data:
        abort(404, description="File not found")
    return Response(
        file_.data,
        headers={
            "Content-Disposition": f'inline;filename="{file_.filename}"',
            "Content-Type": "image/jpeg",
        },
    )


@app.route("/create_place", methods=["GET", "POST"])
@login_required
def create_place():
    form = forms.PlaceForm()
    db = models.db
    if form.validate_on_submit():
        new_place = models.Place(
            name=form.name.data,
            description=form.description.data,
            user_id=current_user.id,  # บันทึก user_id ของผู้ที่เพิ่มสถานที่
        )
        db.session.add(new_place)
        db.session.commit()

        for file in form.images.data:
            if file:
                new_image = models.PlaceImage(
                    filename=file.filename, data=file.read(), place_id=new_place.id
                )
                db.session.add(new_image)

        db.session.commit()
        return redirect(url_for("index"))

    return render_template("create_place.html", form=form)


@app.route("/add_review/<int:place_id>", methods=["GET", "POST"])
@login_required
def add_review(place_id):
    form = forms.ReviewForm()
    place = models.Place.query.get_or_404(place_id)  # ดึงข้อมูลสถานที่หรือแสดงหน้า 404 หากไม่พบ
    db = models.db
    if form.validate_on_submit():
        # สร้างรีวิวใหม่
        new_review = models.Review(
            content=form.content.data,
            place_id=place_id,
            user_id=current_user.id,  # ใช้ ID ของผู้ใช้ปัจจุบัน
        )
        db.session.add(new_review)
        db.session.commit()
        return redirect(url_for("place_detail", place_id=place_id))

    return render_template("add_review.html", form=form, place=place)


@app.route("/place_detail/<int:place_id>")
def place_detail(place_id):
    place = models.Place.query.get_or_404(place_id)  # ดึงข้อมูลสถานที่หรือแสดงหน้า 404 หากไม่พบ
    return render_template("place_detail.html", place=place, user=current_user)


@app.route("/rate_place/<int:place_id>", methods=["POST"])
@login_required
def rate_place(place_id):
    db = models.db
    rating_value = request.form.get("rating")
    place = models.Place.query.get_or_404(place_id)
    existing_rating = models.Rating.query.filter_by(
        user_id=current_user.id, place_id=place_id
    ).first()

    if existing_rating:
        existing_rating.rating = rating_value
    else:
        new_rating = models.Rating(
            rating=rating_value, user_id=current_user.id, place_id=place_id
        )
        db.session.add(new_rating)

    db.session.commit()
    place.update_average_rating()
    return redirect(url_for("place_detail", place_id=place_id))


@app.route("/view_review")
@login_required
def view_review():
    user = current_user
    return render_template("view_review.html", user=user)


@app.route("/view_post")
@login_required
def view_post():
    user = current_user
    return render_template("view_post.html", user=user)


@app.route("/edit_place/<int:place_id>", methods=["GET", "POST"])
@login_required
def edit_place(place_id):
    place = models.Place.query.get_or_404(place_id)
    if place.user_id != current_user.id:
        abort(403)  # Forbidden

    form = forms.PlaceForm(obj=place)

    if form.validate_on_submit():
        # อัปเดตข้อมูลสถานที่
        place.name = form.name.data
        place.description = form.description.data

        # เช็คว่ามีการอัปโหลดไฟล์ใหม่หรือไม่
        if form.images.data:
            # 🔹 ลบรูปเก่าออกจากฐานข้อมูลก่อน
            models.PlaceImage.query.filter_by(place_id=place.id).delete()

            # 🔹 อัปโหลดรูปใหม่
            for image in form.images.data:
                if image.filename:  # ตรวจสอบว่าไฟล์มีชื่อหรือไม่
                    new_image = models.PlaceImage(
                        filename=image.filename,
                        data=image.read(),  # อ่านข้อมูลไบนารี
                        place_id=place.id,
                    )
                    models.db.session.add(new_image)  # เพิ่มไฟล์รูปภาพลง DB

        models.db.session.commit()
        return redirect(url_for("profile"))

    return render_template("edit_place.html", form=form, place=place)


@app.route("/delete_place/<int:place_id>", methods=["POST"])
@login_required
def delete_place(place_id):
    place = models.Place.query.get_or_404(place_id)
    if place.user_id != current_user.id:
        abort(403)  # Forbidden

    models.db.session.delete(place)
    models.db.session.commit()
    return redirect(url_for("profile"))


@app.route("/edit_review/<int:review_id>", methods=["GET", "POST"])
@login_required
def edit_review(review_id):
    review = models.Review.query.get_or_404(review_id)
    if review.user_id != current_user.id:
        abort(403)  # Forbidden

    form = forms.ReviewForm(obj=review)
    if form.validate_on_submit():
        form.populate_obj(review)
        models.db.session.commit()
        return redirect(url_for("index"))

    return render_template("edit_review.html", form=form, review=review)


@app.route("/delete_review/<int:review_id>", methods=["POST"])
@login_required
def delete_review(review_id):
    review = models.Review.query.get_or_404(review_id)
    if review.user_id != current_user.id:
        abort(403)  # Forbidden

    models.db.session.delete(review)
    models.db.session.commit()
    return redirect(url_for("profile"))


if __name__ == "__main__":
    app.run(debug=True)
