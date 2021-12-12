from flask import render_template, request, redirect, url_for, session
from flask_login import login_user, logout_user, login_required
import utils
from app.admin import *
from app.model import UserRole
from app import login, app


@app.route("/")
def home():
    return render_template('index.html')

#login method for employee
@app.route('/nhanvien_login', methods=['get', 'post'])
def nhanvien_login():
    error_msg = ""
    if request.method.__eq__('POST'):
        try:
            username = request.form['username']
            password = request.form['password']

            user = utils.check_user(username=username, password=password, role=UserRole.EMPLOYEE)
            if user:
                login_user(user=user)

                return render_template('employee.html')
            else:
                error_msg = "Chuong trinh dang co loi! Vui long quay lai sau!"

        except Exception as ex:
            error_msg = str(ex)

    return render_template('index.html', error_msg=error_msg)

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

@app.route('/logout')
def nhanvien_logout():
    logout_user()

    return redirect(url_for('nhanvien_login'))



if __name__ == '__main__':
    app.run(debug=True)