

from unittest import TestCase

from flask import current_app

from app import app

"""
    Class contains test that verify the app created with
    development configurations
"""


class TestDevelopmentConfig(TestCase):

    @staticmethod
    def create_app():
        """Application factory method"""
        app.config.from_object('config.config.DevelopmentConfig')
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
                        'postgresql://adrian1:andela@localhost/develop_db')
        self.assertTrue(self.app.config['JWT_SECRET_KEY'] ==
                        'my precious')


class TestTestingConfig(TestCase):
    """
    Class contains test that verify the app created with
    testing configurations
    """
    @staticmethod
    def create_app():
        """Application factory method"""

        app.config.from_object('config.config.TestingConfig')
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
            'postgresql://adrian2:andela@localhost/test_db')
        self.assertTrue(self.app.config['JWT_SECRET_KEY'] ==
                        'my precious')


class TestProductionConfig(TestCase):
    """
    Class contains test that verify the app created with
    production configurations
    """
    @staticmethod
    def create_app():
        """Application factory method"""
        app.config.from_object('config.config.ProductionConfig')
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
        self.assertTrue(self.app.config['JWT_SECRET_KEY'] ==
                        'my precious')
