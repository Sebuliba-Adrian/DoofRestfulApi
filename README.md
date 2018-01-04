[![Build Status](https://travis-ci.org/Sebuliba-Adrian/DoofRestfulApi.svg?branch=master)](https://travis-ci.org/Sebuliba-Adrian/DoofRestfulApi?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/Sebuliba-Adrian/DoofRestfulApi/badge.svg?branch=master)](https://coveralls.io/github/Sebuliba-Adrian/DoofRestfulApi?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ed3fb4470ef140e68783a24de2d426ae)](https://www.codacy.com/app/Sebuliba-Adrian/DoofRestfulApi?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Sebuliba-Adrian/DoofRestfulApi&amp;utm_campaign=Badge_Grade)
[![Code Health](https://landscape.io/github/Sebuliba-Adrian/DoofRestfulApi/master/landscape.svg?style=flat)](https://landscape.io/github/Sebuliba-Adrian/DoofRestfulApi/master)
[![Maintainability](https://api.codeclimate.com/v1/badges/e2975d655ca0fb0fc8be/maintainability)](https://codeclimate.com/github/Sebuliba-Adrian/DoofRestfulApi/maintainability)

# DoofRestfulApi

This is an API version 1.0 for the recipes api called "DOOF" designed using the flask microframework in python

### Live demo
coming soon!

### Set Up
You should have [git](https://git-scm.com/), [python](https://docs.python.org/), [pip](https://pypi.python.org/pypi/pip), [postgresql](https://www.postgresql.org/), [virtualenv](https://virtualenv.pypa.io/en/stable/) installed
##### These instructions are specific to a linux, macOS or and windows based machine
1. Open your terminal/commandline
2. Clone the project using `git clone https://github.com/sebuliba-adrian/DoofRestfulApi`
3. Change to the project directory using `cd DoofRestfulApi`
4. Create a virtual environment for the project using the command `virtualenv venv` and start it using `source venv/bin/activate` for unix or `venv\Scripts\activate`  and using the command `deactivate` to stop the virtual environment
5. Install dependencies using `pip install -r requirements.txt`
6. You can run tests using the command `nose2 --with-cov --coverage tests`
7. To launch the application you should first apply migrations in order to create the database whose process is shown below
8. Run the application using `python run.py`
10. Access to the api documentation  `coming soon!`


### Setup Database:

Install postgres: ```brew install postgresql```

1. ```Type psql in terminal.```

2. ```On postgres interactive interface, type CREATE DATABASE develop_db;```

3. ```Create a user, type; CREATE USER username WITH PASSWORD 'password' ```

4. ```Edit the /config/config.py with the created username and password from step3 above. ```


### Command for  applying migrations to database

```sh
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
$ python manage.py db --help
```

### Run the server
 ```python run.py```


### Specifications for the API are shown below

||Method | Endpoint | Description |
| ---- | ---- | --------------- |
|POST| `/api/v1/auth/register` |  Register a user. |
|POST| `/api/v1/auth/login` | Login user.|
|POST| `/api/v1/auth/logout` | Logout a user.|
|PUT| `/api/v1/auth/reset` | Reset user password.|
|POST| `/api/v1/categories/` | Create a new category. |
|GET| `/api/v1/categories/` | Retrieve all the created categories. |
|GET| `/api/v1/categories/<category_id>` | Get a single category. |
|PUT| `/api/v1/categories/<category_id>` | Update a single category. |
|DELETE| `/api/v1/categories/<category_id>` | Delete single category. |
|POST| `/api/v1/categories/<category_id>/recipes` | Add a new recipe to this category. |
|PUT|`/api/v1/categories/<category_id>/recipes/<recipe_id>` | Update this recipe. |
|DELETE|`/api/v1/categories/<category_id>/recipes/<recipe_id>` | Delete this single recipe. |
|GET| `/api/v1/categories?limit=10&page=1` | Pagination to get 10 category records.|
|GET| `/api/v1/categories?q=a category` | Search for categories with name like a category. 
Others specs coming soon