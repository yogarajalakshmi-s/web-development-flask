from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def greet():
    return render_template('index.html')


@app.route('/login', methods=["POST"])
def receive_data():
    if request.method == "POST":
        name = request.form.get('name')
        password = request.form.get('password')
        return render_template("login.html", name=name, password=password)


if __name__ == "__main__":
    app.run(debug=True)

