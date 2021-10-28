from flask import Blueprint
from flask import  render_template, url_for, request, flash, redirect, g, session


admin = Blueprint('admin', __name__, static_folder='static', template_folder='templates')

def login_admin():
    session['admin_logged'] = 1

def isLogged():
    return  True if session.get('admin_logged') else False

def logout_admin():
    session.pop('admin_logged', None)

@admin.route('/')
def index():
    if not isLogged():
        return redirect(url_for('.login'))
    return render_template('admin/index.html', title= 'Admin-index')

@admin.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form['user'] == 'admin' and request.form['psw'] == '12345':
            login_admin()
            return redirect(url_for('.index'))
        else:
            flash('incorrect password or login')

    return render_template('admin/login.html', title= 'Admin-panel')

@admin.route('/logout', methods=['POST', 'GET'])
def logout():
    if not isLogged():
        return redirect(url_for('.login'))
    logout_admin()
    return redirect(url_for('.login'))