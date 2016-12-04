# Catalog App
## Contents
1. Install
2. User's manual
  * Home page
  * Login page
  * Categories items page
  * Item page
  * New item
  * New category
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
 ```
 
 6. Run the app
 
  ```
 python catalog.py
 ```
 
 7. Open [http://localhost:5000](http://localhost:5000) in a browser
 
 
 
## User's manual
### The link of the blog
You can found the working blog at the following link:
[http://engineapp-vj-blog.appspot.com/](https://engineapp-vj-blog.appspot.com/)
### Home page
Before you signup and/or login, you can see the following layout: 
![alt text][without_login_picture]

If you do not have an acount, please use the [Signup](https://engineapp-vj-blog.appspot.com/signup) link on the navigation section to create a new one. Fill out the registration form. After successfully submitting it, you will be logged in.

If you already have an acount, please use [Login](https://engineapp-vj-blog.appspot.com/login) link on the navigation section. 
Use the login form as appropriate.

### After login
After you succesfully login, you can see the following layout:
![alt text][after_login_picture]

After logging in, you can:
  * Create a New post
  * Edit your own posts
  * Delete your own posts

Just following the link as it shown above.

### A post's page

Click a post's title to reach its page.
![alt text][post_page_picture]

You can add a new comment. Fill the blank text area and click the submit button.

## Developer's manual

### Used technology
  * Google App Engine
  * Google Cloud Datastore
  * Python
  * Jinja
  * Html
  * CSS

### Structure

The main python file: [main.py](https://github.com/janosvincze/blog/blob/master/main.py)
The templates files: [templates](https://github.com/janosvincze/blog/tree/master/templates)

### Classes, entities

#### [BlogHandler](https://github.com/janosvincze/blog/blob/master/main.py#L59)
To rendering templates with passing user. Setting, reading cookies to identify users.

#### [MainPage](https://github.com/janosvincze/blog/blob/master/main.py#L102)
To rendering templates with passing user. Setting, reading cookies to identify users.

#### [User class](https://github.com/janosvincze/blog/blob/master/main.py#L134)
Storing users' name, password's hash and email address.

#### [Post class](https://github.com/janosvincze/blog/blob/master/main.py#L170)
Storing posts' title, content, creation time, author (refering to User entity) and comments counter.

Adding **[author_user](https://github.com/janosvincze/blog/blob/master/main.py#L184)** function to retrieve the post's author (refering to User entity).<br>Adding **[render](https://github.com/janosvincze/blog/blob/master/main.py#L188)** function to render the post entity with author's name to display.

#### [Comment class](https://github.com/janosvincze/blog/blob/master/main.py#L217)
Storing comments' content, creation time and author (refering to User entity).

Adding **[author_user](https://github.com/janosvincze/blog/blob/master/main.py#L230)** function to retrieve the comment's author (refering to User entity).<br>Adding **[render](https://github.com/janosvincze/blog/blob/master/main.py#L234)** function to render the comment entity to display.

#### [Like class](https://github.com/janosvincze/blog/blob/master/main.py#L249)
Storing post's likes.

#### [PostPage](https://github.com/janosvincze/blog/blob/master/main.py#L282)
To display a post with comments and a new comment form if user's logged in.


#### [NewPost](https://github.com/janosvincze/blog/blob/master/main.py#L332)

  [get](https://github.com/janosvincze/blog/blob/master/main.py#L333) function:
  Displaying post form with existing content if there is a given post_id parameter, or a blank form if there is no post_id parameter.
  
  [post](https://github.com/janosvincze/blog/blob/master/main.py#L350) function:
  Update post if there is a valid post_id parameter, otherwise insert a new one.
 
 
#### [DeletePost](https://github.com/janosvincze/blog/blob/master/main.py#L386)
  [get](https://github.com/janosvincze/blog/blob/master/main.py#L387) function:
  Checking that user is the author of the post and displaying a confirmation form.
  
  [post](https://github.com/janosvincze/blog/blob/master/main.py#L410) function:
  Checking that user is the author of the post and he/she is, delete the post.
  
#### [NewComment](https://github.com/janosvincze/blog/blob/master/main.py#L539)
Add a new comment to the post, and increase post's comment counter.
  
#### [DeleteComment](https://github.com/janosvincze/blog/blob/master/main.py#L431)
Delete a comment.

#### [EditComment](https://github.com/janosvincze/blog/blob/master/main.py#L484)
Edit a comment.

#### [NewLike](https://github.com/janosvincze/blog/blob/master/main.py#L574)
Add a new like to the post, and increase post's like counter.
  
#### [DeleteLike](https://github.com/janosvincze/blog/blob/master/main.py#L615)
Delete a like.

#### [Signup](https://github.com/janosvincze/blog/blob/master/main.py#L644)
Handling user signup.

#### [Register](https://github.com/janosvincze/blog/blob/master/main.py#L682)
Handling user signup.


#### [Login](https://github.com/janosvincze/blog/blob/master/main.py#L700)
Handling user login.


#### [Logout](https://github.com/janosvincze/blog/blob/master/main.py#L721)
Handling user login.


#### [Welcome](https://github.com/janosvincze/blog/blob/master/main.py#L730)
New user welome.


#### [ErrorPage](https://github.com/janosvincze/blog/blob/master/main.py#L741)
Displaying error messages. Error **code** pass through to template [blog_error.html](https://github.com/janosvincze/blog/blob/master/templates/blog_error.html), which cointaing the real message to display.

## Sources
  * Udacity Full Stack nanodegree

[without_login_picture]: https://github.com/janosvincze/blog/blob/master/screenshots/without_login.png "Home page"
[after_login_picture]: https://github.com/janosvincze/blog/blob/master/screenshots/base.png "Home page after login"
[post_page_picture]: https://github.com/janosvincze/blog/blob/master/screenshots/post.png "A post's page"
