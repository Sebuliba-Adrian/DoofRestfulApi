import unittest
import os
from flask import current_app
from unittest import TestCase
from config import basedir
from app import app


"""
    Class contains test that verify the app created with
    development configurations
"""


class TestDevelopmentConfig(TestCase):

    @staticmethod
    def create_app():
        """Application factory method"""
        app.config.from_object('config.DevelopmentConfig')
        return app

    def setUp(self):
        """
        Sets up the default configurations
        """
        self.app = self.create_app()

    def tearDown(self):
        pass

    def test_app_is_development(self):
        """
        Tests that app was started with development settings
        """
        self.assertTrue(self.app.config['SECRET_KEY'] ==
                        'XMLZODSHE8N6NFOZDPZA2HULWSIYJU45K6N4ZO9M')
        self.assertTrue(self.app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(self.app.config['SQLALCHEMY_DATABASE_URI'] ==
                        'postgresql://adrian:andela@localhost/develop_db')


class TestTestingConfig(TestCase):
    """
    Class contains test that verify the app created with
    testing configurations
    """
    @staticmethod
    def create_app():
        """Application factory method"""

        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        """
        Sets up the default configurations
        """
        self.app = self.create_app()

    def tearDown(self):
        pass

    def test_app_is_testing(self):
        self.assertTrue(self.app.config['SECRET_KEY'] ==
                        'XMLZODSHE8N6NFOZDPZA2HULWSIYJU45K6N4ZO9M')
        self.assertTrue(self.app.config['DEBUG'])
        self.assertTrue(self.app.config['TESTING'])
        self.assertFalse(self.app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        self.assertTrue(
            self.app.config['SQLALCHEMY_DATABASE_URI'] ==
            'postgresql://adrian:andela@localhost/develop_db')


class TestProductionConfig(TestCase):
    """
    Class contains test that verify the app created with
    production configurations
    """
    @staticmethod
    def create_app():
        """Application factory method"""
        app.config.from_object('config.ProductionConfig')
        return app

    def setUp(self):
        """
        Sets up the default configurations
        """
        self.app = self.create_app()

    def tearDown(self):
        pass

    def test_app_is_production(self):
        self.assertTrue(self.app.config['SECRET_KEY'] ==
                        'XMLZODSHE8N6NFOZDPZA2HULWSIYJU45K6N4ZO9M')
        self.assertFalse(self.app.config['DEBUG'])
        self.assertFalse(self.app.config['TESTING'])



if __name__ == '__main__':
    unittest.main()