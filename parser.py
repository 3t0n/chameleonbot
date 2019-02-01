import postgresql
import config

connection_string = config.CONNECTION_STRING

def get_test():
    with postgresql.open(connection_string) as db:
        test = 'успешно'
        query = 'SELECT 1'
        try:
            result = db.query(query)
        except:
            print('Error: get_test()')
            test = 'отсутствует'

        message = 'Подключение к базе данных {}'.format(test)
        print(message)

        return message

def get_checks():
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
        except:
            print('Error: get_checks()')

        if not checks.strip():
            checks = 'Нет товаров'

        message = 'Товары за сегодня:\n{}'.format(checks)
        print(message)

        return message

def get_sales():
    with postgresql.open(connection_string) as db:
        query = '''
        SELECT 
            sum(sum_check/100) 
        FROM sales.checks 
        WHERE type_payment in (1,2) AND time_check > current_date'''

        try:
            result = db.query(query)
            sales = int(result[0][0])
        except:
            sales = 0

        message = 'Выручка за сегодня: {} грн'.format(sales)
        print(message)

        return message
