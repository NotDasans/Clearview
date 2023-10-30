# ClearView Blogging
#### Video Demo:  <https://youtu.be/gpypFxhqMrU>
## Description:
### Welcome to ClearView Blogging!
### Introduction:
This website allows users to login, register, post, comment and search various blogs. This project uses HTML, CSS, JavaScript, Bootstrap, Python and Flask framework. It has a user interface that allows users to have an easy and comfortable time accessing the various features of the website.
The project contains the following folders and files:
*	Flask_session
*	Static: which contains some images used in the website and styles.css file.
*	Templates: this folder contains all the various html files which are rendered in the website
*	app.py: this file contains all the functions for different routes and backend of the website.
*	clearview.db: this is a database which contains all the data regarding users, blogs and comments.
*	helpers.py: this file contains helper functions like login_required.
*	README.md: this file

### Layout:
The template layout.html contains the basic layout which is rendered into all other templates using Jinja syntax. It contains the meta data in head tag and the navigation bar and footer in body tag.\
The navigation bar allows us to access various pages of the website like home, accounts, about, contact it also contains a search bar and access to login, register and logout (if logged in already).\
The footer contains links to various social media in thee form of buttons with icons and copyright information.

### Login and Register:
The users can login and register under their respective tabs on the navigation bar. The login and register function handle all the corner cases in case any input is invalid (example: wrong password or username in case of login or already in use username in case of register etc.) or left blank and displays the corresponding error message on the same page. Once the users have logged in, they can access the login required features that is the account page (which allows users to post or see their previous blogs) and comment feature (rest of the features can be accessed without logging in).\
The login.html template presents a form which asks for the user’s username and password and works to login if the information is correct and displays and error message below the form and reloading the form to allow the user to enter again. It uses data from the clearview.db database.
The register.html template presents a form which asks for the user’s username name password and another field to confirm password and works to register the user if all requirements are meant and displays an error message like that of login page and reloads the form.
>For security reasons the password is hashed appropriately before storing in the database.
### Logout:
The logout route simply clears the session and logs the user out.
### Index:
The index or the homepage consists of a carousel which displays some awards and achievements and consists of the three of the latest blogs which are in descending order of their date and time of upload. The blogs are displayed in cards which contain the title, name of the writer, an image, and a preview of the content inside it on clicking on the “go to page” button it takes you to the required blog.
### Account:
The account page can be accessed from the navigation. It is required to login in order to access this page if not logged in it redirects to the login page. This page consists of a form that can be filled to make a new blog it asks for a title, an image URL and content of a blog on clicking the post button posts the blog. It also contains the blogs posted by the logged in user in same manner as on the index page (i.e., card with go to button to access the blog).
### Contact Us:
The contact us page consists of a form that can be filled for giving feedback or asking any queries by the user it will be submitted and stored in the database. It also contains the contact details like phone number, email and address of the company.
### About Us:
The about us page consists of the general information about the company’s vision and values, it also contains the company moto.
### Search:
The search bar can be accessed from the navigation bar it brings up any blogs or articles in descending order of date and time of upload whose title is like the text given in the search bar in a similar manner of that of the index page (i.e., card with go to button to access the blog). It displays no result when no results match.
### Blog Page:
The blog page can be accessed by the go to button in the cards present in either index, accounts, or search results page. These bring the pages by the “get” method that means that these pages can also be accessed from URLs that are shared. This page consists of an image, name of writer, date and time of upload and the content of the blog below this it consists of the comment feature.
### Comments:
The user if logged in can comment on any of the blogs. The comments are displayed in descending order of their upload. The comments contain name of the commenter and date and time of upload on left and the comment on the right.\
Comments are unique to every blog.
### clearview database
The clearview database consists of four tables:
1.	Users: the users table consists of the necessary information about all the users. The password is hashed.
1.	Post: the post table consists of all the necessary information about all the posts that have been posted by various users.
1.	Feedback: the feedback table stores all the information that have been given the feedback/queries form in contact us page.
1.	Comment: the comment table consists of the data about all the comments with necessary foreign keys like user_id and post_id.

