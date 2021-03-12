# -*- coding: utf-8 -*-

import json
from urllib import request as urllib_request, error as urllib_error

class PaymentService:
    @staticmethod
    def request_payment_to_api(credit_card, shipping_price):
        pay_req_data = json.dumps({
            "credit_card": credit_card,
            "amount_charged": shipping_price
        })

        req = urllib_request.Request(url='http://jgnault.ddns.net/shops/pay/',
                                     data=bytes(pay_req_data.encode("utf-8")),
                                     method="POST")

        req.add_header("Content-type", "application/json; charset=UTF-8")

        try:
            request_connection = urllib_request.urlopen(req)
        except urllib_error.HTTPError as e:
            return e.code
        else:
            return json.loads(request_connection.read().decode("utf-8"))