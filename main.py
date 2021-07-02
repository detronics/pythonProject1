from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g
import os, sqlite3
from FDataBase import FDataBase

# config
DATABASE = '/tmp/main.db'
DEBUG = True
SECRET_KEY = '89jf98hvs999>ioc'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'main.db')))


#
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


#
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
    if 'userLogged' in session:
        return redirect(url_for('personal_cabinet', username=session['userLogged']))
    elif request.method == "POST" and request.form['username'] == 'kip' and request.form['password'] == '123':
        session['userLogged'] = request.form['username']
        return redirect(url_for('personal_cabinet', username=session['userLogged']))
    return render_template('index.html', title='Авторизация')


@app.route('/personal_cabinet/<username>', methods=['POST', 'GET'])
def personal_cabinet(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    db = get_db()
    dbase = FDataBase(db)
    if request.method == 'POST':
        if len(request.form['sat_value']) == 2 and str(request.form['sat_value']).isnumeric():
            res = dbase.addValue(sat_value=request.form['sat_value'])
            if not res :
                flash('error', category='bad')
            else:
                flash('alright', category='good')
        else:
            flash('errorr', category='bad')
    return render_template('personal_cabinet.html', title='Личный кабинет', username=username, values = dbase.getValues())


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == "POST":
        if len(request.form['name']) > 2:
            flash('Succes', category='good')
        else:
            flash('Error', category='bad')

    return render_template('registration.html', title='Регистрация')


@app.errorhandler(404)
def PageNotFound(error):
    return render_template('page404.html', title='Страница не найдена')


if __name__ == '__main__':
    app.run(debug=True)
