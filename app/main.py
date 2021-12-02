from flask import render_template, request, redirect, url_for, session
import utils
from app.admin import *
from app import login
from app import app


@app.route("/")
def home():
    return render_template('index.html')

@login.user_loader
def load_user(user_id):
    pass




if __name__ == '__main__':
    app.run(debug=True)