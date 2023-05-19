import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import ItemModel
from schemas import ItemUpdateSchema, ItemSchema


blp = Blueprint("Items", __name__, description='Operations on items')


@blp.route('/item')
class ItemList(MethodView):
    # Add item
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except:
            abort(500, message="An error occurred while inserting the item.")

        return item, 201

    # Get all items
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()


@blp.route('/item/<string:item_id>')
class Item(MethodView):
    # Get an item
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    # Update an item with item_id
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get_or_404(item_id)
        raise NotImplementedError("Updating an item is not implemented.")

    # Delete an item with item_id
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        raise NotImplementedError("Deleting an item is not implemented.")
