# -*- coding: utf-8 -*-
from django.test import TestCase
import unittest
from models import *
from yaml import load
from utils import create_model_class
from django.db import models
from django.test.client import Client
from datetime import date
import json


class TestModels(TestCase):
    def setUp(self):
        model_metadata = load(u"""
        users:
            title: Пользователи
            fields:
              - {id: name, title: Имя, type: char}
              - {id: paycheck, title: Зарплата, type: int}
              - {id: date_joined, title: Дата поступления на работу, type: date}
        """)
        self._table_name, self._table_metadata = model_metadata.popitem()
        self._model = create_model_class(self._table_name, self._table_metadata)
        self._field_types = dict(int=models.IntegerField, char=models.CharField, date=models.DateField)
        pass

    def test_class_name(self):
        self.assertEqual(self._model.__name__, u'Users')

    def test_fields_names(self):
        model_field_names = [f.name for f in self._model._meta.fields]
        for field in self._table_metadata['fields']:
            self.assertIn(field['id'], [u'name', u'paycheck', u'date_joined'])

    def test_fields_types(self):
        field_classes = {f.name: f.__class__ for f in self._model._meta.fields}
        for field in self._table_metadata['fields']:
            self.assertIs(self._field_types[field['type']], field_classes[field['id']])


class TestClient(TestCase):
    def setUp(self):
        self._client = Client()
        Users(name="Test user", paycheck=100, date_joined=date(2014, 1, 1)).save()

    def test_good_post_request(self):
        response = self._client.post('/model/Users/', {'name': "Test user", "paycheck": 100, "date_joined": "2014-01-01"})
        self.assertEqual(response.status_code, 200)

    def test_bad_post_request(self):
        response = self._client.post('/model/Users/', {'name': "Test user", "paycheck": 100, "date_joined": "2014--01"})
        self.assertNotEqual(response.status_code, 200)

    def test_get_request(self):
        data = json.loads(self._client.get('/model/Users/').content)
        self.assertEqual(data['objects'][0]['name'], "Test user")



if __name__ == '__main__':
    unittest.main()