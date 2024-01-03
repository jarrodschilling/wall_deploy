from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    data = {
    "email": request.form.get('email')
    }
    user_in_db = User.get_user(data)

    if not user_in_db:
        flash('Invalid Email/Password', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form.get('password')):
        flash('Invalid Email/Password', 'login')
        return redirect('/')
    
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name

    return redirect('/wall')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/register', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form.get('password'))
    print(pw_hash)
    data = {
        "first_name": request.form.get('first_name'),
        "last_name": request.form.get('last_name'),
        "email": request.form.get('email'),
        "password": pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    session['first_name'] = data['first_name']
    print(user_id)
    return redirect('/wall')