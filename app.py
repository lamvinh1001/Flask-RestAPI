from flask import Flask, request, jsonify
import config
import json
import mysql.connector as conn
from functools import wraps
from flask import request

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


def check_auth(username, password):
    return username == config.AUTH_USERNAME and password == config.AUTH_PASSWORD


def login_required(f):
    """ basic auth for api """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return jsonify({'message': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function


@app.route('/auth', methods=['GET'])
@login_required
def secret():
    return f'Logged in as {request.authorization.username}.'


@app.route('/product', methods=['POST'])
@login_required
def add_product():
    try:
        name = request.json['Name']
        description = request.json['Description']
        price = request.json['Price']
        qty = request.json['Quantity']
        if name and description and price and qty and request.method == 'POST':
            db = conn.connect(user=config.MYSQL_USER, password=config.MYSQL_PASSWORD,
                              host=config.MYSQL_HOST, database=config.MYSQL_DATABASE)
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
    finally:
        cursor.close()
        conn.close()

# # Get All Productsow


@app.route('/products', methods=['GET'])
@login_required
def get_products():
    try:
        db = conn.connect(user=config.MYSQL_USER, password=config.MYSQL_PASSWORD,
                          host=config.MYSQL_HOST, database=config.MYSQL_DATABASE)
        cursor = db.cursor(dictionary=True)
        queryString = "SELECT * FROM products"
        cursor.execute(queryString)
        respone = cursor.fetchall()
        return json.dumps(respone)
    except conn.Error as err:
        print(err)
        print("Error Code:", err.errno)
        print("SQLSTATE", err.sqlstate)
        print("Message", err.msg)
    finally:
        cursor.close()
        db.close()

# Get Single Products


@app.route('/product/<int:id>', methods=['GET'])
@login_required
def get_product(id):
    try:
        db = conn.connect(user=config.MYSQL_USER, password=config.MYSQL_PASSWORD,
                          host=config.MYSQL_HOST, database=config.MYSQL_DATABASE)
        cursor = db.cursor(dictionary=True)
        queryString = "SELECT * FROM products WHERE Id =%s"
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
    finally:
        cursor.close()
        db.close()

# # Update a Product


@app.route('/product/<id>', methods=['PUT'])
@login_required
def update_product(id):
    try:
        name = request.json['Name']
        description = request.json['Description']
        price = request.json['Price']
        qty = request.json['Quantity']
        if name and description and price and qty and request.method == 'PUT':
            db = conn.connect(user=config.MYSQL_USER, password=config.MYSQL_PASSWORD,
                              host=config.MYSQL_HOST, database=config.MYSQL_DATABASE)
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
    finally:
        cursor.close()
        db.close()
# Delete Product by Id


@app.route('/product/<id>', methods=['DELETE'])
@login_required
def delete_product(id):
    try:
        db = conn.connect(user=config.MYSQL_USER, password=config.MYSQL_PASSWORD,
                          host=config.MYSQL_HOST, database=config.MYSQL_DATABASE)
        cursor = db.cursor(dictionary=True)
        queryString = "DELETE FROM products WHERE Id =%s"

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
    finally:
        cursor.close()
        db.close()


# Run Server
if __name__ == '__main__':
    app.run(debug=True, threaded=True)
