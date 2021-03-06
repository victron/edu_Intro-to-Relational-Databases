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
        output += '<a href="/restaurants/%s/edit"> Edit<a>' % item.id
        output += '<br>'
        output += '<a href="delete"> Delete<a>'
    return output

def create_restaurant(new_restaurant_name):
    session = init_session()
    new_restaurant = Restaurant(name = new_restaurant_name)
    session.add(new_restaurant)
    session.commit()

def edit_restaurant(restaurant_id, restaurant_new_name):
    session = init_session()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    restaurant.name = restaurant_new_name
    session.commit()

def get_restaurant_name(restaurant_id):
    session = init_session()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return restaurant.name

def main():
    print read_restaurants()


if __name__ == '__main__':
    main()


