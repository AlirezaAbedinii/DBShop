import psycopg2


# functions
def connect_to_db(username, password):
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="OnlineShop",
            user=username,
            password=password)
    except:
        print('wrong username or password')


def enter():
    print('enter username')
    username = input()
    print('enter password')
    password = input()
    connect_to_db(username, password)


def actions():
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
    run_command(command_id)


def run_command(cid):
    if cid == '1':
        print('1')


# init
enter()
