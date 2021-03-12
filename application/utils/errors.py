# -*- coding: utf-8 -*-

class Errors :
    MISSING_FIELD = {"code" : 422, "name" : "missing-fields", "message" : "Il manque un ou plusieurs champs qui sont obligatoires"}
    PRODUCT_OUT_OF_INVENTORY = {"code" : 422, "name" : "out-of-inventory", "message": "Le produit demandé n'est pas en inventaire", }
    ALREADY_PAID = {"code" : 422, "name" : "already-paid", "message": "La commande a déjà été payée."}
    CARD_DECLINED = {"code": 422, "name" : "card-declined", "message" : "La carte de crédit a été déclinée."}
    NOT_FOUND = {"code" : 404, "name" : "not-found", "message" : "La ressource demandé n'a pas pu être trouvé."}
    PAYMENT_REQUEST_NOT_UNIQUE = {'code' : 422, "name" : "request-invalid", 'message' : "Vous ne pouvez pas envoyer les informations client en meme temps de faire le paiement"}
