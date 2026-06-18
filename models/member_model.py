from database import db

class Member(db.Model):
    __tablename__ = "members"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id', ondelete='CASCADE'), nullable=False)
    # phone = db.Column(db.String(20))
    joined_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Member {self.name}>"