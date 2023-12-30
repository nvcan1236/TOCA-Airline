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
    @expose('/')
    def index(self):
        return self.render('/admin/sale-ticket.html')


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
            # to_now = utils.check_same_date(to_date, datetime.now())
            return self.render('/admin/stats.html', stats=stats, total=total, empty=stats == [],
                               from_date=from_date, to_date=to_date)
        else:
            stats = dao.get_stats()
            total = 0
            for s in stats:
                total += s[2]
            print('B')
            return self.render('/admin/stats.html', stats=stats, total=total)


class ScheduleView(EmployeeBaseView):
    @expose('/')
    def index(self):
        return self.render('/admin/schedule.html')


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


class RegulationView(ModelView):
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
