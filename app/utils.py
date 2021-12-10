from app import app, db
from app.model import User, UserRole, Lop, HocSinh, GiaoVien, NhanVien
from flask_login import current_user
from sqlalchemy import func
from sqlalchemy.sql import extract
import hashlib

def general_stats():
    return db.session.query(Lop.IDLop, Lop.TenLop, func.count(HocSinh.IDHocSinh))\
                      .join(HocSinh, Lop.IDLop.__eq__(HocSinh.IDLop), isouter=True)\
                      .group_by(Lop.IDLop, Lop.TenLop).all()

def hocsinh_stats():
    return db.session.query(func.count(HocSinh.IDHocSinh))\
                        .select_from(HocSinh).all()

def giaovien_stats():
    return db.session.query(func.count(GiaoVien.IDGiaoVien))\
                        .select_from(GiaoVien).all()

def nhanvien_stats():
    return db.session.query(func.count(NhanVien.IDNhanVien))\
                        .select_from(NhanVien).all()

def lop_stats():
    return db.session.query(func.count(Lop.IDLop))\
                        .select_from(Lop).all()

def check_user(username, password, role=UserRole.EMPLOYEE):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password),
                             User.user_role.__eq__(role)).first()

def get_user_by_id(user_id):
    return User.query.get(user_id)