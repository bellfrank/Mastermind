# mastermind
a mastermind game, which can be played by a user "against" the computer.

Link to Website: https://fierce-dawn-57055.herokuapp.com/

## Big Picture
- For this project I wanted to leverage my knowledge of Django, a popular web framework to make a dynamic cool looking website.

- Towards the end of my project, I also tried learning different methods used to make sure updates to web pages proceed smoothly by implementing some testing and CI/CD.

- If you didn't know the site is live! Since I built it using the free tier on Heroku, it may take a few seconds to initially load the website, but once on there the website should be as smooth as any other.

- If you're familiar with MVC(model, view, controller) Django is very similar in the way the flow of information goes.

- That's really it big picture, let's just right into it!

# How to get started with the project
If you are trying to run the project locally in your own computer, you'll have to install a few programs, which are listed in my requirements.txt file. I would also recommend you set up a virtual environment just for this project. 

Once you've done that, and have cloned the project into your local computer, you activate the Django with this command: python3 manage.py runserver/

If you just want to play the game :) Check it out! -> https://fierce-dawn-57055.herokuapp.com/


# Step by step process

## Routes
views.py contains a number of different views and can be thought of as what the user might like to see. These functions can take in a request and return for example a HttpResponse. We then associate each view with a specific URL in our urls.py. urls.py contains all the possible views that the user may visit on our site.

## Forms
Django has a feature known as Django forms that creates an even easier method of collecting user information. One of the advantages of this feature is that it does client side and server side validation. I decided not to go this route because I wanted the ability to manipulate the DOM using JavaScript and add features like auto tabbing when the user types in a number. For this reason I had to implement my own front and backend validations.

The user can enter 4 digits and those are handled as a form with 4 invidiual inputs. I use this same form to update the webpage with the user's guess history as a post method.

## Sessions
A problem I ran into while building this application was that the users game session wasn't private. In other words, if you were playing and someone else went to the website at the same time, they would have your current game scores. To solve this I learned about sessions and how they store unique data on the server for each new visit to the website. Django likes to store information regarding sessions in tables and in order to do this you have to do what is known as a migration.

## Django Models
Django provides us with Models that one can think of as a level of abstraction on top of SQL where we don't have to make direct SQL queries ourselves. It's as easy as creating a class with all the data we want to store, for example, a users id as an integer.

Foreign Keys =  means they refer to another object.
on_delete=models.CASCADE

## Templates
Django has template inheritance, and I was able to create a layout.html that contains the general structure of my project.


## Users
Django makes it very easy to create a login feature for authenticated users, and provides most of the required documentation in its docs. 


create an index on a table to make faster querying, takes time and memory but once it exists
it makes querying way more efficient

create an index on the passengers last name or first name


in the app inside models.py we can define which models will exist

create the migrations on how to manipulate >> python3 manage.py make migrations
take those instructions and apply them to the database >> python3 manage.py migrate

look into foreign keys and on_cascade as well as related name 
from .models import name of models

Did I forget extends layout???


admin app, python3 manage.py createsuperuser
must add models to admin.py



Authentication
- for users to login to logout
- Django has authentication features written already



Using unittest in python and our Django applications
only if the test is comprehensive is the test good to an extent


Ran into an issue with having a the timer reset if the user clicked refresh
Solution was to use local storage, storing information inside a users webbrowser
localStorage.getItem(key) retrieves key
localStorage.setItem(key, value) replaces existing key to value


# Big Picture View
├── manage.py
├── Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── mastergame      <----- MasterGame App
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── helpers.py <----- Helper Functions
|
├── static
│   ├── css
│   └── js  
└── templates  <----- Django Template Files
│   ├── index.html
│   ├── layout.html
│   ├── login.html
│   └── register.html
|   └── settings.html
|
├── Procfile <--- Heroku Requirement




Database Schema's and Data: 

Leaderboards
+----+--------+----------------+
| id |  name  |      score     |
+----+--------+----------------+
| 0  | David  |        1       |
| 1  | Carter |       20       |
| 2  | Emma   |       30       |
+----+--------+----------------+
Notes: id is foreign key to User id

User
+----+------------+---------------------+
| id |  username  |      password       |
+----+------------+---------------------+
| 0  | David      | pbkdf_HASHED        |
| 1  | Carter     | pbsdf_HASHED        |
| 2  | Emma       | psdff_HASHED        |
+----+------------+---------------------+


# Deploying the Site to Heroku
1. First step is to download the Heroku toolbelt so we can deploy the site on the backend (our terminal)
Note: Django web server isn't suitable for production so we need to use Gunicorn (install gunicorn)
2. Django natively uses a SQLite3 database which is not suitable for Heroku
- pip3 install django-heroku( installs psycopg2, a posgres database which replaces SQLite3)
- pip3 install python-decouple
3. Add a file called "Procfile"
- this file tells heroku what kind of app it is, in our case we write "web: gunicorn"
4. We also need a requirement.txt to tell Heroku all our requirements
5. The last step is to tweak some of the settings found in our Django settings.py which can be found in Django's Documentation


# Testing and CI/CD
I wanted to find a method to efficiently and effectively test my code as the project grows. So I began my journey into Test Driven Development.

Python has an assert stament and it turns out that if nothing happens, that's actually a good thing.
ex: assert square(10) == 100 // if nothing happens thats a good thing 

Using pythons unittest library allows us to really quickly test.

I ended up using TestCase which is very similar to unittest and wrote a few tests to make sure that every route in my page works as intented by simulating a get request and that the status code is the status code that we expect.

So far I haven't really tested a user clicking buttons and making sure the page is working as it should.
For this I wanted the ability to have a user play a crazy amount of games and see if the backend could handle that. As I'm writing this, I'm learning about Selenium and how to use a web chrome driver to achieve this.