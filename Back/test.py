import psycopg2
import json
from tabulate import tabulate

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

        # user_id = username[-1]
        # print(user_id)
        # exit(2)
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


def get_user_id(role):
    role_to_id = {'userp1': 'userp111', 'userp2': 'userp222',
                  'userp3': 'userp333', 'userp4': 'userp444', 'userp5': 'userp555'}
    return role_to_id[role]


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
        print('16: modify user')
        print('17: modify category')

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
        print(e)


def run_command(cursor, cid, conn):
    if cid == '1':
        list_products(cursor)

    elif cid == '2':
        shop(cursor, conn)

    elif cid == '3':
        modify_product(cursor, conn)

    elif cid == '4':
        get_reports(cursor)

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

    elif cid == '12':
        remove_user(cursor, conn)

    elif cid == '13':
        list_shops(cursor)

    elif cid == '14':
        add_to_basket(cursor, conn)

    elif cid == '15':
        clean_basket(cursor, conn)

    elif cid == '16':
        edit_lastname(cursor, conn)

    elif cid == '17':
        modify_category(cursor, conn)


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
        print(e)


def add_category(cursor, conn):
    print("Enter category's name:")
    cat_name = input()

    try:
        cursor.execute("call add_category(%s,%s)",
                       (int(user_id), cat_name))

        conn.commit()
    except Exception as e:
        print(e)


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
        print(e)


def clean_basket(cursor, conn):
    print("Enter target id:")
    target_id = input()

    try:
        cursor.execute("call clean_basket(%s, %s)",
                       (int(user_id), int(target_id)))

        conn.commit()
    except Exception as e:
        print(e)


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


def remove_user(cursor, conn):
    print('Enter target id')
    tid = input()

    try:
        cursor.execute("call remove_user(%s, %s)",
                       (int(user_id), int(tid)))

        conn.commit()
    except Exception as e:
        print(e)


def edit_lastname(cursor, conn):
    print('Enter target id')
    tid = input()
    print('Enter new last name')
    new_lname = input()
    try:
        cursor.execute("call edit_lname(%s, %s, %s)",
                       (int(user_id), int(tid), new_lname))

        conn.commit()
    except Exception as e:
        print(e)


def modify_category(cursor, conn):
    print('Enter old name')
    old = input()
    print('Enter new name')
    new = input()
    try:
        cursor.execute("call edit_category(%s, %s, %s)",
                       (int(user_id), old, new))

        conn.commit()
    except Exception as e:
        print(e)


def shop(cursor, conn):
    try:
        cursor.execute("call shop(%s)",
                       (int(user_id)))

        conn.commit()
    except Exception as e:
        print(e)


def get_reports(cursor):
    print('1: Daily, monthly, and yearly sells')
    print('2: Shop and Category overview')
    print("3: Products' popularity in their shops")
    print("4: Products and their categories' average prices")
    print("5: Best customers")
    print("6: Customers' favourite categories")
    cmnd = input()
    if cmnd == '1':
        date_related_report(cursor)
    elif cmnd == '2':
        shop_and_category_overview_report(cursor)
    elif cmnd == '3':
        products_popularity_report(cursor)
    elif cmnd == '4':
        products_and_categories_average_prices_report(cursor)
    elif cmnd == '5':
        best_customers_report(cursor)
    elif cmnd == '6':
        customers_favourite_categories_report(cursor)


def date_related_report(cursor):
    cursor.execute('''
    select case 
	when yyear is null then 'All years'
	else yyear
	end,
	case 
	when mmonth is null then 'All months'
	else mmonth
	end,
	case 
	when dday is null then 'All days'
	else dday
	end,
	total_sell
from (select extract(year from date)::varchar as yyear,
	extract(month from date)::varchar as mmonth,
	extract(day from date)::varchar as dday,
	sum(total_price) as total_sell
	
	from "Reciept"
	group by cube(yyear, mmonth, dday)
	 ) as foo
order by yyear, mmonth, dday;
    ''')
    result = cursor.fetchall()
    print(tabulate(result, headers=[desc[0] for desc in cursor.description], tablefmt='orgtbl'))


def shop_and_category_overview_report(cursor):
    cursor.execute('''
    SELECT
case grouping(sname)
when 0 then sname
when 1 then 'All shops'
end as sname,
case grouping(category)
when 0 then category
when 1 then 'All categories'
end as category,
SUM (num_sold) as sold
FROM "Product" left join "Shop" on shop_id = sid
GROUP BY CUBE(sname, category)
ORDER BY sname, category;
    ''')
    result = cursor.fetchall()
    print(tabulate(result, headers=[desc[0] for desc in cursor.description], tablefmt='orgtbl'))


def products_popularity_report(cursor):
    cursor.execute('''
    SELECT pname, sname, price, num_sold,
ROW_NUMBER () OVER (
PARTITION BY shop_id
ORDER BY num_sold desc) as sold_rank
FROM "Product" LEFT JOIN "Shop" on shop_id = sid;
''')
    result = cursor.fetchall()
    print(tabulate(result, headers=[desc[0] for desc in cursor.description], tablefmt='orgtbl'))


def products_and_categories_average_prices_report(cursor):
    cursor.execute('''SELECT pname, price, category,
AVG (price) OVER (
PARTITION BY category
)
FROM "Product";''')
    result = cursor.fetchall()
    print(tabulate(result, headers=[desc[0] for desc in cursor.description], tablefmt='orgtbl'))


def best_customers_report(cursor):
    cursor.execute('''select fname, lname, bought
from (select costumer_id as cid, sum(total_price) as bought
from "Reciept"
group by costumer_id
having sum(total_price)>0) as foo inner join "User" on cid = uid;''')
    result = cursor.fetchall()
    print(tabulate(result, headers=[desc[0] for desc in cursor.description], tablefmt='orgtbl'))


def customers_favourite_categories_report(cursor):
    cursor.execute('''select fname, lname, category as favourite_category
from  (select distinct on (cid) cid, category
from (select costumer_id as cid, category as category, sum(purchase_num) as bought
from "Reciept" as r inner join "Product" as p on r.pid = p.pid
group by costumer_id, category) as foo
order by cid, bought desc) foo2 left join "User" on cid = uid;''')
    result = cursor.fetchall()
    print(tabulate(result, headers=[desc[0] for desc in cursor.description], tablefmt='orgtbl'))


# init
enter()
