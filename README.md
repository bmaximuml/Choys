# Choys

[![Build Status](https://travis-ci.com/benjilev08/Choys.svg?token=y1QpyeyoJ4P5i7MEt1gp&branch=master)](https://travis-ci.com/benjilev08/Choys)

This is a [Flask](https://flask.palletsprojects.com/en/1.1.x/) application for comparing different locations within the UK.

## Installation

### Pre-Install
You will first need to install *git* and *Python 3*.

* To install git, follow the instructions [here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

* To install Python 3, follow the instructions [here](https://wiki.python.org/moin/BeginnersGuide/Download)

You will also need a database. Currently, the only supported database system is PostgreSQL 11.

To connect to PostgreSQL, this application uses the _psycopg2_ package. This requires the _pg\_config_ program, which can be installed from the _libpq-dev_ package.
* To install _libpq-dev_, run `apt-get install libpq-dev`.

#### Installing and setting up PostgreSQL 11
To install PostgreSQL 11 on Ubuntu 19.04, follow the instructions below.

To install PostgreSQL 11 on other distributions, follow the instructions [here](https://www.postgresql.org/download/), and then follow the steps below.  
1. `sudo apt update`
2. `sudo apt install postgresql-11 postgresql-server-dev-11`
3. Edit the file `/etc/postgresql/11/main/pg_hba.conf`, to change the second uncommented line from:
    `local   all             all                                     peer`
    to
    `local   all             all                                     md5`  
4. `pg_ctlcluster 11 main start`
    Start the database server
5. `sudo su -c "psql -c '\password postgres'" postgres`
    Set the password for the default postgres user
6. `sudo su -c "psql -c 'CREATE ROLE <username> SUPERUSER LOGIN CREATEDB;'" postgres`
    Create a new database user to manage the database, replacing `<username>` with your desired username.
7. `sudo su -c "psql -c 'CREATE DATABASE <username>;'" postgres`
    Create a database for your new user
8. `sudo su -c "psql -c '\password <username>'" postgres`
    Set the password for the new user you have created
9. `psql -c 'create database locations;' -U <username> -W`
    Create a database called *locations* using the newly created user, replacing `<username>` with the username you specified in the previous step
10. `psql locations < schema.sql -U <username>`
    Load the schema for the site into the created database. You will need to have cloned the repository before you can load the schema 


### Install
1. `git clone https://github.com/benjilev08/Choys`
2. `cd Choys`
3. `pip3 install .`

### Setup

In order to use the [Google Maps Distance Matrix API](https://developers.google.com/maps/documentation/distance-matrix/intro), an appropriate API key must be set in the environment variable `GMAPI`. 

A connection to your database must be configured in order for the application to work.
There are two environment variables available for this purpose; `DATABASE_URL` and `TEST_DATABASE_URL`. 
`TEST_DATABASE_URL` allows an alternative database to be used when testing.
`DATABASE_URL` is the database to be used at all other times.

* `psql locations < test/data.sql -U <username>`
    Load in a set of data for testing
* `export DATABASE_URL=<database_url>`
    Set the URL for the database
* `export DATABASE_URL='postgresql:///locations'`
    Set the URL for the database to be a local postgres database called locations
* `export GMAPI=<API_KEY>`
    Set the Google Maps Distance Matrix API key
* `export FLASK_SECRET_KEY=<secret_key>`
    Set a secret key to be used by Flask. This must be set in order for the application to function. More detail on the Flask secret key can be found in [the Flask docs](https://flask.palletsprojects.com/en/1.1.x/quickstart/#sessions).
* `export FLASK_APP=flaskr`,
    Specify the directory to be targeted by the Flask development web server
* `export FLASK_ENV=development` 
    Set the environment to development to use the Flask development web server 
    
## Usage
* `flask run`
    Start a development web server to host the website locally on port 5000
* `flask shell`
    Enter a Python terminal in the context of the application

It is not recommended to use Flask's development server in a production environment.
See [the Flask docs](https://flask.palletsprojects.com/en/1.1.x/deploying/#deployment) for more information on deploying a Flask-based application.

## Editing

This template uses SASS. After making changes to `static/sass/sass_styles.scss`,
run the command `sass --no-source-map sass/sass_styles.scss:sass_styles.css` to
regenerate the `static/sass_styles.css` file, which is looked at by the
application.

To run these commands, you will first need to install SASS.
SASS installation instructions can be found [here](https://sass-lang.com/install).
