import psycopg2
import json

# Local variables
user_id = -1


# functions
def connect_to_db(username, password):
    global user_id
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="testshop",
            user=username,
            password=password)

        cursor = conn.cursor()

        cursor.execute('select uid from "User" where role = %s', (username,))

        result = cursor.fetchall()
        user_id = result[0][0]

        print(user_id)
        return cursor, conn

    except Exception as e:
        print(e)
        # print('wrong username or password')
        enter()


def enter():
    print('enter username')
    username = input()
    print('enter password')
    password = input()
    cursor, conn = connect_to_db(username, password)
    actions(cursor, conn)


def actions(cursor, conn):
    exit_time = 'n'
    while exit_time == 'n':
        print('01: list products')  # func, input shop id D
        print('02: buy basket')  # ... H
        print('03: modify product')  # procedure, input pid, input all fields except num_sold M
        print('04: get reports')  # ... H
        print('05: remove products')  # proc, pid, trigger M
        print('06: add products')  # proc, input fields of products E
        print('07: view shop basket')  # func E
        print('08: charge')  # proc, input target uid, amount E
        print('09: view receipts')  # func E
        print('10: view categories')  # func E
        print('11: add categories')  # proc, name E
        print('12: remove users')  # proc, target uid, trigger M
        print('13: list shops')  # func E
        print('14: add to basket')  # proc, pid, count M
        print('15: clean basket')  # proc, target id E
        print('16: exit')

        command_id = input()
        run_command(cursor, command_id, conn)
        print('Wanna quit? y/n')
        exit_time = input()
    print('Good Bye')


def list_products(cursor):
    print('Enter shop id:')
    shop_id = input()
    cursor.callproc('list_products', (user_id, int(shop_id)))
    products = cursor.fetchall()
    print(products)


def list_shops(cursor):
    cursor.callproc('list_shops', (user_id,))
    shops = cursor.fetchall()
    print(shops)


def modify_product(cursor, conn):
    print('Enter product id:')
    product_id = input()
    print('Enter new price:')
    new_price = input()
    print('Enter new available numbers:')
    new_av_num = input()
    print('Enter new category:')
    new_cat = input()
    print('Enter new product name:')
    new_product_name = input()
    print('Enter new shop id:')
    new_shop_id = input()
    try:
        cursor.execute("call modify_product(%s,%s,%s,%s,%s,%s)",
                       (int(product_id), int(new_price), int(new_av_num), new_cat, new_product_name, int(new_shop_id)))
        # result = cursor.fetchall()
        conn.commit()
    # print(result)
    except Exception as e:
        print('ERROR: bad input')


def run_command(cursor, cid, conn):
    if cid == '1':
        list_products(cursor)

    elif cid == '3':
        modify_product(cursor, conn)

    elif cid == '6':
        add_product(cursor, conn)

    elif cid == '7':
        view_basket(cursor)

    elif cid == '8':
        charge(cursor, conn)

    elif cid == '9':
        view_receipts(cursor)

    elif cid == '10':
        view_categories(cursor)

    elif cid == '11':
        add_category(cursor, conn)

    elif cid == '13':
        list_shops(cursor)

    elif cid == '14':
        add_to_basket(cursor, conn)

    elif cid == '15':
        clean_basket(cursor, conn)

# current_user_id int, product_id int, new_price int, new_num_avail int,new_num_sold int, new_category varchar,
# new_pname varchar, new_shop_id int
def add_product(cursor, conn):
    print('Enter product id:')
    product_id = input()
    print('Enter new price:')
    new_price = input()
    print('Enter new available numbers:')
    new_av_num = input()
    print('Enter new category:')
    new_cat = input()
    print('Enter new product name:')
    new_product_name = input()
    print('Enter new shop id:')
    new_shop_id = input()
    try:
        cursor.execute("call add_product(%s,%s,%s,%s,%s,%s,%s,%s)",
                       (int(user_id), int(product_id), int(new_price), int(new_av_num), 0, new_cat, new_product_name,
                        int(new_shop_id)))

        conn.commit()
    except Exception as e:
        print('ERROR: bad input')


def charge(cursor, conn):
    print('Enter target id:')
    target_id = input()
    print('Enter charge amount:')
    amount = input()
    try:
        cursor.execute("call charge(%s,%s,%s)",
                       (int(user_id), int(target_id), int(amount)))

        conn.commit()
    except Exception as e:
        print('ERROR: bad input')


def add_category(cursor, conn):
    print("Enter category's name:")
    cat_name = input()

    try:
        cursor.execute("call add_category(%s,%s)",
                       (int(user_id), cat_name))

        conn.commit()
    except Exception as e:
        print('ERROR: bad input')


def add_to_basket(cursor, conn):
    print("Enter basket id:")
    basket_id = input()
    print("Enter product id:")
    product_id = input()
    print("Enter count:")
    count = input()
    try:
        cursor.execute("call add_to_basket(%s,%s, %s, %s)",
                       (int(basket_id), int(user_id), int(product_id), int(count)))

        conn.commit()
    except Exception as e:
        print('ERROR: bad input')


def clean_basket(cursor, conn):
    print("Enter target id:")
    target_id = input()

    try:
        cursor.execute("call clean_basket(%s, %s)",
                       (int(user_id), int(target_id)))

        conn.commit()
    except Exception as e:
        print('ERROR: bad input')


def view_categories(cursor):
    cursor.callproc('view_categories', (user_id,))
    categories = cursor.fetchall()
    print(categories)


def view_basket(cursor):
    print('Enter target id')
    target_id = input()
    cursor.callproc('view_basket', (user_id, target_id,))
    baskets = cursor.fetchall()
    print(baskets)


def view_receipts(cursor):
    cursor.callproc('view_reciepts', (user_id,))
    receipts = cursor.fetchall()
    print(receipts)


# init
enter()
