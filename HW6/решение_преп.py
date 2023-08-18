def get_sales(author_id = 0, author_name = ''):
    res = session.query(Book.title, Shop.name, Sale.price, Sale.count, Sale.date_sale).\
          join(Publisher).join(Stock).join(Sale).join(Shop).\
          filter(or_(Publisher.id==author_id, Publisher.name.ilike(f'%{publisher_name}%')))

    for book, shop, price, count, date in res:
        print(f'{book: <40} | {shop: <10} | {price*count: <8} | {date.strftime('%d-%m-%Y')}')


...        
if __name__ == '__main__':
    ...
    q = input('Введите id или название издателя: ')
    if q.isdigit():
        get_sales(author_id=int(q))
    else:
        get_sales(author_name=q)