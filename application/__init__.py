# -*- coding: utf-8 -*-

from flask import Flask

from application.services.productService import *

from application.models.product import *
from application.models.Transaction import *
from application.models.ShippingInformation import *
from application.models.order import *
from application.models.ProductOrder import *
from application.models.CreditCard import *

app = Flask('__main__')
app.config['SECRET_KEY'] = 'random'
app.debug = True

db = SqliteDatabase('Payment.db')
db.connect()


@app.cli.command("init-db")
def init_db():
    db.drop_tables([Order, ProductOrder, Transaction, ShippingInformation, CreditCard])
    db.create_tables([CreditCard, Transaction, ShippingInformation, ProductOrder, Order])


app.cli.add_command(init_db)

ProductService.clear_all_from_db()
ProductService.fetch_all_to_db("http://jgnault.ddns.net/shops/products/")

print(len(list(Product.select().dicts())))

from application.controllers import *
