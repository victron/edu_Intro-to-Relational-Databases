__author__ = 'vic'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant


def init_session():
    engine = create_engine('sqlite:///restaurantmenu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session

def read_restaurants():
    session = init_session()
    items = session.query(Restaurant).all()
    output = ''
    for item in items:
        # output += '<br>'
        output += '<h3> %s </h3>' % item.name
        output += '<a href="edit"> Edit<a>'
        output += '<br>'
        output += '<a href="delete"> Delete<a>'
    return output

def create_restaurant(new_restaurant_name):
    session = init_session()
    new_restaurant = Restaurant(name = new_restaurant_name)
    session.add(new_restaurant)
    session.commit()

def main():
    print read_restaurants()


if __name__ == '__main__':
    main()


