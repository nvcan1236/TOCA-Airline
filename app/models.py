from datetime import datetime
from app import db, app
from sqlalchemy import Column, String, ForeignKey, Float, Boolean, Enum, DateTime, Double
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from enum import Enum as UserEnum


class UserRole(UserEnum):
    ADMIN = 1
    USER = 2


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(String(50), primary_key=True)

    def __str__(self):
        return self.name

class SanBay(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    diaChi = Column(String(50), nullable=False, unique=True)
    chuyenbays = relationship('DungChan', backref='sanbay', lazy=True)
    tuyenbaydis = relationship('TuyenBay', backref='sanbay',lazy=True)
    tuyenabydens = relationship('TuyenBay', backref='sanbay',lazy=True)
    def __str__(self):
        return self.name

class MayBay(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    ghes = relationship('Ghe', backref='maybay')
    chuyenbays = relationship('ChuyenBay', backref='maybay', lazy=True)

    def __str__(self):
        return self.name


class Ghe(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    maybay_id = Column(String(50), ForeignKey(MayBay.id), nullable=False)
    ves = relationship('Ve' , backref='ghe', lazy= True)

    def __str__(self):
        return self.name



class HangVe(BaseModel):
    gia = Column(Float)
    ves = relationship('Ve',backref='hangve' )

    def __str__(self):
        return self.name


class ChuyenBay(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    gioBay = Column(DateTime, default=datetime.now())
    ves = relationship('Ve',backref='chuyenbay', lazy=True)
    maybay_id = Column(String(50), ForeignKey(MayBay.id), nullable=False)
    sanbays = relationship('DungChan', backref='chuyenbay')

    def __str__(self):
        return self

class TuyenBay(BaseModel):
    sanBayKhoiHanh_id = Column(String(50), ForeignKey(SanBay.id), nullable=False)
    sanBayDen_id = Column(String(50), ForeignKey(SanBay.id), nullable=False)
    def __str__(self):
        return self

class DungChan(BaseModel):
    left_id = Column(ForeignKey(SanBay.id), primary_key= True)
    right_id = Column(ForeignKey(ChuyenBay.id), primary_key= True)
    thoiGianDung = Column(Double)

    def __str__(self):
        return self


class NguoiDung(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    phone = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    gioiTinh = Column(String(10), nullable=False)
    taikhoans= relationship('TaiKhoan', backref='nguoidung', lazy=True)
    def __str__(self):
        return self


class NhanVien(NguoiDung):
    chucVu = Column(String(50), nullable=False)
    hoadons = relationship('HoaDon', backref='nhanvien', lazy=True)
    def __str__(self):
        return self


class KhachHang(NguoiDung):
    quocTich = Column(String(50), nullable=False)
    laNguoiLon = Column(Boolean, default=True)
    hoadons = relationship('HoaDon', backref='khachhang', lazy=True)
    def __str__(self):
        return self

class TaiKhoan(db.Model):
    username = Column(String(50), nullable=False, primary_key=True)
    password = Column(String(50), nullable=False)
    role = Column(String(30))
    nguoidung_id =Column(String(30),ForeignKey(NguoiDung.id), nullable=False)
    def __str__(self):
        return self

class HoaDon(BaseModel):
    khachhang_id = Column(String(30),ForeignKey(KhachHang.id), nullable=False)
    nhanvien_id = Column(String(30),ForeignKey(NhanVien.id), nullable=False)
    ves = relationship('Ve' , backref='hoadon', lazy=True)
    def __str__(self):
        return self

class Ve(BaseModel):
    ghe_id = Column(String(50), ForeignKey(Ghe.id), nullable=False)
    hangve_id = Column(String(50), ForeignKey(HangVe.id), nullable=False)
    chuyenbay_id = Column(String(50), ForeignKey(ChuyenBay.id), nullable=False)
    hoadon_id = Column(String(50), ForeignKey(HoaDon.id), nullable=False)
    def __str__(self):
        return self


if __name__ == '__main__':
    with app.app_context():
        db.create_all()


