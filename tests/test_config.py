import unittest
from flask import current_app
from flask_testing import TestCase

class TestDevelopmentConfig(TestCase):
    def create_app(self):
        pass