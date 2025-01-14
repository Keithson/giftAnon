from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session, request
from flask import flash
from flask_app.models import user
import re

class Purchase:
    db = "giftanon" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.item_name = data['item_name']
        self.category = data['category']
        self.facility = data['facility']
        self.city = data['city']
        self.quantity = data['quantity']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.maker = None

    @classmethod
    def save(cls, data):
        query = """INSERT INTO purchases (item_name, category, facility, city, quantity, user_id) 
        VALUES (%(item_name)s, %(category)s, %(facility)s, %(city)s, %(quantity)s, %(user_id)s);"""
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = """ 
        SELECT * 
        FROM purchases
        LEFT JOIN users
        ON purchases.user_id = users.id;"""
        final = connectToMySQL(cls.db).query_db(query)
        results = []
        for result in final:
            this_purchase = cls(result)
            user_data = {
                    "id": result['id'],
                    "first_name": result['first_name'],
                    "last_name": result['last_name'],
                    "email": result['email'],
                    "password": "",
                    "created_at": result['created_at'],
                    "updated_at": result['updated_at']
            }
            this_purchase.maker = user.User(user_data)
            results.append(this_purchase)
        return results
    
    @classmethod
    def get_by_id(cls, id):
        data = {
            "id" : id
        }
        query = """
        SELECT * 
        FROM purchases
        LEFT JOIN users
        ON purchases.user_id = users.id
        WHERE purchases.id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query,data)
        purchase_list = []
        for result in results:
            this_purchase = cls(result)
            user_data = {
                    "id": result['id'],
                    "first_name": result['first_name'],
                    "last_name": result['last_name'],
                    "email": result['email'],
                    "password": "",
                    "created_at": result['users.created_at'],
                    "updated_at": result['users.updated_at']
            }
            this_purchase.maker = user.User(user_data)
            purchase_list.append(this_purchase)
        return purchase_list[0]
    
    @classmethod
    def get_all_purchases(cls, id):
        data = {
            "id" : id
        }
        query = """
        SELECT *
        FROM purchases
        LEFT JOIN users
        ON purchases.purchaser_id = users.id
        WHERE purchaser_id = %(id)s"""
        results = connectToMySQL(cls.db).query_db(query,data)
        purchase_list = []
        for result in results:
            this_list = cls(result)
            purchase_data = {
                "city": result['city'],
                "facility": result['facility'],
                "item": result['item'],
                "quantity": result['quantity']
            }
            purchase_list.append(this_list)
        return purchase_list
    
    @classmethod
    def get_by_item_name(cls, item_name):
        data = {
            "item_name" : item_name
        }
        query = """
        SELECT * 
        FROM purchases
        LEFT JOIN users
        ON purchases.user_id = users.id
        WHERE purchases.item_name = %(item_name)s;"""
        results = connectToMySQL(cls.db).query_db(query,data)
        purchase_list = []
        for result in results:
            this_purchase = cls(result)
            user_data = {
                    "id": result['id'],
                    "first_name": result['first_name'],
                    "last_name": result['last_name'],
                    "email": result['email'],
                    "password": "",
                    "created_at": result['users.created_at'],
                    "updated_at": result['users.updated_at']
            }
            this_purchase.maker = user.User(user_data)
            purchase_list.append(this_purchase)
            print(user_data)
        if not results:
            return False
        return purchase_list[0]
    
    @classmethod
    def update(cls, data):
        query = """
        UPDATE purchases
        SET item_name = %(item_name)s, 
        category = %(category)s, 
        facility = %(facility)s, 
        city = %(city)s
        WHERE id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return results
    
    @classmethod
    def delete(cls, id):
        data = {
            'id' : id
        }
        query = """
        DELETE FROM purchases
        WHERE id = %(id)s"""
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_purchase(data):
        is_valid = True # we assume this is true
        if len(data['item_name']) < 3:
            flash("Item name must be at least 3 characters.", "purchase")
            is_valid = False
        if len(data['category']) < 3:
            flash("Category must be at least 3 characters.", "purchase")
            is_valid = False
        if data['facility'] == '':
            flash('Select your preferred facility.', "purchase")
            is_valid = False
        if len(data['city']) < 3:
            flash("Select your preferred city.", "purchase")
            is_valid = False
        if len(data['quantity']) < 1:
            flash("Quantity must be at least 3 characters.", "purchase")
            is_valid = False
        return is_valid