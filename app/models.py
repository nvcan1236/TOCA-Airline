from datetime import datetime
from app import db, app
from sqlalchemy import Column, String, ForeignKey, Float, Boolean, Enum, DateTime, Integer
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from enum import Enum as MyEnum


class UserRole(MyEnum):
    CUSTOMER = 1
    EMPLOYEE = 2
    ADMIN = 3


class GenderEnum(MyEnum):
    NAM = 1
    NU = 2
    OTHER = 3


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


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
    chuyenbays = relationship('ChuyenBay', backref='maybay', lazy=True)

    def __str__(self):
        return self.name


class TuyenBay(BaseModel):
    sanBayKhoiHanh_id = Column(Integer, ForeignKey(SanBay.id), nullable=False)
    sanBayDen_id = Column(Integer, ForeignKey(SanBay.id), nullable=False)
    chuyenbays = relationship('ChuyenBay', backref='tuyenbay', lazy=True)
    def __str__(self):
        return self.sanbaydi.name + ' - ' + self.sanbayden.name


class ChuyenBay(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    gioBay = Column(DateTime, default=datetime.now())
    gia = Column(Float)
    tuyenbay_id = Column(Integer, ForeignKey(TuyenBay.id), nullable=False)
    ves = relationship('Ve', backref='chuyenbay', lazy=False)
    ghes = relationship('Ghe', backref='chuyenbay', lazy=True)
    maybay_id = Column(Integer, ForeignKey(MayBay.id), nullable=False)
    tramdungs = relationship('DungChan', backref='chuyenbay', lazy=True)

    def __str__(self):
        return self.name


class HangVe(BaseModel):
    name = Column(String(100), nullable=False)
    gia = Column(Float, nullable=False)
    quyenloi = Column(String(500))
    ghes = relationship('Ghe', backref='hangve', lazy=True)
    ves = relationship('Ve', backref='hangve', lazy=True)

    def __str__(self):
        return self.name


class Ghe(BaseModel):
    chuyenbay_id = Column(Integer, ForeignKey(ChuyenBay.id), nullable=False)
    hangve_id = Column(Integer, ForeignKey(HangVe.id), nullable=False)
    so_luong = Column(Integer, default=True)

    def __str__(self):
        return self.name


class DungChan(BaseModel):
    sanbay_id = Column(ForeignKey(SanBay.id), primary_key=True)
    chuyenbay_id = Column(ForeignKey(ChuyenBay.id), primary_key=True)
    thoiGianDung = Column(Float)


class Nguoi(BaseModel):
    name = Column(String(50), nullable=False)
    phone = Column(String(50),  unique=True)
    email = Column(String(50),  unique=True)
    ngay_sinh = Column(DateTime)
    gioi_tinh = Column(Enum(GenderEnum), default=GenderEnum.NAM)


class NguoiDung(Nguoi, UserMixin):
    username = Column(String(50), nullable=False, default='')
    password = Column(String(50), nullable=False, default='')
    avatar = Column(String(200), default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQgee_ioFQrKoyiV3tnY77MLsPeiD15SGydSQ&usqp=CAU')
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER)
    hoadons = relationship('HoaDon', backref='nhanvien', lazy=True, foreign_keys='HoaDon.nguoi_thanh_toan_id')


class HanhKhach(Nguoi):
    la_nguoi_lon = Column(Integer, default=1)
    quoc_tich = Column(String(100))
    dia_chi = Column(String(100))
    ves = relationship('Ve', backref='khachhangdi', lazy=True, foreign_keys='Ve.hanhkhach_id')


class HoaDon(BaseModel):
    nguoi_thanh_toan_id = Column(Integer, ForeignKey(NguoiDung.id), nullable=False)
    tong_hoa_don = Column(Float, default=0)
    da_thanh_toan = Column(Boolean, default=False)
    ngay_tao = Column(DateTime, default=datetime.now())
    ves = relationship('Ve', backref='hoadon', lazy=True)


class Ve(BaseModel):
    hangve_id = Column(Integer, ForeignKey(HangVe.id), nullable=False)
    chuyenbay_id = Column(Integer, ForeignKey(ChuyenBay.id), nullable=False)
    hoadon_id = Column(Integer, ForeignKey(HoaDon.id), nullable=False)
    hanhkhach_id = Column(Integer, ForeignKey(HanhKhach.id), nullable=False)
    tong_tien_ve = Column(Float, nullable=False)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
