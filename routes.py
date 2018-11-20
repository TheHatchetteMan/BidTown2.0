from app_config import app
from flask import render_template

# @app.context_processor  # use this for loading base.html layout with common elements among views

@app.route("/")
def base():
    return render_template("base.html")