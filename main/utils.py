# -*- coding: utf-8 -*-
__author__ = 'Vershinin M.S.'
from django.db import models

FIELD_TYPES = dict(int=models.IntegerField, char=models.CharField, date=models.DateField)


def create_model_class(table_name, table_metadata):
    class Meta:
        app_label = __package__
        verbose_name = table_metadata['title']

    class_attrs = dict(__module__='', Meta=Meta)
    for field_desription in table_metadata['fields']:
        field = FIELD_TYPES[field_desription['type']]
        class_attrs[field_desription['id']] = field(verbose_name=field_desription['title'], max_length=10)
    return type(table_name.title(), (models.Model, ), class_attrs)