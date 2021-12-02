from flask_admin import BaseView, expose, AdminIndexView, Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user, current_user
from flask import redirect
from app import db, app, utils
from app.model import Lop, HocSinh, Diem, MonHoc

admin = Admin(app=app, name="QuanLyHocSinh", template_mode="bootstrap4")

admin.add_view(ModelView(HocSinh, db.session, name='Hoc Sinh'))