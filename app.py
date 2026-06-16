from flask import Flask, render_template, url_for, request, redirect, flash
from flask_cors import CORS
from database import get_db_connection, init_db
import mysql.connector

app = Flask(__name__,
            static_folder='static',
            static_url_path='/static')

app.secret_key = 'your_very_secret_key_here_12345_change_in_production'

CORS(app, origins=["http://127.0.0.1:5500"])


# ====================== HOME - GET ======================
@app.route("/")
def home():
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM classes ORDER BY id ASC")
        classes = cur.fetchall()
        cur.close()
        conn.close()
    except:
        classes = []

    return render_template(
        "index.html",
        username="instructor",
        role="role",
        classes=classes,
        url_for=url_for
    )


# ====================== CREATE CLASS ======================
@app.route("/create_class", methods=["POST"])
def create_class():
    try:
        name = request.form.get("name")
        description = request.form.get("description")

        if not name:
            flash("Class name is required!", "error")
            return redirect(url_for('home'))

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO classes (name, description) VALUES (%s, %s)",
                    (name, description))
        conn.commit()
        cur.close()
        conn.close()

        flash("Class created successfully!", "success")
    except Exception as e:
        flash(f"Error: {e}", "error")

    return redirect(url_for('home'))


# ====================== EDIT FORM (GET) ======================
@app.route("/edit_class/<int:class_id>")
def edit_class(class_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM classes WHERE id = %s", (class_id,))
        class_data = cur.fetchone()
        cur.close()
        conn.close()

        if not class_data:
            flash("Class not found!", "error")
            return redirect(url_for('home'))

        return render_template("edit_class.html", 
                               class_data=class_data, 
                               url_for=url_for)
    except Exception as e:
        flash(f"Error: {e}", "error")
        return redirect(url_for('home'))


# ====================== UPDATE CLASS (POST) ======================
@app.route("/update_class/<int:class_id>", methods=["POST"])
def update_class(class_id):
    try:
        name = request.form.get("name")
        description = request.form.get("description")

        if not name:
            flash("Class name is required!", "error")
            return redirect(url_for('edit_class', class_id=class_id))

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE classes 
            SET name = %s, description = %s 
            WHERE id = %s
        """, (name, description, class_id))
        conn.commit()
        cur.close()
        conn.close()

        flash("Class updated successfully!", "success")
    except Exception as e:
        flash(f"Error updating class: {e}", "error")

    return redirect(url_for('home'))


# ====================== DELETE CLASS ======================
@app.route("/delete_class/<int:class_id>", methods=["POST"])
def delete_class(class_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM classes WHERE id = %s", (class_id,))
        conn.commit()
        cur.close()
        conn.close()

        flash("Class deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting class: {e}", "error")

    return redirect(url_for('home'))


@app.route("/members")
def members():
    return render_template("members.html", url_for=url_for)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)