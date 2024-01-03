from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user, post

class Comment:
    db = 'dojo_wall_schema'
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.user_id = data['user_id']
        self.post_id = data['post_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None


    @classmethod
    def save(cls, data):
        query = """INSERT INTO comments (content, user_id, post_id) 
                VALUES (%(content)s, %(user_id)s, %(post_id)s);"""
        return connectToMySQL(cls.db).query_db(query, data)