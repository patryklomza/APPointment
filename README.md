#APPointment app documentation
========

Welcome to APPointment, my first web application written with 
Python Flask framework.

This project is a very simple scheduler for your business' customers.
It aims to help your customers effortlessly schedule an appointment 
with you, or your employees. 


##Features
========

- Register new users
- Login users to their unique profiles
- Customers can make new appointments or cancel existing ones 
- You can set a user as Admin, which can look up all the visits of your customers

##For developers
========

Application uses: 

**Python 3.7.3** 
**Flask 1.0.3**
**Werkzeug 0.15.4**

**All necessary dependencies with their versions are also available in the requirements.txt file.**

**Make sure you have proper Python version and *pip* installed**

Run following command to install all dependencies from requirements.txt file:

`pip install -r requirements.txt`


Application uses following extensions:

**Python-Dotenv** - allows environment variables saved in .flaskenv file to be automatically imported when you run the `flask` command

Link to Documentation: <TODO>

*Installation:*
`(venv) $ pip install python-dotenv`

**Flask-WTF** - handles the web forms in this application. It is a wrapper around the WTForms package that integrates it with Flask.

*Installation:*
`(venv) $ pip install flask-wtf`

Link to Documentation: <TODO>

**Flask-Login** - manages the user logged-in state, so that for example users can log in to the application and then navigate to different pages while the application "remembers" that the user is logged in. It also provides the "remember me" functionality that allows users to remain logged in even after closing the browser window

*Installation:*
`(venv) $ pip install flask-login`

Link to Documentation: <TODO>

**Flask-Bootstrap** -  provides a ready to use base template that has the Bootstrap framework installed

*Installation:*
`(venv) $ pip install flask-bootstrap`

Link to Documentation: <TODO>

**Flask-SQLAlchemy** - provides a Flask-friendly wrapper to the SQLAlchemy package, which is an Object Relational Mapper

*Installation:*
`(venv) $ pip install flask-sqlalchemy`

Link to Documentation: <TODO>

**Flask-Migrate** - Flask wrapper for Alembic, a database migration framework for SQLAlchemy

*Installation:*
`(venv) $ pip install flask-migrate`

Link to Documentation: < TODO >

##Starting Application on MacOS Mojave 0.14.5 

To run this applicaton:

-1- In the terminal make sure you are in the `appoinment` directory (contains all necessary files)

-2- Use following commands to start the application server:

`export FLASK_APP=microblog.py`
`flask run`

-3- Now application should be accessible in a browser of your choice at the following address:

`http://127.0.0.1:5000/`

-*- Alternatively you can run **appointment.py** script to start the application server:

`python appointment.py`


##Setting Database

*Waiting for update*

Contribute
*Waiting for update*

Support
*Waiting for update*

##List of features to implement:
< TODO >


If you are having issues, please let me know at lomza.patryk@gmail.com 


