from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
secret_api_key = "test1234"

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Cafe TABLE Configuration
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


# db.create_all()


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
            "img_url": cafe.img_url}


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route('/random')
def get_cafe():
    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes)
    return jsonify(cafe=create_json_template(random_cafe))


@app.route('/all')
def all():
    cafes = []
    all_cafes = db.session.query(Cafe).all()
    print(all_cafes)
    for cafe in all_cafes:
        cafes.append(create_json_template(cafe))
    return jsonify(cafes=cafes)


@app.route('/search')
def search():
    location = request.args.get("loc")
    cafes_by_location = db.session.query(Cafe).filter_by(location=location)
    cafes_by_location_search = []
    for cafe in cafes_by_location:
        cafes_by_location_search.append(create_json_template(cafe))
    if cafes_by_location_search:
        return jsonify(cafe_by_location=cafes_by_location_search), 200
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404


# HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def post_new_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        seats=request.form.get("seats"),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        has_sockets=bool(request.form.get("sockets")),
        can_take_calls=bool(request.form.get("calls")),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."}), 200


# HTTP PUT/PATCH - Update Record
@app.route('/update-price/<int:cafe_id>', methods=["PATCH"])
def update_price(cafe_id):
    cafe = db.session.query(Cafe).filter_by(id=cafe_id).first()
    print(cafe)
    updated_price = request.args.get("update_price")
    if cafe:
        cafe.coffee_price = updated_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price"})
    else:
        return jsonify(error={"Not Found": "Enter a valid id"}), 404


# HTTP DELETE - Delete Record
@app.route('/cafe-closed/<int:cafe_id>', methods=["DELETE"])
def closed_cafe(cafe_id):
    secret_key = request.args.get('secret_key')
    if secret_key == secret_api_key:
        cafe = db.session.query(Cafe).filter_by(id=cafe_id).first()
        db.session.delete(cafe)
        return jsonify(response={"success": f"Deleted the cafe with id {cafe_id}"})
    else:
        return jsonify(error={"Not Authorised": "You are not authorised"}), 403


if __name__ == '__main__':
    app.run(debug=True)
