from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from flask_bootstrap import Bootstrap

EMAIL = "admin@email.com"
PASSWORD = "12345678"

class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[validators.DataRequired(), validators.Email(message="Invalid Email Address")])
    password = PasswordField(label='Password', validators=[validators.DataRequired(), validators.Length(min=8, message="Password should contain atleast 8 characters")])
    submit = SubmitField(label="Sign In")


app = Flask(__name__)
app.secret_key = "The answer to life is 42"  # We need secret key to use CSRF token
Bootstrap(app)

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login_page():
    login_form = LoginForm()
    email = login_form.email.data
    password = login_form.password.data
    if login_form.validate_on_submit():
        if email == EMAIL and password == PASSWORD:
            return render_template('success.html')
        else:
            return render_template('denied.html')
    return render_template('login.html', form=login_form)


if __name__ == '__main__':
    app.run(debug=True)
