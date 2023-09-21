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
    
    bakeries = []
    for bakery in Bakery.query.all():
        bakery_dict = {
            "created_at": bakery.created_at,
             "id": bakery.id,
             "name": bakery.name,
             "updated_at": bakery.updated_at
        }
        bakeries.append(bakery_dict)

    response = make_response(
        bakeries, 200
    )

    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakeries=[]
    bakery = Bakery.query.filter(Bakery.id == id).first()

    bakery_dict = {
            "created_at": bakery.created_at,
             "id": bakery.id,
             "name": bakery.name,
             "updated_at": bakery.updated_at
          }
    
    bakeries.append(bakery_dict)

    response = make_response(
        bakeries, 200
    )

    return response

@app.route('/baked_goods')
def baked_goods():
    
    baked_goods = []
    for baked_good in BakedGood.query.all():
        baked_good_dict = {
             "bakery_id": baked_good.bakery_id,
             "created_at": baked_good.created_at,
             "id": baked_good.id,
             "name": baked_good.name,
             "price": baked_good.price,
             "updated_at": baked_good.updated_at
        }
        baked_goods.append(baked_good_dict)

    response = make_response(
        baked_goods, 200
    )

    return response


@app.route('/baked_goods/by_price/<float:price>')
def baked_goods_by_price(price):
    baked_goods = BakedGood.query.filter(BakedGood.price == price).all()

    
    baked_goods_list = []
    for baked_good in baked_goods:
        baked_good_dict = {
            "bakery": {
                "created_at": baked_good.bakery.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "id": baked_good.bakery.id,
                "name": baked_good.bakery.name,
                "updated_at": baked_good.bakery.updated_at.strftime('%Y-%m-%d %H:%M:%S') if baked_good.bakery.updated_at else None
            },
            "bakery_id": baked_good.bakery_id,
            "created_at": baked_good.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "id": baked_good.id,
            "name": baked_good.name,
            "price": baked_good.price,
            "updated_at": baked_good.updated_at.strftime('%Y-%m-%d %H:%M:%S') if baked_good.updated_at else None
        }
        baked_goods_list.append(baked_good_dict)

    return jsonify(baked_goods_list)


@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()

    if baked_good is None:
        # Return a 404 Not Found response if no baked goods are found
        return jsonify({"error": "No baked goods found"}), 404

    bakery = {
        "created_at": baked_good.bakery.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        "id": baked_good.bakery.id,
        "name": baked_good.bakery.name,
        "updated_at": baked_good.bakery.updated_at.strftime('%Y-%m-%d %H:%M:%S') if baked_good.bakery.updated_at else None
    }

    baked_good_dict = {
        "bakery": bakery,
        "bakery_id": baked_good.bakery_id,
        "created_at": baked_good.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        "id": baked_good.id,
        "name": baked_good.name,
        "price": baked_good.price,
        "updated_at": baked_good.updated_at.strftime('%Y-%m-%d %H:%M:%S') if baked_good.updated_at else None
    }

    return jsonify(baked_good_dict)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
