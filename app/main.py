from flask import render_template, request, redirect, url_for, session
from flask_login import login_user, logout_user, login_required
import utils
from app.admin import *
from app.model import UserRole
from app import login, app


@app.route("/")
def home():
    return render_template('index.html')


# Login method for admin, page admin
@app.route('/admin-login', methods=['post'])
def admin_login():
    username = request.form['username']
    password = request.form['password']

    user = utils.check_user(username=username,
                            password=password,
                            role=UserRole.ADMIN)
    if user:
        login_user(user=user)

    return redirect('/admin')


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)





if __name__ == '__main__':
    app.run(debug=True)