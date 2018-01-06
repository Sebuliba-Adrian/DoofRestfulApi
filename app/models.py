from flask import request, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from db import db


class UserModel(db.Model):
    """
    This class represents the user model 
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), index=True)
    password_hash = db.Column(db.String(128))
    recipes = db.relationship(
        'RecipeModel', backref=db.backref(
            "user"), cascade='all, delete-orphan')
    categories = db.relationship(
        'CategoryModel', backref=db.backref(
            "user"), cascade='all, delete-orphan')

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
        "category"), lazy='dynamic', cascade='all, delete-orphan')

    def json(self):
        """
        This method turns category model to json representantion
        """
        return {'id': self.id, 'name': self.name,
                'recipes': [recipe.json() for recipe in self.recipes.all()]}

    @classmethod
    def find_by_name(cls, name):
        """
        This class method queries the database and returns the category model by name
        """
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        """
        This class method queries the database and returns the category model by id
        """
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        """
        This method saves the category model to the db
        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """
        This method deletes the category model from the db
        """
        db.session.delete(self)
        return db.session.commit()


def get_url():
    return url_for(request.endpoint, _external=True)


class RecipeModel(db.Model):
    """
    This recipe model class
    represents the recipe model 
    """
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp())
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    created_by = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)

    def json(self):
        """
        This method jsonifies the recipe model
        """
        return {'name': self.name, 'description': self.description}

    @classmethod
    def find_by_name(cls, name):
        """
        This class method returns the recipe by name
        """
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_category(cls, category_id):
        """
        This class method returns the recipe by category id
        """
        return cls.query.filter_by(category_id=category_id).first()

    @classmethod
    def find_by_id(cls, id):
        """
        This class method returns the recipe by id
        """
        return cls.query.filter_by(id=id).first()

    @classmethod
    def row_count(cls):
        """
        This class method returns the number of rows
        """
        return cls.query.count()

    def save_to_db(self):
        """This method  saves recipe to the database"""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """
        This method deletes recipe from the database
        """
        db.session.delete(self)
        db.session.commit()


class Blacklist(db.Model):

    __tablename__ = "blacklist"
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)

    def save_to_db(self):
        """
        This method saves the blacklist model to the db
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_or_create(cls, jti):
        exists = db.session.query(Blacklist.id).filter_by(
            jti=jti).scalar() is not None
        if exists:
            return True
        return False
