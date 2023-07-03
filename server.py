from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

# Line below only required once, when creating DB.
# db.create_all()


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # return User.get(int(user_id))
    return db.session.query(User).filter_by(id=int(user_id)).first()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        user = db.session.query(User).filter_by(email=email).first()
        if user:
            flash("You've already signed up with this email. Please login!")
            return redirect(url_for('login'))
        else:
            new_user = User(email=email, password=generate_password_hash(password, method='pbkdf2:sha256', salt_length=8), name=name)
            db.session.add(new_user)
            db.session.commit()
            # Log in and authenticate user after adding details to database.
            login_user(new_user)
            return render_template('secrets.html', username=name)

    print(current_user.is_authenticated)
    return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        # print(email, password)

        # Find user by email entered.
        user = db.session.query(User).filter_by(email=email).first()

        if not user:
            flash("Email ID doesn't exist. Please sign-up!")
            return redirect(url_for('login'))
        else:
            # Check stored password hash against entered password hashed.
            # print(user.password)
            if check_password_hash(user.password, password):
                # print("Hello")
                login_user(user)
                return render_template('secrets.html', username=user.name)
            else:
                flash("Password is incorrect. Please try again!")
                return redirect(url_for('login'))

    print(current_user.is_authenticated)
    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    # print(current_user.name)
    return render_template("secrets.html", username=current_user.name)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download')
@login_required
def download():
    return send_from_directory('static/files', 'cheat_sheet.pdf')


if __name__ == "__main__":
    app.run(debug=True)
