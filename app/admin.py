from flask_admin import Admin, BaseView, expose
from app import app

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
