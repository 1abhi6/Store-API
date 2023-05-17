# TODO Connect this application with database
import uuid
from flask import Flask, request
from db import stores, items

app = Flask(__name__)


# Get all stores
@app.get('/store')
def get_stores():
    return {
        'stores': list(stores.values())
    }


# Add store
@app.post('/store')
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    store = {
        **store_data,
        'id': store_id
    }
    stores[store_id] = store
    return store, 201

# Get data of a specific store with store_id


@app.get('/store/<string:store_id>')
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        return {
            'message': 'Store not found'
        }, 404


# Get all items
@app.get('/item')
def get_all_items():
    return {
        'items': list(items.values())
    }


# Add item to the store
@app.post('/item')
def create_item():
    item_data = request.get_json()
    if item_data['store_id'] not in stores:
        return {
            'message': 'Store not found'
        }, 404

    item_id = uuid.uuid4().hex
    item = {**item_data, 'id': item_id}
    items[item_id] = item

    return item, 201


# Get item with item_id
@app.get('/item/<string:item_id>')
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        return {
            'message': 'Item not found'
        }, 404


# Handle 404 error
@app.errorhandler(404)
def page_not_found(e):
    return {
        'message': 'Invalid URL, Page not found'
    }, 404


if __name__ == '__main__':
    app.run(debug=True)
