from datetime import datetime

from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from app.models import SanBay, TuyenBay, MayBay, ChuyenBay, Ve, HangVe, Ghe, DungChan, NguoiDung, HoaDon, UserRole, \
    QuyDinh
from app import db, app, dao, utils
from flask_login import current_user, logout_user
from flask import redirect, request

admin = Admin(app=app, template_mode='bootstrap4', name='TOCA Admin')


class EmployeeBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == UserRole.EMPLOYEE


class AdminBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == UserRole.ADMIN


class SaleView(EmployeeBaseView):
    @expose('/', methods=['post', 'get'])
    def index(self):
        from_code = request.args.get('from-location')
        to_code = request.args.get('to-location')
        flight = dao.get_flight_by_id(request.args.get('flight'))
        ticket_class = dao.get_ticket_class_by_id(request.args.get('ticket-class'))
        global user
        global bill
        user = bill = None
        flights = dao.search_flight(from_code, to_code)
        if request.method == 'POST':
            fname = request.form.get('fname')
            lname = request.form.get('lname')
            # is_adult = request.form.get('adult')
            gender = request.form.get('gender')
            dob = request.form.get('dob')
            nationality = request.form.get('nationality')
            phone = request.form.get('phone')
            email = request.form.get('email')
            address = request.form.get('address')

            c = {}
            c['name'] = lname + fname
            # c['is_adult'] = is_adult.__eq__('true')
            c['gender'] = gender
            c['dob'] = dob
            c['nationality'] = nationality
            c['phone'] = phone
            c['email'] = email
            c['address'] = address

            user = dao.create_customer(name=c['name'], gender=c['gender'], dob=c['dob'],
                                       nationality=c['nationality'], phone=c['phone'],
                                       email=c['email'], address=c['address'])

            bill = dao.create_bill(current_user.id, (flight.gia + ticket_class.gia) * 1.08)

        return self.render('/admin/sale-ticket.html', flights=flights, flight=flight,
                           ticket_class=ticket_class, user=user, bill=bill)


class StatsView(AdminBaseView):
    @expose('/', methods=['post', 'get'])
    def stats(self):
        if request.method == 'POST':
            from_date = request.form.get('from-date')
            to_date = request.form.get('to-date')
            if not to_date:
                to_date = utils.format_date(datetime.now())

            stats = dao.get_stats(from_date, to_date)
            total = 0
            for s in stats:
                total += s[2]
            print(from_date, to_date, to_date.__eq__(datetime.now))
            return self.render('/admin/stats.html', stats=stats, total=total, empty=stats == [],
                               from_date=from_date, to_date=to_date)
        else:
            stats = dao.get_stats()
            total = 0
            for s in stats:
                total += s[2]
            return self.render('/admin/stats.html', stats=stats, total=total)


class ScheduleView(EmployeeBaseView):
    @expose('/', methods=['post', 'get'])
    def index(self):
        scheduled_flights = dao.get_scheduled_fllights()
        flight_id = request.args.get('flight-id')
        flight = dao.get_flight_by_id(flight_id)

        if request.method == 'POST':
            form = request.form
            if flight:
                flight.gio_bay = form.get('flight-from-date')
                flight.gio_den = form.get('flight-to-date')
                flight.gia = form.get('flight-price')
                flight_seats = form.getlist('flight-seat-num')

                print(flight_seats)
                for i, c in enumerate(dao.get_ticket_classes()):
                    print(flight_id, c.id, flight_seats[i])
                    dao.set_seat(flight_id, c.id, flight_seats[i])

        return self.render('/admin/schedule.html', scheduled_flights=scheduled_flights, flight=flight)


class ChangeRegulationView(AdminBaseView):
    @expose('/')
    def index(self):
        return self.render('/admin/change-regulation.html')


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class EmployeeView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == UserRole.EMPLOYEE


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == UserRole.ADMIN


class MySanBayView(AdminView):
    create_modal = True
    column_list = ['name', 'diachi', 'tuyenbaydis', 'tuyenbaydens']


class MyTuyenBayView(AdminView):
    create_modal = True
    column_list = ['chuyenbays', 'name', 'sanbaydi.name', 'sanbayden.name']


class MyChuyenBayView(AdminView):
    create_modal = True
    column_list = ['name', 'maybay', 'gia', 'giobay']


class MyMayBayView(AdminView):
    column_list = ['name', 'chuyenbays']


class RegulationView(AdminView):
    column_editable_list = ['gia_tri']
    edit_modal = True


admin.add_view(SaleView(name='Bán vé'))
admin.add_view(StatsView(name='Báo cáo thống kê'))
admin.add_view(ScheduleView(name='Lập lịch chuyến bay'))
# admin.add_view(ChangeRegulationView(name='Thay đổi quy định'))

admin.add_view(MyTuyenBayView(TuyenBay, db.session, name='Tuyến Bay'))
admin.add_view(MySanBayView(SanBay, db.session, name='Sân Bay'))
admin.add_view(MyChuyenBayView(ChuyenBay, db.session, name='Chuyến Bay'))
admin.add_view(MyMayBayView(MayBay, db.session, name='Máy Bay'))
admin.add_view(EmployeeView(Ve, db.session, name='Vé'))
admin.add_view(AdminView(HangVe, db.session, name='Hạng Vé'))
admin.add_view(AdminView(NguoiDung, db.session, name='Người dùng'))
admin.add_view(RegulationView(QuyDinh, db.session, name='Thay đổi quy định'))
admin.add_view(LogoutView(name='Đăng xuất'))
