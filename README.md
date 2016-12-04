# Catalog App
## Contents
1. Install
2. User's manual
  * Home page
  * Login page
  * After login
  * Item page
  * Create or edit an item
  * Create or edit a category
  * Deleting
3. Developer's manual
4. Sources

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
  * Copy Client ID to [/templates/login.html](https://github.com/janosvincze/catalog/blob/master/templates/login.html#L48):
  
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
 
 6. Run the app
 
  ```
 python catalog.py
 ```
 
 7. Open [http://localhost:5000](http://localhost:5000) in a browser
 
 
 
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


### Classes, entities

#### [BlogHandler](https://github.com/janosvincze/blog/blob/master/main.py#L59)
To rendering templates with passing user. Setting, reading cookies to identify users.

## Sources
  * Udacity Full Stack nanodegree

[home_page_picture]: https://github.com/janosvincze/catalog/blob/master/screenshot/homepage.png "Home page"
[login_picture]: https://github.com/janosvincze/catalog/blob/master/screenshot/Login.png "Login page"
[logged_home_page_picture]: https://github.com/janosvincze/catalog/blob/master/screenshot/logged_homepage.png "After login"
[item_page_picture]: https://github.com/janosvincze/catalog/blob/master/screenshot/item.png "An item's page"
[edit_item_picture]: https://github.com/janosvincze/catalog/blob/master/screenshot/edit_item.png "Editing an item"
[new_category_picture]: https://github.com/janosvincze/catalog/blob/master/screenshot/new_category.png "Create a new category"
[deleting_confirmation]: https://github.com/janosvincze/catalog/blob/master/screenshot/confirm_deleting.png "Deleting a category"
