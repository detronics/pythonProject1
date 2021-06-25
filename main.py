from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title='Авторизация')

@app.route('/personal_cabinet')
def personal_cabinet():
    return render_template('personal_cabinet.html', title='Личный кабинет')

@app.route('/registration', methods= ['POST', 'GET'])
def registration():
    return render_template('registration.html', title='Регистрация')


if __name__ == '__main__':
    app.run(debug=True)