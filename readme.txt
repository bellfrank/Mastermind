one project may have multiple applications, we are going to make a mastergame applicaiton
django has a urls.py that works for the entire project but we would like one
for our indivdual app

installed pytz for pacific time zone

Django uses SQLite, stores as a file
SQLite Types
TEXT 
NUMERIC
INTEGER
REAL
BLOB

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


Overview
├── manage.py
├── Django
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── mastergame      <----- mastergame app
│   ├── __init__.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── assets     <----- our front-end project source
│   ├── javascript
│   └── styles
├── static     <----- our front-end project outputs (and other Django static files)
│   ├── css
│   ├── images
│   └── js  
└── templates  <----- our Django template files
    └── myapp





Adding a timer feature using REACT ( React, ReactDOM, Babel(translate JSX to plain JS that browsers can understand) 


Testing and CI/CD
a method to efficiently and effectively test my code as the project grows, Test Driven Development
uses docstring to send message 

Using Assert: 
ex: assert square(10) == 100 // if nothing happens thats a good thing 

Using pythons unittest library allows us to really quickly test
import unittest
class Tests(unittest.TestCase):
    def test_1(self):
    self.assertFalse(is_prime(1))

if __name__ = "__main__":
    unittest.main()


I ended up using TestCase which is very similar to unittest and wrote a few tests
to make sure that every route in my page works as intented by simulating a get request and 
that the status code is the status code that we expect

So far I haven't really tested a user clicking buttons and making sure the page is working as it should
For this I wanted the ability to have a user play a crazy amount of games and see if the backend could handle that
I went with Selenium as my framework

This required using googles web chrome driver
pip install chromedriver-py and selenium





Deploying the Site :)
I ended up going with Heroku's free tier for this
I was considering buying a domain but its $12 and I don't have a job :( so...
First step is to download the Heroku toolbelt so we can deploy the site on the backend, aka our terminal
Django web server isn't suitable for production so we need to use Gunicorn (pip3 install gunicorn)
pip3 install django-heroku( installs psycopg2, a posgres database...)
sqlite3 database isn't suitable for Heroku and we need a different database, reason for ^^
pip3 install python-decouple
Procfile tells heroku what kind of app it is( web: gunicorn
we need a requirement.txt to tell Heroku our requirements
Modify settings.py file
