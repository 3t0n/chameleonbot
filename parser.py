import postgresql
import config

from apscheduler.schedulers.background import BackgroundScheduler

connection_string = config.CONNECTION_STRING
white_list = config.IDS

def test():
    with postgresql.open(connection_string) as db:
        test = 'успешно'
        query = 'SELECT 1'
        try:
            result = db.query(query)
        except Exception as e:
            print('test(): {}'.format(e))
            test = 'отсутствует'

        message = 'Подключение к базе данных {}'.format(test)
        print(message)

        return message


def checks():
    with postgresql.open(connection_string) as db:
        checks = ''
        query = '''
        SELECT  
            goods.name_goods,
            SUM(quantity) as sum_quantity, 
            unit.name_unit, 
            SUM(summ/100) as sum_summ_and_discount,
            (SELECT symbol_currency from front.currencies LIMIT 1)  
        FROM sales.check_lines t 
        LEFT OUTER JOIN 
            front.goods goods ON (t.id_goods=goods.id_goods) 
        LEFT OUTER JOIN 
            front.unit unit ON (t.id_unit=unit.id_unit  AND t.id_goods=unit.id_goods)     
        LEFT OUTER JOIN 
            sales.checks che ON (t.id_check=che.id_check) 
        LEFT OUTER JOIN 
            front.workplace ON (t.id_workplace=front.workplace.id_workplace) 
        WHERE che.time_check > current_date 
        GROUP BY   
            t.id_goods, 
            t.id_unit, 
            goods.name_goods,
            unit.name_unit'''

        try:
            result = db.query(query)

            for line in result:
                for element in line:
                    checks += ' ' + str(element)
                checks += '\n'
        except Exception as e:
            print('checks(): {}'.format(e))

        if not checks.strip():
            checks = 'Нет товаров'

        message = 'Товары за сегодня:\n{}'.format(checks)
        print(message)

        return message


def sales():
    with postgresql.open(connection_string) as db:
        query = '''
        SELECT 
            sum(sum_check/100) 
        FROM sales.checks 
        WHERE type_payment in (1,2) AND time_check > current_date'''

        try:
            result = db.query(query)
            sales = int(result[0][0])
        except Exception as e:
            print('sales(): {}'.format(e))
            sales = 0

        message = 'Выручка за сегодня: {} грн'.format(sales)
        print(message)

        return message


def average():
    with postgresql.open(connection_string) as db:
        query = '''
        SELECT 
            avg(sum_check/100)::numeric(10,2) 
        FROM sales.checks 
        WHERE type_payment in (1,2) AND time_check > current_date'''

        try:
            result = db.query(query)
            average = int(result[0][0])
        except Exception as e:
            print('average(): {}'.format(e))
            average = 0

        message = 'Средний чек за сегодня: {} грн'.format(average)
        print(message)

        return message


def find(name):
    with postgresql.open(connection_string) as db:
        find = ''
        query = '''
        SELECT
            id_goods, 
            name_goods,
            (SELECT (price_new/100.0)::numeric(12,2) FROM spring.doc_reprice_table where id_goods = goods.id_goods 
                ORDER BY date_doc DESC LIMIT 1) as price, 
            'грн за 1',
            (SELECT name_unit FROM front.unit WHERE is_default = true AND id_goods = goods.id_goods) as unit
        FROM front.goods
        WHERE name_goods ILIKE '%{}%' 
        ORDER BY id_goods
        LIMIT 10'''.format(name)

        print(query)

        try:
            result = db.query(query)

            for line in result:
                for element in line:
                    find += ' ' + str(element)
                find += '\n'
        except Exception as e:
            print('find(): {}'.format(e))

        if not find.strip():
            find = 'Нет товаров'

        message = 'Найдено первых 10 товаров:\n{}'.format(find)
        print(message)

        return message


def security(user_id):
    result = True
    if white_list.count(user_id) == 0:
        print("User {} unregistered".format(user_id))
        result = False

    return result
