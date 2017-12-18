from db import db
from flask import url_for, request
from sqlalchemy import func


class RecipeModel(db.Model):
    """This is a recipe model class"""
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(800))

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('CategoryModel')

    def __init__(self, name, description, category_id):
        self.name = name
        self.description = description
        self.category_id = category_id

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
