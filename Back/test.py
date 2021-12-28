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

    print('01: list products') #func, input shop id D
    print('02: buy basket') #... H
    print('03: modify products')  #procedure, input pid, input all fields excpet num_sold M
    print('04: get reports')    #... H
    print('05: remove products')    #proc, pid, trigger M
    print('06: add products')   #proc, input fields of products E
    print('07: view shop basket')   #func E
    print('08: charge') #proc, input target uid, amount E
    print('09: view receipts')  #func E
    print('10: view categories')    #func E
    print('11: add categories') #proc, name E
    print('12: remove users')   #proc, target uid, trigger M
    print('13: list shops') #func E
    print('14: add to basket')  #proc, pid, count M
    print('15: clean basket')   #proc, target id E
    # print('15: exit')

    command_id = input()
    run_command(cursor, command_id)


def run_command(cursor, cid):
    if cid == '1':
        # cursor.callproc('list_products')
        # products = cursor.fetchall()
        # print(products)
        #
        cursor.execute("select current_user")
        print(cursor.fetchall())


# init
enter()
