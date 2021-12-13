from flask_admin import BaseView, expose, AdminIndexView, Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user, current_user
from flask import redirect, request
from app import db, app, utils
from app.model import Lop, HocSinh, Diem, MonHoc, UserRole, User
from datetime import datetime

class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated

class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):

        return self.render('admin/index.html',
                           hocsinh_stats=utils.hocsinh_stats(),
                           giaovien_stats=utils.giaovien_stats(),
                           lop_stats=utils.lop_stats(),
                           nhanvien_stats=utils.nhanvien_stats())

class StatsViewDiem(BaseView):
    @expose('/')
    def index(self):
        kw = request.args.get('kw')
        return self.render('admin/lop_stats.html',
                           kw=kw,
                           stats=utils.general_stats(),
                           diemtb=utils.DiemTB())


admin = Admin(app=app, name="QuanLyHocSinh", template_mode="bootstrap4", index_view=MyAdminIndex())


admin.add_view(AuthenticatedModelView(HocSinh, db.session, name='Toàn Học Sinh'))
admin.add_view(AuthenticatedModelView(Lop, db.session, name='Lớp'))
admin.add_view(AuthenticatedModelView(User, db.session, name='User'))
# admin.add_view(AuthenticatedModelView(Diem, db.session, name='Diem'))
admin.add_view(StatsViewDiem(name='Stats Diem'))
admin.add_view(LogoutView(name='Logout'))
