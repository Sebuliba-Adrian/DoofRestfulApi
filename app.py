from flask import Flask
import logging

#Instantiate the app 
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
#Add logger for sanity check
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.warning(app.config['SQLALCHEMY_DATABASE_URI'])


if __name__ == "__main__":
    app.run()
