from app import app, db
from app.model import User, UserRole, Lop, HocSinh, GiaoVien, NhanVien, Diem, MonHoc
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


#  Tinh Trung Binh Diem Cac Mon Hoc Cua Cac Hoc Sinh Lop Bat Ki
# Select SinhVien.MaSV,TenSV,Lop.TenLop, SUM(DiemLan1*SoTrinh)/SUM(SoTrinh) as DiemTrungBinh
#   From SinhVien,Diem,MonHoc,Lop
#    Where SinhVien.MaLop=Lop.MaLop And Diem.MaSV=SinhVien.MaSV And Diem.MaMH=MonHoc.MaMH
#          And TenLop=N'MÁy Tính 3'
#    Group By SinhVien.MaSV,TenSV,Lop.TenLop
def DiemTB(kw='TH6'):
    return db.session.query(HocSinh.IDLop,HocSinh.IDHocSinh, HocSinh.name,
                            func.avg(HocSinh.Diem_HocSinh)) \
        .group_by(HocSinh.IDLop, HocSinh.IDHocSinh, HocSinh.name).all()
    # if kw:
    #     q = q.filter(HocSinh.IDLop.contain(kw))
    #
    # return q.group_by(Lop.TenLop, HocSinh.IDHocSinh, HocSinh.name).all()

def check_user(username, password, role=UserRole.EMPLOYEE):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password),
                             User.user_role.__eq__(role)).first()
def register(name, gender, email, birthday, phone, username, password, role, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    user = User(name=name.strip(), gender=gender, birthday=birthday, phone=phone,
                username=username.strip(),
                password=password,
                email=email.strip() if email else email,
                avatar=avatar, role=role)

    db.session.add(user)

    try:
        db.session.commit()
    except:
        return False
    else:
        return True

def get_user_by_id(user_id):
    return User.query.get(user_id)
