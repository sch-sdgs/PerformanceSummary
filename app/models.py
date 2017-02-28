from app.performance_summary import db
from sqlalchemy.orm import relationship

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False)
    admin = db.Column(db.Integer)

    def __init__(self, username, admin):
        self.username = username
        self.admin = admin

    def __repr__(self):
        return '<Users %r>' % (self.username)
