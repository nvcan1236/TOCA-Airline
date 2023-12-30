import hashlib

from sqlalchemy import func

from app import db, utils
from app.models import SanBay, TuyenBay, ChuyenBay, HangVe, NguoiDung, HanhKhach, Ve, HoaDon, QuyDinh, Ghe
from cloudinary import uploader


def get_stats(from_date=None, to_date=None):
    if from_date and to_date:
        # from_date = utils.format_date(from_date)
        # to_date = utils.format_date(to_date)
        result = db.session.query(TuyenBay.id, TuyenBay.name, func.sum(Ve.tong_tien_ve).label('total_tong_tien_ve')) \
            .join(ChuyenBay, TuyenBay.id == ChuyenBay.tuyenbay_id, isouter=True) \
            .filter(ChuyenBay.gio_bay.between(from_date, to_date)) \
            .join(Ve, ChuyenBay.id == Ve.chuyenbay_id) \
            .group_by(TuyenBay.id) \
            .all()
    else:
        result = db.session.query(TuyenBay.id, TuyenBay.name, func.sum(Ve.tong_tien_ve).label('total_tong_tien_ve')) \
            .join(ChuyenBay, TuyenBay.id == ChuyenBay.tuyenbay_id, isouter=True) \
            .join(Ve, ChuyenBay.id == Ve.chuyenbay_id) \
            .group_by(TuyenBay.id) \
            .all()

    return result


def get_airports():
    return SanBay.query.all()


def get_scheduled_fllights():
    scheduled_fllights = ChuyenBay.query.filter(ChuyenBay.san_sang.__eq__(False))
    return scheduled_fllights.all()


def get_regulations():
    return QuyDinh.query.all()


def get_airport_by_id(id):
    return SanBay.query.get(id)


def get_airport_name(id):
    return SanBay.query.get(id).name


def get_ticket_class_by_id(id=None):
    return HangVe.query.get(id)


def get_bill_by_id(bill_id):
    return HoaDon.query.get(bill_id)


def get_ticket_classes():
    return HangVe.query.all()


def get_flight_by_id(id=None):
    return ChuyenBay.query.get(id)


def get_flights():
    return ChuyenBay.query.all()


def get_routes():
    return TuyenBay.query.all()


def search_flight(from_code, to_code, date=None):
    t = TuyenBay.query.filter(TuyenBay.sanBayKhoiHanh_id.__eq__(from_code),
                              TuyenBay.sanBayDen_id.__eq__(to_code))
    if t.first():
        ds_chuyenbay = ChuyenBay.query.filter(ChuyenBay.tuyenbay_id.__eq__(t.first().id))
        return ds_chuyenbay.all()
    else:
        return []


def get_user_by_id(user_id):
    return NguoiDung.query.get(user_id)


def create_customer(name, phone, email, nationality, **kwargs):
    c = HanhKhach(name=name,
                  email=email,
                  phone=phone,
                  # ngay_sinh=dob,
                  gioi_tinh=kwargs.get('gender'),
                  # la_nguoi_lon=kwargs.get('is_adult'),
                  quoc_tich=nationality,
                  dia_chi=kwargs.get('address')
                  )
    db.session.add(c)
    db.session.commit()
    return c


def create_bill(nguoi_thanh_toan_id, tong_hoa_don=0):
    b = HoaDon(nguoi_thanh_toan_id=nguoi_thanh_toan_id, tong_hoa_don=tong_hoa_don)
    db.session.add(b)
    db.session.commit()
    return b


def create_ticket(flight_id, ticket_class_id, customer_id, bill_id):
    t = Ve(hangve_id=ticket_class_id, chuyenbay_id=flight_id, hanhkhach_id=customer_id, hoadon_id=bill_id)
    flight = get_flight_by_id(flight_id)
    ticket_class = get_ticket_class_by_id(ticket_class_id)
    t.tong_tien_ve = flight.gia + ticket_class.gia
    db.session.add(t)
    db.session.commit()
    return t


def create_user(username, email, password, name, avatar=None):
    u = NguoiDung()
    u.name = name
    u.email = email
    u.username = username
    u.password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    if avatar:
        avatar_result = uploader.upload(avatar)

        u.avatar = avatar_result['secure_url']
        print(avatar_result['secure_url'])
    db.session.add(u)
    db.session.commit()


def set_seat(flight_id, class_id, qty):
    seat = Ghe.query.filter(Ghe.chuyenbay_id.__eq__(flight_id), Ghe.hangve_id.__eq__(class_id)).first()
    if seat:
        seat.so_luong = qty
        db.session.add(seat)
    else:
        seat = Ghe()
        seat.chuyenbay_id = flight_id
        seat.hangve_id = class_id
        seat.so_luong = qty
        db.session.add(seat)

    db.session.commit()



def check_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = NguoiDung.query.filter(NguoiDung.username.__eq__(username.strip()),
                               NguoiDung.password.__eq__(password)).first()

    if u:
        return u
