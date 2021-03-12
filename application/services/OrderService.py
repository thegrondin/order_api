# -*- coding: utf-8 -*-

from playhouse.shortcuts import dict_to_model
from application.models.CreditCard import CreditCard
from application.models.ProductOrder import ProductOrder
from application.models.ShippingInformation import ShippingInformation
from application.models.Transaction import Transaction
from application.models.order import Order


class OrderService:
    @staticmethod
    def create_order_from_req(req, product):
        new_product_order = ProductOrder(
            product=product,
            quantity=req['product']['quantity'])

        new_product_order.save()

        total_price = req['product']['quantity'] * product.price
        order = Order(product=new_product_order,
                      total_price=total_price,
                      shipping_price=total_price + (
                          5 if product.weight <= 500 else 10 if product.weight <= 2000 else 25))

        order.save()

        return order

    @staticmethod
    def add_client_info_from_req(req, order):
        new_shipping_info = dict_to_model(ShippingInformation, req['shipping_information'])
        order = Order.get_by_id(order.id)
        order.email = req['email']
        order.shipping_information = new_shipping_info

        new_shipping_info.save()
        order.save()

    @staticmethod
    def add_payment_from_res(res_data, order):
        new_credit_card_payment = dict_to_model(CreditCard, res_data['credit_card'])
        new_transaction = dict_to_model(Transaction, res_data['transaction'])

        new_credit_card_payment.save()
        new_transaction.save(force_insert=True)

        order.credit_card = new_credit_card_payment
        order.transaction = new_transaction
        order.paid = True
        order.save()
