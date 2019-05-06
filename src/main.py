import os
from flask import Flask
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import flash, render_template, request, session, redirect, url_for

from models import db
from config import DevelopmentConfig, ProductionConfig, StagingConfig, TestingConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.static_url_path = app.config.get('STATIC_FOLDER')
app.static_folder = app.root_path+app.static_url_path

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db.init_app(app)

from models import Users



# @app.route('/', methods=['GET', 'POST'])
# def home():
#     if not session.get('logged_in'):
#         return render_template('login.html')
#     else:
#         return "You're logged in!"

@app.route('/')
@app.route('/index/')
def index():
    return render_template("index.html")


@app.route('/login/', methods=['GET', 'POST'])
def login():
    user = request.form['username']
    user_obj = Users.query.filter_by(login=user).first()
    password = request.form['password']

    if user == '' or password == '':
        flash('Incorrect data!')
    elif user_obj is None:
        flash(f"User {user} is not registered!")
    elif user_obj.password == password:
        flash("You're logged in!")
        login_user(user_obj)
    else:
        flash("Incorrect password!")

    return redirect(url_for('index'))

@app.route('/register/', methods=['POST'])
def register():
    user = request.form['username']
    password = request.form['password']

    if user == '' or password == '':
        flash('Incorrect data!')
    elif Users.query.filter_by(login=user).first():
        flash(f"User {user} is already registered!")
    else:
        db.session.add(user, password)
        db.session.commit()
        flash(f"User {user} was registered!")

    return redirect(url_for('index'))


@app.route('/files/')
@login_required
def files():
    return "files"

@app.route('/files/<file_id>', methods=['GET'])
def file():
    return "file"


@app.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    flash(f"User {current_user.login} was logged out!")
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


if __name__ == '__main__':
    app.run()

