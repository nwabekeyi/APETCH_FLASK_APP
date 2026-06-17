from flask import Flask, render_template, url_for, request, redirect, flash
from flask_cors import CORS

from email_service import send_email
from database import db, init_app, init_db
from models import Class, Member

# ================= APP SETUP =================
app = Flask(__name__,
            static_folder='static',
            static_url_path='/static')

app.secret_key = 'your_very_secret_key_here_12345_change_in_production'

CORS(app, origins=["http://127.0.0.1:5500"])

# ================= DB INIT =================
init_app(app)

# ================= HOME =================
@app.route("/")
def home():
    try:
        classes = Class.query.order_by(Class.id.asc()).all()
    except:
        classes = []

    return render_template(
        "index.html",
        username="instructor",
        role="role",
        classes=classes,
        url_for=url_for
    )

# ================= CREATE CLASS =================
@app.route("/create_class", methods=["POST"])
def create_class():
    try:
        name = request.form.get("name")
        description = request.form.get("description")

        if not name:
            flash("Class name is required!", "error")
            return redirect(url_for('home'))

        new_class = Class(name=name, description=description)
        db.session.add(new_class)
        db.session.commit()

        flash("Class created successfully!", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Error: {e}", "error")

    return redirect(url_for('home'))


# ================= EDIT CLASS =================
@app.route("/edit_class/<int:class_id>")
def edit_class(class_id):
    class_data = Class.query.get(class_id)

    if not class_data:
        flash("Class not found!", "error")
        return redirect(url_for('home'))

    return render_template("edit_class.html",
                           class_data=class_data,
                           url_for=url_for)


# ================= UPDATE CLASS =================
@app.route("/update_class/<int:class_id>", methods=["POST"])
def update_class(class_id):
    try:
        db.session.query(Class).filter(Class.id == class_id).update({
            "name": request.form.get("name"),
            "description": request.form.get("description")
        })

        db.session.commit()
        flash("Class updated successfully!", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Error: {e}", "error")

    return redirect(url_for("home"))


# ================= DELETE CLASS =================
@app.route("/delete_class/<int:class_id>", methods=["POST"])
def delete_class(class_id):
    try:
        class_obj = Class.query.get(class_id)

        if class_obj:
            db.session.delete(class_obj)
            db.session.commit()
            flash("Class deleted successfully!", "success")
        else:
            flash("Class not found!", "error")

    except Exception as e:
        db.session.rollback()
        flash(f"Error: {e}", "error")

    return redirect(url_for('home'))


# =========================================================
# ====================== MEMBERS ===========================
# =========================================================

# ================= GET ALL MEMBERS =================
@app.route("/members")
def members():
    try:
        all_members = Member.query.order_by(Member.id.desc()).all()
    except:
        all_members = []

    return render_template(
        "members.html",
        members=all_members,
        url_for=url_for
    )


# ================= CREATE MEMBER + EMAIL =================
@app.route("/create_member", methods=["POST"])
def create_member():
    try:
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")

        if not name or not email:
            flash("Name and email are required!", "error")
            return redirect(url_for("members"))

        new_member = Member(
            name=name,
            email=email,
            phone=phone
        )

        db.session.add(new_member)
        db.session.commit()

        # 📧 SEND EMAIL TO MEMBER
        send_email(
            subject="Welcome to Our System",
            body=f"Hello {name},\n\nYou have been successfully registered as a member.\n\nWelcome aboard!",
            to_email=email
        )

        flash("Member created successfully!", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Error: {e}", "error")

    return redirect(url_for("members"))


# ================= EDIT MEMBER =================
@app.route("/edit_member/<int:member_id>")
def edit_member(member_id):
    member = Member.query.get(member_id)

    if not member:
        flash("Member not found!", "error")
        return redirect(url_for("members"))

    return render_template(
        "edit_member.html",
        member=member,
        url_for=url_for
    )


# ================= UPDATE MEMBER =================
@app.route("/update_member/<int:member_id>", methods=["POST"])
def update_member(member_id):
    try:
        member = Member.query.get(member_id)

        if not member:
            flash("Member not found!", "error")
            return redirect(url_for("members"))

        member.name = request.form.get("name")
        member.email = request.form.get("email")
        member.phone = request.form.get("phone")

        db.session.commit()

        flash("Member updated successfully!", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Error: {e}", "error")

    return redirect(url_for("members"))


# ================= DELETE MEMBER =================
@app.route("/delete_member/<int:member_id>", methods=["POST"])
def delete_member(member_id):
    try:
        member = Member.query.get(member_id)

        if member:
            db.session.delete(member)
            db.session.commit()
            flash("Member deleted successfully!", "success")
        else:
            flash("Member not found!", "error")

    except Exception as e:
        db.session.rollback()
        flash(f"Error: {e}", "error")

    return redirect(url_for("members"))


# ================= RUN APP =================
if __name__ == "__main__":
    init_db(app)
    app.run(debug=True)