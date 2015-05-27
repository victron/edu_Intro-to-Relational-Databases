__author__ = 'vic'

from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, MenuItem, Base

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



app = Flask(__name__)

@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        # restaurants.append({'name': request.form['name'], 'id': 100})
        flash('Restaurant %s created' % request.form['name'])
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    editedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            restaurant_old_name = editedRestaurant.name
            editedRestaurant.name = request.form['name']
            session.add(editedRestaurant)
            session.commit()
        # id = 0
        # for restaurant in restaurants:
        #     if int(restaurant['id']) == restaurant_id:
        #         restaurant_old_name = restaurant['name']
        #         restaurants[id]['name'] = request.form['name']
            flash('changed %s on %s' % (restaurant_old_name, request.form['name']))
            return redirect(url_for('showRestaurants'))
            # id += 1
    else:
        # for restaurant in restaurants:
        #     if int(restaurant['id']) == restaurant_id:
        restaurant_name = editedRestaurant.name
        return render_template('editRestaurant.html', restaurant_id=restaurant_id, restaurant_name=restaurant_name)


@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    deletedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    restaurant_name = deletedRestaurant.name
    if request.method == 'POST':
        session.delete(deletedRestaurant)
        session.commit()
        id = 0
        # for restaurant in restaurants:
        #     if int(restaurant['id']) == restaurant_id:
        #         restaurant_name = restaurants.pop(id)['name']
        flash('Restaurant %s deleted' % restaurant_name)
        return redirect(url_for('showRestaurants'))
            # id += 1
    else:
        # for restaurant in restaurants:
        #     if int(restaurant['id']) == restaurant_id:
        return render_template('deleteRestaurant.html', restaurant_id=restaurant_id, restaurant_name=restaurant_name)

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    restaurant_name = session.query(Restaurant).filter_by(id=restaurant_id).one().name
    # for restaurant in restaurants:
    #     if int(restaurant['id']) == restaurant_id:
    #         restaurant_name = restaurant['name']
    return render_template('menuf.html', restaurant_id=restaurant_id, restaurant_name=restaurant_name, items=items)

@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['POST', 'GET'])
def newMenu(restaurant_id):
    if request.method == 'POST':
        item = MenuItem(name=request.form['name'], course=request.form['course'], price=request.form['price'],
                        description=request.form['description'], restaurant_id=restaurant_id)
        session.add(item)
        session.commit()
        # items.append({'name': request.form['name'], 'id': 100, 'course': request.form['course'],
        #               'price': request.form['price'], 'description': request.form['description']})
        flash('Menu: %s created' % request.form['name'])
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        restaurant_name = session.query(Restaurant).filter_by(id=restaurant_id).one()
        # for restaurant in restaurants:
        #     if int(restaurant['id']) == restaurant_id:
        #         restaurant_name = restaurant['name']
        return render_template('newMenu.html', restaurant_name=restaurant_name.name, restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['POST', 'GET'])
def editMenue(restaurant_id, menu_id ):
    restaurant_name = session.query(Restaurant).filter_by(id=restaurant_id).one().name
    item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).one()
    if request.method == 'POST':
        # item.name ='name'
        for key in request.form:
            setattr(item, key, request.form[key])
        #
        # id = 0
        # for item in items:
        #     if int(item['id']) == menu_id:
        #         for key in request.form:
        #             if request.form[key] != '':
        #                 items[id][key] = request.form[key]
        #         # items[id]['name'] = request.form['name']
        #         # items[id]['course'] = request.form['course']
        #         # items[id]['description'] = request.form['description']
        #         # items[id]['price'] = request.form['price']
        #         items[id]['id'] = menu_id
        session.add(item)
        session.commit()
        flash('menu %s changed' % request.form['name'])
        return redirect(url_for('showMenu', restaurant_id=restaurant_id, menu_id=menu_id))
            # id += 1
    else:

        # for restaurant in restaurants:
        #     if int(restaurant['id']) == restaurant_id:
        #         restaurant_name = restaurant['name']
        #         for item in items:
        #             if int(item['id']) == menu_id:

        return render_template('editMenu.html', restaurant_id=restaurant_id, restaurant_name=restaurant_name,
                                               item=item)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['POST', 'GET'])
def deleteMenu(restaurant_id, menu_id):
    restaurant_name = session.query(Restaurant).filter_by(id=restaurant_id).one()
    deleted_item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).one()
    if request.method == 'POST':
        session.delete(deleted_item)
        session.commit()
        # id = 0
        # for item in items:
        #     if int(item['id']) == menu_id:
        #         deleted_item = items.pop(id)
        flash('menu %s deleted' % deleted_item.name)
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
            # id += 1

    else:
        # for restaurant in restaurants:
        #     if int(restaurant['id']) == restaurant_id:
        #         restaurant_name = restaurant['name']
        #         for item in items:
        #             if int(item['id']) == menu_id:
        return render_template('deleteMenu.html', restaurant_id=restaurant_id, menu_id=menu_id,
                                                restaurant_name=restaurant_name.name, item=deleted_item)

# ---------------- API --------------------

@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[ i.serialize for i in restaurants])

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def menusJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItem=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuJSON(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).one()
    return jsonify(Menu=item.serialize)



#Fake Restaurants
# restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

# restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
# items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'},
#           {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},
#           {'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},
#           {'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},
#           {'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
#
# item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'key'
    app.run(host='0.0.0.0', port=5000)
