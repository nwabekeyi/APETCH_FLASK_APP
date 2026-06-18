from flask import Flask, render_template, url_for, request, redirect, flash
from flask_cors import CORS
from flask_login import LoginManager, login_required, current_user
from dotenv import load_dotenv

# ====================== CONFIG & EXTENSIONS ======================
from database import db, init_db
from config import Config
from models import User, Class, Member
from services.email_service import init_mail
from blueprints.auth import auth

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, origins=["http://127.0.0.1:5500"])

# ====================== FLASK-LOGIN SETUP ======================
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login"""
    return User.query.get(int(user_id))

# ====================== INITIALIZE EXTENSIONS ======================
init_mail(app)
login_manager.init_app(app)

# Register Authentication Blueprint
app.register_blueprint(auth, url_prefix="/auth")

# ====================== ROUTES ======================

@app.route("/")
@login_required
def home():
    """Home Page - List of Classes"""
    try:
        classes = Class.query.order_by(Class.id.asc()).all()
    except:
        classes = []

    return render_template(
        "index.html",
        username=current_user.username,
        role=current_user.role,
        classes=classes,
        url_for=url_for
    )


@app.route("/create_class", methods=["POST"])
@login_required
def create_class():
    """Create New Class"""
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


@app.route("/edit_class/<int:class_id>")
@login_required
def edit_class(class_id):
    """Edit Class Page"""
    class_data = Class.query.get(class_id)

    if not class_data:
        flash("Class not found!", "error")
        return redirect(url_for('home'))

    return render_template("edit_class.html",
                           class_data=class_data,
                           url_for=url_for)


@app.route("/update_class/<int:class_id>", methods=["POST"])
@login_required
def update_class(class_id):
    """Update Class"""
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


@app.route("/delete_class/<int:class_id>", methods=["POST"])
@login_required
def delete_class(class_id):
    """Delete Class"""
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


# ====================== MEMBERS ROUTES ======================

@app.route("/members")
@login_required
def members():
    """List All Members"""
    try:
        all_members = Member.query.order_by(Member.id.desc()).all()
        classes = Class.query.order_by(Class.id.asc()).all()
    except:
        all_members = []
        classes = []

    return render_template(
        "members.html",
        members=all_members,
        classes=classes,
        url_for=url_for
    )


@app.route("/create_member", methods=["POST"])
@login_required
def create_member():
    """Create New Member + Send Welcome Email"""
    try:
        name = request.form.get("name")
        email = request.form.get("email")
        class_id = request.form.get("class_id")
        # phone = request.form.get("phone")

        if not name or not email or not class_id:
            flash("Name, email, and class are required!", "error")
            return redirect(url_for("members"))

        new_member = Member(
            name=name,
            email=email,
            class_id=class_id,
            # phone=phone
        )

        db.session.add(new_member)
        db.session.commit()

        # Send Welcome Email using template
        from services.email_service import send_email
        send_email(
            subject="Welcome to Our System",
            to_email=email,
            template_path="emails/welcome.html",
            context={"name": name},
            body=f"Hello {name},\n\nYou have been successfully registered as a member."
        )

        flash("Member created successfully! Welcome email sent.", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Error: {e}", "error")

    return redirect(url_for("members"))


@app.route("/edit_member/<int:member_id>")
@login_required
def edit_member(member_id):
    """Edit Member Page"""
    member = Member.query.get(member_id)

    if not member:
        flash("Member not found!", "error")
        return redirect(url_for("members"))

    return render_template("edit_member.html",
                           member=member,
                           url_for=url_for)


@app.route("/update_member/<int:member_id>", methods=["POST"])
@login_required
def update_member(member_id):
    """Update Member"""
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


@app.route("/delete_member/<int:member_id>", methods=["POST"])
@login_required
def delete_member(member_id):
    """Delete Member"""
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


# ====================== RUN APP ======================
if __name__ == "__main__":
    init_db(app)   # Create tables on first run
    app.run(debug=True)