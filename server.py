from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Connecting to DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


def create_json_template(cafe):
    return {"id": cafe.id,
            "name": cafe.name,
            "location": cafe.location,
            "coffee_price": cafe.coffee_price,
            "seats": cafe.seats,
            "has_wifi": cafe.has_wifi,
            "has_sockets": cafe.has_sockets,
            "has_toilet": cafe.has_toilet,
            "can_take_calls": cafe.can_take_calls,
            "map_url": cafe.map_url,
            "img_url": cafe.img_url
            }


@app.route('/')
def home():
    return "Hello"


@app.route('/all-cafes')
def all_cafes():
    cafes = []
    all_cafes = db.session.query(Cafe).all()
    for cafe in all_cafes:
        print(cafe)
        cafes.append(create_json_template(cafe))
    print(cafes)
    return jsonify(cafes=cafes)


if __name__ == '__main__':
    app.run(debug=True)

