from db import db
"""
UserModel
This class represents the user model
"""


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password
    # Instance method to save user to db

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    # class method to find user by username

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    # class method to find user by id

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
