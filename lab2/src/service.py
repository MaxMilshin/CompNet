from flask import Flask, send_file, request, jsonify
import requests
import io
import uuid

from products import products

app = Flask(__name__)

# Get all products
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)


# Get product by ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((product for product in products if product["id"] == product_id), None)
    if product:
        return jsonify(product)
    else:
        return jsonify({"message": "Product not found"}), 404


# Get product image by ID
@app.route('/products/<int:product_id>/image', methods=['GET'])
def get_product_image(product_id):
    product = next((product for product in products if product["id"] == product_id), None)
    if product:
        image_response = requests.get(product['icon'])
        image_data = image_response.content
        return send_file(
                io.BytesIO(image_data),
                mimetype=image_response.headers.get('content-type')
            )
    else:
        return jsonify({"message": "Product not found"}), 404

# Add new product
@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    product_id = max(products, key=lambda x:x['id'])['id'] + 1
    new_product = {"id": product_id, "name": data["name"], "description": data["description"], "icon": data["icon"]}
    products.append(new_product)
    return jsonify(new_product), 201

# Update product info
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = next((product for product in products if product["id"] == product_id), None)
    if product:
        data = request.get_json()
        product.update(data)
        return jsonify(product)
    else:
        return jsonify({"message": "Product not found"}), 404

# Delete product by ID
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = next((product for product in products if product["id"] == product_id), None)
    if product:
        products.remove(product)
        return jsonify({"message": "Product deleted"})
    else:
        return jsonify({"message": "Product not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
