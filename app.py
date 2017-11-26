from flask import Flask
from db import db

import logging


# Instantiate the app
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

# Add logger for sanity check
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# logging.warning(app.config['SQLALCHEMY_DATABASE_URI'])

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()




if __name__ == "__main__":

    app.run()
