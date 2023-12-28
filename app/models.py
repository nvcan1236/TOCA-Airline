from datetime import datetime
from app import db, app
from sqlalchemy import Column, String, ForeignKey, Float, Boolean, Enum, DateTime
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from enum import Enum as MyEnum


class UserRole(MyEnum):
    CUSTOMER = 1
    EMPLOYEE = 2
    ADMIN = 3


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(String(50), primary_key=True)

    def __str__(self):
        return self.name


class SanBay(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    diaChi = Column(String(50), nullable=False, unique=True)
    tramdungs = relationship('DungChan', backref='sanbay', lazy=True)
    tuyenbaydis = relationship('TuyenBay', backref='sanbaydi', lazy=True, foreign_keys='TuyenBay.sanBayKhoiHanh_id')
    tuyenabydens = relationship('TuyenBay', backref='sanbayden', lazy=True, foreign_keys='TuyenBay.sanBayDen_id')

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
    ves = relationship('Ve', backref='ghe', lazy=True)

    def __str__(self):
        return self.name


class HangVe(BaseModel):
    name = Column(String(100), nullable=False)
    gia = Column(Float)
    quyenloi = Column(String(500))
    ves = relationship('Ve', backref='hangve')

    def __str__(self):
        return self.name


class TuyenBay(BaseModel):
    sanBayKhoiHanh_id = Column(String(50), ForeignKey(SanBay.id), nullable=False)
    sanBayDen_id = Column(String(50), ForeignKey(SanBay.id), nullable=False)
    chuyenbays = relationship('ChuyenBay', backref='tuyenbay', lazy=True)


class ChuyenBay(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    gioBay = Column(DateTime, default=datetime.now())
    gia = Column(Float)
    tuyenbay_id = Column(String(50), ForeignKey(TuyenBay.id), nullable=False)
    ves = relationship('Ve', backref='chuyenbay', lazy=True)
    maybay_id = Column(String(50), ForeignKey(MayBay.id), nullable=False)
    tramdungs = relationship('DungChan', backref='chuyenbay', lazy=False)


class DungChan(BaseModel):
    sanbay_id = Column(ForeignKey(SanBay.id), primary_key=True)
    chuyenbay_id = Column(ForeignKey(ChuyenBay.id), primary_key=True)
    thoiGianDung = Column(Float)


class NguoiDung(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    phone = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    gioiTinh = Column(String(10), nullable=False)
    taikhoans = relationship('TaiKhoan', backref='nguoidung', lazy=True)

    def __str__(self):
        return self


class NhanVien(NguoiDung):
    chucVu = Column(String(50), nullable=False)
    hoadons = relationship('HoaDon', backref='nhanvien', lazy=True, foreign_keys='HoaDon.nhanvien_id')



class KhachHang(NguoiDung):
    quocTich = Column(String(50), nullable=False)
    laNguoiLon = Column(Boolean, default=True)
    hoadons = relationship('HoaDon', backref='khachhangtt', lazy=True, foreign_keys='HoaDon.khachhang_id')
    ves = relationship('Ve', backref='khachhangdi', lazy=True, foreign_keys='Ve.khachhang_id')


class TaiKhoan(db.Model, UserMixin):
    username = Column(String(50), nullable=False, primary_key=True)
    password = Column(String(50), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER)
    nguoidung_id = Column(String(30), ForeignKey(NguoiDung.id), nullable=False)



class HoaDon(BaseModel):
    khachhang_id = Column(String(30), ForeignKey(KhachHang.id), nullable=False)
    nhanvien_id = Column(String(30), ForeignKey(NhanVien.id), nullable=False)
    ves = relationship('Ve', backref='hoadon', lazy=True)


class Ve(BaseModel):
    ghe_id = Column(String(50), ForeignKey(Ghe.id), nullable=False)
    ghetrong = Column(Boolean, default=True)
    hangve_id = Column(String(50), ForeignKey(HangVe.id), nullable=False)
    chuyenbay_id = Column(String(50), ForeignKey(ChuyenBay.id), nullable=False)
    hoadon_id = Column(String(50), ForeignKey(HoaDon.id), nullable=False)
    khachhang_id = Column(String(50), ForeignKey(KhachHang.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
