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
views.py contains a number of different views and can be thought of as what the user might like to see. These functions can take in a request and return for example a HttpResponse. We then associate each view with a specific URL in our urls.py. urls.py contains all the possible views that the user may visit on our site. There are different routes the user can go to including the register page, login, leaderboards and settings. 

The main route is the index page which contains the main game. Here the user can try to guess the correct 4 digit number before exhausting the 10 attempts available to them. While there is a lot of client side validation including a feature that auto tabs after a user types in a number of length > 0, I also have server side validation just in case the user is using an outdated browser or something weird happens.

At the very bottom, I've also included a table. The information for this table is generated in the server by storing it in the users sessions.

I use request.session['var_name'] to generate information that can then be filled using the server and extracted client side.

If you take a look at my index function, I've also implemented two pathways, one for a guest user and the other for those logged in users.

## Forms
Django has a feature known as Django forms that creates an even easier method of collecting user information. One of the advantages of this feature is that it does client side and server side validation. I decided not to go this route because I wanted the ability to manipulate the DOM using JavaScript and add features like auto tabbing when the user types in a number. For this reason I had to implement my own front and backend validations.

This brings me to the add function in views.py. This function handles what happens when the user enters 4 digits and is a form with a request of method POST. This function also depends on my global variable API_CALL as a way to check if the RANDOM Numbers API has yet been called. I do this so as to not change the number generated for the current game session. I later implement a feature that resets the API_CALL to false, if the user chooses to reset the game so as to generate a new number.

The most important thing that happens in my add function is checking user input against API number and generating feedback. For this I use several if conditions to check the numbers and generate the appropriate response such as "Well done!" or "Your guess was incorrect :(". 

The final step is to return the gathered information back to the user with a simple return and sending the appropriate message as well. 

## Sessions
A problem I ran into while building this application was that the users game session wasn't private. In other words, if you were playing and someone else went to the website at the same time, they would have your current game scores. To solve this I learned about sessions and how they store unique data on the server for each new visit to the website. Django likes to store information regarding sessions in tables and in order to do this you have to do what is known as a migration. We create the migrations on how to manipulate the database by running "python3 manage.py makemigrations" and take those instructions and apply them to the database using "python3 manage.py migrate". 

## Django Models
Django provides us with Models that one can think of as a level of abstraction on top of SQL where we don't have to make direct SQL queries ourselves. It's as easy as creating a class with all the data we want to store, for example, a users id as an integer.

This is one feature that I have yet to implement for my project and the idea is to use login feature to record a users score/scores throughout time and update the leaderboards accordingly.

## Templates
Django has template inheritance, and I was able to create a layout.html that contains the general structure of my project. I also tried to get creating and make my website more appealing by using Bootstrap to generate dynamic messages. 

## Users
Django makes it very easy to create a login feature for authenticated users, and provides most of the required documentation in its docs. 

For future use, I'd like to create an index on a table to make faster querying. I am aware that it takes time and memory but once it exists
it makes querying way more efficient. 


## Remaining Bugs
I keep running into an issue with having the timer reset if the user clicks refresh. I tried to use local storage, such as storing information inside a users webbrowser but it doesn't seem to work. I will try to find a method to perhaps start and stop a timer on the server if necessary.



# Big Picture View
```bash
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

```

# Future Database Schemas

```bash
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
```

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

At the end of the day, a test is as good as how comprehensive it is.


# Reflection
This project gave me an appreciation for all those cool looking websites :) 