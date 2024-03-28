"""
===============================================
Name: server.py
Assignment: Lab 10, Exercise A, B, C
Author(s): Zachary Lam, Trevor Nguyen
Submission: March 27, 2024
Description: Flask.
===============================================
"""

import json
import os

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes
# CORS(app, origins=["http://example.com", "http://localhost:3000"])

def load_products():
    with open('products.json', 'r') as f:
        return json.load(f) ['products']
    
@app.route('/products', methods=['GET'])
@app.route('/products/<int:product_id>', methods=['GET'])
def get_products(product_id=None):
    products = load_products()
    if product_id is None:
        # Return all products wrapped in an object with a 'products' key
        return jsonify({"products": products})
    else:
        product = next((p for p in products if p['id'] == product_id), None)
        # If a specific product is requested,
        # wrap it in an object with a 'products' key
        # Note: You might want to change this
        # if you want to return a single product not wrapped in a list
        return jsonify(product) if product else ('', 404)
    
@app.route('/products/add', methods=['POST'])
def add_product():
    new_product = request.json
    products = load_products()
    new_product['id'] = len(products) + 1
    products.append(new_product)
    with open('products.json', 'w') as f:
        json.dump({"products": products}, f)
    return jsonify(new_product), 201

@app.route('/product-images/<path:filename>')
def get_image(filename):
    return send_from_directory('product-images', filename)

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    products = load_products()
    product_index = next((i for i, p in enumerate(products) if p['id'] == product_id), None)
    if product_index is not None:
        products[product_index] = request.json
        products[product_index]['id'] = product_id
        with open('products.json', 'w') as f:
            json.dump({"products": products}, f)
        return jsonify(products[product_index])
    else:
        return jsonify({"error": "Product not found"}), 404

@app.route('/products/<int:product_id>', methods=['DELETE'])
def remove_product(product_id):
    products = load_products()
    product_index = next((i for i, p in enumerate(products) if p['id'] == product_id), None)
    if product_index is not None:
        deleted_product = products.pop(product_index)
        with open('products.json', 'w') as f:
            json.dump({"products": products}, f)
        return jsonify(deleted_product)
    else:
        return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)