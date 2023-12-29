from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from app.models import SanBay,TuyenBay, MayBay, ChuyenBay,  Ve, HangVe, Ghe, DungChan,  NguoiDung, HoaDon, HanhKhach, UserRole
from app import db, app
from flask_login import current_user, logout_user
from flask import redirect


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
    @expose('/')
    def index(self):
        return self.render('/admin/stats.html')


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
    column_list = ['chuyenbays']


class MyChuyenBayView(AdminView):
    create_modal = True
    column_list = ['name','maybay', 'gia', 'giobay']


class MyMayBayView(AdminView):
    column_list = ['name', 'chuyenbays']

admin.add_view(SaleView(name='Bán vé'))
admin.add_view(StatsView(name='Báo cáo thống kê'))
admin.add_view(ScheduleView(name='Lập lịch chuyến bay'))
admin.add_view(ChangeRegulationView(name='Thay đổi quy định'))

admin.add_view(MyTuyenBayView(TuyenBay, db.session, name='Tuyến Bay'))
admin.add_view(MySanBayView(SanBay, db.session, name='Sân Bay'))
admin.add_view(MyChuyenBayView(ChuyenBay, db.session, name='Chuyến Bay'))
admin.add_view(MyMayBayView(MayBay, db.session, name='Máy Bay'))
admin.add_view(EmployeeView(Ve, db.session, name='Vé'))
admin.add_view(AdminView(HangVe, db.session, name='Hạng Vé'))
admin.add_view(AdminView(NguoiDung, db.session, name='NguoiDung'))
admin.add_view(LogoutView(name='Đăng xuất'))
