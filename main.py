from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g
import os, sqlite3
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user
from UserLogin import UserLogin
# config
DATABASE = '/tmp/main.db'
DEBUG = True
SECRET_KEY = '89jf98hvs999>ioc'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'main.db')))
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    print('load user  ', user_id)
    return UserLogin().fromDB(user_id, dbase)


dbase = None
@app.before_request
def before_reqest():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        user = dbase.getUserbyLogin(request.form['login'])
        if user and check_password_hash(user['psw_hash'], request.form['password']):
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            session['userLogged'] = request.form['login']
            return redirect(url_for('personal_cabinet', username=session['userLogged']))
        flash('error login or password', category='bad')
    return render_template('index.html', title='Авторизация')



@app.route('/personal_cabinet/<username>', methods=['POST', 'GET'])
def personal_cabinet(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    if request.method == 'POST':
        if len(request.form['sat_value']) == 2 and str(request.form['sat_value']).isnumeric():
            res = dbase.addValue(sat_value=request.form['sat_value'])
            if not res:
                flash('error', category='bad')
            else:
                flash('alright', category='good')
        else:
            flash('errorr', category='bad')
    return render_template('personal_cabinet.html', title='Личный кабинет', username=username, values=dbase.getValues())


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == "POST":
        if len(request.form['login']) > 2 and len(request.form['psw']) > 4 and request.form['psw'] == request.form[
            'psw2']:
            psw_hash = generate_password_hash(request.form['psw'])
            res = dbase.addUser(request.form['login'], psw_hash, request.form['name'], request.form['subname'],request.form['cognomen'], request.form['age'], request.form['weight'],request.form['height'])
            # TODO редирект в лк пользователя по Id
            if res:
                flash('Succes registration', category='good')
            else:
                flash('DB error', category='bad')
        else:
            flash('Error field', category='bad')

    return render_template('registration.html', title='Регистрация')


@app.errorhandler(404)
def PageNotFound(error):
    return render_template('page404.html', title='Страница не найдена')


if __name__ == '__main__':
    app.run(debug=True)
