from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Thought:

    db_name='skematest'
    def __init__(self,data):
        self.id=data['id'],
        self.content=data['content'],
        self.user_id=data['user_id'],
        self.created_at=data['created_at'],
        self.update_at=data['update_at']


    @classmethod
    def get_All_thoughts(cls):
        query= 'SELECT thoughts.id, content, COUNT(likes.user_id) as likesNr, users.id as creator_id, email, name, lastname FROM thoughts LEFT JOIN users on thoughts.user_id = users.id LEFT JOIN likes on likes.thought_id = thoughts.id GROUP BY thoughts.id;'
        results =  connectToMySQL(cls.db_name).query_db(query)
        thoughts= []
        for row in results:
            thoughts.append(row)
        return thoughts
        


    @classmethod
    def create_thought(cls,data):
        query = 'INSERT INTO thoughts (content, user_id) VALUES ( %(content)s, %(user_id)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_thought_by_id(cls, data):
        query= 'SELECT * FROM thoughts WHERE thoughts.id = %(thought_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results[0]

    @classmethod
    def get_user_thought(cls, data):
        query= 'SELECT * FROM users LEFT JOIN thoughts on thoughts.user_id = users.id WHERE users.id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        thoughts = []
        for row in results:
            thoughts.append(row)
        return thoughts

    @classmethod
    def add_Like(cls, data):
        query= 'INSERT INTO likes (thought_id, user_id) VALUES ( %(thought_id)s, %(user_id)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def remove_Like(cls, data):
        query= 'DELETE FROM likes WHERE thought_id=%(thought_id)s and user_id=%(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def destroy_thought(cls, data):
        query= 'DELETE FROM thoughts WHERE thoughts.id=%(thought_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
        
    @classmethod
    def delete_All_Likes(cls, data):
        query= 'DELETE FROM likes WHERE likes.thought_id =%(thought_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_thought(thought):
        is_valid = True
        if len(thought['content']) < 2:
            flash("Thought content must be at least 2 characters.", 'content')
            is_valid = False
        return is_valid