from db import db


class RecipeModel(db.Model):
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
        return {'name': self.name, 'description': self.description}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
