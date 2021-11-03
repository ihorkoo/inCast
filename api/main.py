import db_func

from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()


@auth.verify_password
def authenticate(login, password):
    """
    Превірка паролю при authenticate
    """

    if login and password:
        res = db_func.authenticate(login, password)
        if res:
            return True
        # TO-DO: ? 
    return False


@app.route('/create_user', methods=['POST'])
def create_user():
    """
    Створення нового юзера
    """

    login = request.args.get('login')
    password = request.args.get('password')
    result = db_func.insert_user(login, password)
    if result:
        return jsonify({'message' :  'User created!'})
    return jsonify({'message' :  'Error'})


@app.route('/edit_user', methods=['POST'])
@auth.login_required
def edit_user():
    """
    Редагування профіля користувача
    """

    login = auth.current_user()
    name = request.args.get('name')
    photo = request.args.get('photo')
    result = db_func.update_user(login, name, photo)
    if result:
        return jsonify({'message' :  'User updated!'})
    return jsonify({'message' :  'Error'})


@app.route('/add_product', methods=['POST'])
@auth.login_required
def add_product():
    """
    Створення нового товару
    """

    login = auth.current_user()
    sku = request.args.get('sku')
    product_name = request.args.get('product_name')
    result = db_func.insert_product(login, sku, product_name)
    if result:
        return jsonify({'message' :  'Product created!'})
    return jsonify({'message' :  'Error'})


@app.route('/add_currency', methods=['POST'])
@auth.login_required
def add_currency():
    """
    Створення валюти
    """

    currency = request.args.get('currency')
    result = db_func.insert_currency(currency)
    if result:
        return jsonify({'message' :  'Currency added!'})
    return jsonify({'message' :  'Error'})


@app.route('/add_price', methods=['POST'])
@auth.login_required
def add_price():
    """
    Створення ціни для товару
    """

    login = auth.current_user()
    sku = request.args.get('sku')
    currency = request.args.get('currency')
    price = request.args.get('price')
    result = db_func.insert_price(login, sku, currency, price)
    if result:
        return jsonify({'message' :  'Price created!'})
    return jsonify({'message' :  'Error'})


@app.route('/products_list', methods=['GET'])
@auth.login_required
def products_list():
    """
    Список товарів за задиними параметрами
    """
    login = auth.current_user()
    sku = request.args.get('sku')
    product_name = request.args.get('product_name')
    type_sort = request.args.get('type_sort')
    page = request.args.get('page')

    result = db_func.products(login, sku, product_name, type_sort, page)
    if result != None:
        return jsonify(
            {
                'message' :  'Success',
                'result' : result
                }
            )
    
    return jsonify({'message' :  'Error'})


if __name__ == '__main__':
    app.run()