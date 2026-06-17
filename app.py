from flask import Flask, render_template, url_for, request, redirect, flash
from flask_cors import CORS

from database import db, init_app, init_db
from models import Class

app = Flask(__name__,
            static_folder='static',
            static_url_path='/static')

app.secret_key = 'your_very_secret_key_here_12345_change_in_production'

CORS(app, origins=["http://127.0.0.1:5500"])

# ================= DB INIT =================
init_app(app)

# ================= ROUTES =================

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


# CREATE CLASS
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


# EDIT PAGE
@app.route("/edit_class/<int:class_id>")
def edit_class(class_id):
    class_data = Class.query.get(class_id)

    if not class_data:
        flash("Class not found!", "error")
        return redirect(url_for('home'))

    return render_template("edit_class.html",
                           class_data=class_data,
                           url_for=url_for)


# UPDATE CLASS
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


# DELETE CLASS
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


# MEMBERS PAGE
@app.route("/members")
def members():
    return render_template("members.html", url_for=url_for)


# ================= RUN =================
if __name__ == "__main__":
    init_db(app)
    app.run(debug=True)