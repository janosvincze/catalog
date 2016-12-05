# Catalog App
## Contents
1. [Install](#install)
2. [User's manual](#users-manual)
  * Home page
  * Login page
  * After login
  * Item page
  * Create or edit an item
  * Create or edit a category
  * Deleting
3. [Developer's manual](#developers-manual)
4. [Sources](#sources)

## Install
### Run Locally
 1. I highly recommend to use [Vagrant](https://www.vagrantup.com/) virtual enviroment to test. 
 Install [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/). Instructions on how to do so can be found on the websites as well as in this [Udacity course materials](https://www.udacity.com/wiki/ud088/vagrant).
 Clone the [fullstack-nanodegree-vm repository](https://github.com/udacity/fullstack-nanodegree-vm). Shortly:
 
 ```
 # Clone the repository, which contains the vagrant files
 git clone https://github.com/udacity/fullstack-nanodegree-vm
 
 # Go to cloned repo vagrant directory
 cd /fullstack_nanodegree-vm/vagrant
 
 # Launch the virtual machine
 vagrant up
 
 # Reach the virtual machine via ssh - ssh client should be installed on your computer
 vagrant ssh
 ```
 
 2. Clone [this repository](https://github.com/janosvincze/catalog.git)
 On your host machine:
 
 ```
 # Go to vagrant directory of your cloned repository
 # It is a shared directory and available on virtual machine
 cd /vagrant
 
 git clone https://github.com/janosvincze/catalog.git
 ```
 
 Or clone it directly to the virtual machine:
 
  ```
 # After you reach the virtual machine via ssh with:
 # vagrant ssh
 
 git clone https://github.com/janosvincze/catalog.git
 ```
 
 3. Obtain OAuth 2.0 credentials from the [Google API Console](https://console.developers.google.com).
 Instructions on how to do can be found on [here](https://developers.google.com/identity/protocols/OAuth2).
 
  * Make a project
  * Go to Creditentals page
  * Choose OAuth client ID from "Create creditental" or use [this link](https://console.developers.google.com/apis/credentials/oauthclient)
  * Choose Web Application and click Create
  * Fill the form as in the [client_secret.json](https://github.com/janosvincze/catalog/blob/master/client_secrets.json)
  * After download the json file, and copy it the catalog directory as client_secret.json
  * Copy Client ID to [login.html](https://github.com/janosvincze/catalog/blob/master/templates/login.html#L48):
  
    ```
    <span class="g-signin"
     data-scope="openid email"
     <!-- Copy here your Google OAuth Client ID -->
     data-clientid="the_place_of_your_google_oauth_client_id"
     data-redirecturi="postmessage"
     data-accesstype="offline"
     data-cookiepolicy="single_host_origin"
     data-callback="signInCallback"
     data-approvalprompt="force">
    </span>
    ```
    
 4. Obtain Facebook App ID from [Facebook for developers site](https://developers.facebook.com/apps/)
   * Create a new App by clicking "Create new app" button
   * Choose your app by clicking the app name
   * Add Facebook Login (you can find it in new products) to your application
   * Add login:5000/login and localhost:5000/fbconnect to "Valid OAuth redirect URIs"
   * Copy the Facebook App ID to [fb_client_secret.json](https://github.com/janosvincze/catalog/blob/master/fb_client_secrets.json#L3)
   * Copy the App Secret to [fb_client_secret.json](https://github.com/janosvincze/catalog/blob/master/fb_client_secrets.json#L4)
   * Copy the App ID to (https://github.com/janosvincze/catalog/blob/master/templates/login.html#L112)
   
 5. Database setup
 Run [database_setup.py](https://github.com/janosvincze/catalog/blob/master/database_setup.py)
 
 ```
 # Go to catalog directory on the virtual machine 
 cd /catalog
 
 python database_setup.py
 python fill_database.py
 ```
 
 6. Change app.secret_key
 To use Flask session safely, you should set app.secret_key.
 Use a random key!
 
 ```
 # This is not a safe secret key!
  app.secret_key = 'super_secret_key'
 ```
 
 7. Run the app
 
  ```
 python catalog.py
 ```
 
 8. Open [http://localhost:5000](http://localhost:5000) in a browser
 
 
 
## User's manual
### Home page
Before you login, you can see the following layout: 
![alt text][home_page_picture]

Without login, you can see all the categories and the latest items. Choose (click) a category to see its items.
You can see an item description by clicking its title.

You can login with your Google or Facebook acount.

### Login
You can login with your Google or Facebook acount. You should approve that website access your basic data, such as e-mail address and your name.
![alt text][login_picture]

### After login

 After logging in, you can:
  * Create a New category
  * Create a New Item
  * Edit your own categories and items
  * Delete your own categories and items

![alt text][logged_home_page_picture]

### Item page

In the item page you can see the item's description. If your own the item, you can edit or delete the item clicking the links under the description.

![alt text][item_page_picture]

### Create or edit an item

To add a new item, click the "Add new item" link on the home page after you login.
To edit an item you own, go to the item page and click the "Edit" link.

![alt text][edit_item_picture]

Fill the form and click "Create"/"Update" button.

### Create or edit a category

To add a new category, click the "Add new category" link on the home page after you login.
To edit a category you own, go to the home page and click the "Edit" link of the category.

![alt text][new_category_picture]

Add or edit the name of the category, and click "Create"/"Update" button to save it.

### Deleting

To delete a category you own, go to home page and click the "Delete" link of the category.
To delete an item you own, go to the item page and click the "Delete" link.

![alt text][deleting_confirmation]

You should confirm that you really want to delete the category or the item.


## Developer's manual

### Used technology
  * Python
  * Flask
  * SqlAlchemy
  * Html
  * CSS

### Structure

The main python file: [catalog.py](https://github.com/janosvincze/catalog/blob/master/catalog.py)

Database setup file: [database_setup.py](https://github.com/janosvincze/catalog/blob/master/database_setup.py)

Test data: [fill_database.py](https://github.com/janosvincze/catalog/blob/master/fill_database.py)

The templates files: [templates](https://github.com/janosvincze/catalog/tree/master/templates)


### Database

Database's tables definition can be found in [database_setup.py](https://github.com/janosvincze/catalog/blob/master/database_setup.py) Using SQLite via SQLAlchemy.

#### User
To store users' data: email address, name, id as primary key.

#### Category
To store data of categories: name, id as primary key and the creator/owner user_id.
Functions to serialize data:
 * serialize
 * serialize_items
 
#### CategoryItem
To store data of items: title, description, id as primary key, the creator/owner user_id and their category id.
Function to serialize data: serialize

### Catalog.py

#### Handling users

 * def createUser(login_session)
 
 To create a user in the database from login session, and return its ID.
 * def getUserId(email)
 
 To return user's ID from an email address.
 * def getUserInfo(user_id)
 
 To return User object from an user_id.

#### Login/logout

 * showLogin()
 
 To render the login page
 
 * fbconnect()
 
 To login user via Facebook OAuth service. For details, please see the installing section.
 
 * fbdisconnect()
 
 To logout the user, who connected via Facebook OAuth.
 
 * gconnect()
 
 To login user via Google OAuth service. For details, please see the installing section.
 
 * gdisconnect()
 
 To logout the user, who connected via Google OAuth.
 
 * disconnect()
 
 To handle users logout.
 
#### Retrieving all data in JSON format
 * CatalogJSON()
 Using jsonify function, to return all the categories and their items in one JSON file.
 In the database I have defined "items" relationship to use it in serializing.
 
 ```
 items = relationship("CategoryItem", back_populates="category")
 ...
 def serialize_items(self):
      return [ item.serialize for item in self.items]
 ```

#### Home Page
 * showCategories()
 Rendering home page after retriving categories and the last ten items from the database:
 
 ```
    categories = db_session.query(Category).order_by(asc(Category.name))
    last_items = db_session.query(CategoryItem).order_by(
                    desc(CategoryItem.id)).limit(10)
    return render_template('categories.html',
                           categories=categories,
                           items=last_items)
 ```
 
#### Handling categories: create, edit and delete
 * newCategory()
 Creating a new category. After checking user is logged in, if the request is GET, rendering the creating category page.
 If the request is POST, creating a Category from request.form data.
 
 ```
 def newCategory():
    # Checking the user is logged on
    if 'username' not in login_session:
        return redirect('/login')
    # If the request is a POST create a new category
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'],
                               user_id=getUserId(login_session['email']))
        db_session.add(newCategory)
        # Add a new flash line to inform the user
        flash('New Category %s Successfully Created' % newCategory.name)
        db_session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newcategory.html')
 ```
 
 * editCategory(category_name)
 Editing a category
 
 ```
 @app.route('/catalog/edit/<category_name>', methods=['GET', 'POST'])
 def editCategory(category_name):
    """Edit a category
    """
    # Checking the user is logged on
    if 'username' not in login_session:
        return redirect('/login')
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
        # Informing the user
        flash('You are not authorized to edit!')
        return redirect(url_for('showCategories'))
    if request.method == 'POST':
        # Assigning the new name value to the category
        if request.form['name']:
            editedCategory.name = request.form['name']
            # Informing the user that editing was succesfull
            flash('Category Successfully Edited %s' % editedCategory.name)
            return redirect(url_for('showCategories'))
    else:
        # Using the newcategory.html to edit the category passing category to fill the form
        return render_template('newcategory.html', category=editedCategory)
 ```
 
 Using the [newcategory.html](https://github.com/janosvincze/catalog/blob/master/templates/newcategory.html) to edit category.
 If category is defined, means it is an update:
 
 ```
  <div class="col-md-11 padding-small">
     <h1>
         {% if (category is defined) %}
                Edit Category
         {% else %}
                New Category
         {% endif %}
     </h1>
  </div>
  
  ...
  
  <input type ="text" class="form-control" maxlength="100"
         name="name"
         {% if category is defined %}
                value="{{category.name}}"
         {% endif %}
         >
 ```
   
 * def deleteCategory(category_name)
 Deleting a category.
 
 ```
    # Find the category to delete
    categoryToDelete = db_session.query(Category).filter_by(
                        name=category_name).one()
    
    ...
    
    if request.method == 'POST':
        # Deleting the category from the database
        db_session.delete(categoryToDelete)
        # Informing the user that deleting was successfull
        flash('%s Successfully Deleted' % categoryToDelete.name)
        # Commit the deleting
        db_session.commit()
        # Redirecting to the home page
        return redirect(url_for('showCategories'))
    else:
        # Rendering the confirmation page
        return render_template('deletecategory.html',
                               category=categoryToDelete)
 ```
 
#### Handling items: show, create, edit and delete
 * showCategoryItems(category_name)
 Show the items of a category
 
 * showItem(category_name, item_title)
 Show the given item.
 
 * newItem()
 Create a new item.
 
 ```
    # Search the choosen category
    cat = db_session.query(Category).filter_by(
                           id=request.form['cat_id']).one()
    # Create a new item. Using getUserId to retrieve the id of the user from login_session
    newItem = CategoryItem(title=request.form['title'],
                           description=request.form['description'],
                           cat_id=request.form['cat_id'],
                           category=cat,
                           user_id=getUserId(login_session['email']))
    # Insert the new item to the database 
    db_session.add(newItem)
 ```
 
 * editItem(category_name, item_title)
 Edit an item.
 
 ```
  # Redirecting after updating the database with the new values
  # keeping in mind that the category and the title of the item maybe changed
  return redirect(url_for('showItem',
                          category_name=category.name,
                          item_title=editedItem.title))
 ```
 
 Using the [newitem.html](https://github.com/janosvincze/catalog/blob/master/templates/newitem.html) to edit the item.
 If item is defined, means it is an update:
 
 ```
  <div class="col-md-11 padding-small">
     <h1>
         {% if (item is defined) %}
                Edit Category
         {% else %}
                New Category
         {% endif %}
     </h1>
  </div>
  
  ...
  
  <input type ="text" class="form-control" maxlength="100"
         name="title"
         {% if item is defined %}
                value="{{item.title}}"
         {% endif %}
         >
 ```
 
 
 * deleteItem(category_name, item_title)
 Deleting an item after confirmation.
 
 
## Sources
  * Udacity Full Stack nanodegree
  * Facebook For Developers: [Facebook Login for the Web with the JavaScript SDK](https://developers.facebook.com/docs/facebook-login/web)
  * Google Guides: [Using OAuth 2.0 for Web Server Applications](https://developers.google.com/identity/protocols/OAuth2WebServer)

[home_page_picture]: https://github.com/janosvincze/catalog/blob/master/screenshot/homepage.png "Home page"
[login_picture]: https://github.com/janosvincze/catalog/blob/master/screenshot/Login.png "Login page"
[logged_home_page_picture]: https://github.com/janosvincze/catalog/blob/master/screenshot/logged_homepage.png "After login"
[item_page_picture]: https://github.com/janosvincze/catalog/blob/master/screenshot/item.png "An item's page"
[edit_item_picture]: https://github.com/janosvincze/catalog/blob/master/screenshot/edit_item.png "Editing an item"
[new_category_picture]: https://github.com/janosvincze/catalog/blob/master/screenshot/new_category.png "Create a new category"
[deleting_confirmation]: https://github.com/janosvincze/catalog/blob/master/screenshot/confirm_deleting.png "Deleting a category"
