from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def greet():
    return render_template('personal_site.html')


if __name__ == "__main__":
    app.run(debug=True)

