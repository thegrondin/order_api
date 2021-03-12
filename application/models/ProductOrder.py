# -*- coding: utf-8 -*-

from peewee import *
from application.models.product import Product

db = SqliteDatabase('Payment.db')


class ProductOrder(Model):
    product = ForeignKeyField(Product, backref="product", null=False)
    quantity = IntegerField()

    class Meta:
        database = db