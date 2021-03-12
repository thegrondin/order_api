# -*- coding: utf-8 -*-

from peewee import *

db = SqliteDatabase('Payment.db')


class Transaction(Model):

    id = CharField(primary_key=True, null=False)
    success = BooleanField()
    amount_charged = IntegerField()

    class Meta:
        database = db



