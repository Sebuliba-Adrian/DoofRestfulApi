#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests.base import BaseTestCase
from models.recipe import RecipeModel
from models.category import CategoryModel
from validator import is_valid


class ValidatorTest(BaseTestCase):
    def test_valid_category_name(self):
        with self.app_context():
            self.assertEqual(is_valid('categoryname'), True)

    def test_invalid_category_name(self):
        with self.app_context():
            self.assertEqual(is_valid('(*&&^!"¬&**'), False)
