from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.thought import Thought
from flask_app.models.user import User
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/createthought', methods=['POST'])
def createthought():

    if not Thought.validate_thought(request.form):
        return redirect(request.referrer)
    data = {
        'content': request.form['content'],
        'user_id': session['user_id']
    }
    Thought.create_thought(data)
    return redirect('/')


@app.route('/like/<int:id>')
def addLike(id):
    data = {
        'thought_id': id,
        'user_id': session['user_id']
    }
    Thought.add_Like(data)
    return redirect(request.referrer)

@app.route('/unlike/<int:id>')
def removeLike(id):
    data = {
        'thought_id': id,
        'user_id': session['user_id']
    }
    Thought.remove_Like(data)
    return redirect(request.referrer)

@app.route('/delete/<int:id>')
def destroyTHOUGHT(id):
    data = {
        'thought_id': id
    }
    thought = Thought.get_thought_by_id(data)
    if session['user_id']== thought['user_id']:
        Thought.delete_All_Likes(data)
        Thought.destroy_thought(data)
        return redirect(request.referrer)
    return redirect(request.referrer)