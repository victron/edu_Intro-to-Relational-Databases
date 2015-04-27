__author__ = 'vic'

from flask import Flask, render_template, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, MenuItem, Restaurant

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

@app.route('/restaurants/<int:restaurant_id>/')
def Helloworld(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    # edit_link = url_for('editMenuItem', restaurant_id=restaurant_id, menu_id=)
    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurants/<int:restaurant_id>/newMenuItem/')
def newMenuItem(restaurant_id):
    return 'page to create new menu item Task=1 - done'


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/editMenuItem/')
def editMenuItem(restaurant_id, menu_id):
    return 'page to create edit menu item Task=2 - done'


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/deleteMenuItem/')
def deleteMenuItem(restaurant_id, menu_id):
    return 'page to create delete menu item Task=3 - done'


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
