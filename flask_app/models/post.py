from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user, comment

class Post:
    db = 'dojo_wall_schema'
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
        self.comments = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO posts (content, user_id) VALUES (%(content)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def all_posts(cls):
        query = """SELECT * FROM posts 
                LEFT JOIN users ON users.id = posts.user_id 
                LEFT JOIN comments ON comments.post_id = posts.id 
                LEFT JOIN users AS commers ON commers.id = comments.user_id
                ORDER BY posts.created_at DESC;"""
        results = connectToMySQL(cls.db).query_db(query)
        # print(results)
        posts = []
        for row in results:
            if not posts or posts[-1].id != row['id']:
                new_post = cls(row)
                posts.append(new_post)
                user_data = {
                    'id': row['users.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': row['password'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at'],
                }
                new_post.user = user.User(user_data)
            
            if row['comments.id']:
                commer_data = {
                    'id': row['commers.id'],
                    'first_name': row['commers.first_name'],
                    'last_name': row['commers.last_name'],
                    'email': row['commers.email'],
                    'password': row['commers.password'],
                    'created_at': row['commers.created_at'],
                    'updated_at': row['commers.updated_at']
                }
                
                comment_data = {
                    'id': row['comments.id'],
                    'content': row['comments.content'],                    
                    'user_id': row['comments.user_id'],
                    'post_id': row['post_id'],
                    'created_at': row['comments.created_at'],
                    'updated_at': row['comments.updated_at']
                }
                a_comment = comment.Comment(comment_data)
                a_comment.user = user.User(commer_data)
                new_post.comments.append(a_comment)
        print(posts[0].comments[0].user.first_name)
        return posts
    
    @classmethod
    def delete_post(cls, data):
        query = "DELETE FROM posts WHERE id = %(id)s;"
        delete_data = {
            'id': data['post_id']
        }
        return connectToMySQL(cls.db).query_db(query, delete_data)
    
    @staticmethod
    def validate_post(post):
        is_valid = True
        if len(post['post_content']) < 1:
            flash("Post cannot be blank")
            is_valid = False
        return is_valid