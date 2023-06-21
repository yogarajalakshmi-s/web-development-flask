from flask import Flask, render_template

app = Flask(__name__)


# Rendering HTML elements through decorators
def make_bold(function):
    def wrapper_function():
        return f"<b>{function()}</b>"
    return wrapper_function


@app.route('/')  # Decorator to print Hello World! only when it's in home page
def hello_world():
    # Adding HTML elements
    return '<h1 style="text-align: center">Hello World!</h1>' \
           '<p>A paragraph</p>' \
           '<img src="https://media.istockphoto.com/id/1035676256/photo/background-of-galaxy-and-stars.jpg?s=612x612&w=0&k=20&c=dh7eWJ6ovqnQZ9QwQQlq2wxqmAR7mgRlQTgaIylgBwc=">'


@app.route('/rendering_html')
def render_html():
    return render_template('index.html')  # Note that html files should be templates folder

@app.route('/bye')
@make_bold
def bye():
    return 'Bye!'


# Creating variable paths and converting paths to a specified datatype
@app.route('/username/<name>/<int:number>')  # Variable rules - URL <name> will be rendered in the page
def greet(name, number):
    return f"Hello {name}! You're {number} years old."


if __name__ == "__main__":
    app.run(debug=True)  # Debug mode on