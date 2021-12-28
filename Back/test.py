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

        cursor.execute('select uid from "User" where role = %s', (username, ))

        result = cursor.fetchall()
        user_id = result[0][0]

        print(user_id)
        return cursor

    except Exception as e:
        print(e)
        # print('wrong username or password')
        enter()


def enter():
    print('enter username')
    username = input()
    print('enter password')
    password = input()
    cursor = connect_to_db(username, password)
    actions(cursor)


def actions(cursor):
    command_id = 0
    while command_id != '16':
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
        print('16: exit')

        command_id = input()
        run_command(cursor, command_id)

    print('Good Bye')

def run_command(cursor, cid):
    if cid == '1':
        cursor.callproc('list_products')
        products = cursor.fetchall()
        print(products)



# init
enter()
