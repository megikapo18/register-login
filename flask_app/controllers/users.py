from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def loginPage():
    if 'user_id' in session:
        return redirect('/')
    return render_template('login.html')

@app.route('/create_user', methods=['POST'])
def createUser():

    if not User.validate_user(request.form):
        return redirect(request.referrer)
    
    if User.get_user_by_email(request.form):
        flash('This email is exist! ', 'emailSignUp')
        return redirect(request.referrer)

    data = {
        'email': request.form['email'],
        'name': request.form['name'],
        'lastName': request.form['lastName'],
        'password': bcrypt.generate_password_hash (request.form['password'])
    }

    User.create_user(data)
    return redirect('/profilePage')


@app.route('/profilePage')
def profilePage():
    return render_template('profilePage.html')



@app.route('/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    if len(request.form['email'])<1:
        flash('Email is required to login', 'emailLogin')
        return redirect(request.referrer)
        
    if not User.get_user_by_email(data):
        flash('This email does not exist', 'emailLogin')
        return redirect(request.referrer)

    user = User.get_user_by_email(data)

    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        # if we get False after checking the password
        flash("Invalid Password", 'passwordLogin')
        return redirect(request.referrer)
        
    session['user_id'] = user['id']
    return redirect('/profilePage')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')