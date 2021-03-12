# -*- coding: utf-8 -*-

from peewee import *

db = SqliteDatabase('Payment.db')

class CreditCard(Model):
    name = CharField()
    first_digits = CharField()
    last_digits = CharField()
    expiration_year = IntegerField()
    expiration_month = IntegerField()

    class Meta:
        database = db
