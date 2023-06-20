from flask import Flask
import random

app = Flask(__name__)
number_to_be_guessed = random.randint(0, 10)
print(number_to_be_guessed)


def guess_decorator(function):
    def wrapper(number):
        return f"<h2 style='color:red'>{function(number)}</h2>"
    return wrapper


@app.route('/')
def invite_page():
    return '<h1 style="text-align:center">Welcome to number guessing game! Guess numbers between 0 and 9</h1>' \
           '<img src="https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif">'


@app.route('/<int:number>')
@guess_decorator
def play(number):
    if number < number_to_be_guessed:
        return "Too low! Guess again!<img style='width:300px' " \
               "src='https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif'>"
    elif number > number_to_be_guessed:
        return "Too High! Guess again!<img style='width:300px'" \
               " src='https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif'>"
    else:
        return "<h2 style='color:green'>You guessed it right!</h2>" \
               "<img style='width:300px' src='https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif'>"


if __name__ == "__main__":
    app.run(debug=True)
