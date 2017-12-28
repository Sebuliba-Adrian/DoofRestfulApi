from db import db
from flask import request, url_for
from werkzeug.security import check_password_hash, generate_password_hash


"""
UserModel
This class represents the user model
"""


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), index=True)
    password_hash = db.Column(db.String(128))
    recipes = db.relationship(
        'RecipeModel', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    categories = db.relationship(
        'CategoryModel', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    # Instance method to save user to db

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self
    # class method to find user by username

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    # class method to find user by id

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()


class CategoryModel(db.Model):
    """This is category model class"""
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipes = db.relationship("RecipeModel", backref=db.backref(
        "category"), cascade='all, delete-orphan')

    # def __init__(self, name, user_id):
    #     self.name = name
    #     self.user_id= user_id

    def json(self):
        """This method turns category model to json representantion"""
        return {'id': self.id, 'name': self.name, 'recipes': [recipe.json() for recipe in self.recipes.all()]}

    def get_url(self):
        return url_for(request.endpoint, _external=True)

    @classmethod
    def find_by_name(cls, name):
        """This class method queries the database and returns the category model by name"""
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        """This class method queries the database and returns the category model by id"""
        return cls.query.filter_by(id=id).first()

    @classmethod
    def row_count(cls):
        """This class method returns the number of rows"""
        return cls.query.count()

    @staticmethod
    def roll_back():
        """This static method rolles back database session """
        db.session().rollback()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        return db.session.commit()


class RecipeModel(db.Model):
    """This is a recipe model class"""
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp())
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    created_by = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)

    # category = db.relationship('CategoryModel')

    def json(self):
        """This method jsonifies the recipe model"""
        return {'name': self.name, 'description': self.description}

    def get_url(self):
        return url_for(request.endpoint, _external=True)

    @classmethod
    def find_by_name(cls, name):
        """This class method returns the recipe by name"""
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_category(cls, category_id):
        """This class method returns the recipe by category id"""
        return cls.query.filter_by(category_id=category_id).first()

    @classmethod
    def find_by_id(cls, id):
        """This class method returns the recipe by id"""
        return cls.query.filter_by(id=id).first()

    @classmethod
    def row_count(cls):
        """This class method returns the number of rows"""
        return cls.query.count()

    def save_to_db(self):
        """This method  saves recipe to the database"""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """This method deletes recipe from the database"""
        db.session.delete(self)
        db.session.commit()