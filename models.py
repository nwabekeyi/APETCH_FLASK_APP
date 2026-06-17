from database import db


class Class(db.Model):
    __tablename__ = "classes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    number_of_students = db.Column(db.Integer, nullable=False, default=2)

    members = db.relationship(
        "Member",
        backref="class_ref",
        cascade="all, delete"
    )


class Member(db.Model):
    __tablename__ = "members"

    id = db.Column(db.Integer, primary_key=True)

    class_id = db.Column(
        db.Integer,
        db.ForeignKey("classes.id"),
        nullable=False
    )

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150))

    joined_at = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )