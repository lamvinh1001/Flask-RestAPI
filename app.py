from flask import Flask, request, jsonify
from connect_database import db
import json
import mysql.connector as conn

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return 'Welcome Product Api'


@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone


@app.route('/product', methods=['POST'])
def add_product():

    try:
        name = request.json['Name']
        description = request.json['Description']
        price = request.json['Price']
        qty = request.json['Quantity']
        if name and description and price and qty and request.method == 'POST':
            cursor = db.cursor(dictionary=True)
            sqlQuery = "INSERT INTO products(Name, Description, Price, Quantity) VALUES(%s, %s, %s, %s)"
            bindData = (name, description, price, qty)
            cursor.execute(sqlQuery, bindData)
            db.commit()
            respone = {
                'statusCode': 200,
                'message': 'Product added successfully!'
            }
            respone = jsonify(respone)
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except conn.Error as err:
        print(err)
        print("Error Code:", err.errno)
        print("SQLSTATE", err.sqlstate)
        print("Message", err.msg)
    # finally:
    #     cursor.close()
    #     conn.close()
# # Get All Productsow


@app.route('/products', methods=['GET'])
def get_products():
    try:
        queryString = "SELECT * FROM products"
        cursor = db.cursor(dictionary=True)
        cursor.execute(queryString)
        respone = cursor.fetchall()
        return json.dumps(respone)
    except conn.Error as err:
        print(err)
        print("Error Code:", err.errno)
        print("SQLSTATE", err.sqlstate)
        print("Message", err.msg)
    # finally:
        # cursor.close()
        # db.close()

# Get Single Products


@app.route('/product/<int:id>')
def get_product(id):
    try:
        queryString = "SELECT * FROM products WHERE Id =%s"
        cursor = db.cursor(dictionary=True)
        cursor.execute(queryString, (id,))
        prodRow = cursor.fetchone()
        respone = jsonify(prodRow)
        respone.status_code = 200
        return respone
    except conn.Error as err:
        print(err)
        print("Error Code:", err.errno)
        print("SQLSTATE", err.sqlstate)
        print("Message", err.msg)

# # Update a Product


@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    try:
        name = request.json['Name']
        description = request.json['Description']
        price = request.json['Price']
        qty = request.json['Quantity']
        if name and description and price and qty and request.method == 'PUT':
            cursor = db.cursor(dictionary=True)
            sqlQuery = "UPDATE products SET Name=%s, Description=%s, Price=%s, Quantity=%s WHERE id=%s"
            bindData = (name, description, price, qty, id,)
            cursor.execute(sqlQuery, bindData)
            db.commit()
            respone = {
                'statusCode': 200,
                'message': f'Product with Id: {id} updated successfully!'
            }
            respone = jsonify(respone)
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except conn.Error as err:
        print(err)
        print("Error Code:", err.errno)
        print("SQLSTATE", err.sqlstate)
        print("Message", err.msg)

# Delete Product by Id


@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    try:
        queryString = "DELETE FROM products WHERE Id =%s"
        cursor = db.cursor(dictionary=True)
        cursor.execute(queryString, (id,))
        db.commit()
        respone = {
            'statusCode': 200,
            'message': f'Product with Id: {id} deleted successfully!'
        }
        respone = jsonify(respone)
        respone.status_code = 200
        return respone
    except conn.Error as err:
        print(err)
        print("Error Code:", err.errno)
        print("SQLSTATE", err.sqlstate)
        print("Message", err.msg)


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
