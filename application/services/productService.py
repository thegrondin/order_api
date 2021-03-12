# -*- coding: utf-8 -*-

import json
import urllib.request
from application.models.product import Product


class ProductService:
    @staticmethod
    def fetch_all_to_db(url):
        with urllib.request.urlopen(url) as res:
            json_res = json.load(res)

            for product in json_res['products']:
                new_product = Product(
                    name=product['name'],
                    description=product['description'],
                    price=product['price'],
                    in_stock=product['in_stock'],
                    image=product['image'],
                    weight=product['weight']
                )

                new_product.save()

    @staticmethod
    def clear_all_from_db():
        query = Product.delete()
        query.execute()
