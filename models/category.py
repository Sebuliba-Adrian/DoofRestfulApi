from db import db
from flask import url_for, request


class CategoryModel(db.Model):
    """This is category model class"""
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    recipes = db.relationship('RecipeModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

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
