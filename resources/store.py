import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from models import StoreModel
from schemas import StoreSchema

blp = Blueprint("Stores", __name__, description="Operaations on stores")


@blp.route('/store')
class StoreList(MethodView):
    # Create store
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the store.")

        return store, 201

    # Get all stores
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()


@blp.route('/store/<string:store_id>')
class Store(MethodView):
    # Get a store
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    # Delete a store
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        raise NotImplementedError("Deleting a store is not implemented.")
