from flask import Flask, render_template
import requests


app = Flask(__name__)


@app.route('/')
def greet():
    return 'Hello! Go to /guess and play the guess game'


@app.route('/guess')
def guess_greet():
    return 'Add any name to the current url'


@app.route('/guess/<path:name>')
def guess(name):
    gender = guess_gender(name)
    age = guess_age(name)
    return render_template('index.html', name=name.capitalize(), gender=gender, age=age)


def guess_gender(name):
    parameters = {
        "name": name
    }
    response = requests.get(url="https://api.genderize.io", params=parameters)
    return response.json()['gender']


def guess_age(name):
    parameters = {
        "name": name
    }
    response = requests.get(url="https://api.agify.io", params=parameters)
    return response.json()['age']


if __name__ == "__main__":
    app.run(debug=True)  # Debug mode on
