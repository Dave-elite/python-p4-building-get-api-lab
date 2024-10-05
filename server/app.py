#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakers = Bakery.query.all()
    bakers_list = [baker.to_dict() for baker in bakers]
    return jsonify(bakers_list)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    bakery_dict = bakery.to_dict()
    #create a return response
    response = make_response(
        jsonify(bakery_dict),
        200
    )
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    #convert the baked good to a dictionary
    baked_goods_list = [baked_good.to_dict() for baked_good in baked_goods]
    
    return jsonify(baked_goods_list), 200
   

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    # Get the most expensive baked good
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    
    # Check if a baked good was found
    if baked_good is None:
        return make_response(jsonify({"error": "No baked goods found"}), 404)

    # Convert the baked good to a dictionary
    baked_good_dict = baked_good.to_dict()
    
    return jsonify(baked_good_dict), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
