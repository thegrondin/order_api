# -*- coding: utf-8 -*-

from peewee import *

db = SqliteDatabase('Payment.db')


class Product(Model):
    name = CharField()
    description = CharField()
    price = FloatField()
    in_stock = BooleanField()
    image = CharField()
    weight = FloatField()

    class Meta:
        database = db



