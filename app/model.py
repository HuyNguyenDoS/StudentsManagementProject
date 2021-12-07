from app import db
from sqlalchemy import Column, Integer, Float, String, Boolean, Enum, ForeignKey, DateTime, Enum, CHAR
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as UserEnum


class UserRole(UserEnum):
    ADMIN = 1
    EMPLOYEE = 2
    TEACHER = 3
    STUDENT = 4

class User(db.Model, UserMixin):
    IDUser = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    avatar = Column(String(100))

    user_role = Column(Enum(UserRole), default=UserRole.EMPLOYEE)

    def __str__(self):
        return self.username

class KyHoc(db.Model):
    IDKyHoc = Column(Integer, primary_key=True, nullable=False)

    IDLop = relationship('Lop', backref='kyhoc', lazy=True)

class Lop(db.Model):
    __tablename__ = 'lop'

    IDLop = Column(CHAR(15), primary_key=True, nullable=False, unique=True)
    TenLop = Column(String(15), nullable=False, unique=True)
    SiSo = Column(Integer)

    IDHocSinh = relationship('HocSinh', backref='lop', lazy=True)

    IDKyHoc = Column(ForeignKey(KyHoc.IDKyHoc))


class MonHoc(db.Model):
    MaMH = Column(CHAR(10), primary_key=True, unique=True)
    TenMH = Column(String(30), nullable=False)

    def __str__(self):
        return self.TenMH

class HocSinh(db.Model):
    IDHocSinh = Column(CHAR(15), primary_key=True, nullable=False, unique=True)
    name = Column(String(50), nullable=False)
    birthday = Column(DateTime, nullable=False)
    address = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    numbers = Column(String(50), nullable=False, unique=True)
    gender = Column(Boolean, nullable=False)
    note = Column(String(100))

    IDLop = Column(ForeignKey(Lop.IDLop))

    Diem_HocSinh = relationship('MonHoc', secondary='diem',lazy='subquery', backref=backref('hocsinh', lazy=True))

    def __str__(self):
        return self.name

Diem = db.Table(
    'diem',
    Column('IDHocSinh', CHAR(15), ForeignKey(HocSinh.IDHocSinh), primary_key=True),
    Column('IDMonHoc', CHAR(10), ForeignKey(MonHoc.MaMH), primary_key=True),
    Column('Diem15pLan1', Integer),
    Column('Diem15pLan2', Integer),
    Column('Diem15pLan3', Integer),
    Column('Diem15pLan4', Integer),
    Column('Diem15pLan5', Integer),

    Column('Diem1TietLan1', Integer),
    Column('Diem1TietLan2', Integer),
    Column('Diem1TietLan3', Integer),

    Column('DiemCuoiKy', Integer),
)

class NhanVien(db.Model):
    IDNhanVien = Column(CHAR(15), primary_key=True, nullable=False, unique=True)
    name = Column(String(50), nullable=False)
    birthday = Column(DateTime, nullable=False)
    address = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    numbers = Column(String(50), nullable=False, unique=True)
    gender = Column(Boolean, nullable=False)
    note = Column(String(100))

    def __str__(self):
        return self.name

class GiaoVien(db.Model):
    IDGiaoVien = Column(CHAR(15), primary_key=True, nullable=False, unique=True)
    name = Column(String(50), nullable=False)
    birthday = Column(DateTime, nullable=False)
    address = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    numbers = Column(String(50), nullable=False, unique=True)
    gender = Column(Boolean, nullable=False)
    note = Column(String(100))

    def __str__(self):
        return self.name

if __name__=='__main__':
    db.create_all()