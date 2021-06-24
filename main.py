from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/personal_cabinet')
def personal_cabinet():
    return render_template('personal_cabinet.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')


if __name__ == '__main__':
    app.run(debug=True)