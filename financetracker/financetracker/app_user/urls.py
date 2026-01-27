

from django.urls import path

from financetracker.app_user import views


app_name="app_user" 
urlpatterns = [
    path("incomedetails/", views.incomedetails, name="incomedetails"),
    path("viewdetails/", views.viewdetails, name="viewdetails"),
    path("deletedetails/<int:id>/", views.deletedetails, name="deletedetails"),
    path("editdetails/<int:id>/", views.editdetails, name="editdetails"),
    path("expensedetails/", views.expensedetails, name="expensedetails"),
    path("viewexpense/", views.viewexpense, name="viewexpense"),
    path("deleteexpense/<int:id>/", views.deleteexpense, name="deleteexpense"),
    path("editexpense/<int:id>/", views.editexpense, name="editexpense"),
    path("budgetdetails/", views.budgetdetails, name="budgetdetails"),
    path("viewbudget/", views.viewbudget, name="viewbudget"),
    path("deletebudget/<int:id>/", views.deletebudget, name="deletebudget"),
    path("editbudget/<int:id>/", views.editbudget, name="editbudget"),
    
]
