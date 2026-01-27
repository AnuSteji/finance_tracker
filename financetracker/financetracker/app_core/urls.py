from app_core import views
from django.urls import path


app_name="core"
urlpatterns = [
    path("dist/",views.dist,name='dist'),
    path("location/",views.location,name='location'),
    path("viewdis/",views.viewdis,name='viewdis'),
    path("deletedist/<int:id>/",views.deletedist,name='deletedist'),
    path("editdis/<int:id>/",views.editdis,name='editdis'),
    path("viewloc/",views.viewloc,name='viewloc'),
    path("deleteloc/<int:id>/",views.deleteloc,name='deleteloc'),
    path("locationup/<int:id>/", views.locationup, name="locationup"),
    path("category/",views.category,name='category'),
    path("viewcat/",views.viewcat,name='viewcat'),
    path("deletecat/<int:name>", views.deletecat, name="deletecat"),
    path("editcat/<int:name>/", views.cateup, name="editcat"),
    path("incomehead/", views.incomehead, name="incomehead"),
    path("viewincome/", views.viewincome, name="viewincome"),
    path("delincome/<int:id>/", views.delincome, name="delincome"),
    path("editincome/<int:id>/", views.editincome, name="editincome"),
    path("viewregistration/", views.viewregistration, name="viewregistration"),
    path("expensehead/", views.expensehead, name="expensehead"),
    path("viewexpense/", views.viewexpense, name="viewexpense"),
    path("deleteexpense/<int:id>/", views.deleteexpense, name="deleteexpense"),
    path("editexpense/<int:id>/", views.editexpense, name="editexpense"),
    ]

