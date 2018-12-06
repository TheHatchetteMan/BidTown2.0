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
    app = Flask(__name__)

    return app

app = create_app()
# SECRET_KEY = os.urandom(8)
app.secret_key = os.urandom(8)