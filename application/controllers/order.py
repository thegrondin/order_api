# -*- coding: utf-8 -*-

from playhouse.shortcuts import model_to_dict
from flask import request, redirect
from flask import jsonify

from application.models.order import Order
from application.models.product import Product
from application import app
from application.services.OrderService import OrderService
from application.services.PaymentService import PaymentService
from application.utils.ApiException import ApiException
from application.utils.errors import Errors
from application.utils.validation import field_exists


@app.route('/order', methods=['GET'])
def order_get_all():
    return jsonify(list(Order.select().dicts()))


@app.route('/order', methods=['POST'])
def order_post():
    req = request.json

    if 'product' not in req:
        raise ApiException(Errors.MISSING_FIELD, "product")

    if 'quantity' not in req['product']:
        raise ApiException(Errors.MISSING_FIELD, "product", "La creation d'une commande necessite une quantité")

    if 'id' not in req['product']:
        raise ApiException(Errors.MISSING_FIELD, "product", "La creation d'une commande necessite un l'id d'un produit")

    product = Product.get_or_none(Product.id == req['product']['id'])

    if product is None or not product.in_stock:
        raise ApiException(Errors.PRODUCT_OUT_OF_INVENTORY, "product")

    new_order = OrderService.create_order_from_req(req, product)

    return redirect("order/" + str(new_order.id), code=302)


@app.route('/order/<int:order_id>', methods=['GET'])
def order_get(order_id):
    order = Order.get_or_none(Order.id == order_id)

    if order is None:
        raise ApiException(Errors.NOT_FOUND, "order")

    order_dict = model_to_dict(Order.get_by_id(order_id))
    order_dict["product"] = {
        "id": order.product.product.id,
        "quantity": order.product.quantity
    }

    return jsonify(order_dict)


@app.route('/order/<int:order_id>', methods=['PUT'])
def order_put(order_id):
    order = Order.get_or_none(Order.id == order_id)

    if order is None:
        raise ApiException(Errors.NOT_FOUND, "order")

    req = request.json if 'order' not in request.json else request.json['order']

    req["product"] = None

    if 'shipping_information' in req and 'email' in req and 'credit_card' in req:
        raise ApiException(Errors.PAYMENT_REQUEST_NOT_UNIQUE, "order")

    is_client_info_missing_from_req = not field_exists(req, ["email"]) or not field_exists(req["shipping_information"], ["country", "address", "postal_code", "city", "province"])
    client_info_missing_from_model = order.email is None or order.shipping_information is None

    if client_info_missing_from_model and 'credit_card' in req:
        raise ApiException(Errors.MISSING_FIELD, 'order/credit_card', "Les informations du client sont nécessaire avant d'appliquer une carte de crédit")

    if client_info_missing_from_model and is_client_info_missing_from_req:
        raise ApiException(Errors.MISSING_FIELD, "order")

    if "credit_card" in req and not field_exists(req['credit_card'], ['name', 'number', 'expiration_year', 'cvv', 'expiration_month']):
        raise ApiException(Errors.MISSING_FIELD, "order/credit_card")

    if 'shipping_information' in req:
        OrderService.add_client_info_from_req(req, order)
        return order_get(order_id)

    if order.paid:
        raise ApiException(Errors.ALREADY_PAID, 'order/credit_card')

    payment_api_response = PaymentService.request_payment_to_api(req['credit_card'], order.shipping_price)

    if 'success' in payment_api_response and not payment_api_response['success']:
        raise ApiException(Errors.CARD_DECLINED, 'order/payment')

    OrderService.add_payment_from_res(payment_api_response, order)

    return order_get(order_id)
