# NURSERY_WEB_APP
 *techstack used :[python](https://www.python.org/) [flask](https://palletsprojects.com/p/flask/) [mysql](https://www.mysql.com/) [html](https://en.wikipedia.org/wiki/HTML) [css](https://www.w3.org/Style/CSS/Overview.en.html)*

# User Manual For Deployment

## PREREQUISITES
* python-3.6 and newer versions

if python is not installed or if the version is old on your pc follow this  [link](https://www.python.org/downloads/) for the installation.

## CLONING REPOSITORY
create a project folder myproject and clone this repository into the myproject directory

creating project directory  :

    mkdir myproject
    
   changing directory  : 

    cd myproject

cloning this repository  :

    git clone https://github.com/jagadeesh-kethavath-23/NURSERY_WEB_APP.git

## VIRTUAL ENVIRONMENT
Virtual environments are independent groups of Python libraries, one for each project. Packages installed for one
project will not affect other projects or the operating system’s packages.

Python 3 comes bundled with the `venv` module to create virtual environments. If you’re using a modern version of
Python, you can continue on to the next section.

#### creating an environment
change directory to the cloned repository and create `venv` folder as shown

changing directory:

    cd NURSERY_WEB_APP

creating virtualenv:

    python -m venv venv
    

if the above command wont work use this instead


changing directory:

    cd NURSERY_WEB_APP
    
 creating virtualenv:

    py -3 virtual venv venv

### activating environment

    venv\Scripts\activate

## DEPENDENCIES

Open command prompt and use these command lines for the installation of neccessary dependencies

*use these command lines on actived virtual environment*

### Installing dependencies

flask
    
    pip install Flask

mysql and python connector

    pip install mysql-connector-python

mysql client

    pip install mysqlclient

flask and mysql db

    pip install Flask-MySQLdb

## CREATE DATABASE

run the `nursery_db.sql` in mysql workbench

note : *nursery_db.sql file is located inside database directory of this repository*

###  connecting mysql and flask
open app.py file and set mysql connection 

set your mysql credentials into it
```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'set your password'
app.config['MYSQL_DB'] = 'nursery_db'
```
### populating database

Database cannot be empty to as there is no signup option for manager ,admin and delivary boy for security reasons.Whereas manager can add new admins,new managers and new delivery boys

so there should be atleast one manager info inserted into the database

use this query in query tab by selecting the nursery_db database

    INSERT INTO users VALUES('manager','8888888888','male','manager','P@55word#manager#','dvk');

and one bank manager
    
    INSERT INTO users VALUES('bankie','9876543210','male','bankie','P@55word#bankmanager#','dvk');
    

## RUNNING THE APPLICATION
*use these command lines on actived virtual environment*

set flask to work on this application :

    set FLASK_APP=app.py
 
this will active the debugger mode :

    set FLASK_ENV=development

to run application :

    flask run

