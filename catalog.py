from flask import Flask, render_template, request, redirect
from flask import jsonify, url_for, flash
from flask import session as login_session
from flask import make_response
from functools import wraps

from sqlalchemy import create_engine, asc, desc, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from database_setup import Base, Category, CategoryItem, User

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

import requests
import json
import random
import string
import httplib2

app = Flask(__name__)

# Loading json file to use to configure a client object
# This client_secret.json file should you edit, or replace
# your own one from Google Credentials page
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog App"


# Connect to Database and create database session
engine = create_engine('sqlite:///categoryitem.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
db_session = DBSession()


def createUser(login_session):
    """Create a user from login_session
    Returning user's ID
    """
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    db_session.add(newUser)
    db_session.commit()
    flash('New user added!')
    try:
        user = db_session.query(User).filter_by(
                    email=login_session['email']).one()
    except NoResultFound:
        flash('There went something wrong! Not found the user!')
        return None
    return user.id


def getUserId(email):
    """Returning user's ID from email address
    """
    try:
        user = db_session.query(User).filter_by(
                email=email).one()
        return user.id
    except:
        return None


def getUserInfo(user_id):
    """Returning User object
    """
    try:
        user = db_session.query(User).filter_by(id=user_id).one()
        return user
    except:
        return None

def login_required(f):
    """Checking if user is logged in
    """
    @wraps(f)
    def logged_in_checker(*args, **kwargs):
        if 'email' in login_session:
            return f(*args, **kwargs)
        else:
            flash("You are not allowed to access there")
            return redirect('/login')
    return logged_in_checker


@app.route('/clearSession')
def clearSession():
    """Clear login session
    Just for developing, testing
    """
    login_session.clear()
    return "Session cleared"


@app.route('/login')
def showLogin():
    """Login page
    """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    """Login with Facebook's authentication
    """
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    # Loading json file, this one should you edit or replace your own one
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type='
    url += 'fb_exchange_token&client_id='
    url += '%s&client_secret=%s&fb_exchange_token=%s' % (
                app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    # let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?'
    url += '%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserId(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    """Disconnecting user, who connected with Facebook's authentication
    """
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?'
    url += 'access_token=%s' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Login with Google's authentication
    """
    # Validate state token
    print "1. Validate state token"
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    # print "2. Upgrade the authorization code into a credentials object"
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # print "3. Check that the access token is valid."
    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
                    'Current user is already connected.'),
                    200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.

    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id
    login_session['username'] = access_token

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    login_session['user_id'] = getUserId(login_session['email'])

    if login_session['user_id'] == None:
        login_session['user_id'] = createUser(login_session)

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    """Disconnecting user, who connected with Google's authentication
    """
    print login_session.keys()
    credentials = login_session.get('credentials')
    print 'In gdisconnect access token is %s', credentials.access_token
    print 'User name is: '
    print login_session['username']
    if credentials.access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?'
    url += 'token=%s' % credentials.access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:

        response = make_response(json.dumps(
                                 'Failed to revoke token for given user.',
                                 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/disconnect')
def disconnect():
    """Disconnecting user based on provider
    """
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            if 'gplus_id' in login_session:
                del login_session['gplus_id']
            if 'gplus_id' in login_session:
                del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
            del login_session['username']
            del login_session['email']
            del login_session['picture']
            del login_session['user_id']
            del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCategories'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCategories'))


@app.route('/catalog.json')
def CatalogJSON():
    """Generating json file containing categories and their items
    """
    category = db_session.query(Category).all()
    return jsonify(categories=[cat.serialize for cat in category])

@app.route('/catalog/<category_name>/items.json')
def CategoryItemJSON(category_name):
    """Generating json file containing the category and their items
    """
    try:
        category = db_session.query(Category).filter_by(
                            name=category_name).one()
    except NoResultFound:
        flash('There went something wrong' +
              ', %s category not exits!' % category_name)
        return redirect(url_for('showCategories'))
    return jsonify(category=category.serialize)

@app.route('/catalog/<category_name>/item/<item_title>.json')
def ItemJSON(category_name, item_title):
    """Generating json file containing the item
    """
    try:
        category = db_session.query(Category).filter_by(
                                name=category_name).one()
        item = db_session.query(CategoryItem).filter(
                            and_(CategoryItem.title == item_title,
                                 CategoryItem.cat_id == category.id)).one()
    except NoResultFound:
        flash('There went something wrong, cannot display your request!')
        return redirect(url_for('showCategories'))
    return jsonify(item=item.serialize)


@app.route('/')
@app.route('/catalog/')
def showCategories():
    """Show all categories
    """
    categories = db_session.query(Category).order_by(asc(Category.name))
    last_items = db_session.query(CategoryItem).order_by(
                    desc(CategoryItem.id)).limit(10)
    return render_template('categories.html',
                           categories=categories,
                           items=last_items)


@app.route('/catalog/new/', methods=['GET', 'POST'])
@login_required
def newCategory():
    """Create a new category
    """
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'],
                               user_id=getUserId(login_session['email']))
        db_session.add(newCategory)
        flash('New Category %s Successfully Created' % newCategory.name)
        db_session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newcategory.html')


@app.route('/catalog/edit/<category_name>', methods=['GET', 'POST'])
@login_required
def editCategory(category_name):
    """Edit a category
    """
    # Retrieve Category object, and redirecting if not found
    try:
        editedCategory = db_session.query(Category).filter_by(
                            name=category_name).one()
    except NoResultFound:
        flash('There went something wrong' +
              ', %s category not exits!' % category_name)
        return redirect(url_for('showCategories'))
    # Checking user owning the category, if not redirecting
    if getUserId(login_session['email']) != editedCategory.user_id:
        flash('You are not authorized to edit!')
        return redirect(url_for('showCategories'))
    if request.method == 'POST':
        # Assigning the new name value to the category
        if request.form['name']:
            editedCategory.name = request.form['name']
            flash('Category Successfully Edited %s' % editedCategory.name)
            return redirect(url_for('showCategories'))
    else:
        # Using the newcategory.html to edit the category
        return render_template('newcategory.html', category=editedCategory)


@app.route('/catalog/<category_name>/delete/', methods=['GET', 'POST'])
@login_required
def deleteCategory(category_name):
    """Delete a category
    """
    # Retrieve Category object, and redirecting if not found
    try:
        categoryToDelete = db_session.query(Category).filter_by(
                        name=category_name).one()
    except NoResultFound:
        flash('There went something wrong' +
              ', %s category not exits!' % category_name)
        return redirect(url_for('showCategories'))
    # Checking user owning the category, if not redirecting
    if getUserId(login_session['email']) != categoryToDelete.user_id:
        flash('You are not authorized to delete this category!')
        return redirect(url_for('showCategories'))
    if request.method == 'POST':
        # Deleting the category
        db_session.delete(categoryToDelete)
        flash('%s Successfully Deleted' % categoryToDelete.name)
        db_session.commit()
        return redirect(url_for('showCategories'))
    else:
        # Rendering the confirmation page
        return render_template('deletecategory.html',
                               category=categoryToDelete)


@app.route('/catalog/<category_name>/items')
def showCategoryItems(category_name):
    """Show a items of a category
    """
    # Retrieve Category and items objects, and redirecting if anyone not found
    try:
        categories = db_session.query(Category).order_by(
                                    asc(Category.name)).all()
        category = db_session.query(Category).filter_by(
                                    name=category_name).one()
        items = db_session.query(CategoryItem).filter_by(
                                    cat_id=category.id).all()
    except NoResultFound:
        flash('There went something wrong, cannot display your request!!')
        return redirect(url_for('showCategories'))
    return render_template('categoryitems.html',
                           items=items,
                           categories=categories,
                           category=category)


@app.route('/catalog/<category_name>/item/<item_title>')
def showItem(category_name, item_title):
    """Show an item
    """
    # Retrieve Category and Item objects, and redirecting if anyone not found
    try:
        category = db_session.query(Category).filter_by(
                                name=category_name).one()
        item = db_session.query(CategoryItem).filter(
                            and_(CategoryItem.title == item_title,
                                 CategoryItem.cat_id == category.id)).one()
    except NoResultFound:
        flash('There went something wrong, cannot display your request!')
        return redirect(url_for('showCategories'))
    # Checking the user is logged on
    if 'username' not in login_session:
        return render_template('item.html',
                               category_name=category_name,
                               item=item,
                               owner=False)
    else:
        return render_template('item.html',
                               category_name=category_name,
                               item=item,
                               owner=((getUserId(login_session['email']) ==
                                       item.user_id)))


@app.route('/catalog/new_item/', methods=['GET', 'POST'])
@login_required
def newItem():
    """Create a new category item
    """
    categories = db_session.query(Category).order_by(asc(Category.name)).all()
    if request.method == 'POST':
        # Creating the new Item
        cat = db_session.query(Category).filter_by(
                            id=request.form['cat_id']).one()
        newItem = CategoryItem(title=request.form['title'],
                               description=request.form['description'],
                               cat_id=request.form['cat_id'],
                               category=cat,
                               user_id=getUserId(login_session['email']))
        db_session.add(newItem)
        db_session.commit()
        flash('New %s Item Successfully Created' % (newItem.title))
        return redirect(url_for('showCategories'))
    else:
        return render_template('newitem.html', categories=categories)


@app.route('/catalog/<category_name>/item/<item_title>/edit',
           methods=['GET', 'POST'])
@login_required
def editItem(category_name, item_title):
    """Edit a menu item
    """
    # Retrieve Category and item objects, and redirecting if anyone not found
    try:
        category = db_session.query(Category).filter_by(
                                name=category_name).one()
        editedItem = db_session.query(CategoryItem).filter(
                                and_(CategoryItem.title == item_title,
                                     CategoryItem.cat_id == category.id)).one()
    except NoResultFound:
        flash('There went something wrong, item not found!')
        return redirect(url_for('showCategories'))
    # Checking user owning the category, if not redirecting
    if getUserId(login_session['email']) != editedItem.user_id:
        flash('You are not authorized to edit this item!')
        return redirect(url_for('showItem',
                        category_name=category_name,
                        item_title=item_title))
    if request.method == 'POST':
        # Assigning new values to Item
        if request.form['title']:
            editedItem.title = request.form['title']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['cat_id']:
            editedItem.cat_id = request.form['cat_id']
        db_session.add(editedItem)
        db_session.commit()
        # Retrieve the item new Category, and redirecting if anyone not found
        try:
            category = db_session.query(Category).filter_by(
                        id=editedItem.cat_id).one()
        except NoResultFound:
            flash('There went something wrong' +
                  ', the new category of the item not found!')
            return redirect(url_for('showCategories'))
        flash('Category Item Successfully Edited')
        return redirect(url_for('showItem',
                        category_name=category.name,
                        item_title=editedItem.title))
    else:
        # Using the newitem.html to edit the item
        categories = db_session.query(Category).order_by(
                                    asc(Category.name)).all()
        return render_template('newitem.html',
                               categories=categories,
                               item=editedItem)


@app.route('/catalog/<category_name>/item/<item_title>/delete',
           methods=['GET', 'POST'])
@login_required
def deleteItem(category_name, item_title):
    """Delete a menu item
    """
    # Retrieve Category and item objects, and redirecting if anyone not found
    try:
        category = db_session.query(Category).filter_by(
                        name=category_name).one()
        itemToDelete = db_session.query(CategoryItem).filter(
                        and_(CategoryItem.cat_id == category.id,
                             CategoryItem.title == item_title)).one()
    except NoResultFound:
        flash('There went something wrong, item not found!')
        return redirect(url_for('showCategories'))
    # Checking user owning the category, if not redirecting
    if getUserId(login_session['email']) != itemToDelete.user_id:
        flash('You are not authorized to delete this item!')
        return redirect(url_for('showItem',
                                category_name=category_name,
                                item_title=item_title))
    if request.method == 'POST':
        # Deleting the item
        db_session.delete(itemToDelete)
        db_session.commit()
        flash('%s Item Successfully Deleted' % itemToDelete.title)
        return redirect(url_for('showCategories',
                                category_name=category_name))
    else:
        # Rendering the confirmation page
        return render_template('deleteitem.html',
                               category_name=category_name,
                               item_title=item_title)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
