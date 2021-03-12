# -*- coding: utf-8 -*-

from peewee import *


db = SqliteDatabase('Payment.db')


class ShippingInformation(Model):

    country = CharField()
    address = CharField()
    postal_code = CharField()
    city = CharField()
    province = CharField()

    class Meta:
        database = db


