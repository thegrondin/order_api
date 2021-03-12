# -*- coding: utf-8 -*-

from peewee import *

from application.models.CreditCard import CreditCard
from application.models.ProductOrder import ProductOrder
from application.models.ShippingInformation import ShippingInformation
from application.models.Transaction import Transaction

db = SqliteDatabase('Payment.db')


class Order(Model):
    total_price = FloatField(null=False)
    email = CharField(null=True)
    credit_card = ForeignKeyField(CreditCard, backref='credit_card', null=True)
    shipping_information = ForeignKeyField(ShippingInformation, backref="shipping_information", null=True)
    paid = BooleanField(default=False)
    transaction = ForeignKeyField(Transaction, backref="transaction", null=True)
    product = ForeignKeyField(ProductOrder, backref="productorder")
    shipping_price = FloatField(null=True)

    class Meta:
        database = db
