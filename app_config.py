#
#   This file deals with Flask App configuration details. Ideally, all configuration details will go here. 
#
from flask import Flask

###################################################################################################
######################################## APPLICATION CONFIGURATION ################################
###################################################################################################

app = Flask(__name__)  # create flask object. object has underlying configuration capabilities.
app.secret_key = 'bidtown_session_key'  # set a key for session cookie signing.
