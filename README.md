[![Build Status](https://travis-ci.org/Sebuliba-Adrian/DoofRestfulApi.svg?branch=master)](https://travis-ci.org/Sebuliba-Adrian/DoofRestfulApi?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/Sebuliba-Adrian/DoofRestfulApi/badge.svg?branch=master)](https://coveralls.io/github/Sebuliba-Adrian/DoofRestfulApi?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ed3fb4470ef140e68783a24de2d426ae)](https://www.codacy.com/app/Sebuliba-Adrian/DoofRestfulApi?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Sebuliba-Adrian/DoofRestfulApi&amp;utm_campaign=Badge_Grade)
[![Code Health](https://landscape.io/github/Sebuliba-Adrian/DoofRestfulApi/master/landscape.svg?style=flat)](https://landscape.io/github/Sebuliba-Adrian/DoofRestfulApi/master)
[![Maintainability](https://api.codeclimate.com/v1/badges/e2975d655ca0fb0fc8be/maintainability)](https://codeclimate.com/github/Sebuliba-Adrian/DoofRestfulApi/maintainability)

# DoofRestfulApi

This is an API version 1.0 for the recipes api called "DOOF" designed using the flask microframework in python

### Live demo
[https://doofrecipeapi.herokuapp.com/apidocs](https://doofrecipeapi.herokuapp.com/apidocs)


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
10. You can access the api documentation at 
`http://localhost:5000/apidocs`


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

| EndPoint | Functionality | Public Access |
| -------- | ------------- | ------------- |
| [ POST /auth/login ](#) | Logs a user in | TRUE |
| [ POST /auth/register ](#) | Register a user | TRUE |
| [ POST /auth/logout ](#) | Logs a user out | FALSE |
| [ POST /categories/ ](#) | Create a new category list | FALSE |
| [ GET /categories/ ](#) | List all the created categories | FALSE |
| [ GET /categories/\<category_id> ](#) | Get single category | FALSE |
| [ PUT /categories/\<category_id> ](#) | Update this category | FALSE |
| [ DELETE /categories/\<category_id> ](#) | Delete this single category | FALSE |
| [ POST /categories/\<category_id>/recipes ](#) | Create a new recipe category | FALSE |
| [ PUT /categories/\<category_id>/recipes/<recipe_id> ](#) | Update a recipe | FALSE |
| [ DELETE /categories/\<category_id>/recipes/<recipe_id> ](#) | Delete a recipe in a category | FALSE |
| [ GET /categories?limit=<number> ](#) | Gets a number of categories relative to the value passed in number. Maximum records is 100 | FALSE |
| [ GET /categories?q=\<category_name> ](#) | Search for category with the same name as that passed in category_name | FALSE |

Others specs coming soon