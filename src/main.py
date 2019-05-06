import datetime
import io

from flask import Flask, flash, render_template
from flask import request, redirect, url_for, jsonify, send_file
from flask_login import LoginManager, login_user
from flask_login import logout_user, login_required, current_user

from models import db
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.static_url_path = app.config.get('STATIC_FOLDER')
app.static_folder = app.root_path+app.static_url_path

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'

db.init_app(app)

from models import Users, File


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
        db.session.add(Users(user, password))
        db.session.commit()
        flash(f"User {user} was registered!")

    return redirect(url_for('index'))


@app.route('/upload/', methods=['POST'])
def upload():
    file = request.files['file']

    try:
        days = float(request.form['days'])
    except ValueError:
        days = 0
    try:
        hrs = float(request.form['hours'])
    except ValueError:
        hrs = 0

    if file.filename == '' or (days == 0 and hrs == 0):
        flash("Incorrect file data!")
    else:
        expire_at = datetime.datetime.now()
        expire_at += datetime.timedelta(days=days, hours=hrs)
        expire_at = expire_at.replace(microsecond=0)

        new_file = File(
            file.filename,
            file.read(),
            expire_at,
            None if current_user.is_anonymous else current_user.id)

        db.session.add(new_file)
        db.session.commit()
        flash(f"File {file.filename} will be stored until {expire_at}!\n"
              f"The file can be accessed at "
              f"{url_for('file', file_id=new_file.id, _external=True)}!")

    return jsonify(message="OK")


def files_list_prepare(objs_list):
    files_list = []

    for file in objs_list:
        time_remained = file.expire_at - datetime.datetime.now()
        time_remained = str(time_remained).split('.', 2)[0]

        files_list.append(
            {
                'file_id': file.id,
                'filename': file.filename,
                'expire_at': file.expire_at.strftime("%m/%d/%Y, %H:%M:%S"),
                'time_remained': time_remained,
                'file_ref': url_for(
                    'download',
                    file_id=file.id,
                    _external=True),
            }
        )
    return files_list


@app.route('/files/')
@login_required
def files():
    user_files = File.query.filter_by(owner_id=current_user.id).all()
    files_list = files_list_prepare(user_files)

    return render_template('files.html', files_list=files_list)


@app.route('/file/', methods=['GET'])
def file():
    file_id = int(request.args.get('file_id'))
    file_obj = File.query.filter_by(id=file_id).all()
    files_list = files_list_prepare(file_obj)

    return render_template('files.html', files_list=files_list)


@app.route('/download/<int:file_id>/', methods=['GET'])
def download(file_id):
    file = File.query.filter_by(id=file_id).first()

    return send_file(
        io.BytesIO(file.content),
        attachment_filename=file.filename,
        as_attachment=True
    )


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
