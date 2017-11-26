import unittest
import os
from flask import current_app
from unittest import TestCase
from config import basedir

from app import app


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['SECRET_KEY'] ==
                        'XMLZODSHE8N6NFOZDPZA2HULWSIYJU45K6N4ZO9M')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] ==
                        'sqlite:///' + os.path.join(basedir, 'devdb.sqlite'))


                        
