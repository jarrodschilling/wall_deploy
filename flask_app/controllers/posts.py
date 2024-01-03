from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.post import Post
from datetime import datetime


@app.route('/wall')
def wall():
    if 'user_id' not in session:
        return redirect('/')
    posts = Post.all_posts()
    print(posts[0].created_at.strftime('%b %d'))
    return render_template('wall.html', posts=posts)

@app.route('/post', methods=['POST'])
def new_post():
    if not Post.validate_post(request.form):
        return redirect('/wall')
    data = {
        'content': request.form['post_content'],
        'user_id': session['user_id']
    }
    a_post = Post.save(data)
    return redirect('/wall')

@app.route('/post/delete', methods=['POST'])
def delete_post():
    delete = Post.delete_post(request.form)
    return redirect('/wall')