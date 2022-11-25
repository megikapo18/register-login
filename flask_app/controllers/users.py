from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.thought import Thought

from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/loginPage')
def loginPage():
    if 'user_id' in session:
        return redirect('/')
    return render_template('login.html')


@app.route('/create_user', methods=['POST'])
def createUser():
    if not User.validate_user(request.form):
        return redirect(request.referrer)
    
    if User.get_user_by_email(request.form):
        flash('This email already exists!', 'emailSignUp')
        return redirect(request.referrer)

    data = {
        'email': request.form['email'],
        'name': request.form['name'],
        'lastName': request.form['lastName'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    User.create_user(data)
    return redirect('/')




@app.route('/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    if len(request.form['email'])<1:
        flash('Email is required to login', 'emailLogin')
        return redirect(request.referrer)

    if not User.get_user_by_email(data):
        flash('This email doesnt exist ', 'emailLogin')

        return redirect(request.referrer)

    user = User.get_user_by_email(data)

    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash("Invalid Password", 'passwordLogin')
        return redirect(request.referrer)
        
    session['user_id'] = user['id']
    return redirect('/')



@app.route('/')
def dashboard():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
            
        }
        user = User.get_user_by_id(data)

        all_thought= Thought.get_All_thoughts()
        print(all_thought)
        user_Liked_Thought = User.get_logged_user_liked_thoughts(data)

        return render_template('dashboard.html', loginUser= user, allThoughts = all_thought , userLikedThought= user_Liked_Thought)
    return redirect('/logout')


@app.route('/profile/<int:id>')
def profile(id):
    if 'user_id' in session:
        data = {
            'user_id': id,
        }
        dataLogged = {
            'user_id': session['user_id']
        }
        user = User.get_user_by_id(dataLogged)
        thoughts = User.get_all_user_info(data)
        return render_template('userThought.html', thoughts= thoughts, user= user)
    return redirect('/logout')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/loginPage')