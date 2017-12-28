#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests import BaseTestCase
from app.models.recipe import RecipeModel
from app.models.category import CategoryModel
from validator import is_valid


class ValidatorTest(BaseTestCase):
    def test_valid_category_name(self):

        self.assertEqual(is_valid('categoryname'), True)

    def test_invalid_category_name(self):

        self.assertEqual(is_valid('(*&&^!"¬&**'), False)
