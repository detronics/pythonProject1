from flask import Flask, render_template, url_for, request, flash,  redirect, abort, g, make_response
import os, sqlite3
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from UserLogin import UserLogin
from oksy import Recognizer
from forms import LoginForm, RegistrationForm
from admin.admin import admin

# config
DATABASE = '/tmp/main.db'
DEBUG = True
SECRET_KEY = '89jf98hvs999>ioc'

app = Flask(__name__)
app.config.from_object(__name__)

app.register_blueprint(admin, url_prefix = '/admin')
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'main.db')))
login_manager = LoginManager(app)
login_manager.login_view = 'index'
login_manager.loogin_message = ' you need to authorize'


@login_manager.user_loader
def load_user(user_id):
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
    if current_user.is_authenticated:
        return redirect(url_for('personal_cabinet', ))
    form = LoginForm()
    if form.validate_on_submit():
        user = dbase.getUserbyLogin(form.login.data)
        if user and check_password_hash(user['psw_hash'], form.password.data):
            userlogin = UserLogin().create(user)
            rm = form.remember_me.data
            login_user(userlogin, remember=rm)
            return redirect(url_for('personal_cabinet', ))
        flash('Неверные логин или пароль', category='bad')
    return render_template('index.html', title='Авторизация', form=form)


@app.route('/personal_cabinet/', methods=['POST', 'GET'])
@login_required
def personal_cabinet():
    if request.method == 'POST':
        if len(request.form['sat_value']) == 2 and str(request.form['sat_value']).isnumeric():
            res = dbase.addValue(sat_value=request.form['sat_value'], user_id=current_user.get_id())
            # user_log = current_user.get_login()
            if not res:
                flash('Ошибка записи данных', category='bad')
            else:
                flash('Данные успешно добавлены', category='good')
        else:
            flash('Неверный формат данных', category='bad')
    return render_template('personal_cabinet.html', title='Личный кабинет',
                           values=dbase.getValues(user_id=current_user.get_id()), sat_value='')


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        psw_hash = generate_password_hash(form.psw1.data)
        res = dbase.addUser(form.login.data, psw_hash, form.name.data, form.subname.data,form.cognomen.data,
                            form.age.data, form.weight.data, form.height.data)
        if res:
            flash('Вы успешно зарегистрированы', category='good')
            user = dbase.getUserbyLogin(request.form['login'])
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for('personal_cabinet', ))
        else:
            flash('Ошибка записи в базу данных', category='bad')

    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта', category='good')
    return redirect(url_for('index'))


@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    if request.method == "POST":
        file = request.files['file']
        if file and current_user.verifyExt(file.filename):
            try:
                foto = Recognizer(file=file.filename)
                value = foto.recognize()
            except FileNotFoundError as e:
                flash(message='Ошибка чтения файла', category='bad')
        else:
            flash(message='Ошибка добавления данных', category='bad')
    return render_template('personal_cabinet.html', title='Личный кабинет',
                           values=dbase.getValues(user_id=current_user.get_id()), sat_value=value)


@app.route('/userava', methods=['POST', 'GET'])
@login_required
def userava():
    img = current_user.getAvatar(app)
    if not img:
        return ''
    h = make_response(img)
    h.headers["Content-type"] = 'image/jpg'
    return h


@app.route('/updateava', methods=['POST', 'GET'])
@login_required
def updateava():
    if request.method == "POST":
        file = request.files['file']
        if file and current_user.verifyExt(file.filename):
            try:
                img = file.read()
                res = dbase.updateUserAvatar(img, current_user.get_id())
                if not res:
                    flash(message='Ошибка обновления аватара', category='bad')
                flash(message='Аватар обновлен', category='good')
            except FileNotFoundError as e:
                flash(message='Ошибка чтения файла', category='bad')
        else:
            flash(message='Ошибка обновления аватара', category='bad')
    return redirect(url_for('personal_cabinet'))

@app.errorhandler(404)
def PageNotFound(error):
    return render_template('page404.html', title='Страница не найдена')


if __name__ == '__main__':
    app.run(debug=True)
