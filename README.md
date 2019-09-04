# DESCRIPTION

Maintenance Tracker App is an application that provides users with the ability
to reach out to operations or repairs department regarding repair or maintenance
requests and monitor the status of their request.

[![Build Status](https://travis-ci.org/ssewilliam/maintenance-tracker-with-database.svg?branch=master)](https://travis-ci.org/ssewilliam/maintenance-tracker-with-database) [![Coverage Status](https://coveralls.io/repos/github/ssewilliam/maintenance-tracker-with-database/badge.svg?branch=master)](https://coveralls.io/github/ssewilliam/maintenance-tracker-with-database?branch=master)

## LINK TO Maintance Tracker Github Pages

    https://ssewilliam.github.io/maintenanceTracker/

## Project API endpoint routes

| REQUEST | ROUTE                            | ACTION / FUNCTIONALITY                           |
| ------- | -------------------------------- | ------------------------------------------------ |
| POST    | /auth/signup                     | Registers a user                                 |
| POST    | /auth/login                      | Login a user                                     |
| GET     | /users/requests                  | Fetch all the requests of a logged in user       |
| GET     | /users/requests/:requestId       | Fetch a request that belongs to a logged in user |
| POST    | /users/requests                  | Creates a request                                |
| PUT     | /users/requests                  | Modify a request                                 |
| GET     | /requests/                       | Fetches all requests for admin users only        |
| PUT     | /requests/:requestId/approve     | Approve a request                                |
| PUT     | /requests/:requestId/disapprove  | Disapprove a request                             |
| PUT     | /requests/:requestId/resolve     | Resolve a request                                |
| GET     | /users                           | Fetches all users                                |

## BUILT WITH

- Flask a Python Framework

## LINK TO API ON HEROKU

    https://mtracker-with-database.herokuapp.com/

## LINK TO API DOCUMETATION

    https://maintenancetrackerapi1.docs.apiary.io

## SETTING UP APPLICATION

1. Clone this repository to your computer using

   **`$ git clone https://github.com/ssewilliam/maintenance-tracker-with-database.git`**

2. Install virtualenv, create and activate anew enviromment inside this folder you've cloned
   **`$ virtualenv maintanance-tracker-env`**

   **`$ source maintanance-tracker-env`**

3. Install all project dependencies using

   **`pip3 install -r requirements.txt`**

4. Install postgres on you computer and have access to it

   **`sudo apt-get install postgresql postgresql-contrib`**

   **`sudo -i -u postgres psql`**

5. create a new database and gain access to it with anew user

   **`CREATE DATABASE trackerdb;`**

## RUNNING APPLICATION

- To launch the application, run the following command in your terminal

  **`python run.py`**

- To run tests on the application, run the following command in your terminal

  **`nosetests`**

## Author

SSERUBIRI WILLIAM
