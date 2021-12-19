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
                error_msg = "Sai tên đăng nhập hoặc mật khẩu!"

        except Exception as ex:
            error_msg = str(ex)

    return render_template('login.html', error_msg=error_msg)

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

    return redirect(url_for('home'))

@app.route('/register', methods=['get', 'post'])
def register():
    error_msg = ""
    if request.method.__eq__('POST'):
        try:
            name = request.form['name']
            username = request.form['username']
            password = request.form['password']
            confirm = request.form['confirm']
            gender = request.form['gender']
            birthday = request.form['birthday']
            numbers = request.form['numbers']
            role = request.form['role']
            email = request.form['email']
            # avatar = request.form['avatar']
            avatar='test'

            if password.__eq__(confirm):
                # data = request.form.copy()
                # del data['confirm']
                # file = request.files['avatar']
                # res = cloudinary.uploader.upload(file)
                # avatar = res['secure_url']
                if role.__eq__('EMPLOYEE'):
                    if (utils.register(name=name, gender=gender, email=email, birthday=birthday, numbers=numbers,
                                       username=username, password=password, role=role, avatar=avatar)):
                        error_msg = "Successful"
                        return render_template('nhanvien_register.html', error_msg=error_msg)
                    else:
                        error_msg = "Failed"
                        return render_template('nhanvien_register.html', error_msg=error_msg)
                if role.__eq__('TEACHER'):
                    if (utils.register(name=name, gender=gender, email=email, birthday=birthday, numbers=numbers,
                                       username=username, password=password, role=role, avatar=avatar)):
                        error_msg = "Successful"
                        return render_template('nhanvien_register.html', error_msg=error_msg)
                    else:
                        error_msg = "Failed"
                        return render_template('nhanvien_register.html', error_msg=error_msg)
                if role.__eq__('STUDENT'):
                    if (utils.register(name=name, gender=gender, email=email, birthday=birthday, numbers=numbers,
                                       username=username, password=password, role=role, avatar=avatar)):
                        error_msg = "Successful"
                        return render_template('nhanvien_register.html', error_msg=error_msg)
                    else:
                        error_msg = "Failed"
                        return render_template('nhanvien_register.html', error_msg=error_msg)
            else:
                error_msg = "Password incorrect!!!"
        except Exception as ex:
            error_msg = str(ex)

    return render_template('nhanvien_register.html', error_msg=error_msg)

@app.route('/regiter_hocsinh', methods=['get', 'post'])
def regiter_hocsinh():
    error_msg = ""
    if request.method.__eq__('POST'):
        try:
            IDHocSinh = request.form['IDHocSinh']
            name = request.form['name']
            username = request.form['username']
            password = request.form['password']
            confirm = request.form['confirm']
            gender = request.form['gender']
            birthday = request.form['birthday']
            numbers = request.form['numbers']
            lop = request.form['lop']
            email = request.form['email']
            note = request.form['note']
            address = request.form['address']
            avatar = 'test'

            if password.__eq__(confirm):
                if (utils.register_hocsinh(IDHocSinh=IDHocSinh, name=name, gender=gender, email=email, birthday=birthday,
                                           numbers=numbers, username=username, password=password, avatar=avatar, lop=lop,
                                            note=note, address=address)):
                        error_msg = "Successful"
                        return render_template('hocsinh_register.html', error_msg=error_msg)
                else:
                        error_msg = "Failed"
                        return render_template('hocsinh_register.html', error_msg=error_msg)
            else:
                error_msg = "Password incorrect!!!"
        except Exception as ex:
            error_msg = str(ex)

    return render_template('hocsinh_register.html', error_msg=error_msg, lop=utils.ds_lop())


if __name__ == '__main__':
    app.run(debug=True)
