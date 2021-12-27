import psycopg2
import json

# functions
def connect_to_db(username, password):
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="testshop",
            user=username,
            password=password)

        cursor = conn.cursor()
        return cursor

    except:
        print('wrong username or password')


def enter():
    print('enter username')
    username = input()
    print('enter password')
    password = input()
    cursor = connect_to_db(username, password)
    actions(cursor)


def actions(cursor):
    print('01: list products')
    print('02: buy products')
    print('03: modify products')
    print('04: get reports')
    print('05: remove products')
    print('06: add products')
    print('07: view shop basket')
    print('08: charge')
    print('09: view receipts')
    print('10: view categories')
    print('11: modify categories')
    print('12: add categories')
    print('13: remove users')
    print('14: exit')

    command_id = input()
    run_command(cursor, command_id)


def run_command(cursor, cid):
    if cid == '1':
        cursor.callproc('list_products')
        products = cursor.fetchall()
        print(products)


# init
enter()
