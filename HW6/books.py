import json
import datetime
import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


db_name = 'books'
db_user = 'postgres'
db_pass = 'admin'


Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=50), unique=True)



class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=100), unique=True)
    id_pub = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)

    publisher = relationship(Publisher, backref="book")



class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=50), unique=True)



class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'))
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'))
    count = sq.Column(sq.Integer)

    book = relationship(Book, backref="stock")
    shop = relationship(Shop, backref="stock")

    def __str__(self):
        return(f'{self.id}:  book={self.id_book}, shop={self.id_shop}, count={self.count}')



class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.DECIMAL)
    date_sale = sq.Column(sq.DateTime)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'))
    count = sq.Column(sq.Integer)

    stock = relationship(Stock, backref="sale")




def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)




def read_json (file_name, session):
    with open(file_name, 'r', encoding='utf-8') as file:
        jdata = json.load(file)

    for item in jdata:
        model = item['model']
        pk = item['pk']
        fields = item['fields']

        if model == 'publisher':
            m = Publisher(id = pk, name = fields['name'])
        elif model == 'book':
            m = Book(id = pk, title = fields['title'], id_pub = fields['id_publisher'] )
        elif model == 'shop':
            m = Shop(id = pk, name = fields['name'])
        elif model == 'stock':
            m = Stock(id = pk, id_shop = fields['id_shop'], id_book = fields['id_book'],
                      count = fields['count'])
        elif model == 'sale':
            m = Sale(id = pk, id_stock = fields['id_stock'], price = fields['price'],
                     count = fields['count'], date_sale = fields['date_sale'])
        else:
            continue

        session.add(m)

    session.commit()





def print_pub_sale(publisher, session):

    if str(publisher).isdigit():
##        sq0 = session.query(Publisher.id).filter(Publisher.id == int(publisher))
        sq0 = [publisher]
    else:
        sq0 = session.query(Publisher.id).filter(Publisher.name.ilike(f'%{publisher}%'))

    q7 = session.query(Sale)\
        .join(Stock)\
        .join(Book)\
        .join(Shop)\
        .join(Publisher)\
        .filter(Book.id_pub.in_(sq0))\
        .order_by(Book.id).all()

    print()

    if not q7:
        print('Нет данных')
        return

    print('\nПроданные книги:\n')

    # Вычисление длины для форматирования строк
    title_len = max([len(s.stock.book.title) for s in q7])
    shop_len  = max([len(s.stock.shop.name) for s in q7])

    for s in q7:
        print(s.stock.book.title.ljust(title_len),\
              s.stock.shop.name.ljust(shop_len), \
              s.price, \
              s.date_sale.date(), \
              s.stock.book.publisher.name, \
              sep=' | ' )





if __name__ == '__main__':

##    DSN = "postgresql://postgres:admin@localhost:5432/books"
    DSN = f"postgresql://{db_user}:{db_pass}@localhost:5432/{db_name}"
    engine = sqlalchemy.create_engine(DSN)
    create_tables(engine)

    # сессия
    Session = sessionmaker(bind=engine)
    session = Session()

    read_json('fixtures/tests_data.json', session)

    print()
    print('Выберите издателя.\nВедите номер или часть названия:')
    for p in session.query(Publisher).all():
        print(f'  {p.id} - {p.name}')
    pub = input()

    print_pub_sale(pub, session)

    session.close()
