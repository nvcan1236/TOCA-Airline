from app.models import SanBay, ChuyenBay, TuyenBay, HangVe


def get_airports():
    return SanBay.query.all()


def get_airport_by_id(id):
    return SanBay.query.get(id)


def get_ticket_class_by_id(id=None):
    return HangVe.query.get(id)


def get_ticket_classes():
    return HangVe.query.all()


def get_flight_by_id(id=None):
    return ChuyenBay.query.get(id)


def get_flights():
    return ChuyenBay.query.all()


def search_flight(from_code, to_code, date=None):
    t = TuyenBay.query.filter(TuyenBay.sanBayKhoiHanh_id.__eq__(from_code),
                              TuyenBay.sanBayDen_id.__eq__(to_code))
    if t.first():
        ds_chuyenbay = ChuyenBay.query.filter(ChuyenBay.tuyenbay_id.__eq__(t.first().id))
        return ds_chuyenbay.all()
    else:
        return []

