from model import connector
from werkzeug.security import generate_password_hash, check_password_hash

PAG = 5  #кількість елементів при пагінації


def take_user_id(c, login):
    """
    user_id за заданим логіном

    :return: user_id
    """
    
    sql_text = """SELECT user_id FROM users WHERE login = %s"""
    c.execute(sql_text, (login,))
    user_id = c.fetchall()[0][0]

    return user_id


def take_user_pass(c, login):
    """
    password за заданим логіном

    :return: user password
    """
    
    sql_text = """SELECT password FROM users WHERE login = %s"""
    c.execute(sql_text, (login,))
    pwd = c.fetchall()[0][0]

    return pwd

def take_currency(c, currency):
    """
    currency_id за найменуванням

    :return: user password
    """
    sql_text = """SELECT currency_id FROM currency WHERE currency_name = %s"""
    c.execute(sql_text, (currency,))

    return  c.fetchall()[0][0]

def take_product_id(c, sku, login):
    """
    product_id за sku та користувачем

    :return: user password
    """
    
    user_id = take_user_id(c, login)

    sql_text = """SELECT product_id FROM products WHERE sku = %s AND user_id = %s"""
    c.execute(sql_text, (sku,user_id))

    return  c.fetchall()[0][0]


@connector
def authenticate(conn, login, password):
    """
    Перевірка введеного пароля із справжнім паролем

    :return: True or None (if error)
    """
    
    c = conn.cursor()  
    pwd = take_user_pass(c, login)

    return check_password_hash(pwd, password)


@connector
def insert_user(conn, login, password):
    """
    Створення нового юзера

    :return: True or None (if error)
    """

    sql_text = """INSERT INTO users (login, password) VALUES (%s, %s)"""

    c = conn.cursor()  
    c.execute(sql_text, (login, generate_password_hash(password)))

    return True


@connector
def update_user(conn, login, name, photo):
    """
    Редагування даних юзера (імя, фото)

    :return: True or None (if error)
    """

    if name != None:
        sql_text = """UPDATE users SET user_name = %s WHERE login = %s"""

        c = conn.cursor()  
        c.execute(sql_text, (name, login))
    
    if photo != None:
        sql_text = """UPDATE users SET user_photo = %s WHERE login = %s"""

        c = conn.cursor()  
        c.execute(sql_text, (name, photo))

    return True


@connector
def insert_product(conn, login, sku, product_name):
    """
    Створення нового товару

    :return: True or None (if error)
    """

    c = conn.cursor()  
    user_id = take_user_id(c, login)

    sql_text = """INSERT INTO products (sku, product_name, user_id) VALUES (%s, %s, %s)"""
    c.execute(sql_text, (sku, product_name, user_id))

    return True


@connector
def products(conn, login, sku, product_name, type_sort, page):
    """
    Вибірака даних за заданими параметрами

    :return: кортеж із вибраними товарами or None (if error)
    """
    
    c = conn.cursor()
    user_id = take_user_id(c, login)
    params = [user_id,]

    sql_text = """SELECT product_id, product_name FROM products WHERE user_id = %s """
    
    #відбір по артикулу чи назві
    if sku != None:
        sql_text += "AND sku  = %s"
        params.append(sku)
    elif product_name != None:
        sql_text += "AND product_name  LIKE %%s%"
        params.append(product_name)
    
    #сортування по заданому параметру
    if type_sort in ('sku', 'product_name'):
         sql_text += f" ORDER BY {type_sort}"
    
    #пагінація
    if page == None:
        sql_text += f" LIMIT {PAG}"
    else: 
        sql_text += f" LIMIT {int(PAG * int(page))} , {PAG}"

    c = conn.cursor()  
    c.execute(sql_text, params)

    return c.fetchall()


@connector
def insert_currency(conn, currency):
    """
    Створення нової валюти

    :return: True or None (if error)
    """

    sql_text = """INSERT INTO currency (currency_name) VALUES ( %s)"""

    c = conn.cursor()  
    c.execute(sql_text, (currency, ))

    return True


@connector
def insert_price(conn, login, sku, currency, price):
    """
    Створення нової ціни на товар

    :return: True or None (if error)
    """
    
    c = conn.cursor() 

    currency_id = take_currency(c, currency)
    product_id = take_product_id(c, sku, login)

    sql_text = """INSERT INTO prices (product_id, currency_id, price) VALUES (%s, %s, %s)"""
    c.execute(sql_text, (product_id, currency_id, float(price)))

    return True

