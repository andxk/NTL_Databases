import psycopg2

db_name = 'clients'
db_user = 'postgres'
db_pass = 'admin'

##------------------------------------------------------------------------------


def create_db ():
    conn = psycopg2.connect(database = db_name, user = db_user, password = db_pass)
    with conn.cursor() as cur:
        # удаление таблиц
        cur.execute("""
            DROP TABLE IF EXISTS phone ;
            DROP TABLE IF EXISTS client;
        """)

        # создание таблиц
        cur.execute("""
            CREATE TABLE IF NOT EXISTS client (
                id SERIAL PRIMARY KEY,
                fname VARCHAR(20) NOT NULL,
                lname VARCHAR(30) NOT NULL ,
                email VARCHAR(50) UNIQUE NOT NULL
            );


            CREATE TABLE IF NOT EXISTS phone (
                num VARCHAR(20) PRIMARY KEY,
                client_id SERIAL REFERENCES client(id)
            );
        """)
        conn.commit()
    conn.close()




def add_client (first_name, last_name, email, phones=[]) -> int:
    ''' Return client_id '''

    with psycopg2.connect(database = db_name, user = db_user, password = db_pass) as conn:
        with conn.cursor() as cur:

            cur.execute("""
                INSERT INTO client (fname, lname, email)
                VALUES (%s, %s, %s)
                RETURNING id;
            """, (first_name, last_name, email));

            id = cur.fetchone()[0]

            if len(phones) > 0:
                for num in phones:
                    cur.execute("""
                        INSERT INTO phone
                        VALUES (%s, %s);
                    """, (num, id));

    conn.close()
    return id




def add_phone (client_id, phone):
    try:
        with psycopg2.connect(database = db_name, user = db_user, password = db_pass) as conn:
            if _get_client_by_phone(conn, phone):
                return False
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO phone
                    VALUES (%s, %s);
                """, (phone, client_id));
            return True
    except:
        return False
    finally:
        conn.close()




def del_phone (client_id, phone) -> bool:
    try:
        with psycopg2.connect(database = db_name, user = db_user, password = db_pass) as conn:
            with conn.cursor() as cur:
                if _get_client_by_phone(conn, phone) != client_id:
                    return False

                cur.execute("""
                    DELETE FROM phone WHERE num = %s;
                """, (phone,));
                return True
    except:
        return False
    finally:
        conn.close()




def client_exists (client_id) -> bool:
    '''Return True when client_id exists'''
    with psycopg2.connect(database = db_name, user = db_user, password = db_pass) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT count(*) FROM client WHERE id=%s;
            """, (client_id,));
            count = cur.fetchone()[0]
            return bool(count)
    conn.close()




def change_client (client_id, first_name=None, last_name=None, email=None, phone=None) -> bool:
    '''Return true when client changed'''

    if not client_exists(client_id):
        return False

    try:
        with psycopg2.connect(database = db_name, user = db_user, password = db_pass) as conn:
            with conn.cursor() as cur:
                result = False

                if first_name or last_name or email:
                    query = "UPDATE client "
                    if first_name:
                        query += f"SET fname = '{first_name}' "
                    if last_name:
                        query += f"SET lname = '{last_name}' "
                    if email:
                        query += f"SET email = '{email}' "
                    query += f"WHERE id={client_id};"
                    cur.execute(query)
                    result = True

                if phone:
                    result = add_phone(client_id, phone)
    finally:
        conn.close()
        return result




def _get_client_by_phone (conn, phone) -> int:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT client_id FROM phone WHERE num = %s;
        """, (str(phone),));

        id = cur.fetchone()
        if id:
            return id[0]
        else:
            return None




def _get_client_by_email (conn, email) -> int:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id FROM client WHERE email = %s;
        """, (email,));

        id = cur.fetchone()
        if id:
            return id[0]
        else:
            return None




def _get_list_client_by_name (conn, first_name = None, last_name = None):
    with conn.cursor() as cur:
        try:
            if first_name and last_name:
                cur.execute("""
                    SELECT id FROM client WHERE fname = %s and lname = %s;
                """, (first_name, last_name))
            elif last_name:
                cur.execute("""
                    SELECT id FROM client WHERE lname = %s;
                """, (last_name,))
            elif first_name:
                cur.execute("""
                    SELECT id FROM client WHERE fname = %s;
                """, (first_name,))
            else:
                return []
        except:
            return []

        result = cur.fetchall()
        result = [x[0] for x in result]

        return result




def find_client (first_name=None, last_name=None, email=None, phone=None, strict=True) -> int:
    '''
    Поиск client_id по заданным параметрам
    Если strict==False, результат будет при любом совпадении: email, phone или (фамилия+имя)
    Если strict==True (по-умолчанию), результат будет при совпадении всех переданнных данных
    Входные данные могут быть в любом сочетании, должен быть хотя бы один параметр клиента
    '''
    try:
        with psycopg2.connect(database = db_name, user = db_user, password = db_pass) as conn:
            ide = None
            idp = None
            idn = []

            if email:
                ide = _get_client_by_email(conn, email)
            if phone:
                idp = _get_client_by_phone(conn, phone)
            if first_name or last_name:
                idn = _get_list_client_by_name(conn, first_name, last_name)

            if not strict: # любое совпадение email, phone или names
                if ide:
                    return ide
                elif idp:
                    return idp
                elif idn:
                    return idn[0]
##                    return idn
                else:
                    return None

            else: # strict -> все заданные параметры должны совпасть
                if email and phone:
                    if ide == idp:
                        id = ide
                    else:
                        return None # не совпало
                elif email:
                    id = ide
                elif phone:
                    id = idp
                elif first_name or last_name:
                    return idn[0]
                else:
                    return None

                # Проверка вхождения в список, найденный по именам и фамилиям
                if id in idn  or  idn==[]:
                    return id
                else:
                    return None

    except:
        return None
    finally:
        conn.close()




def find_client_phones (client_id) -> list:
    try:
        with psycopg2.connect(database = db_name, user = db_user, password = db_pass) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT num FROM phone WHERE client_id = %s;
                """, (client_id,));
                result = cur.fetchall()
                return [x[0] for x in result]
    except:
        return []
    finally:
        conn.close()




def print_client (client_id):
    '''Вывод информации о клиенте'''
    if not client_exists(client_id):
        print(f'\nКлиент id={client_id} не существует')
        return

    try:
        print('\n Данные клиента:')
        with psycopg2.connect(database = db_name, user = db_user, password = db_pass) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT fname, lname, email FROM client WHERE id = %s;
                """, (client_id,));
                data = cur.fetchall()[0]
                print(f'id:      {client_id}')
                print(f'Имя:     {data[0]}')
                print(f'Фамилия: {data[1]}')
                print(f'e-mail:  {data[2]}')

    except:
        print('Сбой базы данных')
        return
    finally:
        conn.close()

    phones = find_client_phones(client_id)
    if phones == []:
        print('Телефонов нет')
    else:
        for num in phones:
            print(f'Телефон: {num}')




def del_client (client_id) -> bool:
    ''' Return True when client deleted
        Return False when client not exists
    '''
    if not client_exists(client_id):
        return False

    try:
        with psycopg2.connect(database = db_name, user = db_user, password = db_pass) as conn:
            with conn.cursor() as cur:

                cur.execute("""
                    DELETE FROM phone WHERE client_id = %s;
                    DELETE FROM client WHERE id = %s;
                """, (client_id, client_id));

                return True

    finally:
        conn.close()



##def main():
##    pass

##if __name__ == '__main__':
##    main()




## Функция, создающая структуру БД (таблицы).
print('Создание БД')
create_db()
print('OK')

## Функция, позволяющая добавить нового клиента.
print('\nДобавление нового клиента')
print(add_client('Петр', 'Сергеев', 'ps1999@bk.ru', ['9035550112', '+7 903 555 01 12'])) #1
print(add_client('Алекс', 'Фурсов', 'afur@ya.ru', ['+79152228855'])) #2
print(add_client('Петр', 'Иванов', 'petya007@mail.ru', ['9086661234'])) #3

## Функция, позволяющая добавить телефон для существующего клиента.
print('\nДобавление телефона клиента')
print(add_phone(2, '+7 999 001 02 02'))
print(add_phone(1, 444445))

## Функция, позволяющая изменить данные о клиенте.
print('\nИзменение данных клиента')
print(change_client(2, first_name='Andrey', phone='+123 111 222'))

## Функция, позволяющая удалить телефон для существующего клиента.
print('\nУдаление телефона клиента')
print(del_phone(1,'9035550112'))
print(del_phone(1,'9035550112')) # этот номер уже удалили
print(del_phone(33,'9086661234')) # нет такого клиента

## Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
print('\nНайти клиента по его данным')
print(find_client(email='afur@ya.ru', first_name = 'Алекс2', phone = '112', strict = False)) # найдет по email - 2
print(find_client(first_name = 'Петр', phone = '8 9086661234', strict = True)) # ошибочный телефон, строгий поиск
print(find_client(first_name = 'Петр', phone = '8 9086661234', strict = False)) # ошибочный телефон, мягкий поиск - 1
print(find_client(first_name = 'Петр', phone = '9086661234', strict = False)) # правильный телефон, мягкий поиск- 3
print(find_client(first_name = 'Петр', last_name = 'Иванов')) # строгий поиск по имени и фамилии - 3
print(find_client(email='noemail@ya.ru')) # нет клиента с такими данными

## Найти все телефоны клиента
print('\nВсе телефонные номера клиента')
print(find_client_phones(find_client(first_name='Петр', last_name='Сергеев')))

## Вывод информации о клиентах
print_client(1)
print_client(2)
print_client(3)

## Функция, позволяющая удалить существующего клиента.
print('\nУдаление клиента')
print(del_client(2))

## Удаленный клиент не существует
print_client(2)

print()





