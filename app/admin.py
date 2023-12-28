from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from app.models import SanBay ,MayBay, ChuyenBay, TuyenBay, Ve,HangVe,Ghe,NhanVien,KhachHang,TaiKhoan,DungChan,NguoiDung,HoaDon
from app import db, app
from wtforms import Form, StringField, validators

admin = Admin(app=app, template_mode='bootstrap4', name='TOCA Admin')


class SaleView(BaseView):
    @expose('/')
    def index(self):
        return self.render('/admin/sale-ticket.html')


class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('/admin/stats.html')


class ScheduleView(BaseView):
    @expose('/')
    def index(self):
        return self.render('/admin/schedule.html')


class ChangeRegulationView(BaseView):
    @expose('/')
    def index(self):
        return self.render('/admin/change-regulation.html')


admin.add_view(SaleView(name='Bán vé'))
admin.add_view(StatsView(name='Báo cáo thống kê'))
admin.add_view(ScheduleView(name='Lập lịch chuyến bay'))
admin.add_view(ChangeRegulationView(name='Thay đổi quy định'))

class MySanBayView(ModelView):
    column_list = ['tuyenbaydis','tuyenbaydens','tramdungs','name', 'diachi']

# class MyTuyenBayView(ModelView):
#     column_list = ['sanbaydi', 'sanbayden']
#
# class MyChuyenBayView(ModelView):


admin.add_view(ModelView(ChuyenBay,db.session, name='Chuyến Bay'))
admin.add_view(ModelView(TuyenBay,db.session, name='Tuyến Bay'))
admin.add_view(ModelView(Ve,db.session, name='Vé'))
admin.add_view(ModelView(MayBay,db.session ,name = 'Máy Bay'))
admin.add_view(MySanBayView(SanBay,db.session ,name = 'Sân Bay'))

