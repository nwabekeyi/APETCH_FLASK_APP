from database import db

class Class(db.Model):
    __tablename__ = "classes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    number_of_students = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"<Class {self.name}>"