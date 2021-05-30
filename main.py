from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:MIS385450oy0983892109@localhost/iot_test_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class HockeyGoods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False)
    price = db.Column(db.Float, unique=False)
    weight_in_grams = db.Column(db.Integer, unique=False)
    brand = db.Column(db.String(50), unique=False)
    color = db.Column(db.String(50), unique=False)

    def __init__(self, name, price, weight_in_grams, brand, color):
        self.name = name
        self.price = price
        self.weight_in_grams = weight_in_grams
        self.brand = brand
        self.color = color


class HockeyGoodsSchema(ma.Schema):
    class Meta:
        fields = ('name', 'price', 'weight_in_grams', 'brand', 'color')
    name = fields.String()
    price = fields.Float()
    weight_in_grams = fields.Integer()
    brand = fields.String()
    color = fields.String()


hockeygoods_schema = HockeyGoodsSchema()
hockeygoodss_schema = HockeyGoodsSchema(many=True)


@app.route('/')
def welcome_page():
    return 'Welcome to hockey goods store!'


@app.route('/hockeygoods', methods=['POST'])
def add_hockeygoods():
    name = request.json['name']
    price = request.json['price']
    weight_in_grams = request.json['weight_in_grams']
    brand = request.json['brand']
    color = request.json['color']
    new_hockeygoods = HockeyGoods(name, price, weight_in_grams, brand, color)

    db.session.add(new_hockeygoods)
    db.session.commit()

    return hockeygoods_schema.jsonify(new_hockeygoods)


@app.route('/hockeygoods', methods=['GET'])
def get_hockeygoods():
    all_hockeygoods = HockeyGoods.query.all()
    result = hockeygoodss_schema.dump(all_hockeygoods)
    return jsonify({'hockeygoods': result})


@app.route("/hockeygoods/<id>", methods=["GET"])
def hockeygoods_detail(id):
    hockeygoods = HockeyGoods.query.get(id)
    if not hockeygoods:
        abort(404)
    return hockeygoods_schema.jsonify(hockeygoods)


@app.route("/hockeygoods/<id>", methods=["PUT"])
def hockeygoods_update(id):
    hockeygoods = HockeyGoods.query.get(id)

    hockeygoods.name = request.json['name']
    hockeygoods.price = request.json['price']
    hockeygoods.weight_in_grams = request.json['weight_in_grams']
    hockeygoods.brand = request.json['brand']
    hockeygoods.color = request.json['color']

    db.session.commit()
    return hockeygoods_schema.jsonify(hockeygoods)


@app.route("/hockeygoods/<id>", methods=["DELETE"])
def hockeygoods_delete(id):
    hockeygoods = HockeyGoods.query.get(id)
    if not hockeygoods:
        abort(404)
    db.session.delete(hockeygoods)
    db.session.commit()

    return hockeygoods_schema.jsonify(hockeygoods)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
