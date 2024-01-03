from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.comment import Comment


@app.route('/comment', methods=['POST'])
def new_comment():
    data = {
        'content': request.form['comment_content'],
        'user_id': session['user_id'],
        'post_id': request.form['comment_post_id']
    }
    a_comment = Comment.save(data)
    return redirect('/wall')