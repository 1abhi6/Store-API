import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from schemas import StoreSchema

blp = Blueprint("Stores", __name__, description="Operaations on stores")


@blp.route('/store')
class StoreList(MethodView):
    # Create store
    @blp.arguments(StoreSchema)
    def post(self, store_data):
        for store in stores.values():
            if store_data['name'] == store['name']:
                abort(
                    400,
                    message='Store already exists.'
                )
        store_id = uuid.uuid4().hex
        store = {
            **store_data,
            'id': store_id
        }
        stores[store_id] = store
        return store, 201

    # Get all stores
    def get(self):
        return {
            'stores': list(stores.values())
        }


@blp.route('/store/<string:store_id>')
class Store(MethodView):
    # Get a store
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message='Store not found.')

    # Delete a store
    def delete(self, store_id):
        try:
            del stores[store_id]
            return {
                'message': 'Store deleted.'
            }
        except:
            abort(404, message='Store not found.')
