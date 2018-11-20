#   application entry point: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04
#
#   This file serves as the WSGI entry point in a production environment. Routing.py returns app to wsgi.py
from routing import app

if __name__ == "__main__":
    app.run(port='5000', debug=True)