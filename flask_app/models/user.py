from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:

    db_name='skematest'
    def __init__(self,data):
        self.id=data['id'],
        self.name=data['name'],
        self.lastName=data['lastName'],
        self.email=data['email'],
        self.password=data['password'],
        self.created_at=data['created_at'],
        self.update_at=data['update_at']


    @classmethod
    def getAllUsers(cls):
        query= 'SELECT * FROM users;'
        results =  connectToMySQL(cls.db_name).query_db(query)
        users= []
        for row in results:
            users.append(row)
        return users

    @classmethod
    def create_user(cls,data):
        query="INSERT INTO users (name, lastName, email, password) VALUES (%(name)s,%(lastName)s,%(email)s, %(password)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_user_by_id(cls,data):
        query="SELECT * FROM users WHERE id=%(user_id)s"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        print(results)
        return results[0]

    @classmethod
    def get_user_by_email(cls, data):
        query= 'SELECT * FROM users WHERE users.email = %(email)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results)<1:
            return False
        return results[0]

    @classmethod
    def get_all_user_info(cls, data):
        query= 'SELECT * FROM users LEFT JOIN thoughts on thoughts.user_id = users.id WHERE users.id = %(user_id)s;'
        results =  connectToMySQL(cls.db_name).query_db(query, data)
        thoughts = []
        for row in results:
            thoughts.append(row)
        return thoughts


    @classmethod
    def get_logged_user_liked_thoughts(cls, data):
        query = 'SELECT thought_id as id FROM likes LEFT JOIN users on likes.user_id = users.id WHERE user_id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        Likedthought = []
        for row in results:
            Likedthought.append(row['id'])
        return Likedthought

        

    @staticmethod
    def validate_user(user):
        is_valid = True
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'emailSignUp')
            is_valid = False
        if len(user['name']) < 3:
            flash("Name must be at least 2 characters.", 'name')
            is_valid = False
        if len(user['lastName']) < 3:
            flash("Last name be at least 2 characters.", 'lastName')
            is_valid = False
        if len(user['password']) < 8:
            flash("Password be at least 8 characters.", 'passwordRegister')
            is_valid = False
        if user['confirmpassword'] != user['password']:
            flash("Password do not match!", 'passwordConfirm')
            is_valid = False
        return is_valid