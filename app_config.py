#
#   This file deals with Flask App configuration details. Ideally, all configuration details will go here. 
#
from flask import Flask
import os

###################################################################################################
######################################## APPLICATION CONFIGURATION ################################
###################################################################################################

# app = Flask(__name__)  # flask object has underlying configuration capabilities.
# app.secret_key = 'bidtown_session_key'  # set a key for session cookie signing.
# app.secret_key = os.urandom(8)  # set a key for session cookie signing.

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.urandom(8),
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app

app = create_app()
# SECRET_KEY = os.urandom(8)
# app.secret_key = os.urandom(8)