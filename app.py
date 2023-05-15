from flask import Flask,request

app = Flask(__name__)

stores = [
    {
        "name": "My Store",
        "items": [
            {
                "name": "Chair",
                "price": 15.99
            }
        ]
    }
]

# Get Store
@app.get('/store')
def get_stores():
    return {'stores':stores}

# Add store
@app.post('/store')
def create_store():
    request_data = request.get_json()
    new_store = {
        'name':request_data['name'],
        'items':[]
    }
    stores.append(new_store)
    return new_store, 201

# Add item to the store
@app.post('/store/<string:name>/item')
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name':request_data['name'],
                'price':request_data['price']
            }
            store['items'].append(new_item)
            return new_item, 201
    return {'message':'Store not found'},404

# Get data of a specific store
@app.get('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return store
    return {'message':'Store not found'},404


# Handle 404 error
@app.errorhandler(404)
def page_not_found(e):
    return {'message':'Invalid URL, Page not found'}, 404


if __name__ == '__main__':
    app.run(debug=True)