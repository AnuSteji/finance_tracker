from django.urls import path
from app_dashboard import views


app_name="app_dashboard"

urlpatterns = [
    path("admindashboard/", views.admindashboard, name="admindashboard"),
    path("", views.guestdashboard, name="guestdashboard"),
    path("loginf/", views.loginf, name="loginf"),
    path("userregistration/", views.userregistration, name="userregistration"),
    path("userdashboard/", views.userdashboard, name="userdashboard"),
    path("logout/",views.logout_view,name='logout'),
    path("about/",views.about,name='about'),
    path("services/",views.services,name='services'),
    path("admin_report/", views.admin_report, name="admin_report"),
    path("export_report_excel/", views.export_report_excel, name="export_report_excel"),
]