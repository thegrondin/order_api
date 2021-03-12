# -*- coding: utf-8 -*-
from flask import jsonify

from application import app
from application.models.product import Product


@app.route('/')
def product_list():
    return jsonify(list(Product.select().dicts()))
