import MySQLdb
import sshtunnel
import json

with open('setting.json') as f:
    SETTINGS = json.load(f)


sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0


def create_connection(tunnel):
    """
    Конект до бази даних через ssh

    return: обєкт conn
    """

    conn  = None
    try:
        conn = MySQLdb.connect(
                user=SETTINGS['user'],
                passwd=SETTINGS['passwd'],
                host=SETTINGS['host'], port=tunnel.local_bind_port,
                db=SETTINGS['db'],
            )
        return conn
    except Exception as e:
        print(e)
        return conn


def connector(funck):
    def wrapper(*args, **kvargs):
        with sshtunnel.SSHTunnelForwarder(
            ("ssh.pythonanywhere.com"),
            ssh_username=SETTINGS['ssh_username'], ssh_password=SETTINGS['ssh_password'],
            remote_bind_address= ("ihorko.mysql.pythonanywhere-services.com", 3306)
            ) as tunnel:

            conn = create_connection(tunnel)
            result = None
            if conn == None:
                return result
            else:
                try:
                    result = funck(conn, *args, **kvargs)
                    return result
                except Exception as e:
                    print(e)
                else:
                    conn.commit()
                finally:
                    conn.commit()
                    conn.close()
                return result
    return wrapper


@connector
def users(conn):
    """Створення таблиці із користувачами"""

    sql_text = """CREATE TABLE IF NOT EXISTS users (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    login VARCHAR(50) NOT NULL,
                    password VARCHAR(50) NOT NULL,
                    user_name  VARCHAR(50) NULL,
                    user_photo BLOB NULL,

                    UNIQUE KEY (login)
                  )                  
    """
    c = conn.cursor()  
    c.execute(sql_text)


@connector
def product(conn):
    """Створення таблиці із товарами"""

    sql_text = """CREATE TABLE IF NOT EXISTS products (
                    product_id INT AUTO_INCREMENT PRIMARY KEY,
                    sku VARCHAR(50) NOT NULL,
                    product_name  VARCHAR(50) NULL,
                    product_photo BLOB NULL, 
                    user_id INT NOT NULL,
                    
                    FOREIGN KEY (user_id)  REFERENCES users (user_id),
                    
                    UNIQUE KEY (sku, user_id)  
                  )                
    """

    c = conn.cursor()  
    c.execute(sql_text)


@connector
def currency(conn):
    """Створення таблиці із валютами"""
    
    sql_text = """CREATE TABLE IF NOT EXISTS currency (
                    currency_id INT AUTO_INCREMENT PRIMARY KEY,
                    currency_name  VARCHAR(50) NOT NULL
                  )                
    """

    c = conn.cursor()  
    c.execute(sql_text)


@connector
def prices(conn):
    """Створення таблиці із цінами"""
    
    sql_text = """CREATE TABLE IF NOT EXISTS prices (
                    price_id INT AUTO_INCREMENT PRIMARY KEY,
                   
                   
                    FOREIGN KEY (currency_id)  REFERENCES currency (currency_id),
                    FOREIGN KEY (product_id)  REFERENCES products (product_id),
                    UNIQUE KEY (product_id, currency_id)  
                  )                
    """

    c = conn.cursor()  
    c.execute(sql_text)


def create_all_tables():
    users()
    product()
    currency()
    prices()
    

if __name__ == '__main__':
    create_all_tables()

