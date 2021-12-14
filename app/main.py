from flask import render_template, request, redirect, url_for, session, flash
from flask_login import login_user, logout_user, login_required
import utils
from app.admin import *
from app.model import UserRole
from app import login, app


@app.route("/")
def home():
    return render_template('login.html')

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

                return render_template('index.html')
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
    else:
        flash("Sai tên đăng nhập hoặc mật khẩu!")

    return redirect('/admin')


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)

@app.route('/logout')
def nhanvien_logout():
    logout_user()

    return redirect(url_for('nhanvien_login'))

# @app.route('/test', methods=['get', 'post'])
# def test():
#     return render_template('test.html')

@app.route('/register', methods=['get', 'post'])
def register():
    error_msg = ""
    if request.method.__eq__('POST'):
        try:
            name = request.form.get('name')
            gender = request.form.get('gender')
            email = request.form.get('email')
            birthday = request.form.get('birthday')
            phone = request.form.get('phone')
            username = request.form.get('username')
            password = request.form.get('password')
            password_confirm = request.form.get('confirm')
            role = request.form.get('account')
            if password.__eq__(password_confirm):
                data = request.form.copy()
                del data['confirm']

                file = request.files['avatar']

                if file:
                    res = cloudinary.uploader.upload(file)
                    data['avatar'] = res['secure_url']
                if role == 'STUDENT':
                    suscess = utils.register(name=name, gender=gender, email=email, birthday=birthday,
                                            phone=phone, username=username, password=password, role="STUDENT")
                    redirect(url_for('nhanvien_login'))
                if role == 'TEACHER':
                    suscess = utils.register(name=name, gender=gender, email=email, birthday=birthday,
                                            phone=phone, username=username, password=password, role="TEACHER")
                    redirect(url_for('nhanvien_login'))
                if role == 'EMPLOYEE':
                    suscess = utils.register(name=name, gender=gender, email=email, birthday=birthday,
                                            phone=phone, username=username, password=password, role="EMPLOYEE")
                    redirect(url_for('nhanvien_login'))
                else:
                    error_msg = "Chuong trinh dang co loi! Vui long quay lai sau!"
        except Exception as ex:
            error_msg = str(ex)

    return render_template('index.html', error_msg=error_msg)


if __name__ == '__main__':
    app.run(debug=True)