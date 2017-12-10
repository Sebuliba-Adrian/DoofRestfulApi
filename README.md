[![Build Status](https://travis-ci.org/Sebuliba-Adrian/DoofRestfulApi.svg?branch=master)](https://travis-ci.org/Sebuliba-Adrian/DoofRestfulApi?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/Sebuliba-Adrian/DoofRestfulApi/badge.svg?branch=master)](https://coveralls.io/github/Sebuliba-Adrian/DoofRestfulApi?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ed3fb4470ef140e68783a24de2d426ae)](https://www.codacy.com/app/Sebuliba-Adrian/DoofRestfulApi?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Sebuliba-Adrian/DoofRestfulApi&amp;utm_campaign=Badge_Grade)
[![Code Health](https://landscape.io/github/Sebuliba-Adrian/DoofRestfulApi/master/landscape.svg?style=flat)](https://landscape.io/github/Sebuliba-Adrian/DoofRestfulApi/master)
[![Maintainability](https://api.codeclimate.com/v1/badges/e2975d655ca0fb0fc8be/maintainability)](https://codeclimate.com/github/Sebuliba-Adrian/DoofRestfulApi/maintainability)

# DoofRestfulApi

This is an API for a recipes api called "DOOF" designed using flask framework for python

### Live demo
coming soon!

### Set up
You should have [git](https://git-scm.com/), [python](https://docs.python.org/), [pip](https://pypi.python.org/pypi/pip), [sqlite3](https://www.sqlite.org/), [virtualenv](https://virtualenv.pypa.io/en/stable/) installed
##### These instractions are specific to a linux or unix and windows based machine
1. Open your terminal
2. Clone the project using `git clone https://github.com/sebuliba-adrian/DoofRestfulApi`
3. Change to the project directory using `cd DoofRestfulApi`
4. Create a virtual environment for the project using the command `virtualenv venv` and start it using `source venv/bin/activate` for unix or `venv\Scripts\activate`  and using the command `deactivate` to stop the virtual environment
5. Install packages using `pip install -r requirements.txt`
6. You can run tests using the command `nose2 --with-cov --coverage tests`
7. To launch the application you should first apply migrations in order to create the database whose process is shown below
8. Run the application using `python manage.py runserver or python app.py`
10. Access to the api documentation  `coming soon!`



### Command for creation of the database and applying migrations to it

```sh
$ python manage.py create_db
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
$ python manage.py db --help
```


### Specifications for the API are shown below

| EndPoint | Functionality | Public Access |
| -------- | ------------- | ------------- |
| [ POST /login ](#) | Logs a user in | FALSE |
| [ POST /register ](#) | Register a user | FALSE |
| [ POST /category/\<name> ](#) | Create a new recipe category | TRUE |
| [ GET /categories/ ](#) | List all the created recipe categories | TRUE |
| [ GET /category/\<name> ](#) | Get single recipe category | TRUE |
| [ DELETE /category/\<name> ](#) | Delete this single recipe category | TRUE |
| [ POST /recipe/\<name> ](#) | Create a new recipe | TRUE |
| [ GET /recipies/ ](#) | List all the created recipes | TRUE |
| [ PUT /recipe/\<name> ](#) | Update a recipe | TRUE |
| [ DELETE /recipe/\<name> ](#) | Delete a recipe | TRUE |

Others specs coming soon